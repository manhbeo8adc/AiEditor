#!/usr/bin/env python3
"""
Test script for Rate Limiting (Step 2.2)
"""
import requests
import time
import json

def test_rate_limiting():
    print("🔥 Testing Rate Limiting (Step 2.2)")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Normal status check (should work)
    print("\n1. Testing normal status endpoint...")
    try:
        response = requests.get(f"{base_url}/api/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Rate limiting test
    print("\n2. Testing rate limiting (sending 6 requests quickly)...")
    
    for i in range(1, 7):
        try:
            response = requests.post(f"{base_url}/api/upload")
            print(f"Request {i}: Status {response.status_code}")
            
            if response.status_code == 429:
                print(f"✅ Rate limiting triggered at request {i}")
                try:
                    error_data = response.json()
                    print(f"Error response: {error_data}")
                except:
                    print(f"Error response: {response.text}")
                break
            elif response.status_code == 400:
                print(f"Expected 400 (missing files) for request {i}")
            else:
                print(f"Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Error on request {i}: {e}")
            break
            
        # Small delay between requests
        time.sleep(0.1)
    
    print("\n✅ Rate limiting test completed!")
    print("Expected: Requests should be limited after 5 attempts")

if __name__ == "__main__":
    test_rate_limiting() 