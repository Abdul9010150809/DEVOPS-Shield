#!/usr/bin/env python3
"""
Comprehensive connection and endpoint verification script
Tests all pages and frontend-backend connectivity
"""

import sys
import requests
import json
from urllib.parse import urljoin

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
TIMEOUT = 5

# Color output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_status(title, success, message=""):
    status = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
    msg = f" - {message}" if message else ""
    print(f"{status} {title}{msg}")

def check_backend_health():
    """Check backend health endpoint"""
    print(f"\n{YELLOW}=== Backend Health Check ==={RESET}")
    try:
        response = requests.get(urljoin(BACKEND_URL, "/health"), timeout=TIMEOUT)
        data = response.json()
        success = response.status_code == 200
        print_status("Backend Health", success, f"Status: {data.get('status')}")
        if success:
            print(f"  Service: {data.get('service')}")
            print(f"  Version: {data.get('version')}")
            print(f"  Environment: {data.get('environment')}")
            print(f"  CORS Origins: {data.get('cors_origins', [])}")
        return success
    except Exception as e:
        print_status("Backend Health", False, str(e))
        return False

def check_api_endpoints():
    """Check all API endpoints"""
    print(f"\n{YELLOW}=== API Endpoints Check ==={RESET}")
    
    endpoints = [
        ("GET", "/"),
        ("GET", "/api/fraud/stats"),
        ("GET", "/api/alerts/recent?limit=5"),
        ("GET", "/api/simulate"),
        ("GET", "/health"),
    ]
    
    all_ok = True
    for method, endpoint in endpoints:
        try:
            url = urljoin(BACKEND_URL, endpoint)
            if method == "GET":
                response = requests.get(url, timeout=TIMEOUT)
            else:
                response = requests.post(url, timeout=TIMEOUT)
            
            success = 200 <= response.status_code < 300
            print_status(f"{method} {endpoint}", success, f"HTTP {response.status_code}")
            all_ok = all_ok and success
        except Exception as e:
            print_status(f"{method} {endpoint}", False, str(e))
            all_ok = False
    
    return all_ok

def check_frontend_connectivity():
    """Check frontend server"""
    print(f"\n{YELLOW}=== Frontend Server Check ==={RESET}")
    try:
        response = requests.get(FRONTEND_URL, timeout=TIMEOUT)
        success = response.status_code == 200
        print_status("Frontend Server", success, f"HTTP {response.status_code}")
        return success
    except Exception as e:
        print_status("Frontend Server", False, str(e))
        return False

def check_cors_configuration():
    """Check CORS headers"""
    print(f"\n{YELLOW}=== CORS Configuration Check ==={RESET}")
    try:
        response = requests.options(urljoin(BACKEND_URL, "/api/fraud/stats"), timeout=TIMEOUT)
        headers = response.headers
        
        cors_headers = {
            'Access-Control-Allow-Origin': headers.get('Access-Control-Allow-Origin', 'NOT SET'),
            'Access-Control-Allow-Methods': headers.get('Access-Control-Allow-Methods', 'NOT SET'),
            'Access-Control-Allow-Headers': headers.get('Access-Control-Allow-Headers', 'NOT SET'),
        }
        
        print("  CORS Headers:")
        for key, value in cors_headers.items():
            print(f"    {key}: {value}")
        
        has_cors = 'Access-Control-Allow-Origin' in headers
        print_status("CORS Enabled", has_cors)
        return has_cors
    except Exception as e:
        print_status("CORS Check", False, str(e))
        return False

def check_simulation_endpoint():
    """Check simulation endpoint works"""
    print(f"\n{YELLOW}=== Simulation Endpoint Check ==={RESET}")
    try:
        response = requests.get(urljoin(BACKEND_URL, "/api/simulate"), timeout=TIMEOUT)
        data = response.json()
        success = (response.status_code == 200 and 
                   'fraud_event' in data and 
                   'status' in data)
        
        if success:
            fraud_event = data.get('fraud_event', {})
            print_status("Simulation Response", success, f"Event ID: {fraud_event.get('event_id')}")
            print(f"  Risk Score: {fraud_event.get('risk_score')}")
        else:
            print_status("Simulation Response", success)
        return success
    except Exception as e:
        print_status("Simulation Endpoint", False, str(e))
        return False

def main():
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}DevOps Shield - Connection & Endpoint Verification{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")
    
    print(f"\nBackend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Timeout: {TIMEOUT}s")
    
    results = []
    results.append(("Backend Health", check_backend_health()))
    results.append(("API Endpoints", check_api_endpoints()))
    results.append(("Frontend Server", check_frontend_connectivity()))
    results.append(("CORS Configuration", check_cors_configuration()))
    results.append(("Simulation Endpoint", check_simulation_endpoint()))
    
    print(f"\n{YELLOW}=== Summary ==={RESET}")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for title, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {status} - {title}")
    
    print(f"\n{YELLOW}Result: {passed}/{total} checks passed{RESET}\n")
    
    if passed == total:
        print(f"{GREEN}✓ All systems operational! Frontend and backend are connected properly.{RESET}")
        return 0
    else:
        print(f"{RED}✗ Some checks failed. Please review the errors above.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
