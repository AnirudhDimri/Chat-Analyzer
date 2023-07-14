import streamlit as st
import preprocessor
import help
import matplotlib.pyplot as plt

st.sidebar.title('Chat Behaviour Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("perform analysis on", user_list)

    if st.sidebar.button("Perform Analysis"):

        st.title('Top Statistics')
        
        num_messages, words, num_media, num_links = help.fetch_stats(selected_user,df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        
        with col2:
            st.header('Total Words')
            st.title(words)
        
        with col3:
            st.header('Media shared')
            st.title(num_media)

        with col4:
            st.header('Links shared')
            st.title(num_links)

        #timeline
        st.title("Monthly Chat Timline")
        timeline = help.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #finding the busiest user
        if selected_user == 'Overall':

            st.title('Most Acitve Users')

            x, new_df = help.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
        
        #wordcloud
        st.title('Word Cloud')
        df_wc = help.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        #most common words
        most_common = help.most_common_words(selected_user,df)

        fig, ax = plt.subplots()

        ax.barh(most_common[0], most_common[1])
        plt.xticks(rotation='vertical')

        st.title('Most common words')
        st.pyplot(fig)

        #emoji analysis
        emoji_df = help.emoji_help(selected_user,df)

        st.title("Emoji Analysis")
        
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)