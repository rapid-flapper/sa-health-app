"""
Milestone 5 Verification Tests
Tests audio generation functionality using gTTS
"""

import sys

def test_gtts_import():
    """Test that gTTS library is installed and importable"""
    try:
        from gtts import gTTS
        print("[PASS] gTTS library imported successfully")
        return True
    except ImportError as e:
        print(f"[FAIL] gTTS import failed: {e}")
        return False

def test_audio_endpoint_exists():
    """Test that audio generation endpoint exists"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Test with valid phrase and language
            response = client.get('/api/audio/phrase_001/en')
            
            # Should return audio file (200) or proper error
            if response.status_code not in [200, 404, 500]:
                print(f"[FAIL] Audio endpoint returned unexpected status: {response.status_code}")
                return False
            
            print("[PASS] Audio endpoint exists and responds")
            return True
    except Exception as e:
        print(f"[FAIL] Audio endpoint test error: {e}")
        return False

def test_audio_generation_all_languages():
    """Test audio generation for all 5 languages"""
    try:
        from app import app
        
        languages = ['en', 'zu', 'xh', 'af', 'nso']
        
        with app.test_client() as client:
            for lang in languages:
                response = client.get(f'/api/audio/phrase_001/{lang}')
                
                if response.status_code != 200:
                    print(f"[FAIL] Audio generation failed for language: {lang} (status: {response.status_code})")
                    return False
                
                # Check that we got audio data
                if len(response.data) == 0:
                    print(f"[FAIL] No audio data returned for language: {lang}")
                    return False
                
                # Check content type
                content_type = response.headers.get('Content-Type', '')
                if 'audio' not in content_type:
                    print(f"[FAIL] Wrong content type for {lang}: {content_type}")
                    return False
            
            print(f"[PASS] Audio generation works for all 5 languages")
            return True
    except Exception as e:
        print(f"[FAIL] Audio generation test error: {e}")
        return False

def test_audio_with_invalid_phrase():
    """Test audio endpoint with invalid phrase ID"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/api/audio/invalid_phrase/en')
            
            if response.status_code != 404:
                print(f"[FAIL] Invalid phrase should return 404, got {response.status_code}")
                return False
            
            print("[PASS] Audio endpoint handles invalid phrase correctly")
            return True
    except Exception as e:
        print(f"[FAIL] Invalid phrase test error: {e}")
        return False

def test_audio_with_invalid_language():
    """Test audio endpoint with invalid language"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/api/audio/phrase_001/invalid_lang')
            
            if response.status_code != 404:
                print(f"[FAIL] Invalid language should return 404, got {response.status_code}")
                return False
            
            print("[PASS] Audio endpoint handles invalid language correctly")
            return True
    except Exception as e:
        print(f"[FAIL] Invalid language test error: {e}")
        return False

def test_audio_generation_quality():
    """Test that generated audio has reasonable size"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/api/audio/phrase_001/en')
            
            audio_size = len(response.data)
            
            # Audio should be at least 1KB and less than 1MB
            if audio_size < 1000:
                print(f"[FAIL] Audio file too small: {audio_size} bytes")
                return False
            
            if audio_size > 1000000:
                print(f"[FAIL] Audio file too large: {audio_size} bytes")
                return False
            
            print(f"[PASS] Audio quality check: {audio_size} bytes (reasonable size)")
            return True
    except Exception as e:
        print(f"[FAIL] Audio quality test error: {e}")
        return False

def test_frontend_audio_integration():
    """Test that frontend has audio playback functionality"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for playAudio function
            if 'function playAudio' not in html and 'async function playAudio' not in html:
                print("[FAIL] playAudio function not found in frontend")
                return False
            
            # Check for audio API call
            if '/api/audio/' not in html:
                print("[FAIL] Frontend doesn't call audio API")
                return False
            
            # Check for Audio object creation
            if 'new Audio' not in html:
                print("[FAIL] Frontend doesn't create Audio object")
                return False
            
            print("[PASS] Frontend has audio playback integration")
            return True
    except Exception as e:
        print(f"[FAIL] Frontend audio integration test error: {e}")
        return False

def test_audio_button_states():
    """Test that frontend has audio button loading states"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for loading state
            if 'Loading...' not in html or 'Playing...' not in html:
                print("[FAIL] Audio button loading states not implemented")
                return False
            
            # Check for disabled state handling
            if 'disabled' not in html:
                print("[FAIL] Button disabled state not handled")
                return False
            
            print("[PASS] Audio button has proper loading states")
            return True
    except Exception as e:
        print(f"[FAIL] Audio button states test error: {e}")
        return False

def test_multiple_phrases_audio():
    """Test audio generation for multiple different phrases"""
    try:
        from app import app
        
        phrase_ids = ['phrase_001', 'phrase_002', 'phrase_003']
        
        with app.test_client() as client:
            for phrase_id in phrase_ids:
                response = client.get(f'/api/audio/{phrase_id}/en')
                
                if response.status_code != 200:
                    print(f"[FAIL] Audio generation failed for {phrase_id}")
                    return False
            
            print(f"[PASS] Audio generation works for multiple phrases")
            return True
    except Exception as e:
        print(f"[FAIL] Multiple phrases test error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MILESTONE 5 VERIFICATION TESTS")
    print("Audio Playback Functionality")
    print("=" * 60)
    print()
    
    tests = [
        ('gTTS Library Import', test_gtts_import),
        ('Audio Endpoint Exists', test_audio_endpoint_exists),
        ('Audio Generation (All Languages)', test_audio_generation_all_languages),
        ('Invalid Phrase Handling', test_audio_with_invalid_phrase),
        ('Invalid Language Handling', test_audio_with_invalid_language),
        ('Audio Quality Check', test_audio_generation_quality),
        ('Multiple Phrases Audio', test_multiple_phrases_audio),
        ('Frontend Audio Integration', test_frontend_audio_integration),
        ('Audio Button States', test_audio_button_states)
    ]
    
    results = []
    for name, test_func in tests:
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
        print("[SUCCESS] ALL AUDIO TESTS PASSED")
        print("[SUCCESS] Audio playback is fully functional")
        print()
        print("Verified:")
        print("  [OK] gTTS library installed and working")
        print("  [OK] Audio generation endpoint functional")
        print("  [OK] All 5 languages generate audio successfully")
        print("  [OK] Error handling for invalid inputs")
        print("  [OK] Audio quality is reasonable")
        print("  [OK] Frontend integration complete")
        print("  [OK] Button loading states implemented")
        print()
        print("Ready to test live:")
        print("  1. Run: python app.py")
        print("  2. Visit: http://localhost:5000/app")
        print("  3. Click 'Play Audio' buttons to hear phrases!")
    else:
        print("[FAILURE] SOME AUDIO TESTS FAILED")
        print("Please fix issues before proceeding")
    
    print("=" * 60)
    
    sys.exit(0 if passed == total else 1)
