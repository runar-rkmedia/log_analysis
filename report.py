"""
Reprting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""

# import psycopg2
from psycopg2 import extras, connect

CONNECTION = "dbname=news"


def top_articles(articles_returned=3):
    """Return a list of the most popular articles."""
    connection = connect(CONNECTION)
    cursor = connection.cursor(cursor_factory=extras.DictCursor)
    cursor.execute("""
                   SELECT articles.*,
                          num AS views
                   FROM
                       (SELECT *
                        FROM top_articles_in_log LIMIT (%s)) sub,
                        articles
                   WHERE path = '/article/' || slug
                   ORDER BY views DESC;
                                   """, (articles_returned, ))
    articles = cursor.fetchall()

    cursor.close()
    connection.close()
    return articles

topArticles = top_articles()
# print(topArticles)
for article in topArticles:
    print("{views} views on article '{title}' by {author}".format(**article))
