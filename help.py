import pandas as pd
import emoji
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter
extractor = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())
    
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))    
    
    num_links = len(links)

    return num_messages, len(words), num_media, num_links

def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    f = open(r'D:\Analyzer\venv\stop_hinglish.txt', 'r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    
    f = open(r'D:\Analyzer\venv\stop_hinglish.txt', 'r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common = pd.DataFrame(Counter(words).most_common(20))
    return most_common
    
def emoji_help(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        message_emojis = [c for c in message if c in emoji.UNICODE_EMOJI['en']]
        emojis.extend(message_emojis)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline
    
