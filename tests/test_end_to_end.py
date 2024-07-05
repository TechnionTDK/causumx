import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()  # You may need to adjust this based on your preferred browser
    yield driver
    driver.quit()

def test_upload_so_database(driver):
    # Start the Streamlit app (you may need to adjust this command)
    os.system("streamlit run ui/app.py &")
    time.sleep(5)  # Wait for the app to start

    # Navigate to the Streamlit app
    driver.get("http://localhost:8501")

    # Wait for the file uploader to be present
    file_uploader = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )

    # Upload the SO database CSV
    file_path = os.path.abspath("path/to/so_database.csv")  # Adjust this path
    file_uploader.send_keys(file_path)

    # Wait for the file to be uploaded and processed
    time.sleep(5)  # You may need to adjust this wait time

    # Check if the upload was successful (you may need to adjust this based on your UI)
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'File uploaded successfully')]"))
    )

    assert success_message.is_displayed()

    # Add more assertions here to check if the data is displayed correctly

    # Clean up: stop the Streamlit app
    os.system("pkill -f 'streamlit run ui/app.py'")
