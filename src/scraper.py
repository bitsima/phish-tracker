"""Scraping module specialized for PhishTank submissions.

Contains the following functions:
get_main_page() -> int
get_updated_data(PhishTank_id: int) -> int
get_submissions() -> list[schemas.PhishingSiteCreate]
get_site_object(submission: BeautifulSoup) -> schemas.PhishingSiteCreate
"""

from bs4 import BeautifulSoup
from getuseragent import UserAgent
import requests

import time


from .api import schemas
from . import utils


soup = ""


def get_main_page() -> int:
    """Creates the global soup object for the main page of the phish archive of PhishTank.

    Sends the request with a fake user agent header and sets the html text response to the soup.

    Returns:
        int: error status
    """
    submission = None
    while submission is None:
        global soup

        user_agent = UserAgent()  # instantiating UserAgent seed

        the_user_agent = user_agent.Random()  # Generating a fake randomized user agent

        headers = {"User-agent": the_user_agent}

        url = "https://phishtank.org/phish_archive.php"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return 1

        html_text = response.text
        soup = BeautifulSoup(html_text, "lxml")

        submission = soup.find("tr", style="background: #ffffcc;")
        if submission is None:
            submission = soup.find("tr", style="background: #ffffff;")

    return 0


def get_updated_data(PhishTank_id: int) -> schemas.PhishingSiteUpdate:
    """Sends a new request to PhishTank for the page of the individual submission with the given id.
    Then scrapes and processes the online status and validity of the url. Returns the latest values as a schema.

        Args:
            PhishTank_id (int): id of the url-to-be-updated

        Returns:
            schemas.PhishingSiteUpdate: new updated values, in the form of PhishingSiteUpdate schema
    """
    user_agent = UserAgent()  # instantiating UserAgent seed

    the_user_agent = user_agent.Random()  # Generating a fake randomized user agent

    headers = {"User-agent": the_user_agent}

    url = f"https://phishtank.org/phish_detail.php?phish_id={PhishTank_id}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
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
    """Scrapes the individual submissions on the main page of PhishTank.
    Then creates a list of the said submissions, each a new schema instance of type PhishingSiteCreate.

    Returns:
        list[schemas.PhishingSiteCreate]: the list of schema objects, parsed and generated from the main page soup
    """

    submissions = soup.find("table", class_="data").find_all(recursive=False)[1:-5]

    site_list = []
    for submission in submissions:
        site = get_site_object(submission)
        site_list.append(site)

    return site_list


def get_site_object(submission: BeautifulSoup) -> schemas.PhishingSiteCreate:
    """Creates a new schema object of type PhishingSiteCreate, using the values from the submission soup.

    Args:
        submission (BeautifulSoup): the soup for a single submission

    Returns:
        schemas.PhishingSiteCreate: the newly generated schema instance with the scraped values
    """

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
