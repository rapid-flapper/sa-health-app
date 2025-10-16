"""
Milestone 3 Verification Test
Tests Flask backend, routes, and API endpoints
"""

import sys
import json

def test_flask_import():
    """Test that Flask app can be imported"""
    try:
        from app import app, load_phrases_data, get_phrases_by_category
        print("[PASS] Flask app imported successfully")
        return True, app
    except ImportError as e:
        print(f"[FAIL] Failed to import Flask app: {e}")
        return False, None
    except Exception as e:
        print(f"[FAIL] Error importing Flask app: {e}")
        return False, None

def test_data_loading(app):
    """Test data loading functions"""
    try:
        from app import load_phrases_data
        data = load_phrases_data()
        
        if 'categories' not in data or 'phrases' not in data:
            print("[FAIL] Data loading returned incorrect structure")
            return False
        
        if len(data['categories']) == 0:
            print("[FAIL] No categories loaded")
            return False
            
        if len(data['phrases']) == 0:
            print("[FAIL] No phrases loaded")
            return False
        
        print(f"[PASS] Data loaded: {len(data['categories'])} categories, {len(data['phrases'])} phrases")
        return True
    except Exception as e:
        print(f"[FAIL] Data loading error: {e}")
        return False

def test_home_route(app):
    """Test home page route"""
    try:
        with app.test_client() as client:
            response = client.get('/')
            
            if response.status_code != 200:
                print(f"[FAIL] Home route returned status {response.status_code}")
                return False
            
            if b'SA Health App' not in response.data:
                print("[FAIL] Home page missing expected content")
                return False
            
            print("[PASS] Home route (/) working correctly")
            return True
    except Exception as e:
        print(f"[FAIL] Home route error: {e}")
        return False

def test_categories_api(app):
    """Test /api/categories endpoint"""
    try:
        with app.test_client() as client:
            response = client.get('/api/categories')
            
            if response.status_code != 200:
                print(f"[FAIL] Categories API returned status {response.status_code}")
                return False
            
            data = json.loads(response.data)
            
            if not data.get('success'):
                print("[FAIL] Categories API returned success=False")
                return False
            
            if 'categories' not in data:
                print("[FAIL] Categories API missing 'categories' key")
                return False
            
            if len(data['categories']) == 0:
                print("[FAIL] Categories API returned no categories")
                return False
            
            print(f"[PASS] Categories API working: {len(data['categories'])} categories")
            return True
    except Exception as e:
        print(f"[FAIL] Categories API error: {e}")
        return False

def test_phrases_api(app):
    """Test /api/phrases endpoint"""
    try:
        with app.test_client() as client:
            response = client.get('/api/phrases')
            
            if response.status_code != 200:
                print(f"[FAIL] Phrases API returned status {response.status_code}")
                return False
            
            data = json.loads(response.data)
            
            if not data.get('success'):
                print("[FAIL] Phrases API returned success=False")
                return False
            
            if 'phrases' not in data or 'total' not in data:
                print("[FAIL] Phrases API missing required keys")
                return False
            
            if data['total'] != len(data['phrases']):
                print("[FAIL] Phrases API total count mismatch")
                return False
            
            print(f"[PASS] Phrases API working: {data['total']} phrases")
            return True
    except Exception as e:
        print(f"[FAIL] Phrases API error: {e}")
        return False

def test_phrases_by_category_api(app):
    """Test /api/phrases/category/<category_id> endpoint"""
    try:
        with app.test_client() as client:
            # Test with 'greeting' category
            response = client.get('/api/phrases/category/greeting')
            
            if response.status_code != 200:
                print(f"[FAIL] Phrases by category API returned status {response.status_code}")
                return False
            
            data = json.loads(response.data)
            
            if not data.get('success'):
                print("[FAIL] Phrases by category API returned success=False")
                return False
            
            if 'phrases' not in data or 'category' not in data:
                print("[FAIL] Phrases by category API missing required keys")
                return False
            
            if data['category'] != 'greeting':
                print("[FAIL] Phrases by category API returned wrong category")
                return False
            
            # Verify phrases have greeting category
            for phrase in data['phrases']:
                if 'greeting' not in phrase.get('categories', []):
                    print("[FAIL] Phrase doesn't belong to greeting category")
                    return False
            
            print(f"[PASS] Phrases by category API working: {data['total']} greeting phrases")
            return True
    except Exception as e:
        print(f"[FAIL] Phrases by category API error: {e}")
        return False

