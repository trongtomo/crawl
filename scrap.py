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
URL = "https://www.lazada.vn/products/quan-short-sot-dui-ngan-the-thao-nam-2-tui-keo-khoa-vai-thun-lanh-day-dep-i771292668-s2046180947.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Aqu%2525E1%2525BA%2525A7n%252B%2525C4%252591%2525C3%2525B9i%253Bnid%253A771292668%253Bsrc%253ALazadaMainSrp%253Brn%253A6cd892c031eab240254dc9fa98b52f3e%253Bregion%253Avn%253Bsku%253A771292668_VNAMZ%253Bprice%253A43000%253Bclient%253Adesktop%253Bsupplier_id%253A200161347063%253Bbiz_source%253Ah5_internal%253Bslot%253A1%253Butlog_bucket_id%253A470687%253Basc_category_id%253A11219%253Bitem_id%253A771292668%253Bsku_id%253A2046180947%253Bshop_id%253A1370357%253BtemplateInfo%253A107883_D_E%2523-1_A3_C%2523&freeshipping=1&fs_ab=2&fuse_fs=&lang=en&location=Vietnam&price=4.3E%204&priceCompare=skuId%3A2046180947%3Bsource%3Alazada-search-voucher%3Bsn%3A6cd892c031eab240254dc9fa98b52f3e%3BoriginPrice%3A43000%3BdisplayPrice%3A43000%3BsinglePromotionId%3A-1%3BsingleToolCode%3AmockedSalePrice%3BvoucherPricePlugin%3A0%3Btimestamp%3A1733238069488&ratingscore=4.837865497076024&request_id=6cd892c031eab240254dc9fa98b52f3e&review=6840&sale=48465&search=1&source=search&spm=a2o4n.searchlist.list.1&stock=1"

# Configure Brave options
options = Options()
options.binary_location = BRAVE_PATH

# Initialize the browser and service
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Open the Lazada product page
driver.get(URL)

# Wait for the page to load
time.sleep(10)

comments = []
page_num = 1

while True:
    try:
        # Wait for comments section to load (adjust time as needed)
        time.sleep(3)

        # Find and extract comments excluding seller replies
        comment_elements = driver.find_elements(By.CSS_SELECTOR, ".item .item-content .content:not(.seller-reply-wrapper .content)")
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
