# importing reqired libraries
import streamlit as st
from datapreprocessing import getdata
import helpers
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout='wide')


# title and text for streamlit
st.title('Whatsapp Chat Analysis')
st.write('Please Choose file below to get analysis')




uploaded_file = st.sidebar.file_uploader("Choose Whatsapp chat Text file below")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")


    # getting the raw data frame
    df = getdata(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group-notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    userdf = df
    if selected_user != 'Overall':
            userdf = userdf[userdf['user']==selected_user]

    if st.sidebar.button('Show Raw Data'):
        userdf

    
    num_messages, num_words,num_media, num_links, links = helpers.all_stats(df,selected_user)

    if st.sidebar.button("Show Analysis"):


    # button that shows raw data when clicked


        # Overall Analysis

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(num_words)

        with col3:
            st.header('Total Media')
            st.title(num_media)

        with col4:
            st.header('Total Links')
            st.title(num_links)

        # Monthly timeline

        col1,col2 = st.columns(2)
        monthlydf = helpers.monthly_timeline(userdf)

        fig,ax = plt.subplots()
        ax.plot(monthlydf.time,monthlydf.message,color='darkblue')
        plt.xticks(rotation='vertical')

        with col1:
            st.header('Monthy Timeline')
            st.pyplot(fig)

        dailydf = helpers.daily_timeline(userdf)

        fig,ax = plt.subplots()
        ax.plot(dailydf.date,dailydf.message,color='green')
        plt.xticks(rotation='vertical')

        with col2:
            st.header('Daily Timeline')
            st.pyplot(fig)

        # top group users
        topfive,topusers = helpers.top_users(df)
        
        col1,col2 = st.columns(2)

        with col1:
            fig,ax = plt.subplots()
            ax.bar(topfive.index,topfive.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            topusers

    if st.sidebar.button('Show Links Data'):
        links

        # df

        # c1,c2 = st.columns(2)

        # with c1:
        

        # with c2:
    



