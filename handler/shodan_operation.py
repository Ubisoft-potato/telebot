import shodan
from loguru import logger
from config import settings


class ShodanOperation:
    def __init__(self):
        self.api = shodan.Shodan(settings["shodan_api_key"])
        api_info = self.api.info()
        logger.info(f"Scan credits left: {api_info.get('scan_credits', 0)} | "
                    f"Query credits left: {api_info.get('query_credits', 0)}")

    def search(self, query):
        try:
            results = self.api.search(query)
            return results
        except shodan.APIError as e:
            logger.error(f"search shodan query: {query}, error: {e}")

    def host(self, ip):
        host = self.api.host(ip)
        return host

    def banner(self, ip):
        banner = self.api.host(ip)
        return banner
