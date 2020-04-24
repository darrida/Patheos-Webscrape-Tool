ALTER USER postgres WITH PASSWORD 'password';

CREATE TABLE PATHEOS_BELIEFS (
    BELIEFS_NUMBER SERIAL PRIMARY KEY, 
    BELIEFS_NAME VARCHAR(50) NOT NULL, 
    BELIEFS_TRADITION VARCHAR(50), 
    BELIEFS_URL VARCHAR(1000) NOT NULL,
    LAST_DATE TIMESTAMP,
    LAST_USER VARCHAR(100),
    CREATE_DATE TIMESTAMP,
    CREATE_USER VARCHAR(100)
);

CREATE TABLE PATHEOS_BLOGS (
    BLOGS_NUMBER SERIAL PRIMARY KEY, 
    BLOGS_AUTHOR VARCHAR(150),
    BELIEFS_NUMBER SERIAL NOT NULL, 
    BLOGS_NAME VARCHAR(255), 
    BLOGS_URL VARCHAR(1000) NOT NULL,
    LAST_DATE TIMESTAMP,
    LAST_USER VARCHAR(100),
    CREATE_DATE TIMESTAMP,
    CREATE_USER VARCHAR(100)
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
    POSTS_URL VARCHAR(1000) NOT NULL,
    LAST_DATE TIMESTAMP,
    LAST_USER VARCHAR(100),
    CREATE_DATE TIMESTAMP,
    CREATE_USER VARCHAR(100)
);

alter table patheos_posts 
add constraint fk_posts_number
foreign key (blogs_number) 
REFERENCES patheos_blogs (blogs_number);


CREATE FUNCTION time_stamp() RETURNS trigger AS $time_stamp$
    BEGIN
        -- Remember who/when updated patheos_posts record
        NEW.last_date := current_timestamp;
        NEW.last_user := current_user;
        RETURN NEW;
    END;
$time_stamp$ LANGUAGE plpgsql;

CREATE TRIGGER time_stamp_posts BEFORE INSERT OR UPDATE ON patheos_posts
    FOR EACH ROW EXECUTE FUNCTION time_stamp();

CREATE TRIGGER time_stamp_beliefs BEFORE INSERT OR UPDATE ON patheos_beliefs
    FOR EACH ROW EXECUTE FUNCTION time_stamp();

CREATE TRIGGER time_stamp_blogs BEFORE INSERT OR UPDATE ON patheos_blogs
    FOR EACH ROW EXECUTE FUNCTION time_stamp();

--Waiting until it's convinient to drop triggers to drop and recreate this
CREATE FUNCTION create_stamp() RETURNS trigger AS $create_stamp$
    BEGIN
        -- Remember who/when updated patheos_posts record
        NEW.create_date := current_timestamp;
        NEW.create_user := current_user;
        RETURN NEW;
    END;
$create_stamp$ LANGUAGE plpgsql;

--DROP FUNCTION create_stamp;

CREATE TRIGGER create_stamp_posts BEFORE INSERT ON patheos_posts
    FOR EACH ROW EXECUTE FUNCTION create_stamp();

CREATE TRIGGER create_stamp_beliefs BEFORE INSERT ON patheos_beliefs
    FOR EACH ROW EXECUTE FUNCTION create_stamp();

CREATE TRIGGER create_stamp_blogs BEFORE INSERT ON patheos_blogs
    FOR EACH ROW EXECUTE FUNCTION create_stamp();

--DROP TRIGGER create_stamp_blogs ON patheos_blogs;