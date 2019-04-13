SELECT COUNT(DISTINCT(posts_url)) FROM patheos_posts;

SELECT COUNT(*) FROM patheos_posts;

SELECT COUNT(*) FROM patheos_posts;

SELECT bl.blogs_name, 
    (SELECT COUNT(*) FROM patheos_posts p
        WHERE p.blogs_number = bl.blogs_number) AS total_posts
    --(SELECT MIN(posts_date) FROM patheos_posts p1
      --  WHERE p1.blogs_number = bl.blogs_number) AS first_post
FROM patheos_blogs bl
ORDER BY bl.blogs_name;

SELECT COUNT(*) FROM patheos_posts p, patheos_blogs bl
WHERE p.blogs_number = bl.blogs_number
AND bl.blogs_name = 'jesuscreed';

SELECT bg.blogs_name, p.posts_title, dbms_lob.substr( posts_content, 50,dbms_lob.instr( posts_content, 'Jesus' ) - length( 'Jesus') ) lgbt_reference
FROM patheos_posts p, patheos_blogs bg
WHERE dbms_lob.instr( posts_content, 'Jesus' ) > 0
AND p.blogs_number = bg.blogs_number;

SELECT COUNT(dbms_lob.instr( p.posts_content, 'Jesus' ))
FROM patheos_posts p, patheos_blogs bg
WHERE dbms_lob.instr( posts_content, 'Jesus' ) > 0
AND p.blogs_number = bg.blogs_number;

select v(’WORKSPACE_ID’) from dual;

select * from apex_workspaces;

@apxchpwd;