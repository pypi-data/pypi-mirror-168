from boardgg.v1.client import BoardGameGeekAPIClient


class BoardGame(BoardGameGeekAPIClient):
    thing = "boardgame"
    key = "boardgame"
    root_key = "boardgames"


class Collection(BoardGameGeekAPIClient):
    thing = "collection"
    key = "item"
    root_key = "items"

    def get_owned(self, username: str) -> list:
        return self.retrieve(username, {'own': 1})
