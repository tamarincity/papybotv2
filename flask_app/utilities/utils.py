from typing import List
import unicodedata
import re
import logging
import os
from datetime import datetime

from ..constants import (
    CSV_COLUMN_NAMES,
    CSV_FILENAME,
    OUTPUT_PATH,
)


def remove_accents(text_to_format):
    try:
        if not (
                text_to_format
                and isinstance(text_to_format, str)
        ):

            raise Exception(
                "Error! remove_accents(): arg is wrong or None")
    except Exception as e:
        logging.error(str(e))
        return ""

    return "".join(
        char
        for char in unicodedata.normalize("NFD", text_to_format)
        if unicodedata.category(char) != "Mn"
    )


def remove_punctuation(text_to_format):
    try:
        if not (
                text_to_format
                and isinstance(text_to_format, str)
        ):

            raise Exception(
                "Error! remove_punctuation(): arg is wrong or None")
    except Exception as e:
        logging.error(str(e))
        return ""

    return re.sub(r"[^\w\s]", "", text_to_format)


def remove_some_words_and_format_text(
    text_to_format: str, words_to_remove: List[str]):
    """
    Remove words from the given text and format the text
    """
    try:
        if not (
                text_to_format
                and words_to_remove
                and isinstance(text_to_format, str)
                and isinstance(words_to_remove, list)
        ):
            raise Exception(
                "Error! remove_some_words_and_format_text(): args are wrong or None")
    except Exception as e:
        logging.error(str(e))
        return ""

    text_to_format = text_to_format.lower() if text_to_format else ""

    # save appostrophy and replace minus sign by space
    text_to_format = text_to_format.replace("'", "75dhzkgf85h").replace("-", " ")

    # save " à " because it can help to determine the city
    text_to_format = text_to_format.replace(" à ", "75dhdhfk753f85h")

    text_to_format = remove_accents(text_to_format)
    text_to_format = remove_punctuation(text_to_format)
    # Re-inject the appostrophy
    text_to_format = text_to_format.replace("75dhzkgf85h", "'")

    # Re-inject the " à "
    text_to_format = text_to_format.replace("75dhdhfk753f85h", " à ")

    # Remove courtesy words
    for word in words_to_remove:
        text_to_format = text_to_format.replace(word, "")

    # Remove double space
    while "  " in text_to_format:
        text_to_format = text_to_format.replace("  ", " ")

    text_to_format = text_to_format.strip()
    return text_to_format


def extract_question_from_text(text_to_format, STOP_WORDS: List[str]):
    if not (
            text_to_format
            and STOP_WORDS
            and isinstance(text_to_format, str)
            and isinstance(STOP_WORDS, list)
    ):
        return None
    
    for word in STOP_WORDS:
        if word in text_to_format:
            return text_to_format.split(word)[1].strip()
    return None


def extract_city_from_question(question):
    """
    Extract the city from the question if
    "ville de " is in the question.

    Args:
        question (string): the question including the city

    Returns:
        tuple: question: string, city: string
    """

    city_stop_words = [
        " de la ville de ",
        " de la ville d'",
        " de la ville ",
        "ville de ",
        "ville d'",
        " ville:",
        " ville :",
        " ville ",
    ]

    if not (
            question
            and isinstance(question, str)):
        return "", None

    for stop_word in city_stop_words:
        if stop_word in question:
            elements_of_question = question.split(stop_word)
            return elements_of_question[0].strip(), elements_of_question[-1].strip()

    return question, None


def figure_out_city(question):
    """
    Try to figure out what is the city from the question.
    This function uses keywords such as " à ", " de ".

    Args:
        question (string): the question including the city

    Returns:
        tuple: questions_without_city: [string], possible_cities: [string]
    """

    if not (question and isinstance(question, str)):
        return ["", ""], ["", ""]

    question1 = ""
    question2 = ""
    city1 = ""
    city2 = ""

    if " à " in question:
        elements_of_question = question.split(" à ")
        question1 = elements_of_question[0].strip()
        city1 = elements_of_question[-1].strip()

    elif " a " in question:
        elements_of_question = question.split(" a ")
        question1 = elements_of_question[0].strip()
        city1 = elements_of_question[-1].strip()

    if " de " in question:
        elements_of_question = question.split(" de ")
        question2 = elements_of_question[0].strip()
        city2 = elements_of_question[-1].strip()

    elif " d'" in question:
        elements_of_question = question.split(" d'")
        question2 = elements_of_question[0].strip()
        city2 = elements_of_question[-1].strip()

    return [question1, question2], [city1, city2]


