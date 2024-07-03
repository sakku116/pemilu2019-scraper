from dotenv import load_dotenv

load_dotenv(override=True)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
from datetime import datetime
from pytz import timezone
import json
from selenium.webdriver.remote.webelement import WebElement
from utils.logging import PackagePathFilter
from utils import helper
from config import Env
from selenium.webdriver.edge.options import Options
import os

# create necessary dirs
log_dir = os.path.join(os.getcwd(), "./logs/rekapitulasi")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
result_dir = os.path.join(os.getcwd(), "./result/rekapitulasi")
if not os.path.exists(result_dir):
    os.makedirs(result_dir)


# logging config
logging.Formatter.converter = lambda *args: datetime.now(
    tz=timezone("Asia/Jakarta")
).timetuple()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s  ...[%(pathname)s@%(funcName)s():%(lineno)d]",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")),
        logging.StreamHandler(),
    ],
)
for logger in logging.root.handlers:
    logger.addFilter(PackagePathFilter())

download_dir = os.path.join(os.getcwd(), "result")
logger = logging.getLogger(__name__)

edge_options = Options()
edge_options.use_chromium = True
edge_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    },
)

driver = webdriver.Edge(options=edge_options)
driver.get("https://pemilu2019.pusataplikasi.com/login")

# login
input_email = driver.find_element(By.ID, "email")
logger.info(f"input email: {helper.getHtmlString(input_email)}")
logger.info(f"inputting email: {Env.EMAIL}")
input_email.send_keys(Env.EMAIL)

input_password = driver.find_element(By.ID, "password")
logger.info(f"input password: {helper.getHtmlString(input_password)}")
logger.info(f"inputting password: {Env.PASSWORD}")
input_password.send_keys(Env.PASSWORD)

submit_btn = driver.find_element(By.CSS_SELECTOR, "[type='submit']")
logger.info(f"submit button: {helper.getHtmlString(submit_btn)}")
submit_btn.click()

base_url = "https://pemilu2019.pusataplikasi.com/hasil-rekapitulasi/dpr-ri"
driver.get("https://pemilu2019.pusataplikasi.com/hasil-rekapitulasi/dpr-ri")

# downloading csv nasional data
logger.info(f"getting csv file of nasional data")
try:
    csv_btn = driver.find_element(By.CSS_SELECTOR, ".buttons-csv")
    # csv_btn.click()
except Exception as e:
    raise e


def getUrls(table: WebElement):
    results = []
    hrefs = table.find_elements(By.CSS_SELECTOR, "a")
    for href in hrefs:
        results.append(href.get_attribute("href"))
    return results

errored_province_urls = []

# logger.info("getting all province urls")
# provinces = []
# next_pagination_btn = driver.find_element(By.CSS_SELECTOR, ".paginate_button.next")
# province_page = 1
# while True:
#     logger.info(f"province page: {province_page}")
#     payload = {
#         "province_name": "",
#         "url": "",
#     }
#     table = driver.find_element(By.TAG_NAME, "table")
#     header_texts = []
#     header_elms = table.find_elements(By.CSS_SELECTOR, "th")
#     for elm in header_elms:
#         header_texts.append(elm.text.strip())

#     logger.info(f"header texts: {header_texts}")
#     input()

#     trs = table.find_elements(By.CSS_SELECTOR, "tr")
#     for tr in trs:
#         tds = tr.find_elements(By.CSS_SELECTOR, "td")
#         first_td = tds[0]
#         payload["province_name"] = first_td.text
#         payload["url"] = first_td.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

#     classes = next_pagination_btn.get_attribute("class")
#     if not classes:
#         raise Exception("next pagination button not found")
#     if "disabled" in classes:
#         break
#     province_page += 1
#     next_pagination_btn.click()
#     next_pagination_btn = driver.find_element(By.CSS_SELECTOR, ".paginate_button.next")

# logger.info(f"total province urls: {len(provinces)}")
# # input()

# regency_urls = []
# for i, province in enumerate(provinces):
#     logger.info(f"visiting province {i}: {province['url']}")
#     driver.get(province["url"])

#     # # downloading csv province data
#     # logger.info(f"getting csv file of province data")
#     # try:
#     #     elements = WebDriverWait(driver, 10).until(
#     #         EC.presence_of_element_located((By.CSS_SELECTOR, ".buttons-csv"))
#     #     )
#     #     csv_btn = driver.find_elements(By.CSS_SELECTOR, ".buttons-csv")
#     #     for btn in csv_btn:
#     #         btn.click()
#     # except Exception as e:
#     #     logger.warning(e)
#     #     errored_province_urls.append(url)

#     # get partai sections
#     content_rows = driver.find_elements(By.CSS_SELECTOR, "section.content div.row")

#     logger.info(f"content rows: {len(content_rows)}")

