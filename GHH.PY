import os
import zipfile
import requests
import platform
import shutil

# Set Chrome version (update this if needed)
chrome_version = "132.0.6834.160"

# Get OS type
os_type = platform.system().lower()
if os_type == "windows":
    driver_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"
    driver_filename = "chromedriver.exe"
    extract_folder = "chromedriver-win64"
elif os_type == "linux":
    driver_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/linux64/chromedriver-linux64.zip"
    driver_filename = "chromedriver"
    extract_folder = "chromedriver-linux64"
elif os_type == "darwin":  # macOS
    driver_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/mac-x64/chromedriver-mac-x64.zip"
    driver_filename = "chromedriver"
    extract_folder = "chromedriver-mac-x64"
else:
    print("❌ Unsupported OS!")
    exit(1)

# Download the ChromeDriver zip file
print(f"🔽 Downloading ChromeDriver {chrome_version} for {os_type}...")
response = requests.get(driver_url, stream=True)
zip_path = "chromedriver.zip"

with open(zip_path, "wb") as file:
    for chunk in response.iter_content(chunk_size=1024):
        file.write(chunk)

print("✅ Download complete!")

# Extract ChromeDriver
print("📦 Extracting ChromeDriver...")
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall()

# Move the driver to current directory
if os.path.exists(extract_folder):
    shutil.move(os.path.join(extract_folder, driver_filename), driver_filename)
    shutil.rmtree(extract_folder)  # Remove extracted folder

# Delete the zip file
os.remove(zip_path)

# Make it executable (Linux/macOS)
if os_type != "windows":
    os.chmod(driver_filename, 0o755)

print(f"🚀 ChromeDriver {chrome_version} is ready! Run it using: ./{driver_filename}")
