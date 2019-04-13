import pandas as pd
from tqdm import tqdm
import cx_Oracle
from sqlalchemy import types, create_engine
import sys

invalid_category = []
invalid_blog = []
invalid_post = []

def set_invalid_category(ecategory):
    invalid_category.append(ecategory)
        
def get_invalid_category():
    return invalid_category
    
def set_invalid_blog(eblog):
    invalid_blog.append(eblog)
        
def get_invalid_blog():
    return invalid_blog

def set_invalid_post(epost):
    invalid_post.append(epost)
    
def get_invalid_post():
    return invalid_post
    
#count_row = df.shape[0]
#total_process = df_results.shape[0]

def access_insert_execute(db_user, db_password, user, database, input_df):
    total_process = input_df.shape[0]
    invalid_category = []
    invalid_blog = []
    invalid_post = []
    connection_string = db_user + '/' + db_password + database
    print("\n***CONNECTING***: " + db_user + '/' + "************" + database + "\n--------------")
    con = cx_Oracle.connect(connection_string)
    #cur = con.cursor()
    con_engine = create_engine('oracle+cx_oracle://' + db_user + ':' + db_password + '@192.168.86.108:5522/?service_name=xe')
    #print(con_engine)
    
    c = 0
    ce = 0
    b = 0
    be = 0
    p = 0
    pdup = 0
    pe = 0
    
    #for post_url in a(unique_subblog_list):
    #enumerate(tqdm(...))
    #(1) COMPARE TO EXISTING CATEGORIES:
    for i, row in enumerate(input_df.itertuples(), 1):
    #for i, row in enumerate(tqdm(df_results.itertuples(), 1)):   
        try:
            beliefs_test = pd.read_sql("SELECT * FROM patheos_beliefs WHERE beliefs_url = '" + str(row.beliefs_url) + "'", con_engine)
            if beliefs_test.empty == True:
                cur = con.cursor()
                cur.execute("SELECT MAX(beliefs_number) FROM patheos_beliefs")
                test_number = str(cur.fetchall()[0][0])
                if test_number != 'None':
                    new_number = int(test_number) + 1
                else:
                    new_number = 1                
                beliefs_number = str(new_number)
                cur.execute("""INSERT INTO patheos_beliefs
                                (BELIEFS_NUMBER, BELIEFS_NAME, BELIEFS_URL)
                                VALUES
                                ('""" + str(new_number) + """','""" + row.beliefs_name + """','""" + row.beliefs_url + """')""")
                con.commit()
                cur2 = con.cursor()
                cur2.execute("SELECT * FROM patheos_beliefs WHERE beliefs_number = '" + str(new_number) + "'")
                res = cur2.fetchall()
                cur2.close()
                #print("INSERTED BELIEF: " + str(res))
                cur.close()
                c = c + 1
            else:
                cur3 = con.cursor()
                cur3.execute("SELECT MAX(beliefs_number) FROM patheos_beliefs WHERE beliefs_url = '" + row.beliefs_url + "'")
                beliefs_number = str(cur3.fetchall()[0][0])
                cur3.close()
                #print("BELIEF ALREADY EXISTS: " + beliefs_number + " " + row.beliefs_name)
        except:
            invalid_category.append(row.beliefs_url)
            #print("FAILED TO INSERT " + row.beliefs_url)
            ce = ce + 1 
        
        
    #(2) COMPARE TO EXISTING BLOGS:
        try:
            blogs_test = pd.read_sql("SELECT * FROM patheos_blogs WHERE blogs_url = '" + str(row.blogs_url) + "'", con_engine) 
                                        # beliefs_number = " + beliefs_number + " AND posts_url = '" + str(row.blogs_url) + "'", con_engine)
            if blogs_test.empty == True:
                cur4 = con.cursor()
                cur4.execute("SELECT MAX(blogs_number) FROM patheos_blogs")
                test_number2 = str(cur4.fetchall()[0][0])
                if test_number2 != 'None':
                    new_blog_number = int(test_number2) + 1
                else:
                    new_blog_number = 1                
                blogs_number = str(new_blog_number)
                cur4.execute("""INSERT INTO patheos_blogs
                                (BLOGS_NUMBER, BELIEFS_NUMBER, BLOGS_NAME, BLOGS_URL)
                                VALUES
                                ('""" + str(new_blog_number) + """','""" + beliefs_number + """','""" + row.blogs_name + """','""" + row.blogs_url + """')""")           
                con.commit()
                cur5 = con.cursor()
                cur5.execute("SELECT * FROM patheos_blogs WHERE blogs_number = '" + str(new_blog_number) + "'")
                res2 = cur5.fetchall()
                cur5.close()
                #print("INSERTED BLOG: " + str(res2))
                cur4.close()
                b = b + 1
            else:
                cur6 = con.cursor()
                cur6.execute("SELECT MAX(blogs_number) FROM patheos_blogs WHERE blogs_url = '" + row.blogs_url + "'")
                blogs_number = str(cur6.fetchall()[0][0])
                cur6.close()
                #print("BLOG ALREADY EXISTS: " + blogs_number + " " + row.blogs_name)
        except:
            invalid_blog.append(row.blogs_url)
            #print("FAILED TO INSERT " + row.blogs_url)
            be = be + 1
        
    #(3) COMPARE TO EXISTING POSTS:
        try:
            posts_test = pd.read_sql("SELECT * FROM patheos_posts WHERE posts_url = '" + str(row.posts_url) + "'", con_engine) 
                                    # beliefs_number = " + beliefs_number + " AND posts_url = '" + str(row.blogs_url) + "'", con_engine)
            if posts_test.empty == True:
                cur7 = con.cursor()
                cur7.execute("SELECT MAX(posts_number) FROM patheos_posts")
                test_number3 = str(cur7.fetchall()[0][0])
                if test_number3 != 'None':
                    new_post_number = int(test_number3) + 1
                else:
                    new_post_number = 1    
                var = cur7.var(cx_Oracle.CLOB)
                var.setvalue(0, row.posts_content)    # write a small value first to force the temporary LOB to be created    
                cur7.execute("""INSERT INTO patheos_posts
                                (POSTS_NUMBER, POSTS_TITLE, BLOGS_NUMBER, POSTS_AUTHOR, POSTS_DATE, POSTS_CONTENT, POSTS_URL)
                                VALUES
                                ('""" + str(new_post_number) + """','""" + row.posts_title + """','""" + blogs_number + """','""" + row.posts_author + """',""" 
                                      + """to_date('""" + row.posts_date + """','MONTH DD, YYYY'), :val ,'""" + row.posts_url + """')""", val = var)   
                                    #to_date('March 13, 2019','MONTH DD, YYYY')
                con.commit()
                cur8 = con.cursor()
                cur8.execute("SELECT * FROM patheos_posts WHERE posts_number = '" + str(new_post_number) + "'")
                res3 = cur8.fetchall()
                cur8.close()
                #print("INSERTED POST: " + str(res3) + "\n")
                cur7.close()
                p = p + 1
            else:
                cur9 = con.cursor()
                cur9.execute("SELECT MAX(posts_number) FROM patheos_posts WHERE posts_url = '" + row.posts_url + "'")
                posts_number = str(cur9.fetchall()[0][0])
                cur9.close()
                #print("POST ALREADY EXISTS: " + posts_number + " " + row.posts_title + "\n")
                pdup = pdup + 1
        except:
            invalid_post.append(row.posts_url)
            #print("FAILED TO INSERT " + row.posts_url)
            pe = pe + 1
        #print("Processed " + str(i) + " of " + str(total_process))
        #sys.stdout.write("\033[K")
        sys.stdout.write('\r'+ str(i) + "/" + str(total_process) + " | BELIEFS: new(" + str(c) + ") e(" + str(ce) 
                                                                 + ") | BLOGS: new(" + str(b) + ") e(" + str(be) 
                                                                 + ") | POSTS: new(" + str(p) + ") dup(" + str(pdup) + ") e(" + str(pe) + ")")
        #time.sleep(0.5)
        
    
    #df_data.to_sql('patheos_test', con_engine, if_exists='append',index=False)

    print("\nINSERT COMPLETE.")    
    con.close()
    print("--------------\n***DISCONNECTING***\n")
    #return df_user_access