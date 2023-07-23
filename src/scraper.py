from bs4 import BeautifulSoup
from getuseragent import UserAgent
import requests

import time
import datetime
import logging

from .api import schemas
from . import logging_config
from . import utils

# configuring the Logger object for the module
logging_config.configure_logging()
logger = logging.getLogger(__name__)

soup = ""


def get_main_page(verified="y", active="y") -> int:
    submission = None
    while submission == None:
        global soup

        user_agent = UserAgent()  # instantiating UserAgent seed

        the_user_agent = user_agent.Random()  # Generating a fake randomized user agent

        headers = {"User-agent": the_user_agent}

        url = f"https://phishtank.org/phish_search.php?verified={verified}&active={active}"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logger.exception(
                f"Html error occurred. Status code: {response.status_code}"
            )
            return 1

        html_text = response.text
        soup = BeautifulSoup(html_text, "lxml")

        submission = soup.find("tr", style="background: #ffffcc;")

    return 0


def get_submissions(verified="y") -> list[schemas.PhishingSiteCreate]:
    if verified == "y":
        submissions = soup.find_all("tr", style="background: #ffffcc;")

    site_list = []
    for submission in submissions:
        site = get_site_object(submission)
        site_list.append(site)

    return site_list


def get_site_object(
    submission: BeautifulSoup, verified="y", active="y"
) -> schemas.PhishingSiteCreate:
    values = submission.find_all("td", class_="value")

    Phishtank_id = int(values[0].find("a").text)
    url = values[1].find_next(string=True).strip()

    if verified == "y":
        status = "Valid"
    else:
        status = schemas.StatusEnum.SUSPECTED

    if active == "y":
        is_online = "True"
    else:
        is_online = schemas.IsOnlineEnum.FALSE

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


"""



https://phishtank.org/phish_search.php?verified=u&active=y
https://phishtank.org/phish_search.php?verified=y&active=y
https://phishtank.org/phish_search.php?verified=y&active=n
https://phishtank.org/phish_search.php?verified=u&active=n """
