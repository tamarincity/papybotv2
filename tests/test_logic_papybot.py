# flask_app/logic/papybot.py
# test of all  methods of class PapyBot except the << start >> method

import logging

from flask_app.logic import papybot


PapyBot = papybot.PapyBot

def test_check_response_validity_of_geoloc(monkeypatch):
    print("=> Check if the answer corresponds to the question")
    Sut = PapyBot  # class PapyBot

    words_to_remove = None  # No word to remove in this method
    question_is_none = None
    question_martinique_as_city_is_in_the_question = "clinique st paul de martinique"
    question_tortue_instead_of_paul = "clinique st tortue de martinique"
    location_title = "Clinique Saint-Paul, Fort de France"
    location_title_is_none = None
    location_title_is_not_string = {"message": "Not a string"}
    full_address = "Rue des Hibiscus<br/>97200, Fort-de-France<br/>Martinique"
    full_address_is_none = None
    city_martinique = "martinique"
    city_lyon = "lyon"
    city_none = None

    question_eiffel_tower = "eiffel tower"
    location_title_eiffel_tower = "Eiffel Tower (Tour Eiffel)"
    full_address_eiffel_tower = "5 Avenue Anatole France<br/>75007 Paris"

    def mock_remove_some_words_and_format_text(
            text_to_format, words_to_remove):
        if not(
                words_to_remove
                and words_to_remove == ["kjis552aCfd"]):
            logging.error(
                "The second arg is wrong in: remove_some_words_and_format_text()")
            logging.error('words_to_remove must be exactly this list: ["kjis552aCfd"]')
            raise Exception(
                    "Error in the args of method: check_response_validity_of_geoloc")
            
        if not(
                text_to_format
                and isinstance(text_to_format, str)):
            logging.error(
                "The first arg is wrong in: remove_some_words_and_format_text()")
            logging.error('text_to_format must be a non empty string')
            return ""

        if text_to_format == location_title:
            return "clinique saint paul fort de france"
        if text_to_format == full_address:
            return "rue des hibiscusbr97200 fort de francebrmartinique"
        if text_to_format == location_title_eiffel_tower:
            return "eiffel tower tour eiffel"
        if text_to_format == full_address_eiffel_tower:
            return "5 avenue anatole francebr75007 paris"
        return ""

    monkeypatch.setattr(
        papybot,
        "remove_some_words_and_format_text",
        mock_remove_some_words_and_format_text)

    assert Sut.check_response_validity_of_geoloc(
        question_is_none,
        location_title, full_address,
        city_martinique) == None

    assert Sut.check_response_validity_of_geoloc(
        question_martinique_as_city_is_in_the_question,
        location_title, full_address,
        city_martinique) == location_title

    assert Sut.check_response_validity_of_geoloc(
        question_martinique_as_city_is_in_the_question,
        location_title_is_none, full_address,
        city_martinique) == None

    assert Sut.check_response_validity_of_geoloc(
        question_martinique_as_city_is_in_the_question,
        location_title_is_none, full_address_is_none,
        city_martinique) == None

    assert Sut.check_response_validity_of_geoloc(
        question_martinique_as_city_is_in_the_question,
        location_title_is_none, full_address_is_none,
        city_martinique) == None

    assert Sut.check_response_validity_of_geoloc(
        question_martinique_as_city_is_in_the_question,
        location_title_is_not_string, full_address_is_none,
        city_martinique) == None

    assert Sut.check_response_validity_of_geoloc(
        question_tortue_instead_of_paul,
        location_title, full_address,
        city_martinique) == None

    # The city is in the question but not extracted by the system
    # (so not in the variable city) and not in the address returned by the
    # geoloc API.
    assert Sut.check_response_validity_of_geoloc(
        question_martinique_as_city_is_in_the_question,
        location_title,
        full_address,
        city_none) == None

    # If the value of city is not in the address from the geoloc API
    assert Sut.check_response_validity_of_geoloc(
        question_martinique_as_city_is_in_the_question,
        location_title,
        full_address,
        city_lyon) == None

    # Neither the city nor the country is in the question
    assert Sut.check_response_validity_of_geoloc(
        question_eiffel_tower,
        location_title_eiffel_tower,
        full_address_eiffel_tower,
        city_none) == location_title_eiffel_tower


