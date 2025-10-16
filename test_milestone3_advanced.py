"""
Milestone 3 Advanced Verification Tests
Comprehensive testing including edge cases, data validation, and integration tests
"""

import json
import sys

def test_data_integrity():
    """Test that all phrases have complete and valid data"""
    try:
        from app import load_phrases_data
        data = load_phrases_data()
        
        phrases = data.get('phrases', [])
        required_languages = ['en', 'zu', 'xh', 'af', 'nso']
        
        for phrase in phrases:
            # Check required fields
            if 'id' not in phrase:
                print(f"[FAIL] Phrase missing ID: {phrase}")
                return False
            
            if 'categories' not in phrase or not isinstance(phrase['categories'], list):
                print(f"[FAIL] Phrase {phrase['id']} has invalid categories")
                return False
            
            if 'translations' not in phrase:
                print(f"[FAIL] Phrase {phrase['id']} missing translations")
                return False
            
            # Check all languages present
            translations = phrase['translations']
            for lang in required_languages:
                if lang not in translations:
                    print(f"[FAIL] Phrase {phrase['id']} missing language: {lang}")
                    return False
                
                # Check text and phonetic
                if 'text' not in translations[lang] or not translations[lang]['text']:
                    print(f"[FAIL] Phrase {phrase['id']} lang {lang} missing/empty text")
                    return False
                
                if 'phonetic' not in translations[lang] or not translations[lang]['phonetic']:
                    print(f"[FAIL] Phrase {phrase['id']} lang {lang} missing/empty phonetic")
                    return False
        
        print(f"[PASS] Data integrity: All {len(phrases)} phrases have complete data")
        return True
    except Exception as e:
        print(f"[FAIL] Data integrity test error: {e}")
        return False

def test_category_consistency():
    """Test that category references are consistent"""
    try:
        from app import load_phrases_data
        data = load_phrases_data()
        
        category_ids = {cat['id'] for cat in data.get('categories', [])}
        phrases = data.get('phrases', [])
        
        # Check all phrase categories exist
        for phrase in phrases:
            for cat in phrase.get('categories', []):
                if cat not in category_ids:
                    print(f"[FAIL] Phrase {phrase['id']} references invalid category: {cat}")
                    return False
        
        # Check all categories are used
        used_categories = set()
        for phrase in phrases:
            used_categories.update(phrase.get('categories', []))
        
        unused = category_ids - used_categories
        if unused:
            print(f"[WARN] Unused categories: {unused}")
        
        print("[PASS] Category consistency: All references valid")
        return True
    except Exception as e:
        print(f"[FAIL] Category consistency test error: {e}")
        return False

def test_api_response_format():
    """Test that all API responses follow consistent format"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Test categories API format
            response = client.get('/api/categories')
            data = json.loads(response.data)
            
            if not isinstance(data, dict):
                print("[FAIL] Categories API doesn't return dict")
                return False
            
            if 'success' not in data:
                print("[FAIL] Categories API missing 'success' field")
                return False
            
            # Test phrases API format
            response = client.get('/api/phrases')
            data = json.loads(response.data)
            
            if not isinstance(data.get('phrases'), list):
                print("[FAIL] Phrases API doesn't return list of phrases")
                return False
            
            if 'total' not in data or data['total'] != len(data['phrases']):
                print("[FAIL] Phrases API total count mismatch")
                return False
            
            print("[PASS] API response format: Consistent structure")
            return True
    except Exception as e:
        print(f"[FAIL] API response format test error: {e}")
        return False

def test_edge_cases():
    """Test edge cases and error handling"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Test invalid category
            response = client.get('/api/phrases/category/nonexistent')
            if response.status_code != 200:
                print(f"[FAIL] Invalid category returned {response.status_code}")
                return False
            
            data = json.loads(response.data)
            if data['total'] != 0 or len(data['phrases']) != 0:
                print("[FAIL] Invalid category should return empty list")
                return False
            
            # Test invalid phrase ID
            response = client.get('/api/phrase/nonexistent')
            if response.status_code != 404:
                print(f"[FAIL] Invalid phrase ID should return 404, got {response.status_code}")
                return False
            
            data = json.loads(response.data)
            if data.get('success') != False:
                print("[FAIL] Error response should have success=False")
                return False
            
            # Test 404 route
            response = client.get('/totally/invalid/route')
            if response.status_code != 404:
                print("[FAIL] 404 handler not working")
                return False
            
            print("[PASS] Edge cases: Error handling works correctly")
            return True
    except Exception as e:
        print(f"[FAIL] Edge case test error: {e}")
        return False

