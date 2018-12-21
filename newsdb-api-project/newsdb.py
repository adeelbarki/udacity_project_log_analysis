#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import psycopg2
DBNAME = "news"


HTML_WRAP = '''
<!DOCTYPE html>
<title>News Room</title>
<html>
<body>
<form method="get">
    
    <label>Search:
    <select name="item">
      <option selected value="article">Most Popular Three Articles</option>
      <option value="author">Most Popular Authors</option>
      <option value="mostError">Most Error Day</option>
    </select>
  </label>
  <button type="submit">Search</button>
</form>
<br>

        </body>
    </html>
'''
POST = '''\
    <div class="post"><em class="date"><h3>%s </h3>| </em> %s | </div>
    <p>-------------------------------------------</p>
'''

def get_authors():
    """Return all posts from the 'database'. Most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select authors.name, sum(views) from popular_articles right join authors on author=authors.id group by authors.name, author order by sum desc;")
    return c.fetchall()
    db.close()

def get_articles():
    """Return all posts from the 'database'. Most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select concat('\"', a.title, '\" ', '--', count(substring(l.path, 10)), ' views') as most_popular_articles from log l right join articles a on a.slug=substring(l.path, 10) group by a.title order by count(substring(l.path, 10)) desc limit 3;")
    '''c.execute("SELECT author, title FROM articles")'''
    return c.fetchall()
    db.close()

def get_mostError():
    """Return all posts from the 'database'. Most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select concat(to_char(time::date, 'FMMonth DD, YYYY'), ' --', round(avg( (status <> '200 OK')::int )*100, 1), '% errors') as Most_Errors from log l group by time::date order by avg( (status <> '200 OK')::int )*100 desc limit 1;")
    return c.fetchall()
    db.close()


class NewsHandler(BaseHTTPRequestHandler):
   

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        data = self.path[1:]
        
        self.wfile.write(HTML_WRAP.encode())

    
        if (data == "?item=author"):
            '''posts = "".join(POST % (name, bio) for name, bio in get_authors())'''
            posts = ''
            self.wfile.write("<h1>Most Popular Authors: </h1>".encode()) 
            print ('\nMost Popular Authors\n---------------------')
            posts = "".join(POST % (name, views) for name, views in get_authors())
            for name, views in get_authors():
                output = "".join('"' + name + '" --' + str(views))
                print ('%s' %output)
            print('\n')
            self.wfile.write(posts.encode())

        if (data == "?item=article"):
            '''posts = "".join(POST % title for title in get_articles())'''
            posts = ""
            self.wfile.write("<h1>Most Popular Articles: </h1>".encode())
            print ('\nMost popular Articles')
            print ('---------------------')
            
            for title in get_articles():
                output = title
                print ('%s' %output)
                posts += '%s' %output
                posts += "<br>"
            
            print('\n')
            self.wfile.write(posts.encode())
            
            '''self.wfile.write("<h1>Most Popular Articles: </h1>".encode())
            self.wfile.write(posts.encode())'''

        if (data == "?item=mostError"):
            posts = ""
            self.wfile.write("<h1>Days when more than '1%' of requests lead to errors: </h1>".encode())
            print ('\nMost Error')
            print ('---------------------')
            self.wfile.write(posts.encode()) 

            for time in get_mostError():
                output = time
                print ('%s' %output)
                posts += '%s' %output
                posts += "<br>"
            
            print('\n')
            self.wfile.write(posts.encode())
               

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, NewsHandler)
    httpd.serve_forever()
    