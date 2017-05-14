"""
Reporting tool for newsdata-database.

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


def top_authors(authors_returned=3):
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
        ORDER BY views DESC
        LIMIT (%s)
        ;"""
    return db_lookup(SQL, authors_returned)


def days_of_errors(percentile=0.01):
    """Return a list of days where there were more than <percentile> errors."""
    SQL = """
    SELECT *
    FROM
        (SELECT TIME::date AS date,
                count(*) AS total,
                count(CASE
                          WHEN status = '200 OK' THEN 1
                          ELSE NULL
                      END) AS status_ok,
                count(*)-count(CASE
                                   WHEN status = '200 OK' THEN 1
                                   ELSE NULL
                               END) AS status_not_ok,
                1 - count(CASE
                              WHEN status = '200 OK' THEN 1
                              ELSE NULL
                          END)::numeric / count(*) AS error_fraction
         FROM log
         GROUP BY TIME::date) sub
    WHERE error_fraction > (%s)
    ORDER BY error_fraction DESC ;"""
    return db_lookup(SQL, percentile)

# print(daysOfErrors())
# errorDays = days_of_errors()
# for day in errorDays:
#     print("{}: {} entries, {} ok, {} errors, {:04.2f}%".format(day['date'], day['total'], day['status_ok'], day['status_not_ok'], day['error_fraction']*100))
# topArticles = top_articles()
# topAuthors = topAuthors()
# print(topAuthors)
# for author in topAuthors:
    # print("{views} views from author '{name}'".format(**author))
# for article in topArticles:
    # print(article)
    # print("{views} views on article '{title}' by {name}".format(**article))
