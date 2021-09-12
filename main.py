import argparse
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from print_colors import green, red

parser = argparse.ArgumentParser(
    description='Make markdown template for a TryHackMe room.')
parser.add_argument(
    "-r",
    "--room",
    metavar="Room's URL",
    help=
    "Room's URL (Include full URL) eg:-'https://tryhackme.com/room/linuxfundamentalspart1'",
    required=True)
args = parser.parse_args()


def write_thm_md(url):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(url)

    try:
        tasks = WebDriverWait(browser, 10).until(
            EC.invisibility_of_element_located((By.ID, "loading")))

        soup = BeautifulSoup(browser.page_source, "html.parser")
    finally:
        browser.quit()

    if soup.title.text == "TryHackMe | Why Subscribe":
        red("can't make template from rooms which needs Subscription.")
        return
    title = soup.select_one("#title").text.strip()
    tasks = soup.find(id="taskContent").find_all(class_="card")

    topics = {}

    green(f"getting template for {title}")
    for task in tasks:
        card_title = task.find(class_="card-header").text.strip()
        questions = task.select(
            ".room-task-questions>.room-task-question-details")
        topics[card_title] = []

        for i, question in enumerate(questions):
            topics[card_title].append(question.text.strip())

    questin_num = 1
    with open(f"{title.lower()}.md", "w") as f:
        f.write(f"# {title}\n\n")
        for title, questions in topics.items():
            f.write(f"## {title}\n\n")
            for question in questions:
                f.write(f"{questin_num}. ### {question}\n")
                f.write("```\n```\n\n")
                questin_num += 1

    green(f"Finished writing template for {title}")


room_url: str = args.room
parsed_room_url = urllib.parse.urlparse(room_url)

if parsed_room_url.netloc != "tryhackme.com":
    red("Please enter a valid TryHackMe room's URL including the URL scheme.")
    exit(1)

if not parsed_room_url.path.startswith("/room/"):
    red("That's not a TryHackMe room URL. Please enter a vald room URL")
    exit(1)

try:
    write_thm_md(room_url)
except:
    msg = """Something went wrong. Please try the following methods:
    1. Check if the room's URL is correct.
    2. Check the URL is correct.
    3. Check if the room exists.
    4. Check if the room is not a subscription only room.
    """
    exit(1)
