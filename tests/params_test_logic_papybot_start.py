rephrase_question = "Merci de reformuler la question."

questions = (
    None,
    "",
    ["Not a string"],
    "Tour Eiffel",
    "Où est le théatre de Béziers, s'il te plaît ?",
)


returns_from_function_remove_some_words_and_format_text = (
    None,
    None,
    None,
    None,
    "ou est le theatre de beziers",
)


returns_from_function_extract_question_from_text = (
    None,
    None,
    None,
    None,
    "theatre de beziers",
)


returns_from_function_extract_city_from_question = (
    (None, None),
    (None, None),
    (None, None),
    (None, None),
    ("theatre de beziers" ,  None),
)


returns_from_function_figure_out_city = (
    (["", ""], ["", ""]),
    (["", ""], ["", ""]),
    (["", ""], ["", ""]),
    (["", ""], ["", ""]),
    (['', 'theatre'] ,  ['', 'beziers']),
)


returns_from_function_check_if_city_exists = (
    None,
    None,
    None,
    None,
    ({'Response': {
        'View': [
            {'Result': [
                {
                'Location': {
                    'Address': {
                        'Label': 'Béziers, Occitanie, France',
                        'Country': 'FRA', 'State': 'Occitanie',
                        'County': 'Hérault',
                        'City': 'Béziers',
                        'PostalCode': '34500'}}}
            ]}]}}),
)


returns_from_function_get_geolocation = (
    None,
    None,
    None,
    None,
    ({'item': {
        'title': 'Theatre Municipal de Beziers',
        'highlightedTitle': '<b>Theatre</b> Municipal <b>de</b> <b>Beziers</b>',
        'vicinity': 'Place Jean Jaurès<br/>34500 Béziers',
        'highlightedVicinity': 'Place Jean Jaurès<br/>34500 Béziers',
        'position': [43.3418, 3.21703],
        'category': 'theatre-music-culture',
        'categoryTitle': 'Theatre, Music & Culture'},
    'location_title': 'Theatre Municipal de Beziers',
    'full_address': 'Place Jean Jaurès<br/>34500 Béziers',
    'extracted_city': 'B',
    'street': 'Place Jean Jaurès',
    'name_out_of_street': 'Jean Jaurès',
    'position_list': [43.3418, 3.21703],
    'latitude': 43.3418,
    'longitude': 3.21703,
    'message_from_papy': ''}),
)


returns_from_function_check_response_validity_of_geoloc = (
    None,
    None,
    None,
    None,
    "Theatre Municipal de Beziers",
)


returns_from_function_get_interesting_points_around = (
    None,
    None,
    None,
    None,
    ([
        {'position': [43.3418, 3.21703],
        'distance': 0,
        'title': 'Theatre Municipal de Beziers',
        'averageRating': 0.0,
        'category': {'title': 'Theatre, Music & Culture'},
        'icon': 'https://.../icons/categories/05.icon',
        'vicinity': 'Place Jean Jaurès<br/>34500 Béziers'},
        {'position': [43.34202, 3.21669],
        'distance': 37,
        'title': 'Cafe de la Bourse',
        'averageRating': 0.0,
        'category': {'title': 'Restaurant'},
        'icon': 'https://.../icons/categories/03.icon',
        'vicinity': '32 Place Jean Jaurès<br/>34500 Béziers'}
    ]),
)


returns_from_function_translate_points_categories = (
        None,
        None,
        None,
        None,
    ([
        {'position': [43.3418, 3.21703],
        'title': 'Theatre Municipal de Beziers',
        'category': {
            'title': 'Théâtre, musique et culture'},
        'icon': 'https://.../icons/categories/05.icon',
        'vicinity': 'Place Jean Jaurès<br/>34500 Béziers'},
        {'position': [43.34202, 3.21669],
        'title': 'Cafe de la Bourse',
        'category': {
            'title': 'Le restaurant'},
        'icon': 'https://.../icons/categories/03.icon',
        'vicinity': '32 Place Jean Jaurès<br/>34500 Béziers'}
    ])
)


