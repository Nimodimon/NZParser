from utils import clear_text
from bs4 import BeautifulSoup

def parse_week(page: BeautifulSoup) -> list[list]:
    days_bs = page.find("div", {"class": "dn-items"})
    return [parse_day(day) for day in days_bs.find_all("div", {"class": "dn-item"})]

def parse_day(day: BeautifulSoup) -> list[dict]:
    lessons_bs = day.find("ul", {"class": "dni-predmety"})
    return [parse_lesson(lesson) for lesson in lessons_bs.find_all("li")]

def parse_lesson(lesson: BeautifulSoup) -> dict:
    try:
        name = lesson.find("div", {"class": "part-left"}).find(text=True, recursive=False)
    except AttributeError:
        return {
            "name": "",
            "type": "",
            "topic": "",
            "room": "",
            "homeworks": [],
            "mark": 0
        }

    try:
        room = lesson.find("div", {"class": "part-left"}).find("span").text
    except AttributeError:
        room = ""

    try:
        mark = lesson.find("div", {"class": "part-right"}).find("div", {"class": "dnip-right"}).text
    except AttributeError:
        mark = "0"

    type_and_topic = parse_type_and_topic(lesson)

    return {
        "name": clear_text(name),
        "type": type_and_topic[0],
        "topic": type_and_topic[1],
        "room": clear_text(room)[1:],
        "homeworks": parse_homeworks(lesson),
        "mark": int(clear_text(mark))
    }

def parse_homeworks(lesson: BeautifulSoup) -> list:
    homeworks = lesson.find("div", {"class": "part-right"}).findAll(text=True, recursive=False)
    homeworks_iter = (clear_text(homework) for homework in homeworks)

    return list(filter(None, homeworks_iter))

def parse_type_and_topic(lesson: BeautifulSoup) -> (str, str):
    type_and_topic = lesson.find("div", {"class": "part-right"}).find("div", {"class": "dnip-content"}).text
    type_and_topic_list = clear_text(type_and_topic).split(":")

    return type_and_topic_list[0], type_and_topic_list[1][1:]