def extract_name_out_of_street(street, LOCATION_WORDS):
    if not (
            street
            and LOCATION_WORDS
            and isinstance(street, str)
            and isinstance(LOCATION_WORDS, list)):

        return ""
    try:
        for word in LOCATION_WORDS:
            street = street.replace(word, "").replace(word.title(), "")

    except Exception as e:
        logging.exception(str(e))
    return street.strip()

open = open

def write_file(OUTPUT_PATH: str, filename: str, content: str) -> bool:
    if not (
            filename
            and OUTPUT_PATH
            and content
            and isinstance(filename, str)
            and isinstance(OUTPUT_PATH, str)
            and isinstance(content, str)):
        return False

    try:
        file_path = os.path.join(OUTPUT_PATH, filename)
        file = open(file_path, "a", encoding="utf-8")
        file.write(content)
        file.close()
        logging.info("File created or updated")
        return True

    except Exception as e:
        logging.error(f"Unable to write {file_path}")
        logging.error(str(e))
        print(str(e))
        return False


def create_csv_file_if_not_exists():
    logging.info("In create_csv_file_if_not_exists()")
    if not (OUTPUT_PATH and isinstance(OUTPUT_PATH, str)):
        logging.error("Output directory (OUTPUT_PATH) must be string")
        return False

    if not os.path.isdir(OUTPUT_PATH):
        print("Output directory (OUTPUT_PATH) does not exist!")
        logging.error(f"Wrong directory: {OUTPUT_PATH}")
        return False

    if not isinstance(CSV_FILENAME, str) or not CSV_FILENAME:
        logging.error("utils.py => Issue with CSV_FILENAME!")
        return False

    file_path = os.path.join(OUTPUT_PATH, CSV_FILENAME)

    try:
        if not os.path.exists(file_path):
            logging.info("Creating file...")
            is_file_written = write_file(OUTPUT_PATH, CSV_FILENAME, CSV_COLUMN_NAMES)
            return is_file_written
        return True
    except Exception as e:
        logging.error("utils.py create_csv_file_if_not_exists => Issue with file_path!")
        return False


def check_csv_row(csv_row):
    line_break = "\n"
    if not (
            csv_row
            and isinstance(csv_row, str)
            and csv_row.startswith(line_break)):
            
        logging.error(
            "The row of the csv file must be a string "
            "starting with a line break!")
        return False
    if csv_row.count(",") == 5:
        return True
    logging.error("The row of the csv file is not valid!")
    return False

def add_to_csv(data: dict=None, question="") -> bool:
    csv_row = ",,,,,"
    if not isinstance(question, str):
        logging.error("The question to write on csv file must be a string")
        return False
    if data and question:
        if not isinstance(data, dict):
            logging.error("The data to write on csv file must be a dict")
            return False
        for key in ['country', 'region', 'city']:
            if key not in data:
                return False

        question = question.replace(",", ";")
        line_break = "\n"
        csv_row = line_break + (
            f"{str(datetime.now())[:10]},"
            f"{str(datetime.now())[11:16]},"
            f"{data['country']},"
            f"{data['region']},"
            f"{data['city']},"
            f"{question}")

        is_csv_row_valid = check_csv_row(csv_row)
        if not is_csv_row_valid:
            logging.error("ERROR: The row is not OK for the csv file!")
            return False

        is_csv_file_created = create_csv_file_if_not_exists()

        if not is_csv_file_created:
            logging.error("ERROR: The csv file is not OK!")
            return False
        return write_file(OUTPUT_PATH, CSV_FILENAME, csv_row)
    
    logging.info("Nothing to write to CSV file")
    return True
