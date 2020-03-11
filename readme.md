# Patheos Webscrape Tool

**NOTE:** This repository younger than the actual project. I moved it into GitHub last year with intention of rewriting the tool. That's still on the list.

## History

- Origination: I approached learning Python by choosing a problem to solve. The small task that I took on was to work toward downloading every blog post on Patheos.com (large, multi-section, multi-tenant blogging site). I bit off more than I could chew and had to rise to the occasion.
- CSV: My first version simply exported data to flat files.
- Oracle: My next version inserted data into an Oracle database, and used a simple APEX application to view the data. Before I had a chance to smooth out any rough edges in the APEX app I chose to use a different database, since I was learning the Oracle ecosystem at work.
- PostgreSQL: Ultimately I landed on using Postgres, since experience with it would complement my Oracle experience.

## Proof of concepts for the following complete:

Efficiently scraping:
- categories
- blogs from categories
- blog pages from blogs
- posts content from blog pages
- export to csv
- export to xlsx
- insert into Oracle database tables (3, for category, blog, and posts

