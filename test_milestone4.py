"""
Milestone 4 Verification Tests
Tests frontend UI, routes, and user interface functionality
"""

import sys

def test_app_route():
    """Test that /app route exists and loads"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            
            if response.status_code != 200:
                print(f"[FAIL] /app route returned status {response.status_code}")
                return False
            
            html = response.data.decode('utf-8')
            
            # Check for key UI elements
            required_elements = [
                'SA Health App',
                'Select Language',
                'Filter by Category',
                'language-select',
                'category-chips',
                'phrases-container'
            ]
            
            for element in required_elements:
                if element not in html:
                    print(f"[FAIL] /app missing element: {element}")
                    return False
            
            print("[PASS] /app route loads with all UI elements")
            return True
    except Exception as e:
        print(f"[FAIL] /app route test error: {e}")
        return False

def test_home_page_updated():
    """Test that home page has link to interactive app"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            if '/app' not in html:
                print("[FAIL] Home page missing link to /app")
                return False
            
            if 'Launch Interactive App' not in html:
                print("[FAIL] Home page missing app launch button")
                return False
            
            print("[PASS] Home page has link to interactive app")
            return True
    except Exception as e:
        print(f"[FAIL] Home page test error: {e}")
        return False

def test_ui_components():
    """Test that all UI components are present in app.html"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Language selector
            if '<select id="language-select">' not in html:
                print("[FAIL] Language selector missing")
                return False
            
            # Check all 5 languages
            languages = [
                ('English', 'value="en"'),
                ('Zulu', 'value="zu"'),
                ('Xhosa', 'value="xh"'),
                ('Afrikaans', 'value="af"'),
                ('Sepedi', 'value="nso"')
            ]
            
            for lang_name, lang_value in languages:
                if lang_value not in html:
                    print(f"[FAIL] Language {lang_name} missing")
                    return False
            
            # Category filter
            if 'category-chips' not in html:
                print("[FAIL] Category filter missing")
                return False
            
            # Phrases container
            if 'phrases-container' not in html:
                print("[FAIL] Phrases container missing")
                return False
            
            print("[PASS] All UI components present")
            return True
    except Exception as e:
        print(f"[FAIL] UI components test error: {e}")
        return False

def test_javascript_functionality():
    """Test that JavaScript code is present for interactivity"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for key JavaScript functions
            required_functions = [
                'loadCategories',
                'loadPhrases',
                'renderPhrases',
                'selectCategory',
                'playAudio',
                'fetch(\'/api/'
            ]
            
            for func in required_functions:
                if func not in html:
                    print(f"[FAIL] JavaScript function missing: {func}")
                    return False
            
            print("[PASS] JavaScript functionality present")
            return True
    except Exception as e:
        print(f"[FAIL] JavaScript test error: {e}")
        return False

def test_mobile_responsive_design():
    """Test that mobile-responsive CSS is present"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for viewport meta tag
            if 'name="viewport"' not in html:
                print("[FAIL] Missing viewport meta tag")
                return False
            
            # Check for mobile-first CSS
            if '@media (max-width: 480px)' not in html:
                print("[FAIL] Missing mobile-responsive CSS")
                return False
            
            # Check for flexbox/mobile-friendly layout
            if 'flex-wrap: wrap' not in html:
                print("[FAIL] Missing flexible layout CSS")
                return False
            
            print("[PASS] Mobile-responsive design implemented")
            return True
    except Exception as e:
        print(f"[FAIL] Mobile responsive test error: {e}")
        return False

def test_styling_present():
    """Test that modern styling is applied"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for CSS variables
            if ':root {' not in html or '--primary' not in html:
                print("[FAIL] CSS variables missing")
                return False
            
            # Check for animations/transitions
            if 'transition:' not in html:
                print("[FAIL] CSS transitions missing")
                return False
            
            # Check for modern styling
            styling_features = [
                'border-radius',
                'box-shadow',
                'gradient',
                'backdrop-filter'
            ]
            
            for feature in styling_features:
                if feature not in html.lower():
                    print(f"[FAIL] Modern CSS feature missing: {feature}")
                    return False
            
            print("[PASS] Modern styling applied")
            return True
    except Exception as e:
        print(f"[FAIL] Styling test error: {e}")
        return False

