import requests
import time
import json
import subprocess
from datetime import datetime

# URL dari file JSON
url = "https://contoh.com/data.json"  # Ganti dengan URL JSON yang Anda gunakan

# Fungsi untuk mengambil JSON dan menyimpannya ke dalam file txt
def fetch_and_save_json():
    try:
        # Mengambil data dari URL
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Menyimpan data ke dalam file txt dengan timestamp
        filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Data saved to {filename}")
        return filename
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON data: {e}")
        return None

# Fungsi untuk commit dan push ke Git
def commit_and_push_to_git(filename):
    try:
        # Menambahkan file baru ke staging
        subprocess.run(["git", "add", filename], check=True)
        # Commit perubahan
        subprocess.run(["git", "commit", "-m", f"Add JSON data file {filename}"], check=True)
        # Push ke repository
        subprocess.run(["git", "push"], check=True)
        print(f"{filename} committed and pushed to Git.")
    except subprocess.CalledProcessError as e:
        print(f"Error with Git command: {e}")

# Loop untuk menjalankan setiap 2 jam sekali
while True:
    filename = fetch_and_save_json()
    if filename:
        commit_and_push_to_git(filename)
    # Tunggu 2 jam sebelum mengambil data lagi
    time.sleep(2 * 60 * 60)
