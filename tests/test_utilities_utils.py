# flask_app/utilities/utils.py
import os

import pytest
from flask_app.constants import (
    CSV_COLUMN_NAMES,
    OUTPUT_PATH,
    CSV_FILENAME,
    LOCATION_WORDS,
)
from flask_app.utilities import utils
from flask_app.utilities.utils import (
    add_to_csv,
    check_csv_row,
    create_csv_file_if_not_exists,
    extract_city_from_question,
    extract_question_from_text,
    extract_name_out_of_street,
    figure_out_city,
    remove_some_words_and_format_text,
    remove_accents,
    remove_punctuation,
    write_file,
)


def test_remove_accents():
    print("=> Remove all accents from question")
    text_to_format_is_int = 12345
    text_to_format_is_none = None
    text_to_format_is_dict = {"message": "Not string"}
    text_to_format_is_empty_str = ""
    text_to_format_has_accent = "éèàù-normal  çie ë"


    assert remove_accents(text_to_format_is_int) == ""
    assert remove_accents(text_to_format_is_none) == ""
    assert remove_accents(text_to_format_is_dict) == ""
    assert remove_accents(text_to_format_is_empty_str) == ""
    assert remove_accents(text_to_format_has_accent) == "eeau-normal  cie e"


def test_remove_punctuation():
    print("=> Remove punctuation from question")
    text_to_format_is_int = 12345
    text_to_format_is_none = None
    text_to_format_is_dict = {"message": "Not string"}
    text_to_format_is_empty_str = ""
    text_to_format_has_punctuation = "Salut, comment vas-tu ?...;!:"

    assert remove_punctuation(text_to_format_is_int) == ""
    assert remove_punctuation(text_to_format_is_none) == ""
    assert remove_punctuation(text_to_format_is_dict) == ""
    assert remove_punctuation(text_to_format_is_empty_str) == ""
    assert remove_punctuation(text_to_format_has_punctuation) == "Salut comment vastu "


def test_remove_some_words_and_format_text():
    print("=> Remove the provided words from the text and format the text")
    text_to_format_is_int = 12345
    text_to_format_is_none = None
    text_to_format_is_dict = {"message": "Not string"}
    text_to_format_is_empty_str = ""
    text_to_format_is_correct = (
        "Salût, comment vas-tu l'ami, "
        "à l'approche de la fin du monde? 5 espaces entre la>     <et là !")

    words_to_remove_is_int = 12345
    words_to_remove_is_None = None
    words_to_remove_is_str = "A simple string"
    words_to_remove_is_correct = ["de la fin", "du monde"]


    assert remove_some_words_and_format_text(
        text_to_format_is_int, words_to_remove_is_correct) == ""
    assert remove_some_words_and_format_text(
        text_to_format_is_none, words_to_remove_is_correct) == ""
    assert remove_some_words_and_format_text(
        text_to_format_is_dict, words_to_remove_is_correct) == ""
    assert remove_some_words_and_format_text(
        text_to_format_is_empty_str, words_to_remove_is_correct) == ""
    assert remove_some_words_and_format_text(
        text_to_format_is_correct, words_to_remove_is_int) == ""
    assert remove_some_words_and_format_text(
        text_to_format_is_correct, words_to_remove_is_None) == ""
    assert remove_some_words_and_format_text(
        text_to_format_is_correct, words_to_remove_is_str) == ""
    assert remove_some_words_and_format_text(
        text_to_format_is_correct, words_to_remove_is_correct) == (
        "salut comment vas tu l'ami à l'approche 5 espaces entre la et la")