def test_phrase_by_id_api(app):
    """Test /api/phrase/<phrase_id> endpoint"""
    try:
        with app.test_client() as client:
            # Test with phrase_001
            response = client.get('/api/phrase/phrase_001')
            
            if response.status_code != 200:
                print(f"[FAIL] Phrase by ID API returned status {response.status_code}")
                return False
            
            data = json.loads(response.data)
            
            if not data.get('success'):
                print("[FAIL] Phrase by ID API returned success=False")
                return False
            
            if 'phrase' not in data:
                print("[FAIL] Phrase by ID API missing 'phrase' key")
                return False
            
            if data['phrase']['id'] != 'phrase_001':
                print("[FAIL] Phrase by ID API returned wrong phrase")
                return False
            
            print("[PASS] Phrase by ID API working correctly")
            return True
    except Exception as e:
        print(f"[FAIL] Phrase by ID API error: {e}")
        return False

def test_health_check_api(app):
    """Test /api/health endpoint"""
    try:
        with app.test_client() as client:
            response = client.get('/api/health')
            
            if response.status_code != 200:
                print(f"[FAIL] Health check API returned status {response.status_code}")
                return False
            
            data = json.loads(response.data)
            
            if data.get('status') != 'healthy':
                print("[FAIL] Health check API returned unhealthy status")
                return False
            
            print("[PASS] Health check API working")
            return True
    except Exception as e:
        print(f"[FAIL] Health check API error: {e}")
        return False

def test_404_handling(app):
    """Test 404 error handling"""
    try:
        with app.test_client() as client:
            response = client.get('/nonexistent')
            
            if response.status_code != 404:
                print(f"[FAIL] 404 handler returned wrong status: {response.status_code}")
                return False
            
            data = json.loads(response.data)
            
            if data.get('success') != False:
                print("[FAIL] 404 handler didn't return success=False")
                return False
            
            print("[PASS] 404 error handling working")
            return True
    except Exception as e:
        print(f"[FAIL] 404 handling error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("MILESTONE 3 VERIFICATION TESTS")
    print("=" * 50)
    print()
    
    # Test 1: Import Flask app
    import_success, app = test_flask_import()
    if not import_success:
        print("\n[CRITICAL] Cannot proceed without Flask app")
        sys.exit(1)
    
    tests = [
        ('Import Flask App', import_success),
        ('Data Loading', test_data_loading(app)),
        ('Home Route', test_home_route(app)),
        ('Categories API', test_categories_api(app)),
        ('Phrases API', test_phrases_api(app)),
        ('Phrases by Category API', test_phrases_by_category_api(app)),
        ('Phrase by ID API', test_phrase_by_id_api(app)),
        ('Health Check API', test_health_check_api(app)),
        ('404 Error Handling', test_404_handling(app))
    ]
    
    print()
    print("=" * 50)
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] MILESTONE 3: ALL TESTS PASSED")
        print("[SUCCESS] Flask backend is fully functional")
        print()
        print("API Endpoints Available:")
        print("  - GET /                              (Home page)")
        print("  - GET /api/categories                (All categories)")
        print("  - GET /api/phrases                   (All phrases)")
        print("  - GET /api/phrases/category/<id>     (Phrases by category)")
        print("  - GET /api/phrase/<id>               (Single phrase)")
        print("  - GET /api/health                    (Health check)")
    else:
        print("[FAILURE] MILESTONE 3: SOME TESTS FAILED")
        print("[FAILURE] Please fix issues before proceeding")
    
    print("=" * 50)
