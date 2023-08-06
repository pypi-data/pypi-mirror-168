import requests
import xmltodict


class BaseBoardGameGeekClient:
    base_api_url = ""
    thing = ""
    key = ""
    root_key = ""

    def get_api_url(self) -> str:
        return "/".join([self.base_api_url])

    def get_url(self, *url_params) -> str:
        """
        Returns the url based on the url params
        """
        api_url = self.get_api_url()
        params = (api_url, *url_params)
        return "/".join([str(param) for param in params if param != ""])

    def handle_errors(self, response):
        if 200 <= response.status_code >= 400:
            raise Exception(f"Request failed with status code = {response.status_code}")

    def parse_xml(self, content) -> dict:
        data = xmltodict.parse(content, attr_prefix="", cdata_key="text")
        return data.get(self.root_key, {}).get(self.key)

    def search(self, value: str = "", exact: bool = False):
        url = self.get_url("search")
        params = {"search": value, "exact": 1 if exact else 0}
        response = requests.get(url, params=params)

        self.handle_errors(response)

        data = self.parse_xml(response.content)
        return data

    def retrieve(self, pk, params: dict = None):
        url = self.get_url(self.thing, pk)
        response = requests.get(url, params=params)
        self.handle_errors(response)

        data = self.parse_xml(response.content)
        return data


class BoardGameGeekAPIClient(BaseBoardGameGeekClient):
    base_api_url = "https://boardgamegeek.com/xmlapi"
