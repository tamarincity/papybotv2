# flask_app/external_apis/wikipedia.py
# test of all  methods of class Wikipedia

from flask_app.external_apis.wikipedia import Wikipedia


def test_get_items_from_wikipedia(monkeypatch):
    print("=> Get all Wikipedia excerpts of articles related to the requested topic")
    Sut = Wikipedia  # class Wikipedia

    question = "openclassrooms"
    question_with_no_answer_on_wikipedia = "kf832epos"
    response_from_request_items_found = {
        "query": {
            "searchinfo": {
                "totalhits": 40
            },
            "search": [
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
                }]}}

    response_from_request_no_item_found = {
            "query": {
                "searchinfo": {
                    "totalhits": 0
                },
                "search": []}}

    expected_value = [
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

    class MockRequestsGET:
        def __init__(self, url):
            self.url = url

        def json(self):
            if self.url.endswith(question_with_no_answer_on_wikipedia):
                return response_from_request_no_item_found
            return response_from_request_items_found

    def mock_request_get(url):
        return MockRequestsGET(url)

    monkeypatch.setattr("requests.get", mock_request_get)

    assert Sut.get_items_from_wikipedia(question) == expected_value
    # If no item is found on Wikipedia
    assert Sut.get_items_from_wikipedia(
        question_with_no_answer_on_wikipedia) == []


def test_get_item_info_from_wikipedia(monkeypatch):
    print("=> Get info from Wikipedia about the requested topic")
    Sut = Wikipedia  # class Wikipedia

    # item1: The keys "title" and "pageid" are in this dictionary
    item1 = {
        "ns": 0,
        "title": "OpenClassrooms",
        "pageid": 4338589,
        "size": 13795,
        "wordcount": 1095,
        "snippet": "Short text about OpenClassrooms",
        "timestamp": "2021-11-21T01:36:21Z"}

    # item2: The "title" key is missing from this dictionary
    item2 = {
        "message": 'The "title" key is missing from this dictionary'}

    response_from_request_json = {
        "query": {
            "pages": {
                "4338589": {
                    "pageid": 4338589,
                    "ns": 0,
                    "title": "OpenClassrooms",
                    "extract": ("<p class=\"mw-empty-elt\">\n</p>\n<p><b>"
                    "OpenClassrooms</b> est un site web de formation en ligne,"
                    " créé en 1999 sous le nom de <b>Site du Zéro</b>. "
                    "blablabla...\n</p>")}}}}

    expected_value = (
        "<p class=\"mw-empty-elt\">\n</p>\n<p><b>"
        "OpenClassrooms</b> est un site web de formation en ligne,"
        " créé en 1999 sous le nom de <b>Site du Zéro</b>. "
        "blablabla...\n</p>")

    class MockRequestsGet:
        def __init__(self, url) -> None:
            pass
    
        def json(self):
            return response_from_request_json

    monkeypatch.setattr("requests.get", MockRequestsGet)
    assert Sut.get_item_info_from_wikipedia(item1) == expected_value
    assert Sut.get_item_info_from_wikipedia(item2) == None