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
ALL = 'all'
MONTH = 'month'
WEEK = 'week'
DAY = 'day'

CORONA = 'coronavirus'
NEWS = 'news'
SCIENCE = 'science'
WORLD = 'worldnews'


# changes created UNIX time to standard
def get_date(created):
    return dt.datetime.fromtimestamp(created)


# Gets posts from a certain time period, the sub reddit as well as puts it in a .tsv
def scrape(filename, subreddit, time_period):
    sub = reddit.subreddit(subreddit)  # Only accesses the specifed subreddit
    # top_subreddit = corona.top(limit=x)  # gives you the top x posts of ALL TIME, limit is 1000
    top_subreddit = sub.top(limit=1000, time_filter=time_period)
    file_location = 'data/original'+filename
    table = open(file_location, 'w', encoding='utf-8')
    writer = csv.writer(table, delimiter='\t')
    writer.writerow(['title', 'score', 'num_comm', 'created', 'content'])

    # Writes the information into the .tsv
    for post in top_subreddit:
        row = [post.title, post.score,
               post.num_comments, get_date(post.created),
               post.selftext]
        writer.writerow(row)

    table.close()


# Gets the top 100 of each time frame from a single subreddit into their respective .tsv
def get_data(subreddit):
    scrape(subreddit + '_all.tsv', subreddit, ALL)
    scrape(subreddit + '_month.tsv', subreddit, MONTH)
    scrape(subreddit + '_week.tsv', subreddit, WEEK)
    scrape(subreddit + '_day.tsv', subreddit, DAY)


# Gets the sources that are in the post if it is in the content
def list_post_sources(entry):
    sources = []
    end_index = -1
    # filters out for posts that have content and if they have a source in the content
    if len(entry) == 5 and '](http' in entry[4]:
        content = entry[4]
        while end_index != len(content):
            start_index = int(content.find('](http')) + 2
            end_index = start_index + int(content[start_index:].find(')'))
            if end_index == 0:
                break
            sources.append(content[start_index:end_index])
            content = content[end_index + 1:]
    else:
        entry.pop()  # Removes the blank entry for content and replaces it with none then fills sources with none
        entry.append('None')
        entry.append('None')
        return entry
    entry.append(sources)
    return entry


# Goes through an entire .tsv or a subreddit of a specific time frame and adds the sources if available to each entry
def list_time_frame_sources(subreddit, timeframe):
    new = open('data/updated/' + subreddit + '_' + timeframe + '.tsv', 'w', encoding='utf-8')
    writer = csv.writer(new, delimiter='\t')
    writer.writerow(['title', 'score', 'num_comm', 'created', 'content', 'sources'])

    with open('data/original/' + subreddit + '_' + timeframe + '.tsv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')

        for entry in reader:
            if len(entry) != 0 and entry[0] != 'title':
                writer.writerow(list_post_sources(entry))

    new.close()


# Goes through all the subreddits and adds a source attribute to the entry
def list_subreddit_sources(subreddit):
    list_time_frame_sources(subreddit, ALL)
    list_time_frame_sources(subreddit, MONTH)
    list_time_frame_sources(subreddit, WEEK)
    list_time_frame_sources(subreddit, DAY)


def main():
    # Used to get all .tsv do not want to use as it will change original data
    # get_data('coronavirus')
    # get_data('news')
    # get_data('worldnews')
    # get_data('science')

    # Used to list the sources in each post for each .tsv
    list_subreddit_sources(CORONA)
    list_subreddit_sources(NEWS)
    list_subreddit_sources(SCIENCE)
    list_subreddit_sources(WORLD)


if __name__ == '__main__':
    main()