returns_from_function_turn_interesting_points_into_html_version = (
        None,
        None,
        None,
        None,
    ("""<strong>Theatre Municipal de Beziers</strong> """
    """<img src="https://.../icons/categories/05.icon" """
    """alt="icon for catégorie: Théâtre, musique et culture" """
    """title="catégorie: Théâtre, musique et culture"width="50" />, """
    """<strong>Cafe de la Bourse</strong> """
    """<img src="https://.../icons/categories/03.icon" """
    """alt="icon for catégorie: Le restaurant" """
    """title="catégorie: Le restaurant"width="50" />"""),
)


returns_from_function_get_info_from_wikipedia = (
        None,
        None,
        None,
        None,
    ([
        "<p><b>Béziers</b> est une commune française située dans ...</p>",
        "<p><b>Jean-Jaurès</b> est une station de correspondance ...</p>",
        "<p><b>Jean Jaurès</b>, né le 3 septembre 1859 à Castres ...</p>"
    ]),
)

ip_addresses = (
    "142.12.35.14",
    "142.12.35.14",
    "142.12.35.14",
    "142.12.35.14",
    "142.12.35.14",
)


expected_values = (
        ('Merci de reformuler la question.', 400),
        ('Merci de reformuler la question.', 400),
        ('Merci de reformuler la question.', 400),
        ('Merci de reformuler la question.', 400),
    (("Pour tout de dire...<br />L'adresse de "
    "<< Theatre Municipal de Beziers >> est: "
    "Place Jean Jaurès<br/>34500 Béziers.<br />"
    "Les coordonnées sont: (43.3418, 3.21703)."        
    "<end_of_bubble />Pour ton information :<br/>"
    "<p><b>Béziers</b> est une commune française située dans ...</p>"
    "<end_of_bubble />J'ai bien envie de te parler de ceci :<br/>"
    "<p><b>Jean-Jaurès</b> est une station de correspondance ...</p>"
    "<end_of_bubble />En bonus pour ta culture générale apprends ça:<br/><br/>"
    "<p><b>Jean Jaurès</b>, né le 3 septembre 1859 à Castres ...</p>"
    "<end_of_bubble />Je t'ai fait une petite liste des endroits qui pourraient"
    " t'intéresser autour de l'adresse que tu m'as demandé :<br/><br/>"
    """<strong>Theatre Municipal de Beziers</strong> """
    """<img src="https://.../icons/categories/05.icon" """
    """alt="icon for catégorie: Théâtre, musique et culture" """
    """title="catégorie: Théâtre, musique et culture"width="50" />, """
    """<strong>Cafe de la Bourse</strong> """
    """<img src="https://.../icons/categories/03.icon" """
    """alt="icon for catégorie: Le restaurant" """
    """title="catégorie: Le restaurant"width="50" />"""
    """<br/><br>Je sais, je parle beaucoup. 😁<br/><br/>"""
    """<end_of_bubble />Pour finir, voici la carte ...<br />"""
    """<img src="https://image.maps.ls.hereapi.com/mia/1.6/mapview"""
    """?apiKey=xxx&z=17&w=1000&h=700&c=43.3418,3.21703" />""") ,  200 ),
)


try:
    params = [  # This is a list comprehension
        [
            questions[i],
            returns_from_function_remove_some_words_and_format_text[i],
            returns_from_function_extract_question_from_text[i],
            returns_from_function_extract_city_from_question[i],
            returns_from_function_figure_out_city[i],
            returns_from_function_check_if_city_exists[i],
            returns_from_function_get_geolocation[i],
            returns_from_function_check_response_validity_of_geoloc[i],
            returns_from_function_get_interesting_points_around[i],
            returns_from_function_translate_points_categories[i],
            returns_from_function_turn_interesting_points_into_html_version[i],
            returns_from_function_get_info_from_wikipedia[i],
            ip_addresses[i],
            expected_values[i]
        ] for i in range(len(questions))]
except Exception as e:
    print("Error creating params")
