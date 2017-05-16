"""
Reporting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""
# !/usr/bin/python
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
        SELECT *
        FROM top_articles_in_log
        LIMIT (%s);
        """
    return db_lookup(SQL, articles_returned)


def top_authors(authors_returned=3):
    """Return a list of most popular authors by page-views."""
    SQL = """
        SELECT *
        FROM top_authors_in_log
        LIMIT (%s);
    """
    return db_lookup(SQL, authors_returned)


def days_of_errors(percentile=0.01):
    """Return a list of days where there were more than <percentile> errors."""
    SQL = """
        SELECT *
        FROM days_of_errors((%s));"""
    return db_lookup(SQL, percentile)
