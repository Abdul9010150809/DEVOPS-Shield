# Railway Deployment Guide

## Deployment Issues Fixed ✓

### Issue 1: Frontend Config URL (FIXED)
- **Problem**: `config.js` had `/api` suffix in default URL
- **Fix**: Removed `/api` suffix - endpoints already include it
- **Impact**: Fixes 404 errors on API calls

### Issue 2: WebSocket Client (FIXED)
- **Problem**: Hardcoded `ws://localhost:8000/ws` - won't work on Railway
- **Fix**: Now uses `process.env.REACT_APP_API_URL` with HTTP→WS conversion
- **Impact**: Real-time updates will work on production

### Issue 3: Environment Variable Consistency (VERIFIED)
- ✓ apiConfig.js uses REACT_APP_API_URL
- ✓ apiClient.js uses REACT_APP_API_URL
- ✓ zeroTrustService.js uses apiConfig
- ✓ All consistent across frontend

## Railway Deployment Checklist

### Backend Deployment
1. **Set Environment Variables in Railway Dashboard:**
   ```
   PORT=8080 (Railway sets this automatically)
   ENVIRONMENT=production
   CORS_ORIGINS=https://your-frontend-domain.com,https://your-backend-domain.com
   ALLOWED_HOSTS=your-backend-domain.com,*.railway.app
   SECRET_KEY=<generate-strong-key>
   BLOCKCHAIN_ENABLED=false (unless configured)
   ```

2. **Database Setup:**
   - SQLite will work out of the box (uses `/app/backend/database/`)
   - OR connect PostgreSQL via DATABASE_URL

3. **Verification:**
   - ✓ railway.toml configured correctly
   - ✓ start.sh script executable
   - ✓ requirements.txt has all dependencies
   - ✓ Dockerfile properly configured

### Frontend Deployment (separate Railway service or Vercel/Netlify)
1. **Build Variables:**
   ```
   REACT_APP_API_URL=https://your-backend-on-railway.railway.app
   REACT_APP_ENV=production
   ```

2. **Deployment Command:**
   ```bash
   npm run build
   ```

3. **Serve built files** (if on Railway):
   - Serve from `frontend/build/` directory

## Common Railway Errors & Fixes

### Error: CORS policy error
```
Access to XMLHttpRequest blocked by CORS policy
```
**Fix:** Update `CORS_ORIGINS` in Railway environment variables
- Add your frontend domain
- Format: `https://domain.com,https://another-domain.com`

### Error: Cannot POST /api/...
```
404: Not Found
```
**Fix:** Ensure frontend is sending requests to correct base URL
- Check: `REACT_APP_API_URL` is set in frontend
- Remove any `/api` suffixes from base URL

### Error: WebSocket connection fails
```
WebSocket is closed before the connection is established
```
**Fix:** Already fixed by updating websocketClient.js
- Verify `REACT_APP_API_URL` environment variable

### Error: "Port 8000 is not available"
```
Failed to bind to port 8000
```
**Fix:** Railway uses `PORT` environment variable
- Don't hardcode port
- start.sh correctly uses `${PORT:-8080}`

## Deployment Steps

### 1. Deploy Backend on Railway
```bash
cd /path/to/DEVOPS-Shield
railway link  # Connect to Railway project
railway up    # Deploy backend
```

### 2. Configure Environment Variables
- In Railway Dashboard → Backend Service → Variables
- Set all variables from checklist above

### 3. Test Backend
```bash
# Get your Railway backend URL from dashboard
curl https://your-backend.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "DevOps Shield Backend",
  "environment": "production",
  "cors_origins": ["https://your-frontend-domain.com"]
}
```

### 4. Deploy Frontend (separate service or platform)
- If using Railway: Deploy as separate service
- Set `REACT_APP_API_URL` to backend Railway URL
- OR use Vercel/Netlify with Railway backend

### 5. Verify Connection
- Open frontend in browser
- Go to Dashboard page
- Check browser console for connection logs
- Verify no 404 errors on API calls

## Post-Deployment Testing

### Test Health Endpoint
```bash
curl -X GET https://your-backend.railway.app/health
```

### Test CORS
```bash
curl -X OPTIONS https://your-backend.railway.app/api/fraud/stats \
  -H "Origin: https://your-frontend-domain.com" \
  -H "Access-Control-Request-Method: GET"
```

### Test API
```bash
curl -X GET https://your-backend.railway.app/api/simulate
```

### Browser Console
- Open DevTools (F12)
- Check Network tab for API calls
- Look for `[API Config] Initialized with base URL: ...`
- Verify no CORS errors

## Monitoring on Railway

1. **View Logs:**
   - Railway Dashboard → Backend Service → Deployments → Logs
   - Look for startup messages and errors

2. **Check Metrics:**
   - Memory usage
   - CPU usage
   - Request count
   - Error rate

3. **Environment Variables:**
   - Verify all variables are set correctly
   - Check DATABASE_URL if using PostgreSQL

## Rollback & Recovery

### If deployment has issues:
1. Check Railway logs for errors
2. Verify environment variables are set
3. Check if CORS_ORIGINS includes your domain
4. Test health endpoint: `curl .../health`
5. Review recent commits - any breaking changes?

### Rollback to previous version:
- Railway Dashboard → Deployments → Select previous deployment → Revert

## Files Modified for Railway Compatibility
- ✓ frontend/src/utils/config.js - Fixed API URL
- ✓ frontend/src/services/websocketClient.js - Environment variable support
- ✓ backend/main.py - Enhanced health endpoint
- ✓ frontend/.env.production - Updated to correct URL format

## Next Steps
1. Push changes to GitHub: `git push origin main`
2. Railway will auto-deploy if configured for auto-deploy
3. Monitor deployment logs
4. Test all endpoints
5. Verify frontend-backend connectivity
