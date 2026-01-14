from datetime import datetime
import os

def take_screenshot(driver, test_name, folder_name="Screenshots"):
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # Project root directory
    project_root = os.path.dirname(os.path.dirname(__file__))

    screenshot_dir = os.path.join(project_root, folder_name)
    os.makedirs(screenshot_dir, exist_ok=True)

    screenshot_path = os.path.join(
        screenshot_dir,
        f"{test_name}_{timestamp}.png"
    )

    driver.save_screenshot(screenshot_path)

    return screenshot_path
