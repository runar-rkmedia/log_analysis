CREATE VIEW top_articles_in_log AS
SELECT articles.title,
       min(authors.name) AS name,
       count(*) AS views
FROM authors,
     articles,
     log
WHERE authors.id = articles.author
    AND log.path = concat('/article/', articles.slug)
GROUP BY articles.title
ORDER BY views DESC;


CREATE VIEW top_authors_in_log AS
SELECT authors.name,
       count(*) AS views
FROM authors,
     articles,
     log
WHERE authors.id = articles.author
    AND log.path = concat('/article/', articles.slug)
GROUP BY authors.name
ORDER BY views DESC;
