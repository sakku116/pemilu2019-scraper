from dotenv import load_dotenv

load_dotenv(override=True)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
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
        logging.FileHandler(
            os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        ),
        logging.StreamHandler(),
    ],
)
for logger in logging.root.handlers:
    logger.addFilter(PackagePathFilter())

download_dir = os.path.join(os.getcwd(), "result")
logger = logging.getLogger(__name__)

# edge_options = Options()
# edge_options.use_chromium = True
# edge_options.add_experimental_option(
#     "prefs",
#     {
#         "download.default_directory": download_dir,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True,
#     },
# )

driver = webdriver.Edge()
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
# logger.info(f"getting csv file of national data")
# try:
#     elements = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, ".buttons-csv"))
#     )
#     csv_btn = driver.find_elements(By.CSS_SELECTOR, ".buttons-csv")
#     for btn in csv_btn:
#         btn.click()
# except Exception as e:
#     raise e


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


def getTableData(table: WebElement) -> list[dict]:
    result = []
    header_texts = []
    header_elms = table.find_elements(By.CSS_SELECTOR, "thead th")
    for elm in header_elms:
        header_texts.append(elm.text.strip())

    payload = {text: "" for text in header_texts}

    trs = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    for tr in trs:
        t_payload = payload.copy()
        tds = tr.find_elements(By.CSS_SELECTOR, "td")
        for i, td in enumerate(tds):
            if i == 0:
                # remove indexing number
                text = td.text.strip()
                # text = td.text.strip().split(" ", 1)[1]
            else:
                text = td.text.strip()
            t_payload[header_texts[i]] = text

        result.append(t_payload)

    return result


def getTableDataCalonLegislatif(table: WebElement) -> list[dict]:
    result = []
    header_texts = []
    header_elms = table.find_elements(By.CSS_SELECTOR, "thead th")
    for elm in header_elms:
        header_texts.append(elm.text.strip())

    payload = {text: "" for text in header_texts}

    trs = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    for tr in trs:
        t_payload = payload.copy()
        tds = tr.find_elements(By.CSS_SELECTOR, "td")
        for i, td in enumerate(tds):
            if i == 0:
                # remove indexing number
                text_split = td.text.strip().split(" ", 1)
                text = text_split[1]

                try:
                    t_payload["NOMOR URUT"] = text_split[0].replace(".", "")
                except Exception as e:
                    logger.warning(e)
                    input()
            else:
                text = td.text.strip()
            t_payload[header_texts[i]] = text

        result.append(t_payload)

    return result


base_url = "https://pemilu2019.pusataplikasi.com/hasil-rekapitulasi/dpr-ri"
driver.get(base_url)

mapping = {}
slug_list = []
dir_list = []
next_pagination_btn = driver.find_element(By.CSS_SELECTOR, ".paginate_button.next")


# def nextPagination(next_pagination_btn: WebElement):
#     classes = next_pagination_btn.get_attribute("class")
#     if not classes:
#         raise Exception("next pagination button not found")
#     if "disabled" in classes:
#         return None
#     next_pagination_btn.click()
#     return next_pagination_btn


# def getCurrentPage(curr_index, limit):
#     if limit == 0:
#         raise ValueError("Limit must be greater than 0")
#     current_page = (curr_index // limit) + 1
#     return current_page


# def adjustCurrIndex(curr_index, limit, new_page):
#     # Calculate the start index of the new page
#     start_index_new_page = (new_page - 1) * limit
#     # Calculate the position within the current page
#     position_in_page = curr_index % limit
#     # Adjust the current index to be on the new page
#     adjusted_curr_index = start_index_new_page + position_in_page
#     return adjusted_curr_index


# get province slugs
national_data = []
while True:
    table = driver.find_element(By.TAG_NAME, "table")
    national_data.extend(getTableData(table))

    trs = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    for tr in trs:
        tds = tr.find_elements(By.CSS_SELECTOR, "td")
        first_td = tds[0]
        # logger.info(f"first td: {helper.getHtmlString(first_td)}")
        a = first_td.find_element(By.CSS_SELECTOR, "a")
        href_split = a.get_attribute("href").split("/")
        province_code = href_split[-1]
        province_name = a.text.strip()
        mapping[f"/{province_code}-{province_name}"] = {}
        slug = f"/{province_code}-{province_name}"
        slug_list.append(slug)
        logger.info(f"slug: {slug}")

        # create dir
        dir = os.path.join(os.getcwd(), f"./result/rekapitulasi/dapil/{province_name}")
        if not os.path.exists(dir):
            os.makedirs(dir)

    classes = next_pagination_btn.get_attribute("class")
    if not classes:
        raise Exception("next pagination button not found")
    if "disabled" in classes:
        break
    next_pagination_btn.click()
    next_pagination_btn = driver.find_element(By.CSS_SELECTOR, ".paginate_button.next")

