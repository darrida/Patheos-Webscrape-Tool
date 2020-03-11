# Patheos Webscrape Tool

## Learning Notes

- **NOTE:** This repository younger than the actual project. I moved it into GitHub last year with intention of rewriting the tool. That's still on the list. This code needs refactoring across the board (many many obvious design issues, which are glariingly obvious to me in 2020).
- I approached learning Python (primarily using Jupyter) by choosing a problem to solve. The small task that I took on was to work toward downloading every blog post on Patheos.com (large, multi-section, multi-tenant blogging site). I bit off more than I could chew and had to rise to the occasion.
- Required changes
  - Refactor giant functions into much smaller, ideally single task functionality (current status is very difficult to read, and writing unit test would be a nearly impossible task)
  - Move database connection and database data management into it's own class, and interact with it through a context manager
  - Move data formats used to prepare information to be inserted into the database into classes as well (Uses would include data validattion before attempted database insertion)
  - implement exception handlers across the board (in its current state it crashes upon encountering a form of unstructured data I hadn't designed it to process)
  - Look into using dictionaries instead of Pandas (or even classes, to handle, validation transformation, logging, and errors immediately upon individual data scrape). Whichever is more accessible/readable. performance concerns with this process are not high. Either way, dictionaries will be faster than misusing Pandas.
  - Break the code up into smaller modules, and implement intentional structure in the application directory as a whole.

## Goal

- Perpetually running tool that initally downloads app blog posts from Patheos, then downloads new posts on a schedule.

## History

- CSV: My first version simply exported data to flat files.
- Oracle: My next version inserted data into an Oracle database, and used a simple APEX application to view the data. Before I had a chance to smooth out any rough edges in the APEX app I chose to use a different database, since I was learning the Oracle ecosystem at work.
- PostgreSQL: Ultimately I landed on using Postgres, since experience with it would complement my Oracle experience.
- Docker: My final version was hosted on my NAS using a Jupyter Lab container connected to a Postgres container. This was still really early on (in the 'bit off more that I could chew' phase), so I just downloaded the images from the Docker repository and (for Jupyter) made local directories available to the running container. I didn't yet understand how to write a DockerFile.

## Proof of concepts for the following complete:

Efficiently scraping:
- categories
- blogs from categories
- blog pages from blogs
- posts content from blog pages
- export to csv
- export to xlsx
- insert into Oracle database tables (3, for category, blog, and posts

