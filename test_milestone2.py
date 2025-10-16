"""
Milestone 2 Verification Test
Tests JSON data structure, loading, and content
"""

import json
import os

def test_json_file_exists():
    """Test that phrases.json file exists"""
    if os.path.isfile('data/phrases.json'):
        print("[PASS] phrases.json file exists")
        return True
    else:
        print("[FAIL] phrases.json file not found")
        return False

def test_json_valid():
    """Test that JSON file is valid and can be parsed"""
    try:
        with open('data/phrases.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("[PASS] JSON file is valid and parseable")
        return True, data
    except json.JSONDecodeError as e:
        print(f"[FAIL] JSON parsing error: {e}")
        return False, None
    except Exception as e:
        print(f"[FAIL] Error loading JSON: {e}")
        return False, None

def test_json_structure(data):
    """Test that JSON has expected top-level structure"""
    if data is None:
        print("[FAIL] No data to test structure")
        return False
    
    required_keys = ['categories', 'phrases']
    missing_keys = [key for key in required_keys if key not in data]
    
    if missing_keys:
        print(f"[FAIL] Missing required keys: {missing_keys}")
        return False
    else:
        print("[PASS] JSON has correct top-level structure")
        return True

def test_categories(data):
    """Test categories structure and content"""
    if data is None or 'categories' not in data:
        print("[FAIL] Cannot test categories")
        return False
    
    categories = data['categories']
    
    if not isinstance(categories, list):
        print("[FAIL] Categories is not a list")
        return False
    
    if len(categories) == 0:
        print("[FAIL] No categories defined")
        return False
    
    # Check category structure
    required_fields = ['id', 'name', 'icon', 'description']
    for cat in categories:
        missing = [field for field in required_fields if field not in cat]
        if missing:
            print(f"[FAIL] Category missing fields: {missing}")
            return False
    
    print(f"[PASS] {len(categories)} categories defined with correct structure")
    return True

def test_phrases(data):
    """Test phrases structure and content"""
    if data is None or 'phrases' not in data:
        print("[FAIL] Cannot test phrases")
        return False
    
    phrases = data['phrases']
    
    if not isinstance(phrases, list):
        print("[FAIL] Phrases is not a list")
        return False
    
    if len(phrases) == 0:
        print("[FAIL] No phrases defined")
        return False
    
    # Check phrase structure
    required_fields = ['id', 'categories', 'translations']
    for phrase in phrases:
        missing = [field for field in required_fields if field not in phrase]
        if missing:
            print(f"[FAIL] Phrase {phrase.get('id', 'unknown')} missing fields: {missing}")
            return False
    
    print(f"[PASS] {len(phrases)} phrases defined with correct structure")
    return True

def test_languages(data):
    """Test that all 5 languages are present in phrases"""
    if data is None or 'phrases' not in data:
        print("[FAIL] Cannot test languages")
        return False
    
    required_languages = ['en', 'zu', 'xh', 'af', 'nso']
    phrases = data['phrases']
    
    for phrase in phrases:
        translations = phrase.get('translations', {})
        missing_langs = [lang for lang in required_languages if lang not in translations]
        
        if missing_langs:
            print(f"[FAIL] Phrase {phrase['id']} missing languages: {missing_langs}")
            return False
        
        # Check each translation has text and phonetic
        for lang, trans in translations.items():
            if 'text' not in trans or 'phonetic' not in trans:
                print(f"[FAIL] Phrase {phrase['id']} lang {lang} missing text or phonetic")
                return False
    
    print(f"[PASS] All phrases have all 5 languages (en, zu, xh, af, nso)")
    print(f"[PASS] All translations have text and phonetic guides")
    return True

def test_category_references(data):
    """Test that phrase categories reference valid category IDs"""
    if data is None:
        print("[FAIL] Cannot test category references")
        return False
    
    category_ids = {cat['id'] for cat in data.get('categories', [])}
    phrases = data.get('phrases', [])
    
    for phrase in phrases:
        phrase_cats = phrase.get('categories', [])
        invalid_cats = [cat for cat in phrase_cats if cat not in category_ids]
        
        if invalid_cats:
            print(f"[FAIL] Phrase {phrase['id']} references invalid categories: {invalid_cats}")
            return False
    
    print("[PASS] All phrase category references are valid")
    return True

def print_data_summary(data):
    """Print summary of loaded data"""
    if data is None:
        return
    
    print()
    print("=" * 50)
    print("DATA SUMMARY")
    print("=" * 50)
    
    categories = data.get('categories', [])
    phrases = data.get('phrases', [])
    
    print(f"Total Categories: {len(categories)}")
    for cat in categories:
        print(f"  - {cat['name']} ({cat['id']})")
    
    print(f"\nTotal Phrases: {len(phrases)}")
    print(f"Languages per phrase: 5 (en, zu, xh, af, nso)")
    
    # Count phrases by category
    category_counts = {}
    for phrase in phrases:
        for cat in phrase.get('categories', []):
            category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("\nPhrases by Category:")
    for cat_id, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        cat_name = next((c['name'] for c in categories if c['id'] == cat_id), cat_id)
        print(f"  - {cat_name}: {count} phrases")

if __name__ == '__main__':
    print("=" * 50)
    print("MILESTONE 2 VERIFICATION TESTS")
    print("=" * 50)
    print()
    
    tests = []
    data = None
    
    # Test 1: File exists
    tests.append(('File Exists', test_json_file_exists()))
    
    # Test 2: Valid JSON
    valid, data = test_json_valid()
    tests.append(('Valid JSON', valid))
    
    if data:
        # Test 3-7: Structure and content
        tests.append(('JSON Structure', test_json_structure(data)))
        tests.append(('Categories', test_categories(data)))
        tests.append(('Phrases', test_phrases(data)))
        tests.append(('Languages', test_languages(data)))
        tests.append(('Category References', test_category_references(data)))
    
    print()
    print("=" * 50)
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] MILESTONE 2: ALL TESTS PASSED")
        print("[SUCCESS] JSON data structure is valid and ready")
        print_data_summary(data)
    else:
        print("[FAILURE] MILESTONE 2: SOME TESTS FAILED")
        print("[FAILURE] Please fix issues before proceeding")
    
    print("=" * 50)
