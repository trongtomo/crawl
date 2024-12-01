from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Path to your Brave browser and ChromeDriver
BRAVE_PATH = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
CHROMEDRIVER_PATH = "E:/Chrome driver/chromedriver.exe"

# Lazada product page URL
URL = "https://www.lazada.vn/products/ao-so-mi-ngan-tay-form-rong-chat-lieu-vai-lua-cao-cap-khong-nhan-mau-trang-den-phong-cach-han-quoc-i1399507322-s11793653004.html"

# Configure Brave options
options = Options()
options.binary_location = BRAVE_PATH

# Initialize the browser and service
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Open the Lazada product page
driver.get(URL)

# Wait for the page to load
time.sleep(5)

comments = []
page_num = 1

while True:
    try:
        # Wait for comments section to load (adjust time as needed)
        time.sleep(3)

        # Find and extract comments
        comment_elements = driver.find_elements(By.CSS_SELECTOR, ".item .item-content .content")
        for element in comment_elements:
            comments.append([element.text, ''])  # No need to categorize comments, leaving blank

        # Save to Excel every time a page is scraped
        df = pd.DataFrame(comments, columns=["Comment", "Comment Type"])
        df.to_excel("lazada_comments.xlsx", index=False)

        # Try clicking the 'Next' button
        next_button = driver.find_element(By.CSS_SELECTOR, "button.next-pagination-item.next")
        if next_button.is_enabled():
            next_button.click()
            page_num += 1
            print(f"Reached page {page_num}, moving to next page...")
        else:
            print("No more pages available.")
            break
    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Close the browser after scraping
driver.quit()

print("Scraping completed! Comments saved to 'lazada_comments.xlsx'.")
