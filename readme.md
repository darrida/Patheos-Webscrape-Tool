# Patheos Webscrape Tool

## Rebuild (for notes related to this, see "Learning Notes" below)

- Rebuild process started
  - Started clean up of the messy direction organization
  - Started on the database classes (classes for objects to insert into tables, as well as database connection and manipulation
    - First pass was to build ORM classes (orm_classes.py), but decided to use raw SQL (db_interface_sqlite.py) since this will mostly be a storage repository to insert and query a large number of records. The records will be used for stats and reports, not for application management

## Learning Notes

- **NOTE:** This repository younger than the actual project. *The project is several years old.* I moved it into GitHub last year with intention of rewriting the tool. That's still on the list. This code needs refactoring across almost every line (many many obvious design issues, which are glariingly obvious to me in 2020).
- This was pretty much the **first** project I worked on while learning Python.
- I approached learning Python (primarily using Jupyter) by **choosing a problem to solve**. The **"small task"** that I took on was to work toward downloading **every** blog post across Patheos.com (large, multi-section, multi-tenant blogging site). Patheos hosts hundreds of thousands of blog posts, with all of the variability of unstructured data that brings with it. I bit off more than I could chew and had to rise to the occasion.
- Ultimately, in the midst of my very un-ideal code, my first challenge I took on to learn Python a few years ago **successfully scraped, parsed, and inserted unstructured data** from over **350,000** blog posts into a PostgreSQL database.
- In the current state, it would be difficult for anyone unfamiliar with the code to make sense of, much less run it
- **Required changes**
  - **Refactor gigantic functions** into much smaller, ideally single task functionality (current status is very difficult to read, and writing unit tests would be a nearly impossible task)
  - Move database connection and database data management into a class, and interact with it through a **context manager**
  - Move data formats used to prepare information to be inserted into the database into classes as well (Uses would include **data validattion** before attempted database insertion)
  - implement **exception handlers** across the board (in its current state it crashes upon encountering a form of unstructured data I hadn't designed it to process).
  - Look into using **dictionaries instead of Pandas** (or even classes, to handle, validation transformation, logging, and errors immediately upon individual data scrape). Whichever is **more accessible/readable**. performance concerns with this process are not high. Either way, **dictionaries will be faster than misusing Pandas** (obviously Pandas is incredibly fast when used properly - though, it does takea while to import before running code).
  - **Break code up into smaller modules**, and implement **intentional structure in the application directory** as a whole.
  - Move out of Jupyter Notebook files for "production".
  - Write **unit tests** with a **high level of coverage** (the process is fragile and interconnected - high test coverage would strengthen it across the board).
  - Use **cProfile** to evaluate performance and eliminate bottlenecks.
  - Create mult-step **DockerFile** to containerize the python code and Postgres database, each.
  - Implement a **GitHub CI** Actions to test **build**, run **tests**, measure **coverage**, and **deploy** to a cloud provider.

## Goal

- Perpetually running tool that initally downloads app blog posts from Patheos, then downloads new posts on a schedule.

## History

- CSV: My first version simply exported data to flat files.
- Oracle: My next version inserted data into an Oracle database, and used a simple APEX application to view the data. Before I had a chance to smooth out any rough edges in the APEX app I chose to use a different database, since I was learning the Oracle ecosystem at work.
- PostgreSQL: Ultimately I landed on using Postgres, since experience with it would complement my Oracle experience.
- Docker: My final version was hosted on my NAS using a Jupyter Lab container connected to a Postgres container. This was still really early on (in the 'bit off more that I could chew' phase), so I just downloaded the images from the Docker repository and (for Jupyter) made local directories available to the running container. I didn't yet understand how to write a DockerFile.

## Proof of concepts for the following exist:

#### Basic Functionality

- Scrapes
  - categories
  - blogs from categories
  - blog pages from blogs
  - posts content from blog pages
- Exports
  - export to csv
  - export to xlsx
- Inserts
  - into Oracle database tables (3, for category, blog, and posts)
  - into PostgreSQL database tables (3, for category, blog, and posts)

