import requests
import zipfile
import os
import platform
import subprocess
import json

def get_chrome_version():
    """Get the installed Chrome version."""
    try:
        if platform.system() == "Windows":
            # Try different methods to get Chrome version on Windows
            import winreg
            try:
                # Method 1: Registry
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                return version
            except:
                # Method 2: Command line
                result = subprocess.run([
                    'reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', 
                    '/v', 'version'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'version' in line:
                            version = line.split()[-1]
                            return version
                
                # Method 3: PowerShell
                result = subprocess.run([
                    'powershell', '-Command', 
                    '(Get-Item "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe").VersionInfo.ProductVersion'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    return result.stdout.strip()
        
        elif platform.system() == "Darwin":  # macOS
            result = subprocess.run([
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'
            ], capture_output=True, text=True)
            return result.stdout.split()[-1]
        
        elif platform.system() == "Linux":
            result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
            return result.stdout.split()[-1]
    
    except Exception as e:
        print(f"Error getting Chrome version: {e}")
    
    return None

def download_chromedriver(version):
    """Download ChromeDriver for the specified Chrome version."""
    
    # Get the major version number
    major_version = version.split('.')[0]
    
    print(f"Chrome version: {version}")
    print(f"Major version: {major_version}")
    
    # ChromeDriver API endpoint
    api_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        # Find the best matching ChromeDriver version
        best_match = None
        for version_info in data['versions']:
            if version_info['version'].startswith(major_version + '.'):
                best_match = version_info
        
        if not best_match:
            print(f"No ChromeDriver found for Chrome version {version}")
            return False
        
        chromedriver_version = best_match['version']
        print(f"Found ChromeDriver version: {chromedriver_version}")
        
        # Get download URL for current platform
        platform_name = {
            'Windows': 'win64',
            'Darwin': 'mac-x64',
            'Linux': 'linux64'
        }.get(platform.system(), 'win64')
        
        download_url = None
        for download in best_match['downloads']['chromedriver']:
            if download['platform'] == platform_name:
                download_url = download['url']
                break
        
        if not download_url:
            print(f"No ChromeDriver download found for platform {platform_name}")
            return False
        
        print(f"Downloading ChromeDriver from: {download_url}")
        
        # Download ChromeDriver
        response = requests.get(download_url)
        zip_filename = f"chromedriver_{platform_name}.zip"
        
        with open(zip_filename, 'wb') as f:
            f.write(response.content)
        
        # Extract ChromeDriver
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall('.')
        
        # Clean up zip file
        os.remove(zip_filename)
        
        # Find the extracted chromedriver executable
        chromedriver_path = None
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.startswith('chromedriver') and (file.endswith('.exe') or '.' not in file):
                    chromedriver_path = os.path.join(root, file)
                    break
            if chromedriver_path:
                break
        
        if chromedriver_path:
            # Move to current directory
            final_path = './chromedriver.exe' if platform.system() == 'Windows' else './chromedriver'
            if chromedriver_path != final_path:
                os.rename(chromedriver_path, final_path)
            
            # Make executable on Unix systems
            if platform.system() != 'Windows':
                os.chmod(final_path, 0o755)
            
            print(f"✅ ChromeDriver installed successfully: {final_path}")
            return True
        
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
    
    return False

def main():
    print("🔧 ChromeDriver Setup")
    print("=" * 40)
    
    # Check if ChromeDriver already exists
    chromedriver_path = './chromedriver.exe' if platform.system() == 'Windows' else './chromedriver'
    
    if os.path.exists(chromedriver_path):
        print(f"✅ ChromeDriver already exists: {chromedriver_path}")
        return True
    
    # Get Chrome version
    chrome_version = get_chrome_version()
    
    if not chrome_version:
        print("❌ Could not detect Chrome version.")
        print("Please make sure Google Chrome is installed.")
        return False
    
    # Download ChromeDriver
    success = download_chromedriver(chrome_version)
    
    if success:
        print("\n✅ Setup complete! You can now run the LinkedIn search script.")
    else:
        print("\n❌ Setup failed. You may need to manually download ChromeDriver.")
        print("Visit: https://chromedriver.chromium.org/")
    
    return success

if __name__ == "__main__":
    main()