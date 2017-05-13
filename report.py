"""
Reprting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""

import psycopg2
from psycopg2 import extras

CONNECTION = "dbname=news"


def top_articles(articles_returned=3):
    """Return a list of the most popular articles."""
    connection = psycopg2.connect(CONNECTION)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                   SELECT articles.*,
                          num AS VIEWS
                   FROM
                       (SELECT * from top_articles_in_log limit (%s)) sub,
                        articles
                   WHERE path = '/article/' || slug ;
                                   """, (articles_returned, ))
    articles = cursor.fetchall()

    cursor.close()
    connection.close()
    return articles

topArticles = top_articles()
# print(topArticles)
for article in topArticles:
    print(article)
