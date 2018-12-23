#!/usr/bin/env python3

from urllib.parse import parse_qs
import psycopg2
DBNAME = "news"


def get_authors():
    """Return all posts from the 'database'. Most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select authors.name, sum(views) from popular_articles\
    right join authors on author=authors.id group by authors.name,\
    author order by sum desc;")
    return c.fetchall()
    db.close()


def get_articles():
    """Return all posts from the 'database'. Most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select concat('\"', a.title, '\" ', '--',\
    count(substring(l.path, 10)), ' views') as most_popular_articles\
    from log l right join articles a on a.slug=substring(l.path, 10)\
    group by a.title order by count(substring(l.path, 10)) desc limit 3;")
    '''c.execute("SELECT author, title FROM articles")'''
    return c.fetchall()
    db.close()


def get_mostError():
    """Return all posts from the 'database'. Most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select concat(to_char(time::date, 'FMMonth DD, YYYY'),\
    ' --', round(avg( (status <> '200 OK')::int )*100, 1), '% errors')\
    as Most_Errors from log l group by time::date\
    order by avg( (status <> '200 OK')::int )*100 desc limit 1;")
    return c.fetchall()
    db.close()


print('\nMost Popular Articles\n---------------------')
for title in get_articles():
    output = title
    print('%s' % output)

print('\nMost Popular Authors\n---------------------')
for name, views in get_authors():
    output = "".join('"' + name + '" --' + str(views) + ' views')
    print('%s' % output)

print('\nMore than 1% error on any day\n---------------------')
for time in get_mostError():
    output = time
    print('%s' % output)