def test_extract_question_from_text():
    print("=> Select from the question the location to find")
    text_to_format_is_int = 12345
    text_to_format_is_none = None
    text_to_format_is_dict = {"message": "Not string"}
    text_to_format_is_empty_str = ""
    text_to_format_is_a_word = "openclassrooms"
    text_to_format_is_correct = "quelle est l'adresse d'openclassrooms"
    STOP_WORDS_IS_INT = 12345
    STOP_WORDS_IS_NONE = None
    STOP_WORDS_IS_DICT = {"message": "Not list"}
    STOP_WORDS_IS_STRING = "string"
    STOP_WORDS_IS_CORRECT = ["l'adresse d'"]

    assert extract_question_from_text(text_to_format_is_int, STOP_WORDS_IS_CORRECT) == None
    assert extract_question_from_text(text_to_format_is_none, STOP_WORDS_IS_CORRECT) == None
    assert extract_question_from_text(text_to_format_is_dict, STOP_WORDS_IS_CORRECT) == None
    assert extract_question_from_text(text_to_format_is_empty_str, STOP_WORDS_IS_CORRECT) == None
    assert extract_question_from_text(text_to_format_is_a_word, STOP_WORDS_IS_CORRECT) == None
    assert extract_question_from_text(text_to_format_is_correct, STOP_WORDS_IS_INT) == None
    assert extract_question_from_text(text_to_format_is_correct, STOP_WORDS_IS_NONE) == None
    assert extract_question_from_text(text_to_format_is_correct, STOP_WORDS_IS_DICT) == None
    assert extract_question_from_text(text_to_format_is_correct, STOP_WORDS_IS_STRING) == None
    assert extract_question_from_text(text_to_format_is_correct, STOP_WORDS_IS_CORRECT) == "openclassrooms"


def test_extract_city_from_question():
    print("=> Select the city in the question thanks to specific words")
    question0 = 12345
    question1 = None
    question2 = {"message": "Not string"}
    question3 = ""
    question4 = "ou est le pont de la ville d'avignon"
    question5 = "ou est le pont d'avignon"
    assert extract_city_from_question(question0) == ("", None)
    assert extract_city_from_question(question1) == ("", None)
    assert extract_city_from_question(question2) == ("", None)
    assert extract_city_from_question(question3) == ("", None)
    assert extract_city_from_question(question4) == ("ou est le pont", "avignon")
    assert extract_city_from_question(question5) == ("ou est le pont d'avignon", None)


def test_figure_out_city():
    print('=> Try to determine the name of the city from the keyword "à", "a" and "de" ')
    question0 = 12345
    question1 = None
    question2 = {"message": "Not string"}
    question3 = ""
    question4 = "ou sont les ecluses a beziers"
    question5 = "ou est le musée de la peche de saint-pierre"
    question6 = "ou est le pont d'avignon"
    question7 = "ou se trouve le jardin des poetes"

    assert figure_out_city(question0) == (["", ""], ["", ""])
    assert figure_out_city(question1) == (["", ""], ["", ""])
    assert figure_out_city(question2) == (["", ""], ["", ""])
    assert figure_out_city(question3) == (["", ""], ["", ""])
    assert figure_out_city(question4) == (["ou sont les ecluses", ""], ["beziers", ""])
    assert figure_out_city(question5) == (["", "ou est le musée"], ["", "saint-pierre"])
    assert figure_out_city(question6) == (["", "ou est le pont"], ["", "avignon"])
    assert figure_out_city(question7) == (["", ""], ["", ""])


def test_extract_name_out_of_street():
    print("=> Get the name of the street. It still have useless numbers")
    street1 = "10 Avenue Robespierre"
    street2 = "24Bis allée de la belle vue"
    assert extract_name_out_of_street(street1, LOCATION_WORDS) == "10 Robespierre"
    assert extract_name_out_of_street(street2, LOCATION_WORDS) == "2 belle vue"


output_directory_not_exists = "directory does not exist "
output_directory_is_not_string = ["output directory is not  string"]
good_output_directory = OUTPUT_PATH
output_directory_is_empty = ""
filename_is_not_string = ["file is not string"]
filename_is_empty = ""
filepath_is_empty = ""
filepath_is_not_string = ["file path is not string"]
filepath_does_not_exist = "filepath does not exist"
filepath_exists = "file path exists"
good_filename = CSV_FILENAME
wrong_content1 = "date;heure;pays;région"
content_is_not_string = ["content is not string"]
content_is_string = "Content is string"
good_csv_row = "five,commas,in,this,good,row"
wrong_csv_row = "only four,commas,in,this,row"
unable_to_write = False
file_written = True
unable_to_close_file = False
file_closed = True
expected_false = False
expected_true = True
params = (
    (output_directory_not_exists, good_filename, content_is_string, file_written, file_closed, expected_false),
    (output_directory_is_not_string, good_filename, content_is_string, file_written, file_closed,expected_false),
    (good_output_directory, filename_is_not_string, content_is_string, file_written, file_closed, expected_false),
    (good_output_directory, filename_is_empty, content_is_string, file_written, file_closed, expected_false),
    (good_output_directory, good_filename, content_is_not_string, file_written, file_closed, expected_false),
    (good_output_directory, good_filename, content_is_string, unable_to_write, file_closed, expected_false),
    (good_output_directory, good_filename, content_is_string, file_written, unable_to_close_file, expected_false),
    (good_output_directory, good_filename, content_is_string, file_written, file_closed, expected_true),
)

