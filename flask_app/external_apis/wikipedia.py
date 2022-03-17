import requests

from ..constants import (
    URL_SUGGESTED_ITEMS_FROM_WIKIPEDIA,
    URL_ITEM_INFO_FROM_WIKIPEDIA,
)


class Wikipedia:
    @classmethod
    def get_items_from_wikipedia(cls, question):
        items_from_wikipedia = requests.get(
            URL_SUGGESTED_ITEMS_FROM_WIKIPEDIA + question
        )
        items_from_wikipedia = items_from_wikipedia.json()
        return items_from_wikipedia["query"]["search"]

    @classmethod
    def get_item_info_from_wikipedia(cls, item: dict):
        title_of_wikipedia_page = item.get("title")
        page_id = item.get("pageid")
        if title_of_wikipedia_page:
            item_info_from_wikipedia = requests.get(
                URL_ITEM_INFO_FROM_WIKIPEDIA + title_of_wikipedia_page
            ).json()
            return (
                item_info_from_wikipedia["query"]
                ["pages"]
                [str(page_id)]
                ["extract"])
        return None
