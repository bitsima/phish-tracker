from bs4 import BeautifulSoup
from getuseragent import UserAgent
import requests

import time
import logging

from .api import schemas
from . import logging_config
from . import utils
from .database import services


# configuring the Logger object for the module
logging_config.configure_logging()
logger = logging.getLogger(__name__)

soup = ""


def get_main_page() -> int:
    submission = None
    while submission == None:
        global soup

        user_agent = UserAgent()  # instantiating UserAgent seed

        the_user_agent = user_agent.Random()  # Generating a fake randomized user agent

        headers = {"User-agent": the_user_agent}

        url = "https://phishtank.org/phish_archive.php"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logger.exception(
                f"Html error occurred. Status code: {response.status_code}"
            )
            return 1

        html_text = response.text
        soup = BeautifulSoup(html_text, "lxml")

        submission = soup.find("tr", style="background: #ffffcc;")
        if submission == None:
            submission = soup.find("tr", style="background: #ffffff;")

    return 0


def get_updated_data(PhishTank_id: int) -> int:
    user_agent = UserAgent()  # instantiating UserAgent seed

    the_user_agent = user_agent.Random()  # Generating a fake randomized user agent

    headers = {"User-agent": the_user_agent}

    url = f"https://phishtank.org/phish_detail.php?phish_id={PhishTank_id}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.exception(f"Html error occurred. Status code: {response.status_code}")
        return 1

    html_text = response.text
    soup_submission = BeautifulSoup(html_text, "lxml")

    raw_status = soup_submission.find("tr").find_all(recursive=False)[1].find("h3").text

    raw_is_online = (
        soup_submission.find("h2", style="margin:0;border:0;")
        .find("span", style="font-weight:normal;")
        .text
    )

    status, is_online = utils.status_formatter(raw_status, raw_is_online)

    site_schema = schemas.PhishingSiteUpdate(
        status=status, is_online=is_online, description=""
    )

    return site_schema


def get_submissions() -> list[schemas.PhishingSiteCreate]:
    submissions = soup.find("table", class_="data").find_all(recursive=False)[1:-5]

    site_list = []
    for submission in submissions:
        site = get_site_object(submission)
        site_list.append(site)

    return site_list


def get_site_object(submission: BeautifulSoup) -> schemas.PhishingSiteCreate:
    values = submission.find_all("td", class_="value")

    Phishtank_id = int(values[0].find("a").text)
    url = values[1].find_next(string=True).strip()

    status = values[3].text

    is_online = values[4].text

    # converting into timestamp
    submitted_at = utils.get_timestamp(values[1].find("span").text)
    description = ""
    submitted_by = values[2].find("a").text

    site = schemas.PhishingSiteCreate(
        PhishTank_id=Phishtank_id,
        url=url,
        status=status,
        is_online=is_online,
        submitted_at=submitted_at,
        description=description,
        submitted_by=submitted_by,
        date_created=time.time(),
    )

    return site
