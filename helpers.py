import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urlextract import URLExtract
from IPython.display import HTML

extract = URLExtract()

def all_stats(df,selected_user):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    num_messages = total_messages(df)
    num_words = total_words(df)
    num_media = total_media(df)
    num_links,links = total_links(df)
    links_df = links_dataframe(links)
#     num_links = total_links(df)
    
    return num_messages, num_words,num_media, num_links, links_df
    
def total_messages(df):
    
    return df.shape[0]

def total_words(df):
    
    words = []
    df_word = df.drop(df[df['message']=='<Media omitted>\n'].index,axis=0)
    for message in df_word['message']:
        words.extend(message.split())
    return len(words)

def total_media(df):
    
    df = df[df['message'] == '<Media omitted>\n']
    return df.shape[0]

def total_links(df):
    
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return len(links),links 

def links_dataframe(links):

    ldf = pd.DataFrame(links,columns=['links'])
    ldf = HTML(ldf.to_html(render_links=True,escape=False))

    return ldf

# def graphs(df):

#     top_users = users_top(df)

#     return top_users

def top_users(df):
    n = df.shape[0]
    x = df['user'].value_counts().head()
    maxdf = df['user'].value_counts().reset_index()
    maxdf.columns = ['user','count']
    maxdf['percentage'] = round(100 * (maxdf['count']/n),2)
    
    return x,maxdf

def monthly_timeline(df):
    monthlydf = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    monthlst = []
    for i in range(monthlydf.shape[0]):
        monthlst.append(monthlydf['month'][i]+"-"+str(monthlydf['year'][i]))
    monthlydf['time'] = monthlst

    return monthlydf

def daily_timeline(df):

    dailydf = df.groupby('date').count()['message'].reset_index()

    return dailydf
    