# save data
df = pd.DataFrame(national_data)
file_path = f"./result/rekapitulasi"
df.to_csv(f"{file_path}/data-nasional.csv", index=False)
json.dump(national_data, open(f"{file_path}/data-nasional.json", "w"))
logger.info(f"national_data: {json.dumps(national_data, indent=2)}")

# logger.info(f"mapping: {json.dumps(mapping, indent=2)}")

# get regency slugs
prov_slugs = list(mapping.keys())
prov_slugs.reverse()
for prov_slug in prov_slugs:
    driver.get(f"{base_url}{prov_slug.split('-')[0]}")
    content_rows = driver.find_elements(By.CSS_SELECTOR, "section.content div.row")

    logger.info(f"content rows: {len(content_rows)}")

    # ensure dirs
    data_by_partai_dir = (
        f"./result/rekapitulasi/dapil/{prov_slug.split('-')[1]}/data-by-partai"
    )
    dir = os.path.join(
        os.getcwd(),
        data_by_partai_dir,
    )
    if not os.path.exists(dir):
        os.makedirs(dir)

    for row in content_rows:
        cards = row.find_elements(By.CSS_SELECTOR, ".col-md-12 .card .card-body .card")

        logger.info(f"card len: {len(cards)}")
        if len(cards) == 0 or len(cards) == 1:
            continue

        data_json_all_partai = []
        for partai_index, partai_section in enumerate(cards):
            table = partai_section.find_element(By.TAG_NAME, "table")
            partai_name = partai_section.find_element(
                By.CSS_SELECTOR, ".card-title"
            ).text.strip()
            try:
                partai_name = " ".join(partai_name.split(" ")[:-1])
            except Exception as e:
                logger.warning(e)
                partai_name = partai_name

            ths = table.find_elements(By.CSS_SELECTOR, "thead th")

            if partai_index == 0:
                # just get the first partai section to get header url because the next section is has same headers
                for i, th in enumerate(ths):
                    if i == 0:
                        continue

                    # get url from header text
                    try:
                        a = th.find_element(By.CSS_SELECTOR, "a")
                    except Exception as e:
                        logger.warning(e)
                        continue

                    # logger.info(f"th: {th.text}")
                    url_split = a.get_attribute("href").split("/")
                    regency_name = a.text.strip()
                    regency_code = url_split[-1]

                    mapping[prov_slug][f"/{regency_code}-{regency_name}"] = {}
                    slug = f"{prov_slug}/{regency_code}-{regency_name}"
                    logger.info(f"slug: {slug}")
                    slug_list.append(slug)

                    # create dir
                    dir = os.path.join(
                        os.getcwd(),
                        f"./result/rekapitulasi/dapil/{prov_slug.split('-')[1]}/kabkota/{regency_name}",
                    )
                    if not os.path.exists(dir):
                        os.makedirs(dir)

            # get data
            prov_partai_data = getTableDataCalonLegislatif(table)
            data_json_all_partai.append(
                {"partai": partai_name, "data": prov_partai_data}
            )
            # logger.info(f"prov partai data: {json.dumps(prov_partai_data, indent=2)}")
            logger.info(f"prov partai data: {len(prov_partai_data)}")

            # save data csv by partai
            df = pd.DataFrame(prov_partai_data)
            df.to_csv(f"{data_by_partai_dir}/{partai_name}.csv", index=False)

        # save json data all partai
        json.dump(
            data_json_all_partai,
            open(f"{data_by_partai_dir}/data-all-partai.json", "w"),
        )

    logger.info(f"mapping: {json.dumps(mapping, indent=2)}")

