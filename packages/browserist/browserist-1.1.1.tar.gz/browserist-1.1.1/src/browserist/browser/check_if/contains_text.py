import re

from selenium.webdriver.common.by import By

from ...model.browser.base.driver import BrowserDriver
from ...model.type.xpath import XPath


def check_if_contains_text(browser_driver: BrowserDriver, xpath: str, regex: str, ignore_case: bool = True) -> bool:
    xpath = XPath(xpath)
    try:
        driver = browser_driver.get_webdriver()
        element = driver.find_element(By.XPATH, xpath)  # type: ignore
        text = str(element.text)
        match = re.search(regex, text, re.IGNORECASE) if ignore_case else re.search(regex, text)
        return bool(match)
    except Exception:
        return False
