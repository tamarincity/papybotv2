import os
import logging
import re
from random import choice
from typing import List

from deep_translator import GoogleTranslator  # pipenv install deep_translator

from env import (
    api_key,
    logging_level,
)

from ..constants import (
    CENTER_OF_FRANCE,
    FRENCH,
    LOCATION_WORDS,
    STOP_WORDS,
    WORDS_OF_COURTESY,
)

from ..utilities.utils import (
    add_to_csv,
    extract_city_from_question,
    extract_question_from_text,
    extract_name_out_of_street,
    figure_out_city,
    remove_some_words_and_format_text,
)

from ..external_apis.geoloc_api import GeolocApi
from ..external_apis.wikipedia import Wikipedia
from ..external_apis.ip_api import IpApi


# set logging level
logging.basicConfig(level=os.environ.get("LOGLEVEL", logging_level))


class PapyBot:
    @classmethod
    def check_response_validity_of_geoloc(
            cls, question, location_title, full_address, city):
        try:
            if not (
                    question
                    and isinstance(question, str)
            ):
                return None

            full_address_preformated = remove_some_words_and_format_text(
                full_address, ["kjis552aCfd"])

            formated_full_address = (
                full_address_preformated.replace("st ", "saint ")
                .replace("ste ", "sainte ")
                .replace("-", " "))

            location_title_preformated = remove_some_words_and_format_text(
                location_title, ["kjis552aCfd"])

            formated_location_title = (
                location_title_preformated.replace("st ", "saint ")
                .replace("ste ", "sainte ")
                .replace("-", " "))

            question = (
                question.replace("st ", "saint ")
                .replace("ste ", "sainte ")
                .replace("%20", " "))

            question = question.replace(f" de {city}", "").replace(f" à {city}", "")
            question = question.replace(city, "") if city else question
            question = question.strip()

            all_words_of_question: List = question.split(" ")
            for word in all_words_of_question:
                if word not in formated_location_title:
                    return None
            if city:
                if city in formated_full_address:
                    return location_title
                else:
                    return None
            else:
                return location_title
        except Exception as e:
            logging.error(str(e))
            return None

    @classmethod
    def get_geolocation(cls, question, city, message_from_papy):
        item: dict = None
        location_title: str = None
        full_address: str = None
        street: str = None
        city_extracted_from_full_address: str = None
        name_out_of_street: str = None
        position_list = None
        latitude: float = None
        longitude: float = None
        url_from_france = f"at={CENTER_OF_FRANCE}&"
        url_question = f"q={question}&" if question else ""
        url_city_out_of_question = f"qq=city={city}&" if city else ""
        url_api_key = f"apiKey={api_key}"

        full_url = (
            url_from_france
            + url_question
            + url_city_out_of_question
            + url_api_key)

        response = GeolocApi.request_to_geoloc_api(full_url)

        if response:
            is_location_found = False
            items = response.get("results")
            nbr_of_items_returned = len(items) if items else 0
            index_of_good_item = 0

            # If no item found
            if nbr_of_items_returned == 0:
                message_from_papy += "Je ne sais pas où se trouve ce lieu "

            # If at least one item has been found
            else:
                is_location_found = True
                for i, item in enumerate(items):
                    full_address: str = item.get("vicinity")
                    location_title: str = item.get("title")
                    location_title = cls.check_response_validity_of_geoloc(
                        question, location_title, full_address, city)

                    if location_title:
                        logging.debug(f"location_title: {location_title}")
                        index_of_good_item = i
                        break

            if is_location_found:
                # Details of the location that has been found
                item = items[index_of_good_item]
                position_list = item.get("position")
                latitude = position_list[0]
                longitude = position_list[1]
                full_address: str = item.get("vicinity")

                if "<br/>" in full_address:
                    city_extracted_from_full_address: str = (
                        full_address.split("<br/>")[1])

                    street: str = full_address.split("<br/>")[0]
                else:
                    city_extracted_from_full_address: str = full_address
                    street: str = question

                # Extracting the city from geoloc
                reg_to_extract_city = r"(\d*)([a-zA-Z\s]+)"
                match = re.match(reg_to_extract_city, city_extracted_from_full_address)
                city_extracted_from_full_address = (
                    match.group(2).strip() if match else None)

                reg_to_extract_street_without_the_nbr = r"(\d*)(.+)"
                match = re.match(reg_to_extract_street_without_the_nbr, street)
                street = match.group(2).strip() if match else None

                name_out_of_street = extract_name_out_of_street(street, LOCATION_WORDS)

        else:
            message_from_papy = """
            J'ai rencontré un problème. Ma mémoire est un peu défaillante.
            Merci de reformuler la question ou de me la reposer plus tard."""

        return {
            "item": item,
            "location_title": location_title,
            "full_address": full_address,
            "extracted_city": city_extracted_from_full_address,
            "street": street,
            "name_out_of_street": name_out_of_street,
            "position_list": position_list,
            "latitude": latitude,
            "longitude": longitude,
            "message_from_papy": message_from_papy}

    @classmethod
    def translate_points_categories(cls, interesting_points_list, language):
        for point in interesting_points_list:
            point["category"]["title"] = (
                cls.get_translation(point["category"]["title"], language.title())
                .replace("Les services aux entreprises", "Entreprises & Services")
                .replace("chimiste", "Pharmacie/Laboratoire")
                .replace("Chimiste", "Pharmacie/Laboratoire")
                .replace("Nourriture boisson", "Nourriture boisson à emporter"))

        return interesting_points_list

    @classmethod
    def get_translation(cls, text_to_be_translated, language):
        # translator= Translator(to_lang="French")
        # return translator.translate(text_to_be_translated)
        return GoogleTranslator(source="en", target=language).translate(
            text_to_be_translated)

    @classmethod
    def turn_interesting_points_into_html_version(cls, interesting_points_list):
        interesting_points_list = cls.html_version_of_one_interesting_point(
            interesting_points_list)

        return ", ".join([point for point in interesting_points_list])

    @classmethod
    def html_version_of_one_interesting_point(cls, interesting_points_list):
        return [
            f'<strong>{point["title"]}</strong> '
            f'<img src="{point["icon"]}" '
            f'alt="icon for catégorie: {point["category"]["title"]}" '
            f'title="catégorie: {point["category"]["title"]}"'
            f'width="50" />'
            for point in interesting_points_list]

    @classmethod
    def get_info_from_wikipedia(cls, question):
        items_from_wikipedia = Wikipedia.get_items_from_wikipedia(question)
        if items_from_wikipedia:
            return Wikipedia.get_item_info_from_wikipedia(items_from_wikipedia[0]) + (
                "<a href='https://fr.wikipedia.org/wiki/"
                f"{items_from_wikipedia[0].get('title')}' "
                "target='_blank'>En savoir plus sur Wikipedia</a>")
        return None

    @classmethod
    def very_first_words_of_papy(cls):
        return choice(
            [
                "En fait...<br />",
                "Pour tout de dire...<br />",
                "Si ma mémoire est bonne, (et elle l'est !)...<br />",
                "Je suis heureux de t'informer à ce sujet.<br />",
                "Aaah, je me sens utile !<br />",
                "J'aime ta question, mon petit chaton !<br />",
                "Puisque tu demandes, je vais répondre...<br />"])

    @classmethod
    def display_map(cls, api_key, latitude, longitude):
        return (
            """<end_of_bubble />Pour finir, voici la carte du lieu qui """
            """t'intéresse:<br /><img src="https://image.maps.ls.hereapi.com"""
            f"""/mia/1.6/mapview?apiKey={api_key}&"""
            f"""z=16.4&w=800&h=650&c={latitude},{longitude}" />""")

    @classmethod
    def start(cls, question: str, user_ip_address="") -> tuple:
        # ====================================================================
        # 1 Get question =====================================================
        # ====================================================================
        logging.debug(f"question from front: {question}")
        if not (
                question
                and isinstance(question, str)):

            logging.debug(f"No question or question is not a string!")
            message_from_papy = "Merci de reformuler la question."
            return message_from_papy, 400

        message_from_papy = ""

        if (user_ip_address and isinstance(user_ip_address, str)):
            user_origin = IpApi.get_origin_from_ip_address(user_ip_address)
            if user_origin.get('status') == "success":
                is_added_to_csv = add_to_csv(user_origin, question)
                if not is_added_to_csv:
                    logging.warning(
                        "Warning: user's data has not been added to CSV file")
            else:
                logging.warning(
                        "Warning: Unable to get user's origin (country, region, city)!")
                logging.warning(user_origin)

        text_to_format = question

        formated_text = remove_some_words_and_format_text(
            text_to_format, WORDS_OF_COURTESY)

        logging.debug(
            "formated_text = remove_some_words_and_format_text"
            "(text_to_format, WORDS_OF_COURTESY): "
            f"{formated_text}")

        question = extract_question_from_text(formated_text, STOP_WORDS)
        logging.debug(
            "question (extract_question_from_text(formated_text, STOP_WORDS)): "
            f"{question}")

        if not question:

            logging.debug(f"The question is not a real one!")
            message_from_papy = "Merci de reformuler la question."
            return message_from_papy, 400

        question, city = extract_city_from_question(question)
        logging.debug(
            "question, city = extract_city_from_question(question): "
            f"{question}, "
            f"{city}")

        if not city:
            # Try to figure out the name of the city from the question
            possible_questions, possible_cities = figure_out_city(question)
            logging.debug(
                "possible_questions, possible_cities = figure_out_city(question): "
                f"{possible_questions}, {possible_cities}")

            for i, city in enumerate(possible_cities):
                # Request to see if the city exists
                response_from_api: dict = None
                if city:
                    response_from_api = GeolocApi.check_if_city_exists(city)
                    logging.debug(
                        "response_from_api = GeolocApi.check_if_city_exists(city): "
                        f"{response_from_api}")

                if not response_from_api:
                    continue

                if len(response_from_api["Response"]["View"][0]["Result"]):
                    # question = possible_questions[i]
                    break

                return response_from_api, 400

        # ====================================================================
        # 2 Get geo-location =================================================
        # ====================================================================

        response_from_geoloc_function = cls.get_geolocation(
            question, city, message_from_papy)

        logging.debug(
            "response_from_geoloc_function = cls.get_geolocation"
            "(question, city, message_from_papy): "
            f"{response_from_geoloc_function}")

        try:
            location_title = response_from_geoloc_function["location_title"]
            full_address = response_from_geoloc_function["full_address"]
            location_title = cls.check_response_validity_of_geoloc(
                question, location_title, full_address, city)

            logging.debug(
                "location_title = cls.check_response_validity_of_geoloc"
                "(question, location_title, full_address, city): "
                f"{location_title}")

        except Exception as e:
            logging.debug(str(e))
            location_title = None

        if not location_title:
            message_from_papy = (
                """
            Malheureusement, je n'ai pas d'info à ce sujet.<br />
            M'as tu indiqué le nom de la ville ?<br />
            Par exemple: Où est la gare routière de Montpellier ?<br />
            Peut-être aussi qu'il faudrait que tu vérifies l'orthographe """
                """de ta question.<br />
            Si ce n'est rien de tout ça, tu découvres alors que je ne suis"""
                """ pas une encyclopédie.<br />
            Il y a internet pour ça ! 😅""")

            return message_from_papy, 200

        else:
            message_from_papy += response_from_geoloc_function.get("message_from_papy")
            message_from_papy += (
                f"""L'adresse de << {location_title} >> est:"""
                f""" {full_address}.<br />Les coordonnées sont: ("""
                f"""{response_from_geoloc_function["latitude"]}, """
                f"""{response_from_geoloc_function["longitude"]}).""")


        # ==========================================================================
        # 3 Get interesting points around ==========================================
        # ==========================================================================
        latitude = response_from_geoloc_function["latitude"]
        longitude = response_from_geoloc_function["longitude"]
        interesting_points_list = GeolocApi.get_interesting_points_around(
            latitude, longitude)

        logging.debug("")
        logging.debug(
            "interesting_points_list = GeolocApi.get_interesting_points_around"
            "(latitude, longitude): "
            f"{interesting_points_list}")

        interesting_points_str: str = None
        if interesting_points_list:
            interesting_points_list = cls.translate_points_categories(
                interesting_points_list, FRENCH)

            logging.debug("")
            logging.debug(
                "interesting_points_list = cls.translate_points_categories"
                f"(interesting_points_list, FRENCH): {interesting_points_list}")

            interesting_points_str = cls.turn_interesting_points_into_html_version(
                interesting_points_list)

            logging.debug("")
            logging.debug(
                "interesting_points_str = "
                "cls.turn_interesting_points_into_html_version"
                f"(interesting_points_list): {interesting_points_str}")

        # ==========================================================================
        # 4 Get info from wikipedia ================================================
        # ==========================================================================
        name_out_of_street = response_from_geoloc_function["name_out_of_street"]
        extracted_city = response_from_geoloc_function["extracted_city"]
        if extracted_city:
            street_n_city = (
                response_from_geoloc_function["street"] + " " + extracted_city)

        else:
            street_n_city = response_from_geoloc_function["street"]

        logging.debug("")
        logging.debug(f"question (arg of: get_info_from_wikipedia): {question}")

        wiki_of_initial_question = cls.get_info_from_wikipedia(question)
        logging.debug(
            "wiki_of_initial_question = cls.get_info_from_wikipedia(question): "
            f"{wiki_of_initial_question}")
        logging.debug("")
        logging.debug(
            "street_n_city (arg of: get_info_from_wikipedia): "
            f"{street_n_city}")

        wiki_about_the_street_that_has_been_found = (
            cls.get_info_from_wikipedia(street_n_city))
        logging.debug(
            "wiki_about_the_street_that_has_been_found = "
            "cls.get_info_from_wikipedia(street_n_city): "
            f"{wiki_about_the_street_that_has_been_found}")
        logging.debug("")
        logging.debug(
            "name_out_of_street (arg of: get_info_from_wikipedia): "
            f"{name_out_of_street}")

        wiki_about_the_name_extracted_out_of_the_street = cls.get_info_from_wikipedia(
            name_out_of_street)
        logging.debug(
            "wiki_about_the_name_extracted_out_of_the_street = "
            "cls.get_info_from_wikipedia(name_out_of_street): "
            f"{wiki_about_the_name_extracted_out_of_the_street}")

        # Inserting << wiki_of_initial_question >> in papy's response
        message_from_papy += (
            "<end_of_bubble />Pour ton information :<br/>" + wiki_of_initial_question)

        # Inserting << wiki_about_the_street_that_has_been_found >> in papy's response
        if (
            wiki_about_the_street_that_has_been_found
            and wiki_about_the_street_that_has_been_found not in
            wiki_of_initial_question):
            message_from_papy += (
                "<end_of_bubble />J'ai bien envie de te parler de ceci :<br/>"
                + wiki_about_the_street_that_has_been_found)

        # Inserting << wiki_about_the_name_extracted_out_of_the_street >> in papy's response
        if wiki_about_the_name_extracted_out_of_the_street not in [
                wiki_of_initial_question,
                wiki_about_the_street_that_has_been_found]:

            message_from_papy += (
                "<end_of_bubble />En bonus pour ta culture générale apprends "
                "ça:<br/><br/>"
                f"{wiki_about_the_name_extracted_out_of_the_street}")

        message_from_papy += (
            "<end_of_bubble />Je t'ai fait une petite liste des endroits qui "
            "pourraient t'intéresser autour de l'adresse que tu m'as demandé :"
            "<br/><br/>")

        message_from_papy += interesting_points_str
        message_from_papy += "<br/><br>Je sais, je parle beaucoup. 😁<br/><br/>"

        # ==============================================================
        # RESPONSE OF PAPY =============================================
        # ==============================================================

        sarting_message = cls.very_first_words_of_papy()

        message_from_papy += cls.display_map(
            api_key=api_key, latitude=latitude, longitude=longitude)

        message_from_papy = sarting_message + message_from_papy
        logging.debug("")
        logging.debug("")
        logging.debug(
            "expected_value = message_from_papy, 200: "
            f"({message_from_papy}, 200)")

        return message_from_papy, 200
