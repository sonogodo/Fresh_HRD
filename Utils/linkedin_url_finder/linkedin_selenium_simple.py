import pandas as pd
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import os

def setup_driver():
    """Setup Chrome driver with minimal options."""
    chrome_options = Options()
    
    # Basic options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Set user agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Suppress logs
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Use the ChromeDriver we downloaded
        chromedriver_path = "./chromedriver.exe"
        if not os.path.exists(chromedriver_path):
            print("❌ ChromeDriver not found. Please run setup_chromedriver.py first.")
            return None
        
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome driver initialized successfully")
        return driver
        
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {e}")
        return None

def test_basic_navigation(driver):
    """Test basic browser navigation."""
    try:
        print("🧪 Testing basic navigation...")
        driver.get("https://www.google.com")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print(f"✅ Successfully navigated to: {driver.current_url}")
        print(f"   Page title: {driver.title}")
        return True
        
    except Exception as e:
        print(f"❌ Navigation test failed: {e}")
        return False

def search_duckduckgo_simple(driver, query):
    """Simple DuckDuckGo search."""
    try:
        print(f"🔍 Searching DuckDuckGo for: {query}")
        
        # Navigate to DuckDuckGo
        driver.get("https://duckduckgo.com")
        
        # Wait for search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Enter search query
        search_box.clear()
        search_box.send_keys(query)
        search_box.submit()
        
        # Wait for results
        time.sleep(3)
        
        # Get page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Look for LinkedIn URLs
        linkedin_urls = []
        
        # Search in all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'linkedin.com/in/' in href:
                # Clean DuckDuckGo redirect URLs
                if '/l/?uddg=' in href:
                    try:
                        import urllib.parse
                        actual_url = urllib.parse.unquote(href.split('uddg=')[1])
                        if actual_url.startswith('http'):
                            linkedin_urls.append(actual_url)
                    except:
                        pass
                elif href.startswith('http'):
                    linkedin_urls.append(href)
        
        # Clean URLs
        clean_urls = []
        for url in linkedin_urls:
            clean_url = url.split('?')[0].split('#')[0]
            if clean_url not in clean_urls and 'linkedin.com/in/' in clean_url:
                clean_urls.append(clean_url)
        
        print(f"   Found {len(clean_urls)} LinkedIn URLs")
        return clean_urls[:3]
        
    except Exception as e:
        print(f"   ❌ Search failed: {e}")
        return []

def main():
    print("🚀 LinkedIn Selenium Search - Simple Version")
    print("=" * 50)
    
    # Setup driver
    driver = setup_driver()
    if not driver:
        return
    
    try:
        # Test basic navigation first
        if not test_basic_navigation(driver):
            print("❌ Basic navigation failed. Exiting.")
            return
        
        # Test with a simple search
        print("\n🧪 Testing LinkedIn search...")
        test_query = "linkedin Caio Rodrigues de Oliveira UNESP"
        results = search_duckduckgo_simple(driver, test_query)
        
        if results:
            print("✅ Search test successful!")
            for i, url in enumerate(results, 1):
                print(f"   {i}. {url}")
        else:
            print("❌ No results found in test search")
        
        # Ask if user wants to continue with CSV processing
        if results:
            continue_choice = input("\n🤔 Search is working! Process CSV data? (y/n): ").lower()
            
            if continue_choice == 'y':
                # Load CSV and process a few records
                try:
                    df = pd.read_csv('new_graduates.csv', encoding='utf-8')
                    sample_df = df.head(5)  # Process first 5
                    
                    print(f"\n📊 Processing {len(sample_df)} records...")
                    
                    results_list = []
                    
                    for idx, row in sample_df.iterrows():
                        name = row.get('Nome', '')
                        university = row.get('Faculdade', '')
                        
                        print(f"\n[{idx+1}/5] {name}")
                        
                        if name:
                            query = f"linkedin {name} {university}"
                            urls = search_duckduckgo_simple(driver, query)
                            
                            result = {
                                'Nome': name,
                                'Curso': row.get('Curso', ''),
                                'Faculdade': university,
                                'LinkedIn URL': urls[0] if urls else '',
                                'Match Status': 'Found' if urls else 'Not Found',
                                'Last Updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            results_list.append(result)
                            
                            if urls:
                                print(f"   ✅ Found: {urls[0]}")
                            else:
                                print(f"   ❌ Not found")
                            
                            # Delay between searches
                            time.sleep(3)
                    
                    # Save results
                    with open('linkedin_selenium_test.json', 'w', encoding='utf-8') as f:
                        json.dump(results_list, f, ensure_ascii=False, indent=2)
                    
                    found_count = sum(1 for r in results_list if r['Match Status'] == 'Found')
                    print(f"\n📊 Results: {found_count}/5 profiles found")
                    print("💾 Saved to linkedin_selenium_test.json")
                    
                except Exception as e:
                    print(f"Error processing CSV: {e}")
        
    except Exception as e:
        print(f"Error during execution: {e}")
    
    finally:
        print("\n🔧 Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()