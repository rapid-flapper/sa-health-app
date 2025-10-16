"""
Live Server Test
Starts the Flask server and makes real HTTP requests to verify it works
"""

import subprocess
import time
import requests
import sys
import signal

def test_server_startup():
    """Test that the Flask server starts without errors"""
    print("Starting Flask server...")
    
    # Start server in subprocess
    process = subprocess.Popen(
        ['health-venv\\Scripts\\python.exe', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    print("Waiting for server to initialize...")
    time.sleep(3)
    
    # Check if process is still running
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print("[FAIL] Server failed to start")
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        return None
    
    print("[PASS] Server started successfully")
    return process

def test_live_endpoints(base_url='http://localhost:5000'):
    """Test all endpoints with live HTTP requests"""
    tests_passed = 0
    tests_total = 0
    
    endpoints_to_test = [
        ('Home Page', '/'),
        ('Categories API', '/api/categories'),
        ('Phrases API', '/api/phrases'),
        ('Category Filter', '/api/phrases/category/greeting'),
        ('Single Phrase', '/api/phrase/phrase_001'),
        ('Health Check', '/api/health'),
        ('404 Handler', '/nonexistent')
    ]
    
    for name, endpoint in endpoints_to_test:
        tests_total += 1
        url = f"{base_url}{endpoint}"
        
        try:
            response = requests.get(url, timeout=5)
            
            if endpoint == '/nonexistent':
                # Expect 404
                if response.status_code == 404:
                    print(f"[PASS] {name}: 404 handled correctly")
                    tests_passed += 1
                else:
                    print(f"[FAIL] {name}: Expected 404, got {response.status_code}")
            elif endpoint == '/':
                # Expect HTML
                if response.status_code == 200 and 'SA Health App' in response.text:
                    print(f"[PASS] {name}: Loaded successfully")
                    tests_passed += 1
                else:
                    print(f"[FAIL] {name}: Status {response.status_code}")
            else:
                # Expect JSON
                if response.status_code == 200:
                    data = response.json()
                    if 'success' in data or 'status' in data:
                        print(f"[PASS] {name}: Returns valid JSON")
                        tests_passed += 1
                    else:
                        print(f"[FAIL] {name}: Invalid JSON structure")
                else:
                    print(f"[FAIL] {name}: Status {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            print(f"[FAIL] {name}: Could not connect to server")
        except requests.exceptions.Timeout:
            print(f"[FAIL] {name}: Request timed out")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
    
    return tests_passed, tests_total

def test_performance():
    """Test server performance with multiple requests"""
    print("\nPerformance test: Making 20 rapid requests...")
    
    base_url = 'http://localhost:5000'
    start_time = time.time()
    
    try:
        for i in range(20):
            response = requests.get(f"{base_url}/api/phrases", timeout=5)
            if response.status_code != 200:
                print(f"[FAIL] Request {i+1} failed with status {response.status_code}")
                return False
        
        elapsed = time.time() - start_time
        avg_time = elapsed / 20
        
        print(f"[PASS] 20 requests completed in {elapsed:.2f}s (avg: {avg_time:.3f}s per request)")
        
        if avg_time > 1.0:
            print("[WARN] Average response time > 1 second")
        
        return True
    except Exception as e:
        print(f"[FAIL] Performance test error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("LIVE SERVER TEST")
    print("=" * 60)
    print()
    
    # Start server
    server_process = test_server_startup()
    
    if server_process is None:
        print("\n[CRITICAL] Cannot proceed without running server")
        sys.exit(1)
    
    try:
        print()
        print("Testing live endpoints...")
        print("-" * 60)
        passed, total = test_live_endpoints()
        
        print()
        perf_result = test_performance()
        
        print()
        print("=" * 60)
        print(f"RESULTS: {passed}/{total} endpoint tests passed")
        
        if passed == total and perf_result:
            print("[SUCCESS] Live server is fully functional")
            print("[SUCCESS] All endpoints responding correctly")
        else:
            print("[FAILURE] Some live tests failed")
        
        print("=" * 60)
        
    finally:
        # Stop server
        print("\nShutting down server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
            print("Server stopped successfully")
        except subprocess.TimeoutExpired:
            server_process.kill()
            print("Server force killed")
