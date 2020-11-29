
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

NYPOST_URL='https://nypost.com'

NEWS_TYPE = [
    "all",
    "general",
    "sports",
    "metro",
    "entertainment",
    "business",
    "opinion",
    "fashion",
    "shopping",
    "living",
    "real-estate",
    "tech",
    "media"
]


def get_NYPost_headlines(news_type = "all"):
    """
    :param news_type: New Type, must be one item in NEWS_TYPE
    :return: A list of string contains all headlines
    """
    if type(news_type) != str:
        raise TypeError("news_type must be a string, while {} found.".format(type(news_type)))

    if news_type not in NEWS_TYPE:
        raise ValueError("Unknown news type {}".format(news_type))

    ihtml = urlopen(NYPOST_URL)
    isoup = BeautifulSoup(ihtml, "html.parser")

    headlines = []
    target_news_type = []

    if news_type != "all":
        target_news_type.append(news_type)
    else:
        target_news_type.extend(NEWS_TYPE[1:])

    [headlines.extend(get_NYPost_special_news(isoup, t)) for t in target_news_type]

    return headlines

def clean_headline(headline):
    return re.sub("\t|\r|\n", "", headline)

def get_NYPost_general_news(isoup):
    a = isoup.find("div", {"id": "news-top-stories"})
    a1 = a.find("div", {"class": "featured-stories"})
    a2 = a1.findAll("article")
    news = []
    for i in a2:
        # print(i.find("h3").text)
        news.append(clean_headline(i.find("h3").text))

    a3 = a.find("div", {"class": "home-page-section-stories-wrapper"})
    a4 = a3.findAll("article")
    for i in a4:
        news.append(clean_headline(i.find("h3").text))

    return news


def get_NYPost_special_news(isoup, type):

    if type == "general":
        return get_NYPost_general_news(isoup)

    news = []
    b = isoup.find("div", {"id": "{}-top-stories".format(type)})
    b1 = b.findAll("article")
    for i in b1:
        news.append(clean_headline(i.find("h3").text))
    return news


if __name__ == '__main__':

    for nt in NEWS_TYPE:
        print("\n===================================\n")
        print("Scrape NYPost Type : {} \n".format(nt))
        print("\n".join(get_NYPost_headlines(nt)))