@pytest.mark.parametrize("output_path, filename, content, is_file_written, is_file_closed, expected", [*params])
def test_write_file(monkeypatch, output_path, filename, content, is_file_written, is_file_closed, expected):
    print(" => Write file")
    
    if not (
            filename
            and output_path
            and content
            and isinstance(filename, str)
            and isinstance(output_path, str)
            and isinstance(content, str)):
        expected = False

    try:
        os.path.join(output_path, filename)
    except Exception as e:
        expected = False

    def mock_open(filepath, mode, encoding):
        if not output_path == OUTPUT_PATH:
            raise Exception(f"The output directory must be {OUTPUT_PATH}")
        if not filepath == os.path.join(OUTPUT_PATH, filename):
            raise Exception("Unauthorized path")
        if not (mode == "a" and encoding == "utf-8"):
            raise Exception("Mode must be 'a' and encoding must be 'utf-8'")
        return MockFileObject(filepath)

    class MockFileObject:
        def __init__(self, filepath):
            self.filepath = filepath

        def write(self, content):
            if not is_file_written:
                raise Exception()

        def close(self):
            if not is_file_closed:
                raise Exception()

    monkeypatch.setattr(utils, "open", mock_open)

    assert write_file(output_path, filename, content) == expected


params = (
    (filepath_is_empty, file_written, expected_false),
    (filepath_is_not_string, file_written, expected_false),
    (filepath_does_not_exist, unable_to_write, expected_false),
    (filepath_does_not_exist, file_written, expected_true),
    (filepath_exists, unable_to_write, expected_true),
    (filepath_exists, file_written, expected_true),
)

@pytest.mark.parametrize("filepath, is_file_written, expected", [*params])
def test_create_csv_file_if_not_exists(monkeypatch, filepath, is_file_written, expected):
    print(" => Create a CSV file if it doesn't exist")

    if not (OUTPUT_PATH and isinstance(OUTPUT_PATH, str)):
        expected = False

    if not os.path.isdir(OUTPUT_PATH):
        expected = False

    if not isinstance(CSV_FILENAME, str) or not CSV_FILENAME:
        expected = False

    if not isinstance(CSV_FILENAME, str) or not CSV_FILENAME:
        expected = False

    try:
        os.path.join(OUTPUT_PATH, CSV_FILENAME)
    except Exception as e:
        print(str(e))
        expected = False

    def mock_os_path_exists(file_path):
        file_path = filepath
        if not (file_path and isinstance(file_path, str)):
            raise Exception('Error: file_path must be string and not empty!')
        if file_path == filepath_exists:
            return True

    def mock_write_file(output_dir_path, filename, content):
        if (
                output_dir_path == OUTPUT_PATH
                and filename == good_filename
                and content == CSV_COLUMN_NAMES
                and is_file_written):
            return True
        return False

    monkeypatch.setattr("os.path.exists", mock_os_path_exists)
    monkeypatch.setattr(utils, "write_file", mock_write_file)

    assert create_csv_file_if_not_exists() == expected


params = (
    "",
    ["Row is not a string"],
    wrong_csv_row,
    "No, line, break, in, this, row",
    "\n" + good_csv_row,
)

@pytest.mark.parametrize("csv_row", [*params])
def test_check_csv_row(csv_row):
    line_break = "\n"
    if not (
            csv_row
            and isinstance(csv_row, str)
            and csv_row.startswith(line_break)):
        expected = False
    elif csv_row.count(",") == 5:
        expected =  True
    else:
        expected =  False

    print("Expected: ", expected)
    assert check_csv_row(csv_row) == expected

