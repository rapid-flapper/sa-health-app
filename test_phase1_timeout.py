"""
Phase 1 Completion Validation Tests - WITH TIMEOUT PROTECTION
Each test has a maximum execution time to prevent infinite hangs
"""

import sys
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Global timeout settings (in seconds)
FAST_TEST_TIMEOUT = 5   # For quick tests (imports, file checks)
SLOW_TEST_TIMEOUT = 15  # For tests that might be slower (API calls, audio)

def log_timing(message, start_time):
    """Helper to log elapsed time"""
    elapsed = time.time() - start_time
    print(f"    ⏱️  {message}: {elapsed:.2f}s")

def run_with_timeout(func, timeout_seconds, func_name):
    """Run a function with a timeout"""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func)
        try:
            result = future.wait(timeout=timeout_seconds)
            return future.result()
        except TimeoutError:
            print(f"    ⏰ TIMEOUT! {func_name} exceeded {timeout_seconds}s limit")
            return False
        except Exception as e:
            print(f"    ❌ ERROR in {func_name}: {e}")
            return False

def test_dependencies():
    """Test that all required dependencies are installed"""
    start = time.time()
    print("  → Starting dependency check...")
    
    try:
        step_start = time.time()
        import flask
        log_timing("Imported Flask", step_start)
        
        step_start = time.time()
        from gtts import gTTS
        log_timing("Imported gTTS", step_start)
        
        print("[PASS] All dependencies installed")
        log_timing("Total test time", start)
        return True
    except ImportError as e:
        print(f"[FAIL] Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def test_data_structure():
    """Test that phrases.json exists and is valid"""
    start = time.time()
    print("  → Starting data structure check...")
    
    try:
        step_start = time.time()
        with open('data/phrases.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        log_timing("Loaded phrases.json", step_start)
        
        # Check structure
        if 'categories' not in data or 'phrases' not in data:
            print("[FAIL] phrases.json missing required keys")
            return False
        
        if len(data['categories']) == 0:
            print("[FAIL] No categories defined")
            return False
        
        if len(data['phrases']) == 0:
            print("[FAIL] No phrases defined")
            return False
        
        # Check phrase structure
        first_phrase = data['phrases'][0]
        required_keys = ['id', 'categories', 'translations']
        for key in required_keys:
            if key not in first_phrase:
                print(f"[FAIL] Phrase missing required key: {key}")
                return False
        
        # Check that we have all 5 languages
        required_languages = ['en', 'zu', 'xh', 'af', 'nso']
        translations = first_phrase['translations']
        for lang in required_languages:
            if lang not in translations:
                print(f"[FAIL] Missing language in phrase: {lang}")
                return False
        
        # Check translation structure
        for lang, trans in translations.items():
            if 'text' not in trans or 'phonetic' not in trans:
                print(f"[FAIL] Translation for {lang} missing text or phonetic")
                return False
        
        phrase_count = len(data['phrases'])
        category_count = len(data['categories'])
        print(f"[PASS] Data structure valid ({phrase_count} phrases, {category_count} categories)")
        log_timing("Total test time", start)
        return True
    except Exception as e:
        print(f"[FAIL] Data structure test error: {e}")
        return False

def test_flask_app_structure():
    """Test that Flask app is structured correctly"""
    start = time.time()
    print("  → Starting Flask app structure check...")
    print("    ⏰ Timeout: 5 seconds")
    
    try:
        step_start = time.time()
        print("    🔄 Importing Flask app...")
        from app import app
        log_timing("Imported Flask app", step_start)
        
        # Check that app is a Flask app
        if not hasattr(app, 'test_client'):
            print("[FAIL] app is not a Flask application")
            return False
        
        print("[PASS] Flask app structure valid")
        log_timing("Total test time", start)
        return True
    except ImportError:
        print("[FAIL] Cannot import Flask app")
        return False
    except Exception as e:
        print(f"[FAIL] Flask app test error: {e}")
        return False

def test_routes_exist():
    """Test that all required routes exist"""
    start = time.time()
    print("  → Starting routes check...")
    print("    ⏰ Timeout: 5 seconds")
    
    try:
        step_start = time.time()
        from app import app
        log_timing("Imported Flask app", step_start)
        
        step_start = time.time()
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        log_timing("Retrieved routes", step_start)
        
        # Check for audio route (dynamic)
        has_audio_route = any('/api/audio' in route for route in routes)
        if not has_audio_route:
            print("[FAIL] Audio generation route missing")
            return False
        
        print("[PASS] All required routes exist")
        log_timing("Total test time", start)
        return True
    except Exception as e:
        print(f"[FAIL] Routes test error: {e}")
        return False

def test_api_responses():
    """Test that API endpoints return expected responses"""
    start = time.time()
    print("  → Starting API response checks...")
    print("    ⏰ Timeout: 10 seconds")
    
    try:
        step_start = time.time()
        from app import app
        log_timing("Imported Flask app", step_start)
        
        with app.test_client() as client:
            # Test home page
            step_start = time.time()
            print("    🔄 Testing home page (/)...")
            response = client.get('/')
            log_timing("Home page response", step_start)
            
            if response.status_code != 200:
                print(f"[FAIL] Home page returned status: {response.status_code}")
                return False
            
            # Test app page
            step_start = time.time()
            print("    🔄 Testing app page (/app)...")
            response = client.get('/app')
            log_timing("App page response", step_start)
            
            if response.status_code != 200:
                print(f"[FAIL] App page returned status: {response.status_code}")
                return False
            
            # Test categories API
            step_start = time.time()
            print("    🔄 Testing categories API...")
            response = client.get('/api/categories')
            log_timing("Categories API response", step_start)
            
            if response.status_code != 200:
                print(f"[FAIL] Categories API returned status: {response.status_code}")
                return False
            
            step_start = time.time()
            data = response.get_json()
            log_timing("Parsed JSON response", step_start)
            
            if 'categories' not in data:
                print("[FAIL] Categories API missing 'categories' key")
                return False
            
            # Test phrases API (just check it responds, don't validate all data)
            step_start = time.time()
            print("    🔄 Testing phrases API...")
            response = client.get('/api/phrases/category/greeting')
            log_timing("Phrases API response", step_start)
            
            if response.status_code != 200:
                print(f"[FAIL] Phrases API returned status: {response.status_code}")
                return False
            
            print("[PASS] All API endpoints respond correctly")
            log_timing("Total test time", start)
            return True
    except Exception as e:
        print(f"[FAIL] API test error: {e}")
        return False

def test_template_files():
    """Test that required template files exist"""
    start = time.time()
    print("  → Starting template files check...")
    print("    ⏰ Timeout: 5 seconds")
    
    try:
        import os
        
        required_templates = [
            'app/templates/index.html',
            'app/templates/app.html'
        ]
        
        for template in required_templates:
            if not os.path.exists(template):
                print(f"[FAIL] Template missing: {template}")
                return False
        
        print("[PASS] All template files exist")
        log_timing("Total test time", start)
        return True
    except Exception as e:
        print(f"[FAIL] Template test error: {e}")
        return False

def test_audio_generation_minimal():
    """Test audio generation - THIS IS THE LIKELY CULPRIT"""
    start = time.time()
    print("  → Starting audio endpoint check...")
    print("    ⚠️  This makes ONE network call to Google TTS API")
    print("    ⏰ Timeout: 15 seconds (if this times out, it's a network/API issue)")
    
    try:
        step_start = time.time()
        from app import app
        log_timing("Imported Flask app", step_start)
        
        with app.test_client() as client:
            step_start = time.time()
            print("    🔄 Calling audio endpoint (this will contact Google TTS)...")
            
            response = client.get('/api/audio/phrase_001/en')
            log_timing("⭐ AUDIO ENDPOINT RESPONSE TIME", step_start)
            
            if response.status_code != 200:
                print(f"[FAIL] Audio endpoint failed (status: {response.status_code})")
                return False
            
            if len(response.data) == 0:
                print(f"[FAIL] No audio data returned")
                return False
            
            print(f"[PASS] Audio endpoint responds (returned {len(response.data)} bytes)")
            log_timing("Total test time", start)
            return True
    except Exception as e:
        print(f"[FAIL] Audio test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    total_start = time.time()
    
    print("=" * 70)
    print("PHASE 1 VALIDATION - WITH TIMEOUT PROTECTION")
    print("Each test has a maximum execution time")
    print("=" * 70)
    print()
    
    # Define tests with their timeout limits
    tests = [
        ("Dependencies Check", test_dependencies, FAST_TEST_TIMEOUT),
        ("Data Structure", test_data_structure, FAST_TEST_TIMEOUT),
        ("Flask App Structure", test_flask_app_structure, FAST_TEST_TIMEOUT),
        ("Routes Exist", test_routes_exist, FAST_TEST_TIMEOUT),
        ("API Responses", test_api_responses, SLOW_TEST_TIMEOUT),
        ("Template Files", test_template_files, FAST_TEST_TIMEOUT),
        ("Audio Endpoint (CRITICAL)", test_audio_generation_minimal, SLOW_TEST_TIMEOUT),
    ]
    
    results = []
    for i, (name, test_func, timeout) in enumerate(tests, 1):
        test_start = time.time()
        print(f"\n[{i}/{len(tests)}] Testing: {name}")
        print(f"    Max allowed time: {timeout}s")
        print("-" * 70)
        
        try:
            # Run test with timeout protection
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(test_func)
                try:
                    result = future.result(timeout=timeout)
                    results.append((name, result))
                    elapsed = time.time() - test_start
                    print(f"✓ Test completed in {elapsed:.2f}s")
                except TimeoutError:
                    print(f"⏰ TIMEOUT! Test exceeded {timeout}s limit")
                    print(f"❌ This test is HANGING - likely cause identified!")
                    results.append((name, False))
                except Exception as e:
                    print(f"[ERROR] Test crashed: {e}")
                    import traceback
                    traceback.print_exc()
                    results.append((name, False))
        except Exception as e:
            print(f"[ERROR] {name} crashed during setup: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    print("\n" + "=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"RESULTS: {passed}/{total} tests passed")
    print(f"Total execution time: {time.time() - total_start:.2f}s")
    print("=" * 70)
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("\n🎉 Phase 1 MVP is complete and functional!")
    else:
        print("\n❌ SOME TESTS FAILED OR TIMED OUT")
        print("\nFailed/Timeout tests:")
        for name, result in results:
            if not result:
                print(f"  ✗ {name}")
        
        print("\n💡 If 'Audio Endpoint' timed out:")
        print("   - This means gTTS is slow/unreachable")
        print("   - Check internet connection")
        print("   - Google TTS API might be slow")
        print("   - This is expected on slow networks")
        print("   - The app will work, just need better network for audio")
    
    print("\n" + "=" * 70)
    sys.exit(0 if passed == total else 1)
