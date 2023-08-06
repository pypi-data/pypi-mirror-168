import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import undetected_chromedriver as uc


class Selenium:

    def __init__(self):

        self.capabilities = DesiredCapabilities.CHROME.copy()
        self.capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

        self.options = uc.ChromeOptions()
        self.options.headless = True

        argument_list = [
            '--no-first-run',
            '--no-service-autorun',
            '--password-store=basic',
            '--log-level=3'
        ]
        self.options.arguments.extend(argument_list)

        self.driver = uc.Chrome(
            options=self.options,
            desired_capabilities=self.capabilities
        )

    def get_page(self, url, *args, **kwargs):
        return self.driver.get(url, *args, **kwargs)

    def get_cfpage(self, url, *args, **kwargs):
        page = self.get_page(url, *args, **kwargs)

        WebDriverWait(self.driver, 15).until_not(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'p[data-translate=resolve_captcha_network]')
            )
        )

        return page

    @property
    def source(self):
        return self.driver.page_source

    def exit(self):
        self.driver.quit()