# get district slugs
for prov_slug in list(mapping.keys()):
    regency_slugs = list(mapping[prov_slug].keys())
    regency_slugs.reverse()
    for regency_slug in regency_slugs:
        driver.get(f"{base_url}{prov_slug.split('-')[0]}{regency_slug.split('-')[0]}")
        content_rows = driver.find_elements(By.CSS_SELECTOR, "section.content div.row")

        logger.info(f"content rows: {len(content_rows)}")

        # ensure_dirs
        data_by_partai_dir = f"./result/rekapitulasi/dapil/{prov_slug.split('-')[1]}/kabkota/{regency_slug.split('-')[1]}/data-by-partai"
        dir = os.path.join(
            os.getcwd(),
            data_by_partai_dir,
        )
        if not os.path.exists(dir):
            os.makedirs(dir)

        for row in content_rows:
            cards = row.find_elements(
                By.CSS_SELECTOR, ".col-md-12 .card .card-body .card"
            )

            logger.info(f"card len: {len(cards)}")
            if len(cards) == 0 or len(cards) == 1:
                continue

            data_json_all_partai = []
            for partai_index, partai_section in enumerate(cards):
                table = partai_section.find_element(By.TAG_NAME, "table")
                partai_name = partai_section.find_element(
                    By.CSS_SELECTOR, ".card-title"
                ).text.strip()
                try:
                    partai_name = " ".join(partai_name.split(" ")[:-1])
                except Exception as e:
                    logger.warning(e)
                    partai_name = partai_name

                ths = table.find_elements(By.CSS_SELECTOR, "thead th")
                if partai_index == 0:
                    # just get the first partai section to get headers because the next section is has same headers
                    for i, th in enumerate(ths):
                        if i == 0:
                            continue

                        try:
                            a = th.find_element(By.CSS_SELECTOR, "a")
                        except Exception as e:
                            logger.warning(e)
                            continue

                        # logger.info(f"th: {th.text}")
                        url_split = a.get_attribute("href").split("/")
                        district_code = url_split[-1]
                        district_name = a.text.strip()

                        mapping[prov_slug][regency_slug][
                            f"/{district_code}-{district_name}"
                        ] = {}
                        slug = (
                            f"{prov_slug}{regency_slug}/{district_code}-{district_name}"
                        )
                        slug_list.append(slug)
                        logger.info(f"slug: {slug}")

                        # create dir
                        dir = os.path.join(
                            os.getcwd(),
                            f"./result/rekapitulasi/dapil/{prov_slug.split('-')[1]}/kabkota/{regency_slug.split('-')[1]}/kecamatan/{district_name}",
                        )
                        if not os.path.exists(dir):
                            os.makedirs(dir)

                # get data
                regency_partai_data = getTableDataCalonLegislatif(table)
                data_json_all_partai.append(
                    {"partai": partai_name, "data": regency_partai_data}
                )
                # logger.info(
                #     f"regency partai data: {json.dumps(regency_partai_data, indent=2)}"
                # )
                logger.info(f"regency partai data: {len(regency_partai_data)}")

                # save data csv per partai
                df = pd.DataFrame(regency_partai_data)
                df.to_csv(f"{data_by_partai_dir}/{partai_name}.csv", index=False)

            # save json data all partai
            json.dump(
                data_json_all_partai,
                open(f"{data_by_partai_dir}/data-all-partai.json", "w"),
            )

        logger.info(f"mapping: {json.dumps(mapping, indent=2)}")

