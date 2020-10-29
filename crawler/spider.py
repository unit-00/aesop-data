"""Spider class to be extended"""


class Spider:  # pylint: disable=too-few-public-methods
    """Abstract Spider class for crawling"""
    def __init__(self):
        self.base_url = None

    def crawl(self):  # pylint: disable=unused-argument, no-self-use
        """Crawl method for spider"""
        return

    def _parse(self):  # pylint: disable=unused-argument, no-self-use
        """Parse method for spider"""
        return