#     for row in content_rows:
#         cards = row.find_elements(By.CSS_SELECTOR, ".col-md-12 .card .card-body .card")

#         logger.info(f"card len: {len(cards)}")
#         if len(cards) == 0 or len(cards) == 1:
#             continue

#         partai_data = []
#         for partai_section in cards:
#             partai_payload = {
#                 "name": "",
#                 "data": []
#             }
#             partai_name = partai_section.find_element(By.CSS_SELECTOR, ".card-title").text
#             logger.info(f"partai name: {partai_name}")


#             header_texts = []
#             header_elms = partai_section.find_elements(By.CSS_SELECTOR, "th")
#             for elm in header_elms:
#                 header_texts.append(elm.text.strip())


#             person_data = []
#             trs = partai_section.find_elements(By.CSS_SELECTOR, "tbody tr")
#             for tr in trs:
#                 person_payload = {
#                     text: "" for text in header_texts
#                 }
#                 tds = tr.find_elements(By.CSS_SELECTOR, "td")
#                 for i, td in enumerate(tds):
#                     if i == 0:
#                         # remove indexing number
#                         text = td.text.strip().split(" ", 1)[1]
#                     else:
#                         text = td.text.strip()
#                     person_payload[header_texts[i]] = text

#                 person_data.append(person_payload)

#             partai_payload["name"] = partai_name
#             partai_payload["data"] = person_data
#             partai_data.append(partai_payload)


    # partai_sections = content_rows[1].find_elements(By.CSS_SELECTOR, ".card.card-danger.card-outline")
    # logger.info(f"partai sections: {len(partai_sections)}")
    # input()
    # for section in partai_sections:
    #     logger.info(f"partai section: {helper.getHtmlString(section)}")
    # input()



logger.info(f"errored province urls: {errored_province_urls}")
logger.info(f"total errored province urls: {len(errored_province_urls)}")


base_url = "https://pemilu2019.pusataplikasi.com/hasil-rekapitulasi/dpr-ri"
driver.get(base_url)

mapping = {}
next_pagination_btn = driver.find_element(By.CSS_SELECTOR, ".paginate_button.next")

def nextPagination(next_pagination_btn: WebElement):
    classes = next_pagination_btn.get_attribute("class")
    if not classes:
        raise Exception("next pagination button not found")
    if "disabled" in classes:
        return None
    next_pagination_btn.click()
    return next_pagination_btn

def getCurrentPage(curr_index, limit):
    if limit == 0:
        raise ValueError("Limit must be greater than 0")
    current_page = (curr_index // limit) + 1
    return current_page

def adjustCurrIndex(curr_index, limit, new_page):
    # Calculate the start index of the new page
    start_index_new_page = (new_page - 1) * limit
    # Calculate the position within the current page
    position_in_page = curr_index % limit
    # Adjust the current index to be on the new page
    adjusted_curr_index = start_index_new_page + position_in_page
    return adjusted_curr_index

# get province slugs
while True:
    table = driver.find_element(By.TAG_NAME, "table")

    trs = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    for tr in trs:
        tds = tr.find_elements(By.CSS_SELECTOR, "td")
        first_td = tds[0]
        logger.info(f"first td: {helper.getHtmlString(first_td)}")
        a = first_td.find_element(By.CSS_SELECTOR, "a")
        mapping[a.get_attribute("href").removeprefix(base_url)] = {}

    classes = next_pagination_btn.get_attribute("class")
    if not classes:
        raise Exception("next pagination button not found")
    if "disabled" in classes:
        break
    next_pagination_btn.click()
    next_pagination_btn = driver.find_element(By.CSS_SELECTOR, ".paginate_button.next")

logger.info(f"mapping: {json.dumps(mapping, indent=2)}")

# get regency slugs
for slug in mapping:
    driver.get(f"{base_url}{slug}")
    content_rows = driver.find_elements(By.CSS_SELECTOR, "section.content div.row")

    logger.info(f"content rows: {len(content_rows)}")

    for row in content_rows:
        cards = row.find_elements(By.CSS_SELECTOR, ".col-md-12 .card .card-body .card")

        logger.info(f"card len: {len(cards)}")
        if len(cards) == 0 or len(cards) == 1:
            continue

        for partai_section in cards:
            ths = partai_section.find_elements(By.CSS_SELECTOR, "thead th")
            regency_urls = []
            for i, th in enumerate(ths):
                if i == 0:
                    continue

                logger.info(f"th: {th.text}")
                url_split = th.find_element(By.CSS_SELECTOR, "a").get_attribute("href").split("/")
                regency_code = url_split[-1]
                province_code = url_split[-2]
                mapping[slug][regency_code] = {}

            break # just get the first partai section because the next section is has same regencies

    logger.info(f"mapping: {json.dumps(mapping, indent=2)}")