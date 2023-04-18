import requests

from bs4 import BeautifulSoup
from abc import *

class Crawler(ABC):

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()




