﻿SELECT * FROM patheos_beliefs;
SELECT * FROM patheos_blogs;
SELECT * FROM patheos_posts;
SELECT COUNT(*) FROM patheos_posts;
SELECT COUNT(*) FROM patheos_posts WHERE blogs_number = 1;

SELECT * FROM patheos_posts WHERE posts_content LIKE '%'' + '\u201d%';

ALTER USER postgres WITH PASSWORD 'password';

CREATE TABLE PATHEOS_BELIEFS (
    BELIEFS_NUMBER SERIAL PRIMARY KEY, 
    BELIEFS_NAME VARCHAR(50) NOT NULL, 
    BELIEFS_TRADITION VARCHAR(50), 
    BELIEFS_URL VARCHAR(1000) NOT NULL 
);

CREATE TABLE PATHEOS_BLOGS (
    BLOGS_NUMBER SERIAL PRIMARY KEY, 
    BLOGS_AUTHOR VARCHAR(150),
    BELIEFS_NUMBER SERIAL NOT NULL, 
    BLOGS_NAME VARCHAR(255), 
    BLOGS_URL VARCHAR(1000) NOT NULL
);

alter table patheos_blogs 
add constraint fk_beliefs_number
foreign key (beliefs_number) 
REFERENCES patheos_beliefs (beliefs_number);

CREATE TABLE PATHEOS_POSTS (
    POSTS_NUMBER SERIAL PRIMARY KEY, 
    POSTS_TITLE VARCHAR(255) NOT NULL, 
    BLOGS_NUMBER SERIAL NOT NULL, 
    POSTS_AUTHOR VARCHAR(255), 
    POSTS_DATE DATE, 
    POSTS_TAGS VARCHAR(255), 
    POSTS_CONTENT TEXT, 
    POSTS_URL VARCHAR(1000) NOT NULL
);

alter table patheos_posts 
add constraint fk_posts_number
foreign key (blogs_number) 
REFERENCES patheos_blogs (blogs_number);