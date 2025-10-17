#!/usr/bin/env python3
"""
DOWNLOADER-UX v1.0.0
Universal Downloading Tool
Creator: @GenzPX
"""

import os
import sys
import time
import re
import requests
import json
import zipfile
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
try:
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
except ModuleNotFoundError as e:
missing = str(e).split("'")[1]
print(f"\033[91m[ ! ] Missing dependency: {missing}\033[0m")
print("\033[93m[ * ] Installing dependencies automatically...\033[0m")
os.system(f"pip install {missing}")
os.execv(sys.executable, ['python3'] + sys.argv)

ANSI color codes

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

ASCII Art Banner

BANNER = f"""{CYAN}
[.....        [....     [..        [..[...     [..[..          [....
[..   [..   [..    [..  [..        [..[. [..   [..[..        [..    [..
[..    [..[..        [..[..   [.   [..[.. [..  [..[..      [..        [..
[..    [..[..        [..[..  [..   [..[..  [.. [..[..      [..        [..
[..    [..[..        [..[.. [. [.. [..[..   [. [..[..      [..        [..
[..   [..   [..     [.. [. [.    [....[..    [. ..[..        [..     [..
[.....        [....     [..        [..[..      [..[........    [....

[.       [.....    [........[.......          [..     [..[..      [..  
 [. ..     [..   [.. [..      [..    [..        [..     [.. [..   [..    
[.  [..    [..    [..[..      [..    [..        [..     [..  [.. [..

[..   [..   [..    [..[......  [. [..      [.....[..     [..    [..
[...... [..  [..    [..[..      [..  [..          [..     [..  [.. [..
[..       [.. [..   [.. [..      [..    [..        [..     [.. [..   [..
[..         [..[.....    [........[..      [..        [.....   [..      [..
{RESET}"""

def clear_screen():
"""Clear terminal screen"""
os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text, width=50):
"""Center align text"""
return text.center(width)

def print_banner():
"""Print the application banner"""
print(BANNER)
print(f"{YELLOW}{'='*45}{RESET}")
print(f"{GREEN}{center_text('DOWNLOADER-UX v1.0.0', 45)}{RESET}")
print(f"{GREEN}{center_text('Universal Downloading Tool', 45)}{RESET}")
print(f"{GREEN}{center_text('Creator - @GenzPX', 45)}{RESET}")
print(f"{YELLOW}{'='*45}{RESET}")

def loading_animation(text, duration=2):
"""Show loading animation"""
chars = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
end_time = time.time() + duration
i = 0
while time.time() < end_time:
print(f"\r{CYAN}{chars[i % len(chars)]} {text}{RESET}", end='', flush=True)
time.sleep(0.1)
i += 1
print("\r" + " " * (len(text) + 4), end='\r')

def validate_url(url):
"""Validate if the given string is a valid URL"""
url_pattern = re.compile(
r'^https?://'  # http:// or https://
r'(?:(?:A-Z0-9?.)+[A-Z]{2,6}.?|'  # domain...
r'localhost|'  # localhost...
r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})'  # ...or ip
r'(?::\d+)?'  # optional port
r'(?:/?|[/?]\S+)$', re.IGNORECASE)
return url_pattern.match(url) is not None

def safe_request(url, retries=3, timeout=10):
"""
Safely make HTTP request with retry mechanism
Returns: (response, error_message)
"""
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for attempt in range(retries):  
    try:  
        response = requests.get(url, headers=headers, timeout=timeout, verify=False)  
        response.raise_for_status()  
        return response, None  
    except requests.exceptions.Timeout:  
        error = f"Timeout error on attempt {attempt + 1}"  
        if attempt < retries - 1:  
            print(f"{YELLOW}[ ! ] {error}. Retrying...{RESET}")  
            time.sleep(2)  
    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):  
        error = f"Connection error on attempt {attempt + 1}"  
        if attempt < retries - 1:  
            print(f"{YELLOW}[ ! ] {error}. Retrying...{RESET}")  
            time.sleep(2)  
    except requests.exceptions.RequestException as e:  
        error = f"Request error: {str(e)}"  
        if attempt < retries - 1:  
            print(f"{YELLOW}[ ! ] {error}. Retrying...{RESET}")  
            time.sleep(2)  
  
return None, error

