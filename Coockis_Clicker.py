from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# المسار إلى chromedriver الموجود على جهازك
CHROMEDRIVER_PATH = './chromedriver-win64/chromedriver.exe'

# Initialize ChromeOptions (optional, you can add additional options here)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open the browser in maximized mode

# Initialize WebDriver using the local chromedriver
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)

# Open the Cookie Clicker game page
driver.get('https://cookieclickerfree.github.io/')

time.sleep(2)

# Function to get the current number of cookies
def get_cookie_count():
    try:
        # Wait until the cookie count element appears
        cookie_count_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'cookies'))
        )
        # Extract the text from the element
        cookie_text = cookie_count_element.text
        # Split the text and extract only the part containing the number of cookies
        cookie_count_str = cookie_text.split()[0]  # Take the first part of the text (cookie count)
        cookie_count = int(''.join(filter(str.isdigit, cookie_count_str)))  # Extract only digits
        return cookie_count
    except Exception as e:
        print("Error while extracting cookie count:", e)
        return 0

# Wait until the language selection element (English) appears
try:
    # Wait up to 10 seconds for the element to appear
    lan = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'langSelect-EN'))
    )
    time.sleep(1)
    lan.click()  # Click to select English
    time.sleep(2)
except Exception as e:
    print("Error while waiting for the language element:", e)

# Wait until the cookie element appears
try:
    # Wait up to 10 seconds for the element to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'bigCookie'))
    )
except Exception as e:
    print("Error while waiting for the cookie element:", e)

# Click cookies repeatedly as fast as possible
try:
    while True:
        # Re-fetch the element reference in each iteration
        cookie = driver.find_element(By.ID, 'bigCookie')
        
        # Perform clicks using JavaScript
        driver.execute_script("arguments[0].click();", cookie)
        
        # Check cookie count and purchase upgrades periodically
        current_cookies = get_cookie_count()
        print(f"Cookies Count: {current_cookies}")

        # Purchase upgrades if possible
        for i in range(4):
            try:
                # Re-fetch the element reference in each iteration
                product_price_element = driver.find_element(By.ID, f'productPrice{i}')
                product_price = product_price_element.text.replace(",", "")
                
                if not product_price.isdigit():
                    continue

                product_price = int(product_price)

                if current_cookies >= product_price:
                    # Re-fetch the element reference in each iteration
                    product = driver.find_element(By.ID, f'product{i}')
                    
                    # Scroll the element into view and click using JavaScript
                    driver.execute_script("arguments[0].scrollIntoView(true);", product)
                    driver.execute_script("arguments[0].click();", product)
                    break
            except Exception as e:
                print(f"Error while trying to purchase upgrade {i}:", e)
                continue

except KeyboardInterrupt:
    print("Clicking stopped.")

# Close the browser after finishing
driver.quit()