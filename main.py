import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv
import urllib.parse
import os
from selenium.webdriver.common.action_chains import ActionChains


def check_file_exists(file_path):
    """Check if the file exists and is a supported media type."""
    if not os.path.exists(file_path):
        return False

    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm']
    return os.path.splitext(file_path.lower())[1] in supported_extensions


def send_media(driver, file_path):
    """Send media attachment."""
    try:
        # Click on the attachment clip icon
        clip_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]'))
        )
        clip_button.click()

        # Find and click the image/video input
        media_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
        )

        # Send the file path to the input
        media_input.send_keys(os.path.abspath(file_path))

        # Wait for media to upload and automatically press Enter to send
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="send"]'))
        )
        time.sleep(2)  # Wait for media to process

        # Send Enter key to send the media
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

        return True
    except Exception as e:
        print(f"Error sending media: {str(e)}")
        return False


# CSV file path
csv_file = 'ACSES.csv'

# Initialize undetected ChromeDriver
driver = uc.Chrome(use_subprocess=True)

# WhatsApp Web URL
whatsapp_url = 'https://web.whatsapp.com/'

# Open WhatsApp Web
driver.get(whatsapp_url)
input("Scan the QR code and press Enter after you're logged in.")

# Read the CSV file
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)

    # Loop through each row in the CSV file
    for row in csv_reader:
        number = "+233" + str(row['Number'])  # Adding +233 country code
        name = row['Name']
        media_path = row.get('MediaPath', '')  # Column for media file path

        # Multi-line message with proper line breaks
        message = (
            f"Hello {name} 👋How're you doing?\n\n"
            "My name is King George, Final Year student\n\n"
            "I'm here to introduce DeepStem Hub to you. It's a robotics club on campus that teach students more of A.I, Software development, robotics etc.\n\n"
            "If you want join, please subscribe to our channel for all the needed information\n\n"
            "https://whatsapp.com/channel/0029Vb3ltyDHFxP1f0Kurb1n"
        )

        try:
            # Create URL for the specific chat
            chat_url = f"https://web.whatsapp.com/send?phone={number}&text={urllib.parse.quote(message)}"
            driver.get(chat_url)

            # Wait for chat to load and message box to be present
            message_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@title="Type a message"]'))
            )
            time.sleep(5)  # Additional wait for chat to fully load

            # Send text message using Enter key
            actions = ActionChains(driver)
            actions.send_keys(Keys.ENTER)
            actions.perform()

            print(f"Message sent successfully to {name} ({number})")

            # If media path is provided and file exists, send the media
            if media_path and check_file_exists(media_path):
                time.sleep(2)  # Wait between text and media
                if send_media(driver, media_path):
                    print(f"Media sent successfully to {name} ({number})")
                else:
                    print(f"Failed to send media to {name} ({number})")

        except Exception as e:
            print(f"Error sending message to {name} ({number}): {str(e)}")

        # Add delay between messages
        time.sleep(3)

# Keep the browser window open
input("Press Enter to close the browser...")