def test_get_geolocation(monkeypatch):
    print("=> Get a part of Papybot's message, geolocation and full address "
        "of the requested location")
    Sut = PapyBot  # class PapyBot

    question = "cathedrale de fort de france"
    question_error1 = "error1 cathedrale de fort de france"
    question_error2 = "error2 cathedrale de fort de france"
    question_error3 = "error3 cathedrale de fort de france"
    city = "france"
    city_error3 = "miami"
    message_from_papy = "Blabla bla"

    value_everything_went_well = {
        'item': {
            'title': 'St. Louis Cathedral (Cathédrale Saint-Louis de Fort-de-France)',
            'vicinity': 'Rue Victor Schoelcher<br/>97200, Fort-de-France<br/>Martinique',
            'position': [14.60523, -61.06899], 'category': 'Sites et musées'},
        'location_title': 'St. Louis Cathedral (Cathédrale Saint-Louis de Fort-de-France)',
        'full_address': 'Rue Victor Schoelcher<br/>97200, Fort-de-France<br/>Martinique',
        'extracted_city': None,
        'street': 'Rue Victor Schoelcher',
        'name_out_of_street': 'Victor Schoelcher',
        'position_list': [14.60523, -61.06899],
        'latitude': 14.60523,
        'longitude': -61.06899,
        'message_from_papy': 'Blabla bla'}
    value_for_error_1_and_2 = {
        'item': None,
        'location_title': None,
        'full_address': None,
        'extracted_city': None,
        'street': None,
        'name_out_of_street': None,
        'position_list': None,
        'latitude': None,
        'longitude': None,
        'message_from_papy': 'Blabla blaJe ne sais pas où se trouve ce lieu '}
    value_for_error_3 = {
        'item': {
            'title': 'St. Louis Cathedral (Cathédrale Saint-Louis de Fort-de-France)',
            'vicinity': 'Rue Victor Schoelcher<br/>97200, Fort-de-France<br/>Martinique',
            'position': [14.60523, -61.06899],
            'category': 'Sites et musées'},
        'location_title': None,
        'full_address': 'Rue Victor Schoelcher<br/>97200, Fort-de-France<br/>Martinique',
        'extracted_city': None,
        'street': 'Rue Victor Schoelcher',
        'name_out_of_street': 'Victor Schoelcher',
        'position_list': [14.60523, -61.06899],
        'latitude': 14.60523,
        'longitude': -61.06899,
        'message_from_papy': 'Blabla bla'}


    def mock_request_to_geoloc_api(full_url):

        # location missing in request to geoloc API
        if "error1" in full_url:
            return {
                "status": 400,
                "message": "Required query parameter 'q' is not present",
                "incidentId": "3bdc3f30-dfe0-4faa-9c3f-30dfe01faa69"}
        # api_key not found in request to API
        elif "error2" in full_url:
            return {
                "error": "Unauthorized",
                "error_description": "No credentials found"}
        else:
            return {
                "results": [
                    {
                        "title": "St. Louis Cathedral (Cathédrale Saint-Louis de Fort-de-France)",
                        "vicinity": "Rue Victor Schoelcher<br/>97200, Fort-de-France<br/>Martinique",
                        "position": [
                            14.60523,
                            -61.06899
                        ],
                        "category": "Sites et musées"}]}

    def mock_check_response_validity_of_geoloc(
            question, location_title, full_address, city):
        if city == city_error3:
            return None
        return location_title        

    monkeypatch.setattr(
        papybot.GeolocApi,
        "request_to_geoloc_api",
        mock_request_to_geoloc_api)

    monkeypatch.setattr(
        PapyBot,
        "check_response_validity_of_geoloc",
        mock_check_response_validity_of_geoloc)

    assert Sut.get_geolocation(question, city, message_from_papy) == (
        value_everything_went_well)
    # The location to found is missing in the request to the geoloc API ("q=" is missing)
    assert Sut.get_geolocation(question_error1, city, message_from_papy) == value_for_error_1_and_2
    # api_key is missing in the request to the geoloc API ("apiKey=" is missing)
    assert Sut.get_geolocation(question_error2, city, message_from_papy) == value_for_error_1_and_2
    # The value of city is not in the address from the geoloc API
    assert Sut.get_geolocation(question_error3, city_error3, message_from_papy) == value_for_error_3