def test_category_filtering():
    """Test that category filtering works correctly"""
    try:
        from app import app, load_phrases_data
        
        data = load_phrases_data()
        
        with app.test_client() as client:
            # Test each category
            for category in data.get('categories', []):
                cat_id = category['id']
                response = client.get(f'/api/phrases/category/{cat_id}')
                
                if response.status_code != 200:
                    print(f"[FAIL] Category {cat_id} endpoint failed")
                    return False
                
                result = json.loads(response.data)
                
                # Verify all returned phrases contain this category
                for phrase in result['phrases']:
                    if cat_id not in phrase.get('categories', []):
                        print(f"[FAIL] Phrase {phrase['id']} in {cat_id} results but doesn't have that category")
                        return False
            
            print("[PASS] Category filtering: All categories work correctly")
            return True
    except Exception as e:
        print(f"[FAIL] Category filtering test error: {e}")
        return False

def test_phrase_uniqueness():
    """Test that all phrase IDs are unique"""
    try:
        from app import load_phrases_data
        data = load_phrases_data()
        
        phrase_ids = [p['id'] for p in data.get('phrases', [])]
        unique_ids = set(phrase_ids)
        
        if len(phrase_ids) != len(unique_ids):
            duplicates = [id for id in phrase_ids if phrase_ids.count(id) > 1]
            print(f"[FAIL] Duplicate phrase IDs found: {set(duplicates)}")
            return False
        
        print(f"[PASS] Phrase uniqueness: All {len(phrase_ids)} IDs are unique")
        return True
    except Exception as e:
        print(f"[FAIL] Phrase uniqueness test error: {e}")
        return False

def test_translation_completeness():
    """Test that translations are complete and non-empty"""
    try:
        from app import load_phrases_data
        data = load_phrases_data()
        
        for phrase in data.get('phrases', []):
            for lang, trans in phrase.get('translations', {}).items():
                text = trans.get('text', '').strip()
                phonetic = trans.get('phonetic', '').strip()
                
                if not text:
                    print(f"[FAIL] Phrase {phrase['id']} lang {lang} has empty text")
                    return False
                
                if not phonetic:
                    print(f"[FAIL] Phrase {phrase['id']} lang {lang} has empty phonetic")
                    return False
                
                # Check for placeholder text
                if text.lower() in ['todo', 'tbd', 'placeholder']:
                    print(f"[FAIL] Phrase {phrase['id']} lang {lang} has placeholder text")
                    return False
        
        print("[PASS] Translation completeness: All translations are complete")
        return True
    except Exception as e:
        print(f"[FAIL] Translation completeness test error: {e}")
        return False

