from selenium.webdriver.common.by import By

from ....model.browser.base.driver import BrowserDriver
from ....model.type.xpath import XPath
from ...wait.for_element import wait_for_element


def get_attribute_value(browser_driver: BrowserDriver, xpath: str, attribute: str, timeout: float) -> str:
    xpath = XPath(xpath)
    wait_for_element(browser_driver, xpath, timeout)
    driver = browser_driver.get_webdriver()
    element = driver.find_element(By.XPATH, xpath)  # type: ignore
    return element.get_attribute(attribute)  # type: ignore