def log_error(message):
"""Log error messages to error_log.txt"""
os.makedirs('download', exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open('download/error_log.txt', 'a', encoding='utf-8') as f:
f.write(f"[{timestamp}] {message}\n")

def analyst_url(url):
"""
Analyze URL content and return counts of different media types
Returns: dict with counts or None if error
"""
print(f"\n{CYAN}[ + ] Analyzing URL: {url}{RESET}")
loading_animation("Scanning page", 1)

response, error = safe_request(url)  
if error:  
    log_error(f"Failed to analyze {url}: {error}")  
    return None  
  
try:  
    soup = BeautifulSoup(response.content, 'html.parser')  
      
    # Count different types of content  
    images = soup.find_all(['img'])  
    scripts = soup.find_all('script', src=True)  
      
    # Find files (common file extensions)  
    file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar', '.mp3', '.mp4', '.avi', '.mov']  
    all_links = soup.find_all('a', href=True)  
    files = [link for link in all_links if any(ext in link.get('href', '').lower() for ext in file_extensions)]  
      
    # Extract all links  
    links = [link for link in all_links if not any(ext in link.get('href', '').lower() for ext in file_extensions)]  
      
    return {  
        'images': len(images),  
        'scripts': len(scripts),  
        'files': len(files),  
        'links': len(links),  
        'image_urls': [urljoin(url, img.get('src', '')) for img in images if img.get('src')],  
        'script_urls': [urljoin(url, script.get('src', '')) for script in scripts],  
        'file_urls': [urljoin(url, file.get('href', '')) for file in files],  
        'link_urls': [urljoin(url, link.get('href', '')) for link in links]  
    }  
      
except Exception as e:  
    log_error(f"Parsing error for {url}: {str(e)}")  
    print(f"{YELLOW}[ ! ] Parsing error — switching to fallback mode.{RESET}")  
    # Fallback: basic regex scanning  
    try:  
        content = response.text  
        images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)  
        scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)  
        return {  
            'images': len(images),  
            'scripts': len(scripts),  
            'files': 0,  
            'links': 0,  
            'image_urls': [urljoin(url, img) for img in images],  
            'script_urls': [urljoin(url, script) for script in scripts],  
            'file_urls': [],  
            'link_urls': []  
        }  
    except:  
        return None

