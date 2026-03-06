def validate_article(article):
    """
    Memastikan artikel memiliki data yang valid
    """

    title = article.get("title")
    content = article.get("content")

    if not title:
        return False

    if not content:
        return False

    return True

from datetime import datetime

def filter_by_date(articles, start_date=None, end_date=None):
    """
    Memfilter artikel berdasarkan rentang tanggal
    """

    if not start_date and not end_date:
        return articles

    filtered_articles = []

    for article in articles:
        try:
            article_date = datetime.strptime(article["date"], "%Y-%m-%d")

            if start_date and article_date < start_date:
                continue

            if end_date and article_date > end_date:
                continue

            filtered_articles.append(article)

        except:
            continue

    return filtered_articles