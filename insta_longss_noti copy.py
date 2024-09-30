from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fpdf import FPDF
from PIL import Image  
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_argument("--headless")  
service = Service("C:\\Users\\chait\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

def login_instagram(username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    
    user_input = driver.find_element(By.NAME, "username")
    user_input.send_keys(username)
    
    pass_input = driver.find_element(By.NAME, "password")
    pass_input.send_keys(password)
    
    pass_input.send_keys(Keys.RETURN)
    time.sleep(5)

def capture_full_page_screenshot(url, save_path):
    driver.get(url)
    time.sleep(3)

    if (url == 'https://www.instagram.com/direct/inbox/'):
        handle_notification_popup(driver)

    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    screenshots = []

    for scroll_position in range(0, total_height, viewport_height):
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(2)  

        screenshot_path = f"./screenshots/part_{scroll_position}.png"
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)

    stitch_screenshots(screenshots, save_path)

def stitch_screenshots(screenshots, save_path):
    images = [Image.open(screenshot) for screenshot in screenshots]

    total_height = sum(image.height for image in images)
    width = images[0].width  

    stitched_image = Image.new('RGB', (width, total_height))

    y_offset = 0
    for image in images:
        stitched_image.paste(image, (0, y_offset))
        y_offset += image.height

    stitched_image.save(save_path)

    for screenshot in screenshots:
        os.remove(screenshot)

    print(f"Full page screenshot saved as {save_path}")


from fpdf import FPDF
from fpdf.fonts import FontFace  

def create_pdf_report(images_with_titles, output_pdf, chat_usernames):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    
    font_face = FontFace(family="DejaVu")
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=14)
    
    for title, image in images_with_titles:
        pdf.add_page()
        pdf.cell(0, 10, title, ln=True, align="C")  
        pdf.image(image, x=10, y=20, w=190)  

    pdf.add_page()
    pdf.set_font("DejaVu", size=12)  
    pdf.cell(0, 10, "Chat Usernames:", ln=True)

    for username in chat_usernames:
        pdf.cell(0, 10, username, ln=True)

    pdf.output(output_pdf)
    print(f"PDF report generated: {output_pdf}")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handle_notification_popup(driver):
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
        )
        not_now_button.click()
        print("Clicked 'Not Now' on the notification popup.")
    except Exception as e:
        print(f"Notification popup not handled. Exception: {e}")


def get_chat_list():
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(5)

    handle_notification_popup(driver)

    chat_usernames = []

    for i in range(1, 6):  
        try:
            xpath = f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[{i}]/div/div/div/div/div[2]/div/div[1]/span/span"

            chat_name_element = driver.find_element(By.XPATH, xpath)

            chat_title = chat_name_element.text.strip().split('\n')[0]  

            if chat_title:  
                chat_usernames.append(chat_title)

        except Exception as e:
            print(f"Error extracting chat username from chat {i}: {e}")
    
    return chat_usernames


def capture_chat_screenshot(chat_url, save_path):
    driver.get(chat_url)
    time.sleep(10)
    handle_notification_popup(driver)
    driver.find_element(By.NAME, "Turn On").send_keys(Keys.TAB)
    driver.find_element(By.NAME, "Not Now").send_keys(Keys.RETURN)


    driver.save_screenshot(save_path)

def main():
    username = "ranadivesahil"
    password = "2504@Sahil"
    
    login_instagram(username, password)
    
    profile_url = "https://www.instagram.com/{}/".format(username)
    posts_url = "{}tagged/".format(profile_url)
    saved_url = "{}saved/".format(profile_url)
    
    if not os.path.exists("./screenshots"):
        os.makedirs("./screenshots")
    
    screenshots_with_titles = []
    
    profile_screenshot = "./screenshots/profile_full.png"
    capture_full_page_screenshot(profile_url, profile_screenshot)
    screenshots_with_titles.append(("Profile Page of Suspect", profile_screenshot))
    
    posts_screenshot = "./screenshots/posts_full.png"
    capture_full_page_screenshot(posts_url, posts_screenshot)
    screenshots_with_titles.append(("Tagged Posts", posts_screenshot))
    
    saved_screenshot = "./screenshots/saved_full.png"
    capture_full_page_screenshot(saved_url, saved_screenshot)
    screenshots_with_titles.append(("Saved Posts", saved_screenshot))
    
    inbox_url = "https://www.instagram.com/direct/inbox/"
    inbox_screenshot = "./screenshots/inbox_full.png"
    capture_full_page_screenshot(inbox_url, inbox_screenshot)
    screenshots_with_titles.append(("Inbox", inbox_screenshot))

    chat_usernames = get_chat_list()

    chat_usernames = [username.replace("\n  ·", "") for username in chat_usernames]

    chat_usernames = [item for username in chat_usernames for item in username.split("\n")]
    
    print(chat_usernames)
    output_pdf = "./instagram_report.pdf"
    create_pdf_report(screenshots_with_titles, output_pdf, chat_usernames)
    
    print("Report generated: {}".format(output_pdf))

if __name__ == "__main__":
    main()

    driver.quit()
