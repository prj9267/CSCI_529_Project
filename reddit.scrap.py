# Author: Anthony, Parker, Grace, Drake
# CSCI529: GROUP PROJECT

import praw
import datetime as dt
import csv

# Variable that accesses REDDIT
reddit = praw.Reddit(client_id='qzAog3zZ9acCgQ',
                     client_secret='4Z2VLmc1o5tfQWym_0Oei7xt8Is',
                     user_agent='CSCI529.PROJ.COVID',
                     USERNAME='CSCI529_USER',
                     PASSWORD='csci.529.covid')

# What time period to scrape from Reddit
ALL_TIME = 'all'
MONTH = 'month'
WEEK = 'week'
DAY = 'day'


# changes created UNIX time to standard
def get_date(created):
    return dt.datetime.fromtimestamp(created)


# Gets posts from a certain time period, the sub reddit as well as puts it in a .tsv
def scrape(filename, subreddit, time_period):
    sub = reddit.subreddit(subreddit)  # Only accesses the specifed subreddit

    # top_subreddit = corona.top(limit=x)  # gives you the top x posts of ALL TIME, limit is 1000
    top_subreddit = sub.top(limit=1000, time_filter=time_period)

    file_location = 'data/'+filename
    table = open(file_location, 'a', encoding='utf-8')
    writer = csv.writer(table, delimiter='\t')
    writer.writerow(['title', 'score', 'num_comm', 'created', 'content'])

    # Writes the information into the .tsv
    for post in top_subreddit:
        row = []
        row.append(post.title)
        row.append(post.score)
        row.append(post.num_comments)
        row.append(get_date(post.created))
        row.append(post.selftext)
        writer.writerow(row)

    table.close()
    # WARNING: Does not replace file at destination only adds on to it.
    # If you are going to re run this function and do not want previous data
    # delete the file you are trying to create before running this.


def get_data(subreddit):
    scrape(subreddit+'_all.tsv', subreddit, ALL_TIME)
    scrape(subreddit+'_month.tsv', subreddit, MONTH)
    scrape(subreddit+'_week.tsv', subreddit, WEEK)
    scrape(subreddit+'_day.tsv', subreddit, DAY)


def main():
    get_data('coronavirus')
    get_data('news')
    get_data('worldnews')
    get_data('science')


if __name__ == '__main__':
    main()