def download_file(url, filepath, desc="Downloading"):
"""Download a single file with progress bar"""
try:
response = requests.get(url, stream=True, timeout=30, verify=False, headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
response.raise_for_status()

total_size = int(response.headers.get('content-length', 0))  
      
    with open(filepath, 'wb') as f:  
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=desc,   
                 bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as pbar:  
            for chunk in response.iter_content(chunk_size=8192):  
                if chunk:  
                    f.write(chunk)  
                    pbar.update(len(chunk))  
      
    return True  
except Exception as e:  
    log_error(f"Failed to download {url}: {str(e)}")  
    print(f"{RED}[ ! ] Failed to download: {os.path.basename(filepath)}{RESET}")  
    return False

def download_images(url, analysis_data):
"""Download all images from the URL"""
image_urls = analysis_data.get('image_urls', [])
if not image_urls:
print(f"{YELLOW}[ ! ] No images found to download{RESET}")
return

print(f"\n{GREEN}[ + ] Found {len(image_urls)} images{RESET}")  
download_dir = os.path.join('download', 'images', urlparse(url).netloc)  
os.makedirs(download_dir, exist_ok=True)  
  
success_count = 0  
for i, img_url in enumerate(image_urls):  
    filename = f"image_{i+1}_{os.path.basename(urlparse(img_url).path)}"  
    if not filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')):  
        filename += '.jpg'  
      
    filepath = os.path.join(download_dir, filename)  
    if download_file(img_url, filepath, f"Image {i+1}/{len(image_urls)}"):  
        success_count += 1  
  
print(f"\n{GREEN}[ ✓ ] Downloaded {success_count}/{len(image_urls)} images{RESET}")  
return download_dir

def download_scripts(url, analysis_data):
"""Download all scripts from the URL"""
script_urls = analysis_data.get('script_urls', [])
if not script_urls:
print(f"{YELLOW}[ ! ] No scripts found to download{RESET}")
return

print(f"\n{GREEN}[ + ] Found {len(script_urls)} scripts{RESET}")  
download_dir = os.path.join('download', 'scripts', urlparse(url).netloc)  
os.makedirs(download_dir, exist_ok=True)  
  
success_count = 0  
for i, script_url in enumerate(script_urls):  
    filename = f"script_{i+1}_{os.path.basename(urlparse(script_url).path)}"  
    if not filename.endswith('.js'):  
        filename += '.js'  
      
    filepath = os.path.join(download_dir, filename)  
    if download_file(script_url, filepath, f"Script {i+1}/{len(script_urls)}"):  
        success_count += 1  
  
print(f"\n{GREEN}[ ✓ ] Downloaded {success_count}/{len(script_urls)} scripts{RESET}")  
return download_dir

def download_files(url, analysis_data):
"""Download all files from the URL"""
file_urls = analysis_data.get('file_urls', [])
if not file_urls:
print(f"{YELLOW}[ ! ] No files found to download{RESET}")
return

print(f"\n{GREEN}[ + ] Found {len(file_urls)} files{RESET}")  
download_dir = os.path.join('download', 'files', urlparse(url).netloc)  
os.makedirs(download_dir, exist_ok=True)  
  
success_count = 0  
for i, file_url in enumerate(file_urls):  
    filename = os.path.basename(urlparse(file_url).path)  
    if not filename:  
        filename = f"file_{i+1}"  
      
    filepath = os.path.join(download_dir, filename)  
    if download_file(file_url, filepath, f"File {i+1}/{len(file_urls)}"):  
        success_count += 1  
  
print(f"\n{GREEN}[ ✓ ] Downloaded {success_count}/{len(file_urls)} files{RESET}")  
return download_dir

def extract_links(url, analysis_data):
"""Extract and save all links from the URL"""
link_urls = analysis_data.get('link_urls', [])
if not link_urls:
print(f"{YELLOW}[ ! ] No links found to extract{RESET}")
return

print(f"\n{GREEN}[ + ] Found {len(link_urls)} links{RESET}")  
download_dir = os.path.join('download', 'links')  
os.makedirs(download_dir, exist_ok=True)  
  
filename = f"links_{urlparse(url).netloc}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"  
filepath = os.path.join(download_dir, filename)  
  
with open(filepath, 'w', encoding='utf-8') as f:  
    for link in link_urls:  
        f.write(f"{link}\n")  
  
print(f"{GREEN}[ ✓ ] Links saved to: {filepath}{RESET}")  
return download_dir

def create_zip_archive(directory, zip_name):
"""Create a zip archive of the download directory"""
try:
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
for root, dirs, files in os.walk(directory):
for file in files:
file_path = os.path.join(root, file)
arcname = os.path.relpath(file_path, os.path.dirname(directory))
zipf.write(file_path, arcname)
return True
except Exception as e:
log_error(f"Failed to create zip: {str(e)}")
return False

def upload_to_catbox(filepath):
"""Upload file to catbox.moe (fallback for link generation)"""
try:
print(f"\n{CYAN}[ + ] Uploading to catbox.moe...{RESET}")
with open(filepath, 'rb') as f:
response = requests.post('https://catbox.moe/user/api.php',
data={'reqtype': 'fileupload'},
files={'fileToUpload': f})
if response.status_code == 200:
return response.text.strip()
return None
except Exception as e:
log_error(f"Catbox upload failed: {str(e)}")
return None

def download_menu():
"""Handle download menu operations"""
print(f"\n{CYAN}{'='*45}{RESET}")
url = input(f"{GREEN}Masukkan URL: {RESET}").strip()

if not validate_url(url):  
    print(f"{RED}[ ! ] Invalid URL format{RESET}")  
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")  
    return  
  
# Analyze URL  
start_time = time.time()  
analysis_data = analyst_url(url)  
  
if not analysis_data:  
    print(f"{RED}[ ! ] Failed to analyze URL{RESET}")  
    retry = input(f"{YELLOW}[ ! ] Connection failed. Retry? (y/n): {RESET}").lower()  
    if retry == 'y':  
        download_menu()  
    return  
  
elapsed_time = time.time() - start_time  
  
# Display analysis results  
print(f"\n{GREEN}[ + ] URL: {url}{RESET}")  
print(f"{CYAN}[ 1 ] Image : {analysis_data['images']}{RESET}")  
print(f"{CYAN}[ 2 ] Script : {analysis_data['scripts']}{RESET}")  
print(f"{CYAN}[ 3 ] File : {analysis_data['files']}{RESET}")  
print(f"{CYAN}[ 4 ] Link  : {analysis_data['links']}{RESET}")  
print(f"{GREEN}[+] Complete scanning: {elapsed_time:.1f} s{RESET}")  
  
# Ask what to download  
print(f"\n{YELLOW}[ = ] What do you want to download?{RESET}")  
choice = input(f"{GREEN}Enter choice (1-4): {RESET}").strip()  
  
download_dir = None  
  
if choice == '1':  
    print(f"\n{CYAN}Downloading Images... please wait{RESET}")  
    download_dir = download_images(url, analysis_data)  
elif choice == '2':  
    print(f"\n{CYAN}Downloading Scripts... please wait{RESET}")  
    download_dir = download_scripts(url, analysis_data)  
elif choice == '3':  
    print(f"\n{CYAN}Downloading Files... please wait{RESET}")  
    download_dir = download_files(url, analysis_data)  
elif choice == '4':  
    print(f"\n{CYAN}Extracting Links... please wait{RESET}")  
    download_dir = extract_links(url, analysis_data)  
else:  
    print(f"{RED}[ ! ] Invalid choice{RESET}")  
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")  
    return  
  
# Create zip if multiple files  
if download_dir and os.path.exists(download_dir):  
    files_count = sum(len(files) for _, _, files in os.walk(download_dir))  
    if files_count > 5:  
        zip_name = f"{download_dir}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"  
        print(f"\n{CYAN}[ + ] Creating zip archive...{RESET}")  
        if create_zip_archive(download_dir, zip_name):  
            print(f"{GREEN}[ ✓ ] Archive created: {zip_name}{RESET}")  
              
            # Try to upload to catbox  
            catbox_url = upload_to_catbox(zip_name)  
            if catbox_url:  
                print(f"{GREEN}[ ✓ ] Download link: {catbox_url}{RESET}")  
  
input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def analyst_menu():
"""Handle analyst menu operations"""
print(f"\n{CYAN}{'='*45}{RESET}")
url = input(f"{GREEN}Masukkan URL: {RESET}").strip()

if not validate_url(url):  
    print(f"{RED}[ ! ] Invalid URL format{RESET}")  
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")  
    return  
  
start_time = time.time()  
analysis_data = analyst_url(url)  
  
if not analysis_data:  
    print(f"{RED}[ ! ] Failed to analyze URL{RESET}")  
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")  
    return  
  
elapsed_time = time.time() - start_time  
  
# Display results  
print(f"\n{GREEN}[ + ] Found {analysis_data['images']} Images{RESET}")  
print(f"{GREEN}[ + ] Found {analysis_data['scripts']} Script{RESET}")  
print(f"{GREEN}[ + ] Found {analysis_data['files']} Files{RESET}")  
print(f"{GREEN}[ + ] Found {analysis_data['links']} Links{RESET}")  
print(f"{CYAN}[ * ] Done in {elapsed_time:.1f}s{RESET}")  
  
input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def credits_menu():
"""Display credits"""
clear_screen()
print(f"\n{CYAN}{'='*45}{RESET}")
print(f"{GREEN}{center_text('CREDITS', 45)}{RESET}")
print(f"{CYAN}{'='*45}{RESET}")
print(f"\n{GREEN}[+] Creator: @GenzPX{RESET}")
print(f"{GREEN}[+] Thanks To [+]{RESET}")
print(f"{YELLOW}All user{RESET}")
print(f"\n{CYAN}{'='*45}{RESET}")
input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def main_menu():
"""Display main menu and handle user choice"""
while True:
clear_screen()
print_banner()

print(f"{CYAN}[ 1 ] Download{RESET}")  
    print(f"{CYAN}[ 2 ] Analyst{RESET}")  
    print(f"{CYAN}[ 3 ] Credits{RESET}")  
    print(f"{CYAN}[ 4 ] Exit{RESET}")  
    print(f"{YELLOW}{'='*45}{RESET}")  
      
    choice = input(f"\n{GREEN}Select option >> {RESET}").strip()  
      
    if choice == '1':  
        download_menu()  
    elif choice == '2':  
        analyst_menu()  
    elif choice == '3':  
        credits_menu()  
    elif choice == '4':  
        print(f"\n{CYAN}Exiting DOWNLOADER-UX...{RESET}")  
        print(f"{GREEN}Goodbye 👋{RESET}\n")  
        sys.exit(0)  
    else:  
        print(f"{RED}[ ! ] Invalid option. Please try again.{RESET}")  
        time.sleep(1)

def main():
"""Main function to run the application"""
try:
# Create necessary directories
os.makedirs('download', exist_ok=True)

# Run main menu  
    main_menu()  
      
except KeyboardInterrupt:  
    print(f"\n\n{RED}[!] Program interrupted by user{RESET}")  
    print(f"{GREEN}Goodbye 👋{RESET}\n")  
    sys.exit(0)  
except Exception as e:  
    print(f"\n{RED}[!] Unexpected error: {str(e)}{RESET}")  
    log_error(f"Critical error: {str(e)}")  
    sys.exit(1)

if name == "main":
main()


