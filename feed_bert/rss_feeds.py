from operator import itemgetter

import numpy as np
import tqdm
import bs4
import feedparser
import seaborn as sns
import pandas as pd


medium_publications = [
    "the-artificial-impostor",
    "pytorch",
    "dair.ai",
    "towards-artificial-intelligence",
    "swlh",
    "@ODSC",
    "doctrine",
    "paperswithcode",
]


medium_url_template = "https://medium.com/feed/{}"
medium_url = medium_url_template.format(medium_publications[0])
medium_urls = [
    medium_url_template.format(publication) for publication in medium_publications
]


subreddits = [
    "MachineLearning",
    "deeplearning",
    "datascience",
    "cognitivelinguistics",
    "TopOfArxivSanity",
    "kaggle",
]

reddit_url_template = "https://www.reddit.com/r/{}/.rss"
reddit_url = reddit_url_template.format(subreddits[0])
reddit_urls = [reddit_url_template.format(subreddit) for subreddit in subreddits]


def get_article_text(article):
    article_html_content = article["content"][0]["value"]
    article_text = bs4.BeautifulSoup(article_html_content).text
    return article_text


def get_feed_article_texts(feed):
    return [
        get_article_text(article)
        for article in feed["entries"]
        if "content" in article.keys()
    ]


def get_feed_article_df(feed):
    feed_df = pd.DataFrame.from_records(feed["entries"])
    feed_df["text"] = feed_df["summary"].apply(lambda s: bs4.BeautifulSoup(s).text)
    return feed_df


def add_field(df, field_name, values):
    df[field_name] = values
    return df


paperswithcode_url = "https://us-east1-ml-feeds.cloudfunctions.net/pwc/latest"
hackernews_url = "https://news.ycombinator.com/rss"
rss_feed_urls = [paperswithcode_url, hackernews_url] + medium_urls + reddit_urls


from datetime import date


def to_date(x):
    if str(x)[0].isdigit():
        return str(x)[:10]
    else:
        return (
            str(x).split(" ")[1]
            + " "
            + str(x).split(" ")[2]
            + " "
            + str(x).split(" ")[3]
        )


def get_feed_df(feed_urls):
    feeds = [
        (feed_url, feedparser.parse(feed_url)) for feed_url in tqdm.tqdm(feed_urls)
    ]
    df = pd.concat(
        [
            add_field(get_feed_article_df(feed), "feed", feed_url)
            for (feed_url, feed) in feeds
            if len(feed["entries"]) > 0
        ]
    )

    df["date"] = df["updated"]
    df["date"] = df["date"].fillna(df["published"])
    df["date"] = df["date"].fillna(date.today())

    df["date"] = df["date"].apply(lambda x: to_date(x))
    col = df["date"].unique()

    # return col
    return df