def test_get_translation(monkeypatch):
    print("=> Translate to from English to choosen language")
    Sut = PapyBot  # class PapyBot

    text_to_be_translated = "English sentence"
    language = "fr"
    value_french = "French translation"

    class MockGoogleTranslator:
        def __init__(self, source, target):
            pass
        @classmethod
        def translate(cls, text_to_be_translated):
            return value_french

    monkeypatch.setattr(
        papybot,
        "GoogleTranslator",
        MockGoogleTranslator
    )
    assert Sut.get_translation(text_to_be_translated, language) == value_french

# =======================================================================
food_n_drink = "Food & Drink"
food_n_drink_translated_in_french = 'Nourriture boisson'
food_n_drink_in_french_n_formated = 'Nourriture boisson à emporter'

interesting_points_list = [
    {'alternativeNames': [{'language': 'fr', 'name': 'Champ de Mars'}],
    'averageRating': 0.0,
    'category': {'href': 'https://places.sit.ls.hereapi.com/places/v1/...',
                'id': 'restaurant',
                'system': 'places',
                'title': 'Restaurant',
                'type': 'urn:nlp-types:category'},
    'distance': 396,
    'having': [],
    'href': 'https://places.sit.ls.hereapi.com/places/v1/places/...',
    'icon': ('https://download.vcdn.cit.data.here.com/p/d/places2_stg/'
                'icons/categories/03.icon'),
    'id': '250u09tu-4d278952393145b0966e2eda45e8fa07',
    'openingHours': {'isOpen': True,
                    'label': 'Opening hours',
                    'structured': [{'duration': 'PT24H00M',
                                    'recurrence': (
                                        'FREQ:DAILY;BYDAY:'
                                        'MO,TU,WE,TH,FR,SA,SU'),
                                    'start': 'T000000'}],
                    'text': 'Mon-Sun: 00:00 - 24:00'},
    'position': [48.85797, 2.2999],
    'tags': [{'group': 'cuisine', 'id': 'french', 'title': 'French'}],
    'title': 'Parc du Champ de Mars',
    'type': 'urn:nlp-types:place',
    'vicinity': '45 Avenue de la Bourdonnais<br/>75007 Paris'},
    {'alternativeNames': [{'language': 'fr',
                            'name': 'Boulangerie Legros Père et Fils'}],
    'averageRating': 0.0,
    'category': {'href': 'https://places.sit.ls.hereapi.com/places/v1/...',
                'id': 'food-drink',
                'system': 'places',
                'title': food_n_drink,
                'type': 'urn:nlp-types:category'},
    'distance': 370,
    'having': [],
    'href': 'https://places.sit.ls.hereapi.com/places/v1/places/...',
    'icon': ('https://download.vcdn.cit.data.here.com/p/d/places2_stg/'
                'icons/categories/09.icon'),
    'id': '250u09tu-d0de6649d292468aa50f44ef14b0dd64',
    'openingHours': {'isOpen': True,
                    'label': 'Opening hours',
                    'structured': [{'duration': 'PT13H00M',
                                    'recurrence': ('FREQ:DAILY;BYDAY:'
                                                        'MO,TU,WE,TH,FR,SA'),
                                    'start': 'T070000'}],
                    'text': 'Mon-Sat: 07:00 - 20:00'},
    'position': [48.85492, 2.29477],
    'tags': [{'group': 'cuisine', 'id': 'european', 'title': 'European'},
            {'group': 'cuisine', 'id': 'french', 'title': 'French'}],
    'title': 'Frederic Sicard',
    'type': 'urn:nlp-types:place',
    'vicinity': '34 Avenue de Suffren<br/>75015 Paris'},]

