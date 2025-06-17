#!/usr/bin/env python3
"""
Test script for CORS Configuration (Step 2.3)
"""
import requests
import json

def test_cors():
    print("🌐 Testing CORS Configuration (Step 2.3)")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: CORS with allowed origin (localhost:3000)
    print("\n1. Testing CORS with ALLOWED origin (localhost:3000)...")
    
    headers_allowed = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type"
    }
    
    try:
        response = requests.options(f"{base_url}/api/upload", headers=headers_allowed)
        print(f"Status: {response.status_code}")
        print("Response Headers:")
        for key, value in response.headers.items():
            if "access-control" in key.lower():
                print(f"  {key}: {value}")
        
        if response.status_code == 200:
            print("✅ CORS allowed for localhost:3000")
        else:
            print("❌ CORS request failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: CORS with disallowed origin
    print("\n2. Testing CORS with DISALLOWED origin (malicious-site.com)...")
    
    headers_disallowed = {
        "Origin": "http://malicious-site.com",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type"
    }
    
    try:
        response = requests.options(f"{base_url}/api/upload", headers=headers_disallowed)
        print(f"Status: {response.status_code}")
        print("Response Headers:")
        cors_headers_found = False
        for key, value in response.headers.items():
            if "access-control" in key.lower():
                print(f"  {key}: {value}")
                cors_headers_found = True
        
        if not cors_headers_found:
            print("  No CORS headers found (good - origin blocked)")
            print("✅ CORS correctly blocked malicious origin")
        else:
            print("⚠️  CORS headers found - check if origin is properly restricted")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Test actual POST request with CORS
    print("\n3. Testing POST request with CORS...")
    
    headers_post = {
        "Origin": "http://localhost:3000",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{base_url}/api/upload", 
                               headers=headers_post,
                               json={})
        print(f"Status: {response.status_code}")
        print("CORS Headers in POST response:")
        for key, value in response.headers.items():
            if "access-control" in key.lower():
                print(f"  {key}: {value}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ CORS test completed!")
    print("Expected: localhost:3000 should be allowed, malicious sites should be blocked")

if __name__ == "__main__":
    test_cors() 