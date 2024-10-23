from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

# Function to set up WebDriver
def setup_driver():
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Function to verify the title
def verify_title(driver):
    assert "Spotify" in driver.title, "Application did not load successfully."

# Function to verify UI elements
def verify_ui_elements(driver):
    ui_elements = {
        "home_button": '[data-testid="home-button"]',
        "search_box": "form[role='search'].InputContainer-sc-a5ofs0-0",
        "signup_button": '[data-testid="signup-button"]',
        "login_button": '[data-testid="login-button"]'
    }
    
    for name, selector in ui_elements.items():
        element = driver.find_element(By.CSS_SELECTOR, selector)
        assert element.is_displayed(), f"{name} is not displayed."

    print("UI elements are present and accessible.")

# Function to click on 'Show All'
def click_show_all(driver):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.encore-text-body-small-bold'))
    )
    element.click()
    
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, 'span.encore-text-body-small-bold'))
    )
    print("Show all clicked successfully; 'Show all' has disappeared.")

# Function to hover and click the play button
def hover_and_click_play(driver):
    element_to_hover = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-encore-id="card"]'))
    )

    # Hover over the element
    ActionChains(driver).move_to_element(element_to_hover).perform()

    # Wait for the play button to become clickable and click it
    play_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="play-button"]'))
    )
    play_button.click()
    print("Play button clicked successfully.")

# Main function to execute the test
def spotify():
    driver = setup_driver()
    
    try:
        driver.get("https://open.spotify.com/")
        verify_title(driver)
        verify_ui_elements(driver)
        click_show_all(driver)
        hover_and_click_play(driver)

    except TimeoutException:
        print("Timeout: An element did not load in time.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        driver.quit()

# Run the test
if __name__ == "__main__":
    spotify()
