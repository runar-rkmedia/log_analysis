CREATE VIEW top_articles_in_log AS
SELECT path,
       count(*) AS num
FROM log,
     articles
WHERE path LIKE '/article/%' -- We only want path to articles

    AND status = '200 OK'
GROUP BY path
ORDER BY num DESC;