interesting_points_list_with_translated_categories = [
    {'alternativeNames': [{'language': 'fr', 'name': 'Champ de Mars'}],
    'averageRating': 0.0,
    'category': {'href': 'https://places.sit.ls.hereapi.com/places/v1/...',
                'id': 'restaurant',
                'system': 'places',
                'title': 'Restaurant',
                'type': 'urn:nlp-types:category'},
    'distance': 396,
    'having': [],
    'href': 'https://places.sit.ls.hereapi.com/places/v1/places/...',
    'icon': ('https://download.vcdn.cit.data.here.com/p/d/places2_stg/'
            'icons/categories/03.icon'),
    'id': '250u09tu-4d278952393145b0966e2eda45e8fa07',
    'openingHours': {
        'isOpen': True,
        'label': 'Opening hours',
        'structured': [
            {'duration': 'PT24H00M',
            'recurrence': 'FREQ:DAILY;BYDAY:MO,TU,WE,TH,FR,SA,SU',
            'start': 'T000000'}],
        'text': 'Mon-Sun: 00:00 - 24:00'},
    'position': [48.85797, 2.2999],
    'tags': [
        {'group': 'cuisine',
        'id': 'french',
        'title': 'French'}],
    'title': 'Parc du Champ de Mars',
    'type': 'urn:nlp-types:place',
    'vicinity': '45 Avenue de la Bourdonnais<br/>75007 Paris'
    },
    {'alternativeNames': [
        {'language': 'fr',
        'name': 'Boulangerie Legros Père et Fils'}],
    'averageRating': 0.0,
    'category': {'href': 'https://places.sit.ls.hereapi.com/places/v1/...',
                'id': 'food-drink',
                'system': 'places',
                'title': food_n_drink_in_french_n_formated,
                'type': 'urn:nlp-types:category'},
    'distance': 370,
    'having': [],
    'href': 'https://places.sit.ls.hereapi.com/places/v1/places/...',
    'icon': ('https://download.vcdn.cit.data.here.com/p/d/places2_stg/'
            'icons/categories/09.icon'),
    'id': '250u09tu-d0de6649d292468aa50f44ef14b0dd64',
    'openingHours': {
        'isOpen': True,
        'label': 'Opening hours',
        'structured': [
            {'duration': 'PT13H00M',
            'recurrence': 'FREQ:DAILY;BYDAY:MO,TU,WE,TH,FR,SA',
            'start': 'T070000'}],
        'text': 'Mon-Sat: 07:00 - 20:00'},
    'position': [48.85492, 2.29477],
    'tags': [
        {'group': 'cuisine',
        'id': 'european',
        'title': 'European'
        },
        {'group': 'cuisine',
        'id': 'french',
        'title': 'French'}],
    'title': 'Frederic Sicard',
    'type': 'urn:nlp-types:place',
    'vicinity': '34 Avenue de Suffren<br/>75015 Paris'}]

def test_translate_points_categories(monkeypatch):
    print("=> Translate category of locations in French")
    Sut = PapyBot  # class PapyBot

    language = "fr"
    

    def mock_get_translation(text_to_be_translated, language):
        return text_to_be_translated.replace(
            food_n_drink, food_n_drink_translated_in_french)

    monkeypatch.setattr(
        PapyBot,
        "get_translation",
        mock_get_translation
    )
    assert Sut.translate_points_categories(
        interesting_points_list, language) == interesting_points_list_with_translated_categories


