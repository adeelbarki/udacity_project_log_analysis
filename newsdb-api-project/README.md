# Project: Logs Analysis

## Description

This project is designed for Udacity Full Stack Web Developer Nanodegree Program. Purpose of this project is to connect SQL database using python. The project is a reporting tool that contains three successful tasks handled in PostgreSQL and then printed out on terminal and browser at the same time. 

Three main tasks that are carried out in this project are
* What are the most popular three articles of all time?
* Who are the most popular authors of all time?
* On which days did more than 1% of requests lead to errors?

## Resources

The project contains three files _newsdb.py_, _output.txt_ and _README.md_. These files can be cloned from [github link]( https://github.com/adeelbarki/udacity_project_log_analysis.git) using this commad

`$ git clone https://github.com/adeelbarki/udacity_project_log_analysis.git`

Make sure to `$ cd newsdb-api-project` in terminal to access all three files. 

To run code succesfully make sure that the required newsdata.sql file is imported correctly in to the database. (File can be obtained from udacity nanodegree course). The zip file can also be downloaded from this link:

`https://drive.google.com/open?id=1j7nWvVownvt_1WRsfawtwfR-IUC6ILJd`

## Add Views in Database

Before running the code make sure to add a specific view to database.

```
create view popular_articles
    select author, title, count(*) as views
    from articles a, log l
    where a.slug=substring(l.path, 10)
    group by author, title
    order by views desc;
```
## Run the code

To run application, enter this following command.

`$ python newsdb.py`

Open any internet browser like Chrome, Firefox or internet explorer and type URL

`localhost:8000`. 

Search tab gives the option to select from all three tasks. Select one of the task and click search button. 

## Results

Results of these tasks can be seen on the browser and terminal running this application at the same time. In order to save these results to output.txt type this command.

`$ python newsdb.py > output.txt`

## Simpler solution with printserver.py

Github repo also contains a file named `printserver.py`. This file is rather a simple solution without an http web server. It only prints the required solutions on terminal by using this command.

`$ python printserver.py`

In order to print this data in an output.txt file repeat previous command with printserver.py.

`$ python printserver.py > output.txt`

## SQL Commands

SQL commands used for this projects are described. These commands can be used in postgreSQL terminal to see results separately.

Remember to connect database using this command. 

`postgres=# \c news`

### Most popular three articles of all time?
(consult 'Add view in Database': most_popular_articles)
```
select concat('"', a.title, '" ', '--', 
    count(substring(l.path, 10)), ' views') as most_popular_articles
    from log l right join articles a on a.slug=substring(l.path, 10)
    group by a.title order by count(substring(l.path, 10)) desc limit 3;
```

### Most popular authors of all time?
(consult 'Add view in Database': most_popular_articles)
```
select authors.name, sum(views) from popular_articles
    right join authors on author=authors.id group by authors.name, 
    author order by sum desc;```
```

### Days with more than 1% of requests lead to errors?
```
select concat(to_char(time::date, 'FMMonth DD, YYYY'),
    ' --', round(avg( (status <> '200 OK')::int )*100, 1), '% errors')
    as Most_Errors from log l group by time::date order by 
    avg( (status <> '200 OK')::int )*100 desc limit 1;
```
_(Quests.txt file is attached with this project folder, contains all SQL commands used in this project)._ 

## Code Style

Code is verified with pep8 code style.

## License

Project Logs Analysis is a part of Full Stack Web Development Nanodegree Program at [Udactiy](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).  
