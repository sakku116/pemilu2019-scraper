from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

def getHtmlString(element: WebElement) -> str:
    return element.get_attribute("outerHTML")

def prettifyHtml(html: str, parser: str = "html.parser") -> str:
    bs = BeautifulSoup(html, parser)
    return bs.prettify()