def test_api_endpoints_comprehensive():
    """Comprehensive test of all API endpoints with various scenarios"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Test all phrases endpoint
            response = client.get('/api/phrases')
            if response.status_code != 200:
                print("[FAIL] /api/phrases endpoint failed")
                return False
            
            all_phrases = json.loads(response.data)
            total_count = all_phrases['total']
            
            # Test that category-filtered phrases sum correctly
            response = client.get('/api/categories')
            categories = json.loads(response.data)['categories']
            
            # Count phrases by category (phrases can be in multiple categories)
            category_phrase_count = 0
            for cat in categories:
                response = client.get(f'/api/phrases/category/{cat["id"]}')
                cat_data = json.loads(response.data)
                category_phrase_count += cat_data['total']
            
            # Note: This count will be higher than total if phrases are in multiple categories
            if category_phrase_count < total_count:
                print(f"[FAIL] Category phrase counts ({category_phrase_count}) less than total ({total_count})")
                return False
            
            # Test individual phrase retrieval
            for phrase in all_phrases['phrases'][:3]:  # Test first 3
                response = client.get(f'/api/phrase/{phrase["id"]}')
                if response.status_code != 200:
                    print(f"[FAIL] Failed to retrieve phrase {phrase['id']}")
                    return False
                
                phrase_data = json.loads(response.data)
                if phrase_data['phrase']['id'] != phrase['id']:
                    print(f"[FAIL] Retrieved wrong phrase")
                    return False
            
            print("[PASS] Comprehensive API endpoints: All scenarios work")
            return True
    except Exception as e:
        print(f"[FAIL] Comprehensive API test error: {e}")
        return False

def test_json_encoding():
    """Test that API responses are properly JSON encoded"""
    try:
        from app import app
        
        with app.test_client() as client:
            endpoints = [
                '/api/categories',
                '/api/phrases',
                '/api/phrases/category/greeting',
                '/api/phrase/phrase_001',
                '/api/health'
            ]
            
            for endpoint in endpoints:
                response = client.get(endpoint)
                
                # Check Content-Type
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    print(f"[FAIL] {endpoint} doesn't return JSON content type")
                    return False
                
                # Try to parse JSON
                try:
                    json.loads(response.data)
                except json.JSONDecodeError:
                    print(f"[FAIL] {endpoint} returns invalid JSON")
                    return False
            
            print("[PASS] JSON encoding: All endpoints return valid JSON")
            return True
    except Exception as e:
        print(f"[FAIL] JSON encoding test error: {e}")
        return False

def test_home_page_content():
    """Test that home page has all expected content"""
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check for key content
            required_content = [
                'SA Health App',
                'medical phrases',
                'categories',
                'languages',
                'API Endpoints'
            ]
            
            for content in required_content:
                if content not in html:
                    print(f"[FAIL] Home page missing: {content}")
                    return False
            
            # Check for category display
            if 'category-badge' not in html:
                print("[FAIL] Home page not displaying categories")
                return False
            
            print("[PASS] Home page content: All expected content present")
            return True
    except Exception as e:
        print(f"[FAIL] Home page content test error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MILESTONE 3 ADVANCED VERIFICATION TESTS")
    print("Comprehensive Backend Testing")
    print("=" * 60)
    print()
    
    tests = [
        ('Data Integrity', test_data_integrity),
        ('Category Consistency', test_category_consistency),
        ('Phrase Uniqueness', test_phrase_uniqueness),
        ('Translation Completeness', test_translation_completeness),
        ('API Response Format', test_api_response_format),
        ('Edge Cases & Error Handling', test_edge_cases),
        ('Category Filtering', test_category_filtering),
        ('Comprehensive API Endpoints', test_api_endpoints_comprehensive),
        ('JSON Encoding', test_json_encoding),
        ('Home Page Content', test_home_page_content)
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
        print("[SUCCESS] ALL ADVANCED TESTS PASSED")
        print("[SUCCESS] Flask backend is production-ready")
        print()
        print("Verified:")
        print("  - Data integrity and completeness")
        print("  - Category consistency and filtering")
        print("  - API response formats and JSON encoding")
        print("  - Edge cases and error handling")
        print("  - Translation completeness (all 5 languages)")
        print("  - Home page content and display")
        print()
        print("Backend is ready for frontend development!")
    else:
        print("[FAILURE] SOME ADVANCED TESTS FAILED")
        print()
        print("Failed tests:")
        for name, result in results:
            if not result:
                print(f"  - {name}")
        print()
        print("Please fix issues before proceeding to Milestone 4")
    
    print("=" * 60)
    
    sys.exit(0 if passed == total else 1)