file_created_with_success = "File created with success"
unable_to_create_file = "unable to create file"
not_a_dict = "Not a dict"
good_dict = {
    "city": "Fort-deFrance",
    "region": "Martinique",
    "country": "France"}

wrong_dict = {    
    "city": "Montpellier",
    "region": "Occitanie"}

params = (
    (
        not_a_dict,
        "question with comma (,)",
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_false),
    (
        wrong_dict,
        "question with comma (,)",
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_false),
    (
        not_a_dict,
        "question with comma (,)",
        good_csv_row,
        unable_to_create_file,
        file_written,
        expected_false),
    (
        not_a_dict,
        "question with comma (,)",
        good_csv_row,
        file_created_with_success,
        unable_to_write,
        expected_false),
    (
        not_a_dict,
        "question without comma",
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_false),
    (
        good_dict,
        ["Question is not a string"],
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_false),
    (
        good_dict,
        "question with comma (,)",
        wrong_csv_row,
        file_created_with_success,
        file_written,
        expected_false),
    (
        not_a_dict,
        "question with comma (,)",
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_false),
    (
        None,
        "question with comma (,)",
        good_csv_row,
        unable_to_create_file,
        file_written,
        expected_true),
    (
        None,
        "question with comma (,)",
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_true),
    (
        None,
        "question with comma (,)",
        good_csv_row,
        file_created_with_success,
        unable_to_write,
        expected_true),
    (
        None,
        "question with comma (,)",
        good_csv_row,
        unable_to_create_file,
        unable_to_write,
        expected_true),
    (
        good_dict,
        None,
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_true),
    (
        good_dict,
        None,
        good_csv_row,
        unable_to_create_file,
        file_written,
        expected_true),
    (
        good_dict,
        None,
        good_csv_row,
        file_created_with_success,
        unable_to_write,
        expected_true),

    (
        good_dict,
        "question with comma (,)",
        good_csv_row,
        unable_to_create_file,
        file_written,
        expected_false),
    (
        good_dict,
        "question with comma (,)",
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_true),
    (
        good_dict,
        "question with comma (,)",
        good_csv_row,
        file_created_with_success,
        unable_to_write,
        expected_false),
    (
        good_dict,
        "question with comma (,)",
        good_csv_row,
        unable_to_create_file,
        unable_to_write,
        expected_false),
    (
        good_dict,
        "question without comma",
        good_csv_row,
        file_created_with_success,
        file_written,
        expected_true),
)

@pytest.mark.parametrize(
    "data, question, csv_row, file_creation, is_file_written, expected", [*params])
def test_add_to_csv(
    monkeypatch, data, question, csv_row, file_creation, is_file_written, expected):
    print(" => Add user's geolocalisation to csv file")

    if not isinstance(question, str):
        expected = False
    if data:
        if not isinstance(data, dict):
            expected = False
        for key in ['country', 'region', 'city']:
            if key not in data:
                expected = False

    if not csv_row.count(",") == 5:
            expected = False


    def mock_check_csv_row(csvrow):
        line_break = "\n"
        csvrow = line_break + csv_row
        if not (
                csvrow
                and isinstance(csv_row, str)
                and csvrow.startswith(line_break)):
            return False
        if csv_row.count(",") == 5:
            return True
        return False

    def mock_create_csv_file_if_not_exists():
        if file_creation == unable_to_create_file:
            return False
        return True


    def mock_write_file(output_dir_path, filename, content):
        line_break = "\n"
        end_of_csv_row = line_break + (
            f"{data['country']},"
            f"{data['region']},"
            f"{data['city']},"
            f"{question.replace(',', ';')}")


        if (
                output_dir_path == OUTPUT_PATH
                and filename == CSV_FILENAME
                and content.strip().endswith(end_of_csv_row.strip())
                and content.startswith(line_break)
                and is_file_written):
            
            return True
        return False

    monkeypatch.setattr(utils, "check_csv_row", mock_check_csv_row)
    monkeypatch.setattr(
        utils, "create_csv_file_if_not_exists", mock_create_csv_file_if_not_exists)
    monkeypatch.setattr(utils, "write_file", mock_write_file)

    print("Expected: ", expected)
    assert add_to_csv(data, question) == expected
