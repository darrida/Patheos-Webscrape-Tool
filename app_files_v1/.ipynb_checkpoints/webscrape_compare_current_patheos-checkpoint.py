import pandas as pd
from tqdm import tqdm
import cx_Oracle

def access_compare_query(db_user, db_password, user, database, input_df):
    connection_string = db_user + '/' + db_password + database
    print("\n***CONNECTING***: " + db_user + '/' + "************" + database + "\n--------------")
    con = cx_Oracle.connect(connection_string)
    df_post_urls = pd.read_sql("""SELECT posts_url FROM patheos_posts""", con)
    
    df_new_urls = input_df #pd.read_csv('patheos_posts_test.csv')
    print("New URL list before: ")
    print(df_new_urls.shape[0])

    df_post_urls['master'] = 'master'
    df_post_urls.set_index('master',append=True,inplace=True)
    df_post_urls.rename(columns={'POSTS_URL': 'URL'}, inplace=True)
    df_post_urls.sort_values('URL',inplace=True)
    #print(df_post_urls)
    
    #uncomment in productions
    #df_new_urls = input_df
    df_new_urls['scraped'] = 'scraped'
    df_new_urls.set_index('scraped',append=True,inplace=True)
    df_new_urls.drop('Unnamed: 0', axis=1, inplace=True)
    df_new_urls.rename(columns={'0': 'URL'}, inplace=True)
    df_new_urls.sort_values('URL',inplace=True)
    #print(df_new_urls)
    
    df_merged = df_post_urls.append(df_new_urls, sort=True)
    df_merged = df_merged.drop_duplicates().sort_index()
    idx = pd.IndexSlice
    df_final_list = (df_merged.loc[idx[:, 'scraped'], :])
    print("New URL list after: ")
    print(df_final_list.shape[0])
    
    test_list = df_final_list.values.tolist()
    #for i in test_list:
        #print(i)
    con.close()
    print("--------------\n***DISCONNECTING***\n")
    return test_list