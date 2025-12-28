import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5000'

def test_api():
    print("=== Starting API Tests ===")
    
    # 1. Test Schulte Record
    print("\n[Test 1] Saving Schulte Record...")
    schulte_data = {
        'game_type': 'schulte',
        'player_name': 'SchulteTester',
        'difficulty': '3',
        'score': 10.5,
        'accuracy': 100.0
    }
    try:
        res = requests.post(f'{BASE_URL}/api/record', json=schulte_data)
        if res.status_code == 201:
            print("✅ Schulte record saved.")
        else:
            print(f"❌ Failed to save Schulte record: {res.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return

    # 2. Test Stroop Record
    print("\n[Test 2] Saving Stroop Record...")
    stroop_data = {
        'game_type': 'stroop',
        'player_name': 'StroopTester',
        'difficulty': '20',
        'score': 18.2,
        'accuracy': 100.0
    }
    try:
        res = requests.post(f'{BASE_URL}/api/record', json=stroop_data)
        if res.status_code == 201:
            print("✅ Stroop record saved.")
        else:
            print(f"❌ Failed to save Stroop record: {res.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return

    # 3. Fetch Schulte Records
    print("\n[Test 3] Fetching Schulte Records...")
    try:
        res = requests.get(f'{BASE_URL}/api/records?game_type=schulte')
        data = res.json()
        # Check if our tester is in the list (might not be top if others are better, but let's check structure)
        if isinstance(data, list) and len(data) > 0:
            print(f"✅ Retrieved {len(data)} Schulte records.")
            print(f"   Top record: {data[0]}")
        else:
            print("⚠️ No Schulte records found or invalid format.")
    except Exception as e:
        print(f"❌ Error fetching Schulte records: {e}")

    # 4. Fetch Stroop Records
    print("\n[Test 4] Fetching Stroop Records...")
    try:
        res = requests.get(f'{BASE_URL}/api/records?game_type=stroop')
        data = res.json()
        if isinstance(data, list) and len(data) > 0:
            print(f"✅ Retrieved {len(data)} Stroop records.")
            print(f"   Top record: {data[0]}")
            
            # Verify content
            has_stroop = any(r['game_type'] == 'stroop' for r in data)
            if has_stroop:
                print("✅ Verified 'stroop' game_type in response.")
            else:
                print("❌ 'stroop' game_type missing in response.")
        else:
            print("⚠️ No Stroop records found.")
    except Exception as e:
        print(f"❌ Error fetching Stroop records: {e}")

    print("\n=== Tests Completed ===")

if __name__ == "__main__":
    # Ensure server is running before testing? 
    # For this script, we assume the user might have it running, 
    # OR we can try to run it. 
    # Since I'm an agent, I'll run the server in a separate process in the main flow.
    # This script just hits the endpoints.
    test_api()
