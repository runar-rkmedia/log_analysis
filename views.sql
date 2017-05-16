CREATE OR REPLACE VIEW top_articles_in_log AS
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


CREATE OR REPLACE VIEW top_authors_in_log AS
SELECT authors.name,
       count(*) AS views
FROM authors,
     articles,
     log
WHERE authors.id = articles.author
    AND log.path = concat('/article/', articles.slug)
GROUP BY authors.name
ORDER BY views DESC;


CREATE OR REPLACE FUNCTION days_of_errors(fraction numeric) RETURNS TABLE (date date, total bigint, status_ok bigint, status_not_ok bigint, error_fraction numeric) AS $body$
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
WHERE error_fraction >$1
ORDER BY error_fraction DESC;
$body$ LANGUAGE SQL;
