# Author: Anthony, Parker, Grace, Drake
# CSCI529: GROUP PROJECT

import praw
import pandas as pd
import datetime as dt


# changes created UNIX time to standard
def get_date(created):
    return dt.datetime.fromtimestamp(created)


# Variable that accesses REDDIT
reddit = praw.Reddit(client_id='qzAog3zZ9acCgQ',
                     client_secret='4Z2VLmc1o5tfQWym_0Oei7xt8Is',
                     user_agent='CSCI529.PROJ.COVID',
                     USERNAME='CSCI529_USER',
                     PASSWORD='csci.529.covid')

# Holds a post's information score = likes, content= text in the post
post_dict = {'title': [], 'score': [], 'num_comm': [],  'created': [], 'content': []}

corona = reddit.subreddit('Coronavirus')  # Only accesses the r/Cornavirus topic
top_corona = corona.top()  # Retrieves the top 100 posts of ALL TIME in the topic
# top_corona = corona.top(limit=x)  # gives you the top x posts of ALL TIME, limit is 1000

# Assigns the information from the post to the according section
for post in top_corona:
    post_dict['title'].append(post.title)
    post_dict['score'].append(post.score)
    post_dict['num_comm'].append(post.num_comments)
    post_dict['created'].append(get_date(post.created))
    post_dict['content'].append(post.selftext)

# Turns the data into a table.
post_data = pd.DataFrame(post_dict)

# Stores the data into a .csv file.
# Do not have to remove .csv file. This line will overwrite the previous one will not add on to it.
post_data.to_csv('data.csv', index=False)
