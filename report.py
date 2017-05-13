"""
Reprting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""

# import psycopg2
from psycopg2 import extras, connect

CONNECTION = "dbname=news"


def top_articles(articles_returned=3):
    """Return a list of the most popular articles by page-views."""
    connection = connect(CONNECTION)
    cursor = connection.cursor(cursor_factory=extras.DictCursor)
    cursor.execute("""
                    SELECT *
                    FROM
                        (SELECT articles.*,
                                num AS views
                         FROM
                             (SELECT *
                              FROM top_articles_in_log LIMIT (%s)) subsub,
                              articles
                         WHERE path = '/article/' || slug ) sub,
                         authors
                    WHERE authors.id=author
                    ORDER BY views DESC;
                                   """, (articles_returned, ))
    articles = cursor.fetchall()

    cursor.close()
    connection.close()
    return articles


def topAuthors(authors_returned=3):
    """Return a list of most popular authors by page-views."""
    pass


def daysOfErrors(percentile=1):
    """Return a list of days where there were more than <percentile> errors."""
    pass

topArticles = top_articles()
# print(topArticles)
for article in topArticles:
    print("{views} views on article '{title}' by {name}".format(**article))
