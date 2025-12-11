from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from ..core.fraud_engine import FraudEngine
from ..services.gitlab_service import GitLabService
from ..utils.logger import get_logger
from ..utils.validator import WebhookValidator
import hmac
import hashlib
import json
import time

router = APIRouter()
logger = get_logger(__name__)
fraud_engine = FraudEngine()
gitlab_service = GitLabService()
validator = WebhookValidator()

# Constants for validation
MAX_PAYLOAD_SIZE = 10 * 1024 * 1024  # 10MB
MAX_COMMITS = 1000
MAX_STRING_LENGTH = 1000

@router.post("/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle incoming webhooks from GitLab/GitHub with validation"""
    try:
        # Check payload size
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > MAX_PAYLOAD_SIZE:
            logger.warning(f"Webhook payload too large: {content_length} bytes")
            raise HTTPException(status_code=413, detail="Payload too large")
        
        # Get raw body for signature verification
        body = await request.body()
        
        if not body:
            raise HTTPException(status_code=400, detail="Empty webhook payload")
        
        try:
            payload = json.loads(body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            logger.warning("Invalid JSON payload received")
            raise HTTPException(status_code=400, detail="Invalid JSON payload")

        # Verify webhook signature if configured
        signature = request.headers.get('X-Gitlab-Token') or request.headers.get('X-Hub-Signature-256')
        if signature and not validator.verify_signature(body, signature, request.headers.get('X-Gitlab-Event')):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

        event_type = request.headers.get('X-Gitlab-Event') or request.headers.get('X-Github-Event')
        
        if not event_type or not isinstance(event_type, str) or len(event_type) > 100:
            logger.warning(f"Invalid event type: {event_type}")
            raise HTTPException(status_code=400, detail="Invalid event type")

        if event_type == 'push':
            background_tasks.add_task(process_push_event, payload)
            return {"status": "accepted", "message": "Push event queued for analysis"}

        elif event_type in ['merge_request', 'pull_request']:
            background_tasks.add_task(process_merge_event, payload)
            return {"status": "accepted", "message": "Merge event queued for analysis"}

        else:
            logger.info(f"Unhandled event type: {event_type}")
            return {"status": "ignored", "message": f"Event type {event_type} not processed"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

def _validate_string(value, max_length=MAX_STRING_LENGTH, field_name="value"):
    """Validate string input"""
    if not isinstance(value, str):
        return None
    if len(value) > max_length:
        logger.warning(f"{field_name} exceeds maximum length of {max_length}")
        return value[:max_length]
    return value

def process_push_event(payload):
    """Process push event in background with validation"""
    try:
        logger.info("Processing push event")

        # Validate payload structure
        if not isinstance(payload, dict):
            logger.error("Invalid payload structure")
            return

        # Extract repository information
        repo = payload.get('repository', {})
        if not isinstance(repo, dict):
            logger.error("Invalid repository data")
            return
        
        repo_name = _validate_string(repo.get('name', 'unknown'))
        project_id = repo.get('id') or repo.get('full_name', '').replace('/', '%2F')

        # Get commits from the push
        commits = payload.get('commits', [])
        if not isinstance(commits, list):
            logger.error("Invalid commits data")
            return
        
        if len(commits) > MAX_COMMITS:
            logger.warning(f"Too many commits ({len(commits)}), processing first {MAX_COMMITS}")
            commits = commits[:MAX_COMMITS]

        if not commits:
            logger.info("No commits in push event")
            return

        # Transform commits to our format with validation
        transformed_commits = []
        for commit in commits:
            if not isinstance(commit, dict):
                logger.warning("Skipping invalid commit entry")
                continue
            
            try:
                transformed_commits.append({
                    "id": _validate_string(commit.get('id')),
                    "message": _validate_string(commit.get('message', '')),
                    "author": _validate_string(commit.get('author', {}).get('name', 'unknown')),
                    "timestamp": commit.get('timestamp'),
                    "files_changed": [],
                    "lines_added": max(0, int(commit.get('lines_added', 0))),
                    "lines_deleted": max(0, int(commit.get('lines_deleted', 0)))
                })
            except Exception as e:
                logger.warning(f"Error processing commit: {e}")
                continue

        if not transformed_commits:
            logger.info("No valid commits to process")
            return

        # Get detailed commit information if we have GitLab service
        if project_id and gitlab_service.token:
            for i, commit in enumerate(transformed_commits):
                try:
                    details = gitlab_service.get_commit_details(project_id, commit['id'])
                    if details:
                        transformed_commits[i] = details
                except Exception as e:
                    logger.warning(f"Failed to get commit details: {e}")
                    continue

        # Prepare repository data
        repo_data = {
            "name": repo_name,
            "id": str(project_id)[:100],  # Limit ID length
            "url": _validate_string(repo.get('url') or repo.get('html_url')),
            "timestamp": payload.get('timestamp', time.time()),
            "commits": transformed_commits
        }

        # Run fraud analysis
        result = fraud_engine.analyze_repository(repo_data, transformed_commits)
        logger.info(f"Push event analysis completed for {repo_data['name']}")

    except Exception as e:
        logger.error(f"Error processing push event: {e}", exc_info=True)

def process_merge_event(payload):
    """Process merge/pull request event with validation"""
    try:
        logger.info("Processing merge/pull request event")

        if not isinstance(payload, dict):
            logger.error("Invalid payload structure")
            return

        # Extract relevant information
        pr = payload.get('object_attributes', {}) if 'object_attributes' in payload else payload

        if not isinstance(pr, dict):
            logger.error("Invalid PR data")
            return

        if pr.get('state') != 'merged':
            logger.info("PR not merged, skipping analysis")
            return

        pr_title = _validate_string(pr.get('title', 'unknown'))
        logger.info(f"Merged PR: {pr_title}")

    except Exception as e:
        logger.error(f"Error processing merge event: {e}", exc_info=True)

@router.get("/webhook/test")
async def test_webhook():
    """Test endpoint for webhook functionality"""
    return {
        "status": "ok",
        "message": "Webhook endpoint is active",
        "supported_events": ["push", "merge_request", "pull_request"]
    }