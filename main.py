import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv
import urllib.parse


def send_whatsapp_message():
    # Initialize ChromeDriver
    driver = uc.Chrome(use_subprocess=True)

    # WhatsApp Web URL
    whatsapp_url = 'https://web.whatsapp.com/'
    driver.get(whatsapp_url)

    # Wait for manual QR code scan
    input("Scan the QR code and press Enter after you're logged in.")

    # Read contacts from CSV
    with open('bulkymem.csv', 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            number = "+233" + str(row['Number'])
            name = row['Name']

            message = (
                f"Hello {name}, good day. It's been a while. This is King George.\n\n"
                "Actually, I am reaching out to you because of a robotics club opened up\n\n"
                "for all students from any department to Join. Kindly join the channel\n\n"
                "https://whatsapp.com/channel/0029Vb3ltyDHFxP1f0Kurb1n\n\n"
                "and save my contact to get any update I share"
            )

            try:
                # Directly send message using the send API
                chat_url = f"https://web.whatsapp.com/send?phone={number}&text={urllib.parse.quote(message)}"
                driver.get(chat_url)

                # Wait for message input box
                message_box = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )

                # Focus on the message box
                message_box.click()

                # Wait a moment then send ENTER key
                time.sleep(2)
                message_box.send_keys(Keys.ENTER)

                print(f"Message sent to {name} ({number})")

                # Wait before next message
                time.sleep(5)

            except Exception as e:
                print(f"Failed to send to {name} ({number}): {str(e)}")
                continue

    input("All messages sent. Press Enter to close browser...")
    driver.quit()


if __name__ == "__main__":
    send_whatsapp_message()