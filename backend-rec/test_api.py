#!/usr/bin/env python3
"""
Script de test rapide pour vérifier que l'API fonctionne correctement
Usage: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def test_health_check():
    print_header("Test 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success(f"API is healthy: {response.json()}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Cannot connect to API: {e}")
        return False

def test_register():
    print_header("Test 2: User Registration")
    try:
        data = {
            "email": "test@example.com",
            "password": "Test123!",
            "first_name": "Test",
            "last_name": "User",
            "role": "student"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        
        if response.status_code == 201:
            print_success("User registered successfully")
            print(json.dumps(response.json(), indent=2))
            return True
        elif response.status_code == 400:
            print("⚠️  User already exists (this is OK)")
            return True
        else:
            print_error(f"Registration failed: {response.status_code}")
            print(response.json())
            return False
    except Exception as e:
        print_error(f"Registration error: {e}")
        return False

def test_login():
    print_header("Test 3: User Login")
    try:
        data = {
            "username": "admin@didacticiel.com",
            "password": "Admin123!"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result["access_token"]
            user = result["user"]
            print_success(f"Login successful as {user['first_name']} {user['last_name']}")
            print(f"Token: {token[:50]}...")
            return token
        else:
            print_error(f"Login failed: {response.status_code}")
            print(response.json())
            return None
    except Exception as e:
        print_error(f"Login error: {e}")
        return None

def test_get_modules(token):
    print_header("Test 4: Get Modules")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/modules", headers=headers)
        
        if response.status_code == 200:
            modules = response.json()
            print_success(f"Retrieved {len(modules)} modules")
            for module in modules:
                print(f"  - {module['title']} (Week {module['week']})")
            return True
        else:
            print_error(f"Failed to get modules: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting modules: {e}")
        return False

def test_get_me(token):
    print_header("Test 5: Get Current User")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            print_success(f"Current user: {user['first_name']} {user['last_name']} ({user['role']})")
            print(json.dumps(user, indent=2, default=str))
            return True
        else:
            print_error(f"Failed to get current user: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting current user: {e}")
        return False

def test_admin_stats(token):
    print_header("Test 6: Admin Stats")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/admin/stats", headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            print_success("Admin stats retrieved")
            print(json.dumps(stats, indent=2))
            return True
        else:
            print_error(f"Failed to get admin stats: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting admin stats: {e}")
        return False

def main():
    print("\n" + "🚀 TESTING BACKEND API")
    print("Make sure the backend is running on http://localhost:8000\n")
    
    results = []
    
    # Test 1: Health Check
    results.append(test_health_check())
    
    # Test 2: Registration
    results.append(test_register())
    
    # Test 3: Login
    token = test_login()
    if token:
        results.append(True)
        
        # Test 4: Get Modules
        results.append(test_get_modules(token))
        
        # Test 5: Get Current User
        results.append(test_get_me(token))
        
        # Test 6: Admin Stats
        results.append(test_admin_stats(token))
    else:
        results.append(False)
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
    else:
        print(f"⚠️  {passed}/{total} tests passed")
    
    print("\n" + "="*60)
    print("📝 Next steps:")
    print("  1. Open http://localhost:8000/docs for API documentation")
    print("  2. Test endpoints with Swagger UI")
    print("  3. Connect your frontend to http://localhost:8000")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
