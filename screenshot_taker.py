from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def take_screenshot(app_id, config):
    url = f"{config['resourcemanager_url']}/cluster/app/{app_id}"
    screenshot_path = os.path.join(config['screenshot_folder'], f"{app_id}.png")
    os.makedirs(config['screenshot_folder'], exist_ok=True)

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)

    try:
        driver.get(url)
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()

    return screenshot_path
