"""
Reprting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""

# import psycopg2
from psycopg2 import extras, connect

CONNECTION = "dbname=news"


def db_lookup(SQL, data):
    """Helper for SQL-lookups."""
    connection = connect(CONNECTION)
    cursor = connection.cursor(cursor_factory=extras.DictCursor)
    if not isinstance(data, tuple):
        data = (data,)
    cursor.execute(SQL, data)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def top_articles(articles_returned=3):
    """Return a list of the most popular articles by page-views."""
    SQL = """
        SELECT authors.name, articles.title,
               top_articles_in_log.num AS views
        FROM (select path, num from top_articles_in_log limit (%s)) top_articles_in_log
        INNER JOIN articles
        ON top_articles_in_log.path ='/article/' || articles.slug
        INNER JOIN authors
            ON articles.author = authors.id
        ORDER BY views DESC;"""
    return db_lookup(SQL, articles_returned)


def topAuthors(authors_returned=3):
    """Return a list of most popular authors by page-views."""
    SQL = """
        SELECT authors.name AS name,
               sum(top_articles_in_log.num) AS views
        FROM authors
        INNER JOIN articles
            ON articles.author = authors.id
        INNER JOIN top_articles_in_log
            ON top_articles_in_log.path ='/article/' || articles.slug
        GROUP BY name
        ORDER BY views DESC;"""
    return db_lookup(SQL, authors_returned)


def daysOfErrors(percentile=1):
    """Return a list of days where there were more than <percentile> errors."""
    pass

topArticles = top_articles()
topAuthors = topAuthors()
# print(topAuthors)
for author in topAuthors:
    print("{views} views from author '{name}'".format(**author))
for article in topArticles:
    # print(article)
    print("{views} views on article '{title}' by {name}".format(**article))
