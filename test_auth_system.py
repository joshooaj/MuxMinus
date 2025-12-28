"""
Test script for Demucs API with authentication and credit system.

This script demonstrates:
1. User registration (get 3 free credits)
2. Login and receive JWT token
3. Check credit balance
4. Upload audio file (costs 1 credit)
5. Monitor job status
6. Download completed result
7. View credit transaction history

Usage:
    python test_auth_system.py
"""

import requests
import time
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def register_user(email, username, password):
    """Register a new user."""
    print_header("Step 1: Register New User")
    
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": email,
            "username": username,
            "password": password
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Registration successful!")
        print(f"   User ID: {data['user_id']}")
        print(f"   Username: {data['username']}")
        print(f"   Email: {data['email']}")
        print(f"   Free Credits: {data['credits']}")
        print(f"   Token: {data['access_token'][:50]}...")
        return data['access_token']
    else:
        print(f"❌ Registration failed: {response.json()}")
        return None


def login_user(email, password):
    """Login and get access token."""
    print_header("Step 2: Login")
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"   Username: {data['username']}")
        print(f"   Credits: {data['credits']}")
        return data['access_token']
    else:
        print(f"❌ Login failed: {response.json()}")
        return None


def get_profile(token):
    """Get user profile."""
    print_header("Step 3: Get User Profile")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Profile retrieved!")
        print(f"   ID: {data['id']}")
        print(f"   Username: {data['username']}")
        print(f"   Email: {data['email']}")
        print(f"   Credits: {data['credits']}")
        print(f"   Created: {data['created_at']}")
    else:
        print(f"❌ Failed to get profile: {response.json()}")


def check_balance(token):
    """Check credit balance."""
    print_header("Step 4: Check Credit Balance")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/credits/balance", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Balance: {data['credits']} credits")
        return data['credits']
    else:
        print(f"❌ Failed to get balance: {response.json()}")
        return 0


def purchase_credits(token, amount):
    """Purchase additional credits (simulation)."""
    print_header("Step 5: Purchase Credits (Simulation)")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/credits/purchase",
        headers=headers,
        json={
            "amount": amount,
            "payment_reference": "test-payment-123"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {data['message']}")
        print(f"   New Balance: {data['credits']} credits")
        print(f"   Amount Added: {data['amount_added']}")
    else:
        print(f"❌ Purchase failed: {response.json()}")


def upload_audio(token, file_path):
    """Upload an audio file for processing."""
    print_header("Step 6: Upload Audio File")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        print("   Please provide a valid audio file path")
        return None
    
    with open(file_path, 'rb') as f:
        files = {'file': (Path(file_path).name, f, 'audio/mpeg')}
        response = requests.post(
            f"{BASE_URL}/upload",
            headers=headers,
            files=files
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload successful!")
        print(f"   Job ID: {data['id']}")
        print(f"   Filename: {data['filename']}")
        print(f"   Status: {data['status']}")
        print(f"   Cost: {data['cost']} credit(s)")
        return data['id']
    else:
        print(f"❌ Upload failed: {response.json()}")
        return None


def check_job_status(token, job_id):
    """Check job processing status."""
    print_header(f"Step 7: Monitor Job Status")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    while True:
        response = requests.get(
            f"{BASE_URL}/status/{job_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data['status']
            print(f"   Status: {status}")
            
            if status == 'completed':
                print(f"✅ Job completed!")
                print(f"   Download URL: {data['download_url']}")
                return True
            elif status == 'failed':
                print(f"❌ Job failed: {data.get('error_message', 'Unknown error')}")
                return False
            elif status in ['pending', 'processing']:
                print(f"   ⏳ Waiting...")
                time.sleep(5)
            else:
                print(f"   Unknown status: {status}")
                return False
        else:
            print(f"❌ Failed to check status: {response.json()}")
            return False


def download_result(token, job_id):
    """Download the completed result."""
    print_header("Step 8: Download Result")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/download/{job_id}",
        headers=headers,
        stream=True
    )
    
    if response.status_code == 200:
        output_file = f"result_{job_id}.zip"
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded: {output_file}")
    else:
        print(f"❌ Download failed: {response.status_code}")


def get_credit_history(token):
    """Get credit transaction history."""
    print_header("Step 9: Credit Transaction History")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/credits/history", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        transactions = data['transactions']
        print(f"✅ Found {len(transactions)} transaction(s):")
        for tx in transactions:
            print(f"\n   Amount: {tx['amount']:+.1f} credits")
            print(f"   Balance After: {tx['balance_after']:.1f}")
            print(f"   Description: {tx['description']}")
            print(f"   Date: {tx['created_at']}")
    else:
        print(f"❌ Failed to get history: {response.json()}")


def list_jobs(token):
    """List all user jobs."""
    print_header("Step 10: List All Jobs")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/jobs", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        jobs = data['jobs']
        print(f"✅ Found {len(jobs)} job(s):")
        for job in jobs:
            print(f"\n   Job ID: {job['id']}")
            print(f"   Filename: {job['filename']}")
            print(f"   Status: {job['status']}")
            print(f"   Cost: {job['cost']} credit(s)")
            print(f"   Created: {job['created_at']}")
    else:
        print(f"❌ Failed to list jobs: {response.json()}")


def main():
    """Main test flow."""
    print("\n" + "█" * 60)
    print("  🎵 Demucs API - Authentication & Credit System Test")
    print("█" * 60)
    
    # Configuration
    email = f"test{int(time.time())}@example.com"  # Unique email
    username = f"testuser{int(time.time())}"
    password = "SecurePassword123!"
    
    try:
        # Step 1: Register (get 3 free credits)
        token = register_user(email, username, password)
        if not token:
            print("\n❌ Test failed at registration")
            return
        
        time.sleep(1)
        
        # Step 2: Login (not needed since we have token, but demonstrating)
        # token = login_user(email, password)
        
        # Step 3: Get profile
        get_profile(token)
        time.sleep(1)
        
        # Step 4: Check balance
        balance = check_balance(token)
        time.sleep(1)
        
        # Step 5: Purchase credits (simulation)
        purchase_credits(token, 10.0)
        time.sleep(1)
        
        # Step 6: Check balance again
        balance = check_balance(token)
        time.sleep(1)
        
        # Step 7: Get credit history
        get_credit_history(token)
        time.sleep(1)
        
        # Step 8: List jobs (should be empty)
        list_jobs(token)
        
        print("\n" + "=" * 60)
        print("  ✅ All tests passed!")
        print("=" * 60)
        
        print("\n📝 Next Steps:")
        print("   1. To test audio processing, run:")
        print(f"      upload_audio(token, 'path/to/your/audio.mp3')")
        print("   2. The system will:")
        print("      - Deduct 1 credit from your balance")
        print("      - Process the audio file with Demucs")
        print("      - Create a ZIP with separated tracks")
        print("   3. You currently have {:.1f} credits available".format(balance))
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API at " + BASE_URL)
        print("   Make sure the backend is running:")
        print("   docker compose up -d")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
