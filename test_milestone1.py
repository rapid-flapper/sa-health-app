"""
Milestone 1 Integration Test
Tests that all components are properly installed and configured
"""

from flask import Flask
from gtts import gTTS
import os

def test_flask():
    """Test Flask installation and app creation"""
    try:
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return 'Health App Test'
        
        print("[PASS] Flask app created successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Flask test failed: {e}")
        return False

def test_gtts():
    """Test gTTS installation and object creation"""
    try:
        tts = gTTS(text='Hello', lang='en')
        print("[PASS] gTTS object created successfully")
        return True
    except Exception as e:
        print(f"[FAIL] gTTS test failed: {e}")
        return False

def test_directory_structure():
    """Test that all required directories exist"""
    required_dirs = ['app', 'app/static', 'app/templates', 'data', 'health-venv']
    missing = [d for d in required_dirs if not os.path.isdir(d)]
    
    if missing:
        print(f"[FAIL] Missing directories: {missing}")
        return False
    else:
        print("[PASS] All required directories exist")
        return True

def test_required_files():
    """Test that all required files exist"""
    required_files = ['requirements.txt', '.gitignore', 'README.md']
    missing = [f for f in required_files if not os.path.isfile(f)]
    
    if missing:
        print(f"[FAIL] Missing files: {missing}")
        return False
    else:
        print("[PASS] All required files exist")
        return True

def test_requirements_content():
    """Test that requirements.txt contains Flask and gTTS"""
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_flask = 'Flask' in content
        has_gtts = 'gTTS' in content
        
        if has_flask and has_gtts:
            print("[PASS] requirements.txt contains Flask and gTTS")
            return True
        else:
            print(f"[FAIL] requirements.txt missing: Flask={has_flask}, gTTS={has_gtts}")
            return False
    except Exception as e:
        print(f"[FAIL] requirements.txt test failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("MILESTONE 1 VERIFICATION TESTS")
    print("=" * 50)
    print()
    
    tests = [
        test_flask,
        test_gtts,
        test_directory_structure,
        test_required_files,
        test_requirements_content
    ]
    
    results = [test() for test in tests]
    
    print()
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] MILESTONE 1: ALL TESTS PASSED")
        print("[SUCCESS] Ready to proceed to Milestone 2")
    else:
        print("[FAILURE] MILESTONE 1: SOME TESTS FAILED")
        print("[FAILURE] Please fix issues before proceeding")
    
    print("=" * 50)