def test_api_integration():
    """Test that frontend calls backend APIs"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for API calls
            api_endpoints = [
                '/api/categories',
                '/api/phrases'
            ]
            
            for endpoint in api_endpoints:
                if endpoint not in html:
                    print(f"[FAIL] Frontend not calling {endpoint}")
                    return False
            
            print("[PASS] Frontend integrates with backend APIs")
            return True
    except Exception as e:
        print(f"[FAIL] API integration test error: {e}")
        return False

def test_category_display():
    """Test that categories will be displayed correctly"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for category chip rendering
            if 'category-chip' not in html:
                print("[FAIL] Category chip styling missing")
                return False
            
            # Check for icon display
            if 'class="icon"' not in html:
                print("[FAIL] Category icon display missing")
                return False
            
            print("[PASS] Category display implemented")
            return True
    except Exception as e:
        print(f"[FAIL] Category display test error: {e}")
        return False

def test_phrase_display():
    """Test that phrases will be displayed with all required info"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for phrase display elements
            required_elements = [
                'phrase-card',
                'phrase-text',
                'phrase-phonetic',
                'play-button'
            ]
            
            for element in required_elements:
                if element not in html:
                    print(f"[FAIL] Phrase display element missing: {element}")
                    return False
            
            print("[PASS] Phrase display structure complete")
            return True
    except Exception as e:
        print(f"[FAIL] Phrase display test error: {e}")
        return False

def test_phonetic_guide_display():
    """Test that phonetic pronunciation guides are displayed"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/app')
            html = response.data.decode('utf-8')
            
            # Check for phonetic display
            if 'phrase-phonetic' not in html:
                print("[FAIL] Phonetic guide display missing")
                return False
            
            # Check for phonetic icon
            if '🗣️' not in html:
                print("[FAIL] Phonetic icon missing")
                return False
            
            print("[PASS] Phonetic pronunciation display implemented")
            return True
    except Exception as e:
        print(f"[FAIL] Phonetic guide test error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MILESTONE 4 VERIFICATION TESTS")
    print("Frontend UI Testing")
    print("=" * 60)
    print()
    
    tests = [
        ('App Route', test_app_route),
        ('Home Page Updated', test_home_page_updated),
        ('UI Components', test_ui_components),
        ('JavaScript Functionality', test_javascript_functionality),
        ('Mobile Responsive Design', test_mobile_responsive_design),
        ('Modern Styling', test_styling_present),
        ('API Integration', test_api_integration),
        ('Category Display', test_category_display),
        ('Phrase Display', test_phrase_display),
        ('Phonetic Guide Display', test_phonetic_guide_display)
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
        print("[SUCCESS] ALL FRONTEND TESTS PASSED")
        print("[SUCCESS] UI is ready for user testing")
        print()
        print("Verified:")
        print("  [OK] Interactive app route (/app)")
        print("  [OK] Mobile-first responsive design")
        print("  [OK] Category filtering interface")
        print("  [OK] Language selection (5 languages)")
        print("  [OK] Phrase display with translations")
        print("  [OK] Phonetic pronunciation guides")
        print("  [OK] Modern, clean styling")
        print("  [OK] Backend API integration")
        print()
        print("Ready to test visually:")
        print("  1. Run: python app.py")
        print("  2. Visit: http://localhost:5000/app")
        print("  3. Test on mobile viewport in browser DevTools")
    else:
        print("[FAILURE] SOME FRONTEND TESTS FAILED")
        print("Please fix issues before proceeding")
    
    print("=" * 60)
    
    sys.exit(0 if passed == total else 1)
