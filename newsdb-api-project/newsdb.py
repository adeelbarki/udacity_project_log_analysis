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
    c.execute("SELECT name, bio FROM authors")
    return c.fetchall()
    db.close()

def get_articles():
    """Return all posts from the 'database'. Most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT author, title FROM articles")
    return c.fetchall()
    db.close()

def get_mostError():
    """Return all posts from the 'database'. Most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select time, status from log where time<'2016-07-01 12:00:33+05'")
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
            posts = "".join(POST % (name, bio) for name, bio in get_authors())
            self.wfile.write("<h1>Most Popular Authors: </h1>".encode())
            self.wfile.write(posts.encode()) 

        if (data == "?item=article"):
            posts = "".join(POST % (author, title) for author, title in get_articles())
            self.wfile.write("<h1>Most Popular Articles: </h1>".encode())
            self.wfile.write(posts.encode())   

        if (data == "?item=mostError"):
            posts = "".join(POST % (time, status) for time, status in get_mostError())
            self.wfile.write("<h1>Days when more than '1%' of requests lead to errors: </h1>".encode())
            self.wfile.write(posts.encode()) 
               

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, NewsHandler)
    httpd.serve_forever()
    