def test_html_version_of_one_interesting_point():
    print("=> Return one interesting point in html language")
    Sut = PapyBot  # class PapyBot

    expected = [
        ('<strong>Parc du Champ de Mars</strong> '
        '<img src="https://download.vcdn.cit.data.here.com/p/d/'
        'places2_stg/icons/categories/03.icon" '
        'alt="icon for catégorie: Restaurant" '
        'title="catégorie: Restaurant"width="50" />'),
        ('<strong>Frederic Sicard</strong> '
        '<img src="https://download.vcdn.cit.data.here.com/p/d/'
        'places2_stg/icons/categories/09.icon" '
        'alt="icon for catégorie: Nourriture boisson à emporter" '
        'title="catégorie: Nourriture boisson à emporter"width="50" />')]

    assert Sut.html_version_of_one_interesting_point(interesting_points_list) == expected


def test_turn_interesting_points_into_html_version(monkeypatch):
    print("=> Return all interesting points into html language")
    Sut = PapyBot  # class PapyBot

    expected = (
        """<strong>Parc du Champ de Mars</strong> """
        """<img src="https://download.vcdn.cit.data.here.com/p/d/"""
        """places2_stg/icons/categories/03.icon" """
        """alt="icon for catégorie: Restaurant" """
        """title="catégorie: Restaurant"width="50" />, """
        """<strong>Frederic Sicard</strong> """
        """<img src="https://download.vcdn.cit.data.here.com/p/d/"""
        """places2_stg/icons/categories/09.icon" """
        """alt="icon for catégorie: Nourriture boisson à emporter" """
        """title="catégorie: Nourriture boisson à emporter"width="50" />""")

    assert Sut.turn_interesting_points_into_html_version(
        interesting_points_list) == expected


def test_get_info_from_wikipedia(monkeypatch):
    print("=> Get info from Wikipedia about the topic")
    Sut = PapyBot  # class PapyBot
    
    question = "openclassrooms"
    question_not_found_in_wikipedia = "No info in Wikipedia"
    items_from_wikipedia = [
        {
            "ns": 0,
            "title": "OpenClassrooms",
            "pageid": 4338589,
            "size": 13795,
            "wordcount": 1095,
            "snippet": "Short text about OpenClassrooms",
            "timestamp": "2021-11-21T01:36:21Z"
        },
        {
            "ns": 0,
            "title": "Massive Open Online Course",
            "pageid": 6436398,
            "size": 54841,
            "wordcount": 5697,
            "snippet": (
                "sur <span class=\"searchmatch\">openclassrooms</span>"
                ".com (consulté le 22 septembre 2015) « Google », sur "
                "<span class=\"searchmatch\">openclassrooms</span>.com "
                "(consulté le 22 septembre 2015) « IBM », sur "
                "<span class=\"searchmatch\">openclassrooms</span>.com"),
            "timestamp": "2022-01-06T16:07:00Z"
        }]

    response_from_get_item_info_from_wikipedia = (
        "<p class=\"mw-empty-elt\">\n</p>\n<p><b>"
        "OpenClassrooms</b> est un site web de formation en ligne,"
        " créé en 1999 sous le nom de <b>Site du Zéro</b>. "
        "blablabla...\n</p>")
    
    expected = (
        response_from_get_item_info_from_wikipedia
        + (
            "<a href='https://fr.wikipedia.org/wiki/OpenClassrooms' "
            "target='_blank'>En savoir plus sur Wikipedia</a>"))


    def mock_get_items_from_wikipedia(question):
        return items_from_wikipedia

    def mock_get_item_info_from_wikipedia(first_item_in_items_from_wikipedia):
        return response_from_get_item_info_from_wikipedia
    
    monkeypatch.setattr(
        papybot.Wikipedia,
        "get_items_from_wikipedia",
        mock_get_items_from_wikipedia)
    
    monkeypatch.setattr(
        papybot.Wikipedia,
        "get_item_info_from_wikipedia",
        mock_get_item_info_from_wikipedia)

    assert Sut.get_info_from_wikipedia(question) == expected
    assert Sut.get_info_from_wikipedia(question_not_found_in_wikipedia) == expected
