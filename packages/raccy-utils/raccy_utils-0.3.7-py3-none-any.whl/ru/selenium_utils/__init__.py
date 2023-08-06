"""
Copyright 2021 Daniel Afriyie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import time
import typing
import warnings
import sys
import random as rd

try:
    from selenium.webdriver.remote.webdriver import WebDriver, WebElement
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import (
        TimeoutException, WebDriverException, ElementClickInterceptedException,
        StaleElementReferenceException
    )
except ImportError:
    warnings.warn("It seems you don't have selenium installed. "
                  "Install it before using this module!\npip3 install selenium")
try:
    import pyperclip
except ImportError:
    warnings.warn("It seems you don't have pyperclip installed. "
                  "Install it before using this module!\npip3 install pyperclip")

Element = typing.Union[WebElement, typing.List[WebElement]]
Condition = typing.Optional[typing.Callable[[typing.Tuple[str, str]], typing.Any]]
Seconds = typing.Optional[typing.Union[int, float]]
Args = typing.Tuple[typing.Any, ...]
Kwargs = typing.Dict[str, typing.Any]
Action = typing.Optional[str]


def window_scroll_to(driver: WebDriver, loc: typing.Union[int, float]) -> None:
    driver.execute_script(f"window.scrollTo(0, {loc});")


def scroll_into_view(driver: WebDriver, element: WebElement, offset: typing.Optional[int] = 200) -> None:
    window_scroll_to(driver, element.location['y'] - offset)


def scroll_into_view_js(driver: WebDriver, element: WebElement) -> None:
    driver.execute_script("arguments[0].scrollIntoView();", element)


def _driver_wait(
        driver: WebDriver,
        locator: str,
        by: str,
        secs: Seconds = 10,
        condition: Condition = ec.element_to_be_clickable,
        action: Action = None,
        *args: Args,
        **kwargs: Kwargs
) -> Element:
    wait: WebDriverWait = WebDriverWait(driver=driver, timeout=secs)
    element: Element = wait.until(condition((by, locator)))
    if action:
        if hasattr(element, action):
            action_func = getattr(element, action)
            action_func(*args, **kwargs)
    return element


def find_element_by_xpath(
        driver: WebDriver,
        xpath: str,
        secs: Seconds = 10,
        condition: Condition = ec.element_to_be_clickable,
        action: Action = None,
        *args: Args,
        **kwargs: Kwargs
) -> Element:
    return _driver_wait(driver, xpath, By.XPATH, secs, condition, action, *args, **kwargs)


def find_element_by_css(
        driver: WebDriver,
        selector: str,
        secs: Seconds = 10,
        condition: Condition = ec.element_to_be_clickable,
        action: Action = None,
        *args: Args,
        **kwargs: Kwargs
) -> Element:
    return _driver_wait(driver, selector, By.CSS_SELECTOR, secs, condition, action, *args, **kwargs)


def find_element_by_id(
        driver: WebDriver,
        id: str,
        secs: Seconds = 10,
        condition: Condition = ec.element_to_be_clickable,
        action: Action = None,
        *args: Args,
        **kwargs: Kwargs
) -> Element:
    return _driver_wait(driver, id, By.ID, secs, condition, action, *args, **kwargs)


def find_element_by_link_text(
        driver: WebDriver,
        text: str,
        secs: Seconds = 10,
        condition: Condition = ec.element_to_be_clickable,
        action: Action = None,
        *args: Args,
        **kwargs: Kwargs
) -> Element:
    return _driver_wait(driver, text, By.LINK_TEXT, secs, condition, action, *args, **kwargs)


def driver_or_js_click(
        driver: WebDriver,
        xpath: str,
        secs: Seconds = 5,
        condition: Condition = ec.element_to_be_clickable
) -> None:
    try:
        elm: WebElement = find_element_by_xpath(driver, xpath, secs=secs, condition=condition)
        ActionChains(driver).move_to_element(elm).click().perform()
    except WebDriverException:
        elm: WebElement = driver.find_element(By.XPATH, xpath)
        try:
            ActionChains(driver).move_to_element(elm).click().perform()
        except WebDriverException:
            driver.execute_script("arguments[0].click()", elm)


def manual_entry(
        driver: WebDriver,
        xpath: str,
        text: str,
        secs: Seconds = 10,
        condition: Condition = ec.element_to_be_clickable,
        sleep_time: Seconds = 0.05,
        *args: Args
) -> None:
    if (not isinstance(sleep_time, int)) and (not isinstance(sleep_time, float)):
        args += (sleep_time,)
        sleep_time = 0.05
    elm: WebElement = find_element_by_xpath(driver, xpath, secs=secs, condition=condition)
    ActionChains(driver).move_to_element(elm).perform()
    elm.clear()
    text = f"{text}"
    for letter in text:
        elm.send_keys(letter)
        time.sleep(sleep_time)
    time.sleep(sleep_time)
    elm.send_keys(*args)


def enter(
        driver: WebDriver,
        xpath: str,
        text: str,
        secs: Seconds = 10,
        condition: Condition = ec.element_to_be_clickable,
        *args: Args
) -> None:
    elm: WebElement = find_element_by_xpath(driver, xpath, secs=secs, condition=condition)
    ActionChains(driver).move_to_element(elm).perform()
    elm.clear()
    text = f"{text}"
    elm.send_keys(text, *args)


def paste(
        driver: WebDriver,
        xpath: str,
        text: str,
        secs: Seconds = 10,
        condition: Condition = ec.element_to_be_clickable
) -> None:
    elm: WebElement = find_element_by_xpath(driver, xpath, secs=secs, condition=condition)
    pyperclip.copy(text)
    if sys.platform == 'darwin':
        ctrl = Keys.COMMAND
    else:
        ctrl = Keys.CONTROL
    actions: ActionChains = ActionChains(driver)
    actions.move_to_element(elm)
    actions.click()
    actions.key_down(ctrl)
    actions.send_keys('v')
    actions.key_up(ctrl)
    actions.perform()


def random_delay(a: typing.Optional[int] = 1, b: typing.Optional[int] = 3) -> None:
    delay: int = rd.randint(a, b)
    precision: float = delay / (a + b)
    sleep_time: float = delay + precision
    time.sleep(sleep_time)


driver_wait = find_element_by_xpath
