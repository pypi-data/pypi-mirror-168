#!/usr/bin/python
import glob
import os
import re
import sys
import time
import pathlib

from tqdm.auto import trange
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chromium.service import ChromiumService


# Define some important script constants
PATH_DRIVER = '/usr/bin/chromedriver'
NAME_ANIME = '//div[@class="anime__details__title"]/h3'
YEAR_ANIME = '//div[@class="anime__details__widget"]//ul/li[7]'
NUMBER_EPISODES = '//div[@class="anime__details__widget"]//ul/li[5]'
DOWNLOAD_MENU = '//a[@class="video-download"]'
DOWNLOAD_BUTTON = '//a[@id="jkdown"]'
BAR_FORMAT = '{desc}: {n_fmt} de {total_fmt} |{bar}|[{elapsed}<{remaining}]'


def setup_driver():
    # Install the service with Chrome/Chromium driver
    # service = ChromeService(ChromeDriverManager().install())
    service = ChromeService(executable_path=PATH_DRIVER)

    # Add some options to be carried by the driver
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")

    return webdriver.Chrome(service=service, options=options)


def request_and_download(driver, url):
    # Make a request to the URL
    driver.get(url)

    # Getting the anime name
    name_anime = driver.find_element(by=By.XPATH, value=NAME_ANIME).text

    # Getting the anime year
    year_anime = driver.find_element(by=By.XPATH, value=YEAR_ANIME).text
    year_anime = re.findall("\d{4}", year_anime)[0]

    # Get the total number of episodes
    number_episodes = driver.find_element(
        by=By.XPATH, value=NUMBER_EPISODES).text
    number_episodes = int(number_episodes.split(":")[-1])

    # Check if the directory where the files will be downloaded exists.
    name_dir = f"./Anime/{name_anime} ({year_anime})/Season 01"
    pathlib.Path(name_dir).mkdir(parents=True, exist_ok=True)

    # Call the function to download each episode
    print(f"Download {name_anime}:")

    for index in trange(1, number_episodes + 1,
                        desc="Episode",
                        leave=None,
                        colour="green",
                        initial=1,
                        bar_format=BAR_FORMAT):

        url_episode = f"{url}{index}"

        download_a_video(driver=driver,
                         url=url_episode,
                         name_anime=name_anime,
                         name_dir=name_dir,
                         index=index)


def download_a_video(driver, url, name_anime, name_dir, index):
    # Make a request to episode URL
    driver.get(url)

    # Search for the download menu element
    download_menu = driver.find_element(by=By.XPATH, value=DOWNLOAD_MENU)
    download_menu.click()

    # Search for the download button element
    download_button = driver.find_element(by=By.XPATH, value=DOWNLOAD_BUTTON)
    download_button.click()

    # Wait until the download of the complete file is complete
    timeout = 300

    for t in trange(timeout,
                    desc="Timeout",
                    colour="green",
                    leave=None):

        # Check if the file has finished downloading
        episode_mp4 = f"{str(index).zfill(2)}.mp4"
        file_episode = glob.glob(f"./*-{episode_mp4}")

        if not file_episode:
            time.sleep(1)
        else:
            # Rename the downloaded file and move it to its directory
            os.rename(file_episode[0], f"{name_dir}/E{episode_mp4}")
            break

    if not file_episode:
        print(
            f"\nERROR: Timeout to download {name_anime} - Episode: {index} was exceeded.")


def run():
    driver = setup_driver()
    URLs = sys.argv[1:]

    for url in URLs:
        request_and_download(driver, url)

    driver.close()


if __name__ == "__main__":
    run()
