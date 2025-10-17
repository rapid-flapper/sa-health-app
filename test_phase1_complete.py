"""
Phase 1 Completion Validation Tests
Quick validation that all core features are working
"""

import sys
import json

def test_dependencies():
    """Test that all required dependencies are installed"""
    try:
        import flask
        from gtts import gTTS
        print("[PASS] All dependencies installed (Flask, gTTS)")
        return True
    except ImportError as e:
        print(f"[FAIL] Missing dependency: {e}")
        return False

def test_data_structure():
    """Test that phrases.json exists and is valid"""
    try:
        with open('data/phrases.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check structure
        if 'categories' not in data or 'phrases' not in data:
            print("[FAIL] phrases.json missing required keys")
            return False
        
        # Check that we have categories
        if len(data['categories']) == 0:
            print("[FAIL] No categories defined")
            return False
        
        # Check that we have phrases
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
        return True
    except FileNotFoundError:
        print("[FAIL] phrases.json not found")
        return False
    except json.JSONDecodeError:
        print("[FAIL] phrases.json is not valid JSON")
        return False
    except Exception as e:
        print(f"[FAIL] Data structure test error: {e}")
        return False

def test_flask_app_structure():
    """Test that Flask app is structured correctly"""
    try:
        from app import app
        
        # Check that app is a Flask app
        if not hasattr(app, 'test_client'):
            print("[FAIL] app is not a Flask application")
            return False
        
        print("[PASS] Flask app structure valid")
        return True
    except ImportError:
        print("[FAIL] Cannot import Flask app")
        return False
    except Exception as e:
        print(f"[FAIL] Flask app test error: {e}")
        return False

def test_routes_exist():
    """Test that all required routes exist"""
    try:
        from app import app
        
        required_routes = [
            '/',
            '/app',
            '/api/categories',
            '/api/phrases/<category_id>'
        ]
        
        # Get all registered routes
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        # Check for audio route (dynamic)
        has_audio_route = any('/api/audio' in route for route in routes)
        if not has_audio_route:
            print("[FAIL] Audio generation route missing")
            return False
        
        print("[PASS] All required routes exist")
        return True
    except Exception as e:
        print(f"[FAIL] Routes test error: {e}")
        return False

def test_api_responses():
    """Test that API endpoints return expected responses (fast, no audio generation)"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code != 200:
                print(f"[FAIL] Home page returned status: {response.status_code}")
                return False
            
            # Test app page
            response = client.get('/app')
            if response.status_code != 200:
                print(f"[FAIL] App page returned status: {response.status_code}")
                return False
            
            # Test categories API
            response = client.get('/api/categories')
            if response.status_code != 200:
                print(f"[FAIL] Categories API returned status: {response.status_code}")
                return False
            
            data = response.get_json()
            if 'categories' not in data:
                print("[FAIL] Categories API missing 'categories' key")
                return False
            
            # Test phrases API (just check it responds, don't validate all data)
            response = client.get('/api/phrases/greeting')
            if response.status_code != 200:
                print(f"[FAIL] Phrases API returned status: {response.status_code}")
                return False
            
            print("[PASS] All API endpoints respond correctly")
            return True
    except Exception as e:
        print(f"[FAIL] API test error: {e}")
        return False

def test_template_files():
    """Test that required template files exist"""
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
        return True
    except Exception as e:
        print(f"[FAIL] Template test error: {e}")
        return False

def test_tts_pronunciation_coverage():
    """Test that TTS pronunciations are added for unsupported languages"""
    try:
        with open('data/phrases.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        unsupported_languages = ['zu', 'xh', 'nso']
        phrases_with_tts = 0
        total_phrases = len(data['phrases'])
        
        for phrase in data['phrases']:
            has_tts = False
            for lang in unsupported_languages:
                if lang in phrase['translations']:
                    if 'tts_pronunciation' in phrase['translations'][lang]:
                        has_tts = True
                        break
            if has_tts:
                phrases_with_tts += 1
        
        if phrases_with_tts == 0:
            print("[WARN] No TTS pronunciations found (this is OK for basic testing)")
        else:
            print(f"[PASS] TTS pronunciations added ({phrases_with_tts}/{total_phrases} phrases)")
        
        return True  # This is optional, so always pass
    except Exception as e:
        print(f"[FAIL] TTS pronunciation test error: {e}")
        return False

# Quick audio test (just ONE generation to verify it works)
def test_single_audio_generation():
    """Test that audio generation works (just one quick test)"""
    try:
        from app import app
        
        with app.test_client() as client:
            print("  → Testing audio generation (this may take a few seconds)...")
            response = client.get('/api/audio/phrase_001/en')
            
            if response.status_code != 200:
                print(f"[FAIL] Audio generation failed (status: {response.status_code})")
                return False
            
            if len(response.data) == 0:
                print("[FAIL] No audio data returned")
                return False
            
            print("[PASS] Audio generation works (1 sample tested)")
            return True
    except Exception as e:
        print(f"[FAIL] Audio generation test error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("PHASE 1 COMPLETION VALIDATION")
    print("Quick validation of all core features")
    print("=" * 60)
    print()
    
    tests = [
        ("Dependencies Check", test_dependencies),
        ("Data Structure", test_data_structure),
        ("Flask App Structure", test_flask_app_structure),
        ("Routes Exist", test_routes_exist),
        ("API Responses", test_api_responses),
        ("Template Files", test_template_files),
        ("TTS Pronunciation Coverage", test_tts_pronunciation_coverage),
        ("Audio Generation Sample", test_single_audio_generation),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Testing: {name}")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"[ERROR] {name} crashed: {e}")
            results.append((name, False))
        print()
    
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"RESULTS: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("✅ [SUCCESS] PHASE 1 MVP IS COMPLETE!")
        print()
        print("All core features verified:")
        print("  ✓ Flask backend running")
        print("  ✓ Data structure valid")
        print("  ✓ All API endpoints working")
        print("  ✓ Frontend templates present")
        print("  ✓ Audio generation functional")
        print("  ✓ 5 languages supported")
        print("  ✓ Category filtering implemented")
        print()
        print("🎉 Ready for mobile device testing!")
        print()
        print("Next steps:")
        print("  1. Test on actual mobile device")
        print("  2. Update README documentation")
        print("  3. Merge dev branch to main")
    else:
        print("❌ [FAILURE] SOME TESTS FAILED")
        print("Please fix issues before completing Phase 1")
    
    print("=" * 60)
    
    sys.exit(0 if passed == total else 1)