# get village slugs
for prov_slug in list(mapping.keys()):
    for regency_slug in list(mapping[prov_slug].keys()):
        district_slugs = list(mapping[prov_slug][regency_slug].keys())
        district_slugs.reverse()
        for district_slug in district_slugs:
            driver.get(
                f"{base_url}{prov_slug.split('-')[0]}{regency_slug.split('-')[0]}{district_slug.split('-')[0]}"
            )
            content_rows = driver.find_elements(
                By.CSS_SELECTOR, "section.content div.row"
            )

            logger.info(f"content rows: {len(content_rows)}")

            # enusure dirs
            data_by_partai_dir = f"./result/rekapitulasi/dapil/{prov_slug.split('-')[1]}/kabkota/{regency_slug.split('-')[1]}/kecamatan/{district_slug.split('-')[1]}/data-by-partai"
            dir = os.path.join(
                os.getcwd(),
                data_by_partai_dir,
            )
            if not os.path.exists(dir):
                os.makedirs(dir)

            for row in content_rows:
                cards = row.find_elements(
                    By.CSS_SELECTOR, ".col-md-12 .card .card-body .card"
                )

                logger.info(f"card len: {len(cards)}")
                if len(cards) == 0 or len(cards) == 1:
                    continue

                data_json_all_partai = []
                for partai_index, partai_section in enumerate(cards):
                    table = partai_section.find_element(By.TAG_NAME, "table")
                    partai_name = partai_section.find_element(
                        By.CSS_SELECTOR, ".card-title"
                    ).text.strip()
                    try:
                        partai_name = " ".join(partai_name.split(" ")[:-1])
                    except Exception as e:
                        logger.warning(e)
                        partai_name = partai_name

                    ths = table.find_elements(By.CSS_SELECTOR, "thead th")
                    if partai_index == 0:
                        # just get the first partai section to get headers because the next section is has same headers
                        for i, th in enumerate(ths):
                            if i == 0:
                                continue

                            try:
                                a = th.find_element(By.CSS_SELECTOR, "a")
                            except Exception as e:
                                logger.warning(e)
                                continue

                            # logger.info(f"th: {th.text}")
                            url_split = a.get_attribute("href").split("/")
                            village_code = url_split[-1]
                            village_name = a.text.strip()

                            mapping[prov_slug][regency_slug][district_slug][
                                f"/{village_code}-{village_name}"
                            ] = {}
                            slug = f"{prov_slug}{district_slug}/{village_code}-{village_name}"
                            slug_list.append(slug)
                            logger.info(f"slug: {slug}")

                            # create dir
                            dir = os.path.join(
                                os.getcwd(),
                                f"./result/rekapitulasi/dapil/{prov_slug.split('-')[1]}/kabkota/{regency_slug.split('-')[1]}/kecamatan/{district_slug.split('-')[1]}/kelurahan/{village_name}",
                            )
                            if not os.path.exists(dir):
                                os.makedirs(dir)

                    # get data csv per partai
                    district_partai_data = getTableData(table)
                    data_json_all_partai.append(
                        {"partai": partai_name, "data": district_partai_data}
                    )
                    # logger.info(
                    #     f"district partai data: {json.dumps(district_partai_data, indent=2)}"
                    # )
                    logger.info(f"district partai data: {len(district_partai_data)}")

                    # save data csv per partai
                    df = pd.DataFrame(district_partai_data)
                    df.to_csv(f"{data_by_partai_dir}/{partai_name}.csv", index=False)

                # save json data all partai
                json.dump(
                    data_json_all_partai,
                    open(f"{data_by_partai_dir}/data-all-partai.json", "w"),
                )

            logger.info(f"mapping: {json.dumps(mapping, indent=2)}")

# get village data
for prov_slug in list(mapping.keys()):
    for regency_slug in list(mapping[prov_slug].keys()):
        for district_slug in list(mapping[prov_slug][regency_slug].keys()):
            village_slugs = list(
                mapping[prov_slug][regency_slug][district_slug].keys()
            )
            village_slugs.reverse()
            for village_slug in village_slugs:
                driver.get(
                    f"{base_url}{prov_slug.split('-')[0]}{regency_slug.split('-')[0]}{district_slug.split('-')[0]}{village_slug.split('-')[0]}"
                )
                content_rows = driver.find_elements(
                    By.CSS_SELECTOR, "section.content div.row"
                )

                logger.info(f"content rows: {len(content_rows)}")

                data_by_partai_dir = f"./result/rekapitulasi/dapil/{prov_slug.split('-')[1]}/kabkota/{regency_slug.split('-')[1]}/kecamatan/{district_slug.split('-')[1]}/kelurahan/{village_slug.split('-')[1]}/data-by-partai"
                dir = os.path.join(
                    os.getcwd(),
                    data_by_partai_dir,
                )
                if not os.path.exists(dir):
                    os.makedirs(dir)
                else:
                    continue

                for row in content_rows:
                    cards = row.find_elements(
                        By.CSS_SELECTOR, ".col-md-12 .card .card-body .card"
                    )

                    logger.info(f"card len: {len(cards)}")
                    if len(cards) == 0 or len(cards) == 1:
                        continue

                    data_json_all_partai = []
                    for partai_section in cards:
                        table = partai_section.find_element(By.TAG_NAME, "table")
                        partai_name = partai_section.find_element(
                            By.CSS_SELECTOR, ".card-title"
                        ).text.strip()
                        try:
                            partai_name = " ".join(partai_name.split(" ")[:-1])
                        except Exception as e:
                            logger.warning(e)
                            partai_name = partai_name

                        village_partai_data = getTableDataCalonLegislatif(table)
                        data_json_all_partai.append(
                            {"partai": partai_name, "data": village_partai_data}
                        )
                        # logger.info(
                        #     f"village partai data: {json.dumps(village_partai_data, indent=2)}"
                        # )
                        logger.info(f"village partai data: {len(village_partai_data)}")

                        # save data csv per partai
                        df = pd.DataFrame(district_partai_data)
                        df.to_csv(
                            f"{data_by_partai_dir}/{partai_name}.csv", index=False
                        )

                    # save json data all partai
                    json.dump(
                        data_json_all_partai,
                        open(f"{data_by_partai_dir}/data-all-partai.json", "w"),
                    )
