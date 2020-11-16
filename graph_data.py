"""
authors: Parker, Anthony, Drake, Grace
description: Parses through tsv files and graphs data that was gathered from Reddit
"""
import re
import csv
import plotly.graph_objects as go
import datetime


# Post object that represents a single Reddit post.  Attributes are the following...
#   ID: id number to reference a post
#   Title: title of the post
#   Score: Sum of the "likes"/upvotes minus the sum of the "dislikes"/downvotes.
#   Num_Comm: Number of comments
#   Created: Date posted
#   Content: The text content of the post.  Content with images do not appear.
#   Relevant:  If it is in regards to COVID-19 in any way.
#   Sources: List of websites listed in the content of the post.

class Post:

    def __init__(self):
        self.id = None
        self.title = ""
        self.score = 0
        self.num_comm = 0
        self.created = ""
        self.content = ""
        self.relevant = False
        self.sources = list()

    def __eq__(self, other):
        if self.title == other.title and self.content == other.content:
            return True
        return False


# Parses through the updated .tsv files for data to be graphed.  Stores the data in dictionaries of Post objects

def parse_data(sub_reddit_name, sub_reddit_dict):
    file_list = [
        "{name}_all.tsv".format(name=sub_reddit_name),
        "{name}_day.tsv".format(name=sub_reddit_name),
        "{name}_month.tsv".format(name=sub_reddit_name),
        "{name}_week.tsv".format(name=sub_reddit_name)
    ]

    sub_reddit_dict["all_time"] = dict()
    sub_reddit_dict["day"] = dict()
    sub_reddit_dict["month"] = dict()
    sub_reddit_dict["week"] = dict()

    for file_name in file_list:
        file = open("data/updated/" + file_name, "r", encoding="utf8")
        reader = csv.reader(file, delimiter="\t")

        post_count = 0
        for entry in reader:
            if post_count == 0:
                post_count += 1
                cols = entry

            elif len(entry) != 0:

                post = Post()

                post.id = post_count
                post.title = entry[0]
                post.score = entry[1]
                post.num_comm = entry[2]
                post.created = entry[3]

                post_count += 1

                if sub_reddit_name == "coronavirus":
                    post.relevant = True
                elif re.search("coronavirus", post.title, re.IGNORECASE) or \
                        re.search("covid", post.title, re.IGNORECASE) or \
                        re.search("sars-cov-2", post.title, re.IGNORECASE) or \
                        re.search("pandemic", post.title, re.IGNORECASE) or \
                        re.search("virus", post.title, re.IGNORECASE):
                    post.relevant = True

                # If the post doesn't have text content.  Most likely an image.
                if entry[4] != "None":
                    post.content = entry[4]

                    # Search the content for keywords
                    if re.search("coronavirus", post.content, re.IGNORECASE) or \
                            re.search("covid", post.content, re.IGNORECASE) or \
                            re.search("sars-cov-2", post.content, re.IGNORECASE) or \
                            re.search("pandemic", post.content, re.IGNORECASE) or \
                            re.search("virus", post.content, re.IGNORECASE):
                        post.relevant = True

                if entry[5] != "None":
                    source_string = entry[5][1:len(entry[5]) - 1]
                    post.sources = source_string.split(",")

                if file_name == file_list[0]:
                    sub_reddit_dict["all_time"][post.id] = post
                elif file_name == file_list[1]:
                    sub_reddit_dict["day"][post.id] = post
                elif file_name == file_list[2]:
                    sub_reddit_dict["month"][post.id] = post
                elif file_name == file_list[3]:
                    sub_reddit_dict["week"][post.id] = post

        file.close()


#   Graphs a pie chart of the number of COVID related posts vs the non-covid related posts

def graph_covid_post_count(sub_reddit_name, sub_reddit_dict):
    covid_count, total_posts = 0, 0

    for time_key in sub_reddit_dict.keys():
        for post_id in sub_reddit_dict[time_key].keys():
            post = sub_reddit_dict[time_key][post_id]
            total_posts += 1

            if post.relevant:
                covid_count += 1

        labels = ["COVID Related Posts", "Other Posts"]
        values = [covid_count, total_posts - covid_count]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo="label+percent")])
        if time_key == "all_time":
            fig.update_layout(
                title={
                    "text": "Covid Related Posts in " + sub_reddit_name + ": Top 1000 Posts of all time."
                }
            )
        elif time_key == "day":
            fig.update_layout(
                title={
                    "text": "Covid Related Posts in " + sub_reddit_name + ": Top 1000 Posts of Today"
                }
            )
        elif time_key == "month":
            fig.update_layout(
                title={
                    "text": "Covid Related Posts in " + sub_reddit_name + ": Top 1000 Posts of the Month"
                }
            )
        else:
            fig.update_layout(
                title={
                    "text": "Covid Related Posts in " + sub_reddit_name + ": Top 1000 Posts of the Week"
                }
            )

        fig.update_layout(
            title={
                'y': 0.95,
                'x': 0.025,
                'xanchor': 'left',
                'yanchor': 'top',
            },
            font=dict(size=20),
        )

        fig.show()
        covid_count, total_posts = 0, 0


#   Graphs a pie chart of the number of COVID related posts that have sources or not

def graph_sources_in_covid_posts(sub_reddit_name, sub_reddit_dict):
    source_count, total_covid_posts = 0, 0

    for time_key in sub_reddit_dict.keys():
        for post_id in sub_reddit_dict[time_key].keys():
            post = sub_reddit_dict[time_key][post_id]

            if post.relevant:
                total_covid_posts += 1

                if len(post.sources) > 0:
                    source_count += 1

        labels = ["Posts with Provided Sources", "Posts without Sources"]
        values = [source_count, total_covid_posts - source_count]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo="label+percent")])
        if time_key == "all_time":
            fig.update_layout(
                title={
                    "text": "Sources in Covid Posts from " + sub_reddit_name + ": \nTop 1000 Posts of all time."
                }
            )
        elif time_key == "day":
            fig.update_layout(
                title={
                    "text": "Sources in Covid Posts from " + sub_reddit_name + ": \nTop 1000 Posts of Today"
                }
            )
        elif time_key == "month":
            fig.update_layout(
                title={
                    "text": "Sources in Covid Posts from " + sub_reddit_name + ": \nTop 1000 Posts of the Month"
                }
            )
        else:
            fig.update_layout(
                title={
                    "text": "Sources in Covid Posts from " + sub_reddit_name + ": \nTop 1000 Posts of the Week"
                }
            )
        fig.update_layout(
            title={
                'y': 0.95,
                'x': 0.025,
                'xanchor': 'left',
                'yanchor': 'top',
            },
            font=dict(size=17)
        )
        fig.show()
        source_count, total_covid_posts = 0, 0


#   Graphs a double bar Histogram comparing the average engagement (upvotes or comments) for covid posts vs non-covid posts
#   Calculated average is the mean value

def graph_covid_engagement(data_dict, engagement_type):
    tracker = dict()
    covid_engagement_values = [None, None, None, None]
    non_covid_engagement_values = [None, None, None, None]

    for sub_reddit_name in data_dict.keys():
        sub_reddit_dict = data_dict[sub_reddit_name]
        covid_count, non_covid_count = 0, 0
        covid_engagement_count, non_covid_engagement_count = 0, 0

        for time_key in sub_reddit_dict.keys():
            for post_id in sub_reddit_dict[time_key]:
                post = sub_reddit_dict[time_key][post_id]

                if post.title not in tracker.keys():
                    tracker[post.title] = 1

                    if engagement_type == "score":
                        if post.relevant:
                            covid_count += 1
                            covid_engagement_count += int(post.score)
                        else:
                            non_covid_count += 1
                            non_covid_engagement_count += int(post.score)
                    elif engagement_type == "comments":
                        if post.relevant:
                            covid_count += 1
                            covid_engagement_count += int(post.num_comm)
                        else:
                            non_covid_count += 1
                            non_covid_engagement_count += int(post.num_comm)

        if sub_reddit_name == "Coronavirus":
            covid_engagement_values[0] = covid_engagement_count / covid_count
            non_covid_engagement_values[0] = 0  # Subreddit Rules for r/Coronavirus makes it so any non-covid related post is removed
        elif sub_reddit_name == "News":
            covid_engagement_values[1] = covid_engagement_count / covid_count
            non_covid_engagement_values[1] = non_covid_engagement_count / non_covid_count
        elif sub_reddit_name == "Science":
            covid_engagement_values[2] = covid_engagement_count / covid_count
            non_covid_engagement_values[2] = non_covid_engagement_count / non_covid_count
        else:
            covid_engagement_values[3] = covid_engagement_count / covid_count
            non_covid_engagement_values[3] = non_covid_engagement_count / non_covid_count

        tracker.clear()

    labels = ["Coronavirus", "News", "Science", "WorldNews"]

    if engagement_type == "score":
        fig = go.Figure(data=[
            go.Bar(name="Average Score on Covid Related Posts", x=labels, y=covid_engagement_values),
            go.Bar(name="Average Score on Non-Covid Related Posts", x=labels, y=non_covid_engagement_values)
        ])

        fig.update_layout(
            title="Average Upvotes for Posts Related and Not Related to Covid - All SubReddits, All Time Filters",
            xaxis_title="Subreddit",
            yaxis_title="Score",
            font=dict(size=20)
        )
    else:
        fig = go.Figure(data=[
            go.Bar(name="Average Number of Comments on Covid Related Posts", x=labels, y=covid_engagement_values),
            go.Bar(name="Average Number of Comments on Non-Covid Related Posts", x=labels, y=non_covid_engagement_values)
        ])

        fig.update_layout(
            title="Average Number of Comments for Posts Related and Not Related to Covid - All SubReddits, All Time Filters",
            xaxis_title="Subreddit",
            yaxis_title="Comments",
            font=dict(size=20)
        )

    fig.update_xaxes(showgrid=True, gridcolor="rgb(140,140,140)")
    fig.update_yaxes(showgrid=True, gridcolor="rgb(140,140,140)")

    fig.show()


#   Graphs a double bar Histogram comparing the average engagement (upvotes or comments) for covid posts with/without sources
#   Calculated average is the mean value

def graph_covid_source_engagement(data_dict, engagement_type):
    tracker = dict()
    source_engagement_values = [None, None, None, None]
    non_source_engagement_values = [None, None, None, None]

    for sub_reddit_name in data_dict.keys():
        sub_reddit_dict = data_dict[sub_reddit_name]
        source_count, non_source_count = 0, 0
        source_engagement_count, non_source_engagement_count = 0, 0

        for time_key in sub_reddit_dict.keys():
            for post_id in sub_reddit_dict[time_key]:
                post = sub_reddit_dict[time_key][post_id]

                if post.title not in tracker.keys():
                    tracker[post.title] = 1

                    if engagement_type == "score":
                        if post.relevant:
                            if len(post.sources) > 0 or sub_reddit_name == "WorldNews":
                                source_count += 1
                                source_engagement_count += int(post.num_comm)
                            else:
                                non_source_count += 1
                                non_source_engagement_count += int(post.num_comm)
                    else:
                        if post.relevant:
                            if len(post.sources) > 0 or sub_reddit_name == "WorldNews":
                                source_count += 1
                                source_engagement_count += int(post.num_comm)
                            else:
                                non_source_count += 1
                                non_source_engagement_count += int(post.num_comm)

        if sub_reddit_name == "Coronavirus":
            source_engagement_values[0] = source_engagement_count / source_count
            non_source_engagement_values[0] = non_source_engagement_count / non_source_count
        elif sub_reddit_name == "News":
            source_engagement_values[1] = source_engagement_count / source_count
            non_source_engagement_values[1] = non_source_engagement_count / non_source_count
        elif sub_reddit_name == "Science":
            source_engagement_values[2] = source_engagement_count / source_count
            non_source_engagement_values[2] = non_source_engagement_count / non_source_count
        else:  # Every post in r/WorldNews has a link
            source_engagement_values[3] = source_engagement_count / source_count
            non_source_engagement_values[3] = 0

        tracker.clear()

    labels = ["Coronavirus", "News", "Science", "WorldNews"]

    if engagement_type == "score":
        fig = go.Figure(data=[
            go.Bar(name="Average Score on Posts WITH Sources", x=labels, y=source_engagement_values),
            go.Bar(name="Average Score on Posts WITHOUT Sources", x=labels, y=non_source_engagement_values)
        ])

        fig.update_layout(
            title="Average Upvotes for Covid Related Posts With and Without Provided Sources - All SubReddits, All Time Filters",
            xaxis_title="Subreddit",
            yaxis_title="Score",
            font=dict(size=20)
        )
    else:
        fig = go.Figure(data=[
            go.Bar(name="Average Number of Comments on Posts WITH Sources", x=labels, y=source_engagement_values),
            go.Bar(name="Average Number of Comments on Posts WITHOUT Sources", x=labels, y=non_source_engagement_values)
        ])

        fig.update_layout(
            title="Average Number of Comments for Covid Related Posts With and Without Provided Sources - All SubReddits, All Time Filters",
            xaxis_title="Subreddit",
            yaxis_title="Comments",
            font=dict(size=20)
        )

    fig.update_xaxes(showgrid=True, gridcolor="rgb(140,140,140)")
    fig.update_yaxes(showgrid=True, gridcolor="rgb(140,140,140)")

    fig.show()


#   Graphs a time series visualization of the average engagement (upvotes or comments) change through each day of the week.
#   Graphs both average engagement for covid vs non-covid posts.


def graph_time_series_engagement_daily(sub_reddit_name, sub_reddit_dict, engagement_type):
    tracker = dict()

    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    week_covid_engagement_values = [0, 0, 0, 0, 0, 0, 0]
    week_covid_post_count = [0, 0, 0, 0, 0, 0, 0]
    week_non_covid_engagement_values = [0, 0, 0, 0, 0, 0, 0]
    week_non_covid_post_count = [0, 0, 0, 0, 0, 0, 0]

    for time_key in sub_reddit_dict.keys():
        for post_id in sub_reddit_dict[time_key].keys():
            post = sub_reddit_dict[time_key][post_id]

            if post.title not in tracker.keys():
                tracker[post.title] = 1

                date_data = post.created.strip().split(" ")[0].split("-")
                date = datetime.datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]))
                day_of_week = date.strftime("%A")

                if day_of_week == "Monday":
                    if post.relevant:
                        if engagement_type == "score":
                            week_covid_engagement_values[0] += int(post.score)
                            week_covid_post_count[0] += 1
                        else:
                            week_covid_engagement_values[0] += int(post.num_comm)
                            week_covid_post_count[0] += 1
                    else:
                        if engagement_type == "score":
                            week_non_covid_engagement_values[0] += int(post.score)
                            week_non_covid_post_count[0] += 1
                        else:
                            week_non_covid_engagement_values[0] += int(post.num_comm)
                            week_non_covid_post_count[0] += 1
                elif day_of_week == "Tuesday":
                    if post.relevant:
                        if engagement_type == "score":
                            week_covid_engagement_values[1] += int(post.score)
                            week_covid_post_count[1] += 1
                        else:
                            week_covid_engagement_values[1] += int(post.num_comm)
                            week_covid_post_count[1] += 1
                    else:
                        if engagement_type == "score":
                            week_non_covid_engagement_values[1] += int(post.score)
                            week_non_covid_post_count[1] += 1
                        else:
                            week_non_covid_engagement_values[1] += int(post.num_comm)
                            week_non_covid_post_count[1] += 1
                elif day_of_week == "Wednesday":
                    if post.relevant:
                        if engagement_type == "score":
                            week_covid_engagement_values[2] += int(post.score)
                            week_covid_post_count[2] += 1
                        else:
                            week_covid_engagement_values[2] += int(post.num_comm)
                            week_covid_post_count[2] += 1
                    else:
                        if engagement_type == "score":
                            week_non_covid_engagement_values[2] += int(post.score)
                            week_non_covid_post_count[2] += 1
                        else:
                            week_non_covid_engagement_values[2] += int(post.num_comm)
                            week_non_covid_post_count[2] += 1
                elif day_of_week == "Thursday":
                    if post.relevant:
                        if engagement_type == "score":
                            week_covid_engagement_values[3] += int(post.score)
                            week_covid_post_count[3] += 1
                        else:
                            week_covid_engagement_values[3] += int(post.num_comm)
                            week_covid_post_count[3] += 1
                    else:
                        if engagement_type == "score":
                            week_non_covid_engagement_values[3] += int(post.score)
                            week_non_covid_post_count[3] += 1
                        else:
                            week_non_covid_engagement_values[3] += int(post.num_comm)
                            week_non_covid_post_count[3] += 1
                elif day_of_week == "Friday":
                    if post.relevant:
                        if engagement_type == "score":
                            week_covid_engagement_values[4] += int(post.score)
                            week_covid_post_count[4] += 1
                        else:
                            week_covid_engagement_values[4] += int(post.num_comm)
                            week_covid_post_count[4] += 1
                    else:
                        if engagement_type == "score":
                            week_non_covid_engagement_values[4] += int(post.score)
                            week_non_covid_post_count[4] += 1
                        else:
                            week_non_covid_engagement_values[4] += int(post.num_comm)
                            week_non_covid_post_count[4] += 1
                elif day_of_week == "Saturday":
                    if post.relevant:
                        if engagement_type == "score":
                            week_covid_engagement_values[5] += int(post.score)
                            week_covid_post_count[5] += 1
                        else:
                            week_covid_engagement_values[5] += int(post.num_comm)
                            week_covid_post_count[5] += 1
                    else:
                        if engagement_type == "score":
                            week_non_covid_engagement_values[5] += int(post.score)
                            week_non_covid_post_count[5] += 1
                        else:
                            week_non_covid_engagement_values[5] += int(post.num_comm)
                            week_non_covid_post_count[5] += 1
                elif day_of_week == "Sunday":
                    if post.relevant:
                        if engagement_type == "score":
                            week_covid_engagement_values[6] += int(post.score)
                            week_covid_post_count[6] += 1
                        else:
                            week_covid_engagement_values[6] += int(post.num_comm)
                            week_covid_post_count[6] += 1
                    else:
                        if engagement_type == "score":
                            week_non_covid_engagement_values[6] += int(post.score)
                            week_non_covid_post_count[6] += 1
                        else:
                            week_non_covid_engagement_values[6] += int(post.num_comm)
                            week_non_covid_post_count[6] += 1
        tracker.clear()

    week_covid_engagement = list()
    week_non_covid_engagement = list()
    fig = None

    for i in range(7):
        week_covid_engagement.append(week_covid_engagement_values[i] / week_covid_post_count[i])
        if sub_reddit_name == "Coronavirus":
            week_non_covid_engagement.append(0)
        else:
            week_non_covid_engagement.append(week_non_covid_engagement_values[i] / week_non_covid_post_count[i])

    if engagement_type == "score":
        fig = go.Figure(data=[
                        go.Scatter(x=week, y=week_covid_engagement, name="Average Upvotes on Covid Related Posts"),
                        go.Scatter(x=week, y=week_non_covid_engagement, name="Average Upvotes on Non-Covid Related Posts")])

        fig.update_layout(
            title="Daily Average Score for Covid Related or Non-Covid Related Posts - " + sub_reddit_name + ", All Time Filters",
            xaxis_title="Day of Week",
            yaxis_title="Score",
            font=dict(size=20)
        )
    else:
        fig = go.Figure(data=[
            go.Scatter(x=week, y=week_covid_engagement, name="Average Number of Comments on Covid Related Posts"),
            go.Scatter(x=week, y=week_non_covid_engagement, name="Average Number of Comments on Non-Covid Related Posts")])

        fig.update_layout(
            title="Daily Average Number of Comments for Covid Related or Non-Covid Related Posts - " + sub_reddit_name + ", All Time Filters",
            xaxis_title="Day of Week",
            yaxis_title="Comments",
            font=dict(size=20)
        )

    fig.update_xaxes(showgrid=True, gridcolor="rgb(140,140,140)")
    fig.update_yaxes(showgrid=True, gridcolor="rgb(140,140,140)")

    fig.show()


#   Graphs a time series visualization of the average engagement(upvotes or comments) change through each month of the year.
#   Graphs both average engagement for covid vs non-covid posts.


def graph_time_series_engagement_monthly(sub_reddit_name, sub_reddit_dict, engagement_type):
    tracker = dict()

    year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    year_covid_engagement_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    year_covid_post_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    year_non_covid_engagement_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    year_non_covid_post_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for time_key in sub_reddit_dict.keys():
        for post_id in sub_reddit_dict[time_key].keys():
            post = sub_reddit_dict[time_key][post_id]

            if post.title not in tracker.keys():
                tracker[post.title] = 1

                date_data = post.created.strip().split(" ")[0].split("-")
                date = datetime.datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]))
                month = date.strftime("%B").strip()

                if month == "January":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[0] += int(post.score)
                            year_covid_post_count[0] += 1
                        else:
                            year_covid_engagement_values[0] += int(post.num_comm)
                            year_covid_post_count[0] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[0] += int(post.score)
                            year_non_covid_post_count[0] += 1
                        else:
                            year_non_covid_engagement_values[0] += int(post.num_comm)
                            year_non_covid_post_count[0] += 1
                elif month == "February":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[1] += int(post.score)
                            year_covid_post_count[1] += 1
                        else:
                            year_covid_engagement_values[1] += int(post.num_comm)
                            year_covid_post_count[1] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[1] += int(post.score)
                            year_non_covid_post_count[1] += 1
                        else:
                            year_non_covid_engagement_values[1] += int(post.num_comm)
                            year_non_covid_post_count[1] += 1
                elif month == "March":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[2] += int(post.score)
                            year_covid_post_count[2] += 1
                        else:
                            year_covid_engagement_values[2] += int(post.num_comm)
                            year_covid_post_count[2] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[2] += int(post.score)
                            year_non_covid_post_count[2] += 1
                        else:
                            year_non_covid_engagement_values[2] += int(post.num_comm)
                            year_non_covid_post_count[2] += 1
                elif month == "April":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[3] += int(post.score)
                            year_covid_post_count[3] += 1
                        else:
                            year_covid_engagement_values[3] += int(post.num_comm)
                            year_covid_post_count[3] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[3] += int(post.score)
                            year_non_covid_post_count[3] += 1
                        else:
                            year_non_covid_engagement_values[3] += int(post.num_comm)
                            year_non_covid_post_count[3] += 1
                elif month == "May":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[4] += int(post.score)
                            year_covid_post_count[4] += 1
                        else:
                            year_covid_engagement_values[4] += int(post.num_comm)
                            year_covid_post_count[4] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[4] += int(post.score)
                            year_non_covid_post_count[4] += 1
                        else:
                            year_non_covid_engagement_values[4] += int(post.num_comm)
                            year_non_covid_post_count[4] += 1
                elif month == "June":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[5] += int(post.score)
                            year_covid_post_count[5] += 1
                        else:
                            year_covid_engagement_values[5] += int(post.num_comm)
                            year_covid_post_count[5] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[5] += int(post.score)
                            year_non_covid_post_count[5] += 1
                        else:
                            year_non_covid_engagement_values[5] += int(post.num_comm)
                            year_non_covid_post_count[5] += 1
                elif month == "July":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[6] += int(post.score)
                            year_covid_post_count[6] += 1
                        else:
                            year_covid_engagement_values[6] += int(post.num_comm)
                            year_covid_post_count[6] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[6] += int(post.score)
                            year_non_covid_post_count[6] += 1
                        else:
                            year_non_covid_engagement_values[6] += int(post.num_comm)
                            year_non_covid_post_count[6] += 1
                elif month == "August":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[7] += int(post.score)
                            year_covid_post_count[7] += 1
                        else:
                            year_covid_engagement_values[7] += int(post.num_comm)
                            year_covid_post_count[7] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[7] += int(post.score)
                            year_non_covid_post_count[7] += 1
                        else:
                            year_non_covid_engagement_values[7] += int(post.num_comm)
                            year_non_covid_post_count[7] += 1
                elif month == "September":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[8] += int(post.score)
                            year_covid_post_count[8] += 1
                        else:
                            year_covid_engagement_values[8] += int(post.num_comm)
                            year_covid_post_count[8] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[8] += int(post.score)
                            year_non_covid_post_count[8] += 1
                        else:
                            year_non_covid_engagement_values[8] += int(post.num_comm)
                            year_non_covid_post_count[8] += 1
                elif month == "October":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[9] += int(post.score)
                            year_covid_post_count[9] += 1
                        else:
                            year_covid_engagement_values[9] += int(post.num_comm)
                            year_covid_post_count[9] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[9] += int(post.score)
                            year_non_covid_post_count[9] += 1
                        else:
                            year_non_covid_engagement_values[9] += int(post.num_comm)
                            year_non_covid_post_count[9] += 1
                elif month == "November":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[10] += int(post.score)
                            year_covid_post_count[10] += 1
                        else:
                            year_covid_engagement_values[10] += int(post.num_comm)
                            year_covid_post_count[10] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[10] += int(post.score)
                            year_non_covid_post_count[10] += 1
                        else:
                            year_non_covid_engagement_values[10] += int(post.num_comm)
                            year_non_covid_post_count[10] += 1
                elif month == "December":
                    if post.relevant:
                        if engagement_type == "score":
                            year_covid_engagement_values[11] += int(post.score)
                            year_covid_post_count[11] += 1
                        else:
                            year_covid_engagement_values[11] += int(post.num_comm)
                            year_covid_post_count[11] += 1
                    else:
                        if engagement_type == "score":
                            year_non_covid_engagement_values[11] += int(post.score)
                            year_non_covid_post_count[11] += 1
                        else:
                            year_non_covid_engagement_values[11] += int(post.num_comm)
                            year_non_covid_post_count[11] += 1

    year_covid_engagement = list()
    year_non_covid_engagement = list()
    fig = None

    # Calculate the mean of each month
    for i in range(12):
        if year_covid_post_count[i] == 0 or year_non_covid_post_count[i] == 0:
            if year_covid_post_count[i] == 0:
                year_covid_engagement.append(0)
                if sub_reddit_name == "Coronavirus":
                    year_non_covid_engagement.append(0)
                else:
                    year_non_covid_engagement.append(year_non_covid_engagement_values[i] / year_non_covid_post_count[i])
            else:
                year_non_covid_engagement.append(0)
                year_covid_engagement.append(year_covid_engagement_values[i] / year_covid_post_count[i])

        else:
            year_covid_engagement.append(year_covid_engagement_values[i] / year_covid_post_count[i])
            if sub_reddit_name == "Coronavirus":
                year_non_covid_engagement.append(0)
            else:
                year_non_covid_engagement.append(year_non_covid_engagement_values[i] / year_non_covid_post_count[i])

    if engagement_type == "score":
        fig = go.Figure(data=[
                        go.Scatter(x=year, y=year_covid_engagement, name="Average Upvotes on Covid Related Posts"),
                        go.Scatter(x=year, y=year_non_covid_engagement, name="Average Upvotes on Non-Covid Related Posts")])

        fig.update_layout(
            title="Monthly Average Score for Covid Related or Non-Covid Related Posts - " + sub_reddit_name + ", All Time Filters",
            xaxis_title="Month",
            yaxis_title="Score",
            font=dict(size=20)
        )
    else:
        fig = go.Figure(data=[
            go.Scatter(x=year, y=year_covid_engagement, name="Average Number of Comments on Covid Related Posts"),
            go.Scatter(x=year, y=year_non_covid_engagement, name="Average Number of Comments on Non-Covid Related Posts")])

        fig.update_layout(
            title="Monthly Average Number of Comments for Covid Related or Non-Covid Related Posts - " + sub_reddit_name + ", All Time Filters",
            xaxis_title="Month",
            yaxis_title="Comments",
            font=dict(size=20)
        )

    fig.update_xaxes(showgrid=True, gridcolor="rgb(140,140,140)")
    fig.update_yaxes(showgrid=True, gridcolor="rgb(140,140,140)")

    fig.show()


#   Gets user input for which subreddit to generate a graph on.

def choose_subreddit():
    print("\nWhich SubReddit?\n"
          "\t1. Coronavirus\n"
          "\t2. News\n"
          "\t3. Science\n"
          "\t4. WorldNews")

    input1 = input("Enter numeric choice: ")

    if input1 == "1":
        sub_reddit_name = "Coronavirus"
    elif input1 == "2":
        sub_reddit_name = "News"
    elif input1 == "3":
        sub_reddit_name = "Science"
    else:
        sub_reddit_name = "WorldNews"

    return sub_reddit_name


def main():
    coronavirus_dict = dict()
    news_dict = dict()
    science_dict = dict()
    worldnews_dict = dict()

    parse_data("coronavirus", coronavirus_dict)
    parse_data("news", news_dict)
    parse_data("science", science_dict)
    parse_data("worldnews", worldnews_dict)

    data_dict = dict()
    data_dict["Coronavirus"] = coronavirus_dict
    data_dict["News"] = news_dict
    data_dict["Science"] = science_dict
    data_dict["WorldNews"] = worldnews_dict

    print("Pick one of the following visualizations to generate:")
    print("\t1. Pie Chart\n"
          "\t2. Histogram\n"
          "\t3. Time Series")
    input1 = input("Enter numeric choice: ")

    if input1 == "1":
        print("\nPick one of the following pie charts to visualize:\n"
              "\t1. Number of COVID Related Posts\n"
              "\t2. Number of Sources Provided in COVID Related Posts")
        input1 = input("Enter numeric choice: ")

        if input1 == "1":  # Chose number of COVID related posts
            sub_reddit_name = choose_subreddit()
            if sub_reddit_name == "Coronavirus":
                graph_covid_post_count(sub_reddit_name, coronavirus_dict)
            elif sub_reddit_name == "News":
                graph_covid_post_count(sub_reddit_name, news_dict)
            elif sub_reddit_name == "Science":
                graph_covid_post_count(sub_reddit_name, science_dict)
            elif sub_reddit_name == "WorldNews":
                graph_covid_post_count(sub_reddit_name, worldnews_dict)

        elif input1 == "2":  # Chose number of sources provided in covid related posts
            sub_reddit_name = choose_subreddit()
            if sub_reddit_name == "Coronavirus":
                graph_sources_in_covid_posts(sub_reddit_name, coronavirus_dict)
            elif sub_reddit_name == "News":
                graph_sources_in_covid_posts(sub_reddit_name, news_dict)
            elif sub_reddit_name == "Science":
                graph_sources_in_covid_posts(sub_reddit_name, science_dict)
            elif sub_reddit_name == "WorldNews":
                graph_sources_in_covid_posts(sub_reddit_name, worldnews_dict)

    elif input1 == "2":
        print("\nPick one of the following histograms to visualize:\n"
              "\t1. Average Upvotes in Covid Related Posts vs Non-Covid Related Posts\n"
              "\t2. Average Upvotes in Covid Related Posts with/without sources.\n"
              "\t3. Average Number of Comments in Covid Related Posts vs Non-Covid Related Posts\n"
              "\t4. Average Number of Comments in Covid Related Posts with/without sources.")
        input1 = input("Enter numeric choice: ")

        if input1 == "1":
            graph_covid_engagement(data_dict, "score")
        elif input1 == "2":
            graph_covid_source_engagement(data_dict, "score")
        elif input1 == "3":
            graph_covid_engagement(data_dict, "comments")
        elif input1 == "4":
            graph_covid_source_engagement(data_dict, "comments")
    elif input1 == "3":
        print("\nPick one of the following time series to visualize:\n"
              "\t1. Average Daily Upvotes in Covid Related Posts\n"
              "\t2. Average Daily Number of Comments in Covid Related Posts\n"
              "\t3. Average Monthly Upvotes in Covid Related Posts\n"
              "\t4. Average Montly Number of Comments in Covid Related Posts")
        input1 = input("Enter numeric choice: ")
        sub_reddit_name = choose_subreddit()

        if input1 == "1":
            if sub_reddit_name == "Coronavirus":
                graph_time_series_engagement_daily(sub_reddit_name, coronavirus_dict, "score")
            elif sub_reddit_name == "News":
                graph_time_series_engagement_daily(sub_reddit_name, news_dict, "score")
            elif sub_reddit_name == "Science":
                graph_time_series_engagement_daily(sub_reddit_name, science_dict, "score")
            elif sub_reddit_name == "WorldNews":
                graph_time_series_engagement_daily(sub_reddit_name, worldnews_dict, "score")
        if input1 == "2":
            if sub_reddit_name == "Coronavirus":
                graph_time_series_engagement_daily(sub_reddit_name, coronavirus_dict, "comments")
            elif sub_reddit_name == "News":
                graph_time_series_engagement_daily(sub_reddit_name, news_dict, "comments")
            elif sub_reddit_name == "Science":
                graph_time_series_engagement_daily(sub_reddit_name, science_dict, "comments")
            elif sub_reddit_name == "WorldNews":
                graph_time_series_engagement_daily(sub_reddit_name, worldnews_dict, "comments")
        if input1 == "3":
            if sub_reddit_name == "Coronavirus":
                graph_time_series_engagement_monthly(sub_reddit_name, coronavirus_dict, "score")
            elif sub_reddit_name == "News":
                graph_time_series_engagement_monthly(sub_reddit_name, news_dict, "score")
            elif sub_reddit_name == "Science":
                graph_time_series_engagement_monthly(sub_reddit_name, science_dict, "score")
            elif sub_reddit_name == "WorldNews":
                graph_time_series_engagement_monthly(sub_reddit_name, worldnews_dict, "score")
        if input1 == "4":
            if sub_reddit_name == "Coronavirus":
                graph_time_series_engagement_monthly(sub_reddit_name, coronavirus_dict, "comments")
            elif sub_reddit_name == "News":
                graph_time_series_engagement_monthly(sub_reddit_name, news_dict, "comments")
            elif sub_reddit_name == "Science":
                graph_time_series_engagement_monthly(sub_reddit_name, science_dict, "comments")
            elif sub_reddit_name == "WorldNews":
                graph_time_series_engagement_monthly(sub_reddit_name, worldnews_dict, "comments")

    # UNCOMMENT THIS CODE TO REWRITE THE DATA_DICTIONARY.TXT FILE AGAIN
    # file = open("data/data_dictionary.txt", mode="w", encoding="utf8")
    #
    # file.write(
    #     "========================================== r/Coronavirus Data ==========================================\n")
    # for dict_name in coronavirus_dict.keys():
    #     file.write("Sorted by: " + dict_name)
    #     for key in sorted(coronavirus_dict[dict_name].keys()):
    #         file.write("\n\t\t\tTitle: " + coronavirus_dict[dict_name][key].title +
    #                    "\n\t\t\tScore: " + str(coronavirus_dict[dict_name][key].score) +
    #                    "\n\t\t\tNumber of Comments: " + str(coronavirus_dict[dict_name][key].num_comm) +
    #                    "\n\t\t\tDate Created: " + coronavirus_dict[dict_name][key].created +
    #                    "\n\t\t\tPost Content: " + coronavirus_dict[dict_name][key].content +
    #                    "\n\t\t\tCOVID Related?: " + str(coronavirus_dict[dict_name][key].relevant) +
    #                    "\n\t\t\tSources: " + str(coronavirus_dict[dict_name][key].sources) + "\n")
    #
    # file.write("========================================== r/News Data ==========================================\n")
    # for dict_name in news_dict.keys():
    #     file.write("Sorted by: " + dict_name)
    #     for key in sorted(news_dict[dict_name].keys()):
    #         file.write("\n\t\t\tTitle: " + news_dict[dict_name][key].title +
    #                    "\n\t\t\tScore: " + str(news_dict[dict_name][key].score) +
    #                    "\n\t\t\tNumber of Comments: " + str(news_dict[dict_name][key].num_comm) +
    #                    "\n\t\t\tDate Created: " + news_dict[dict_name][key].created +
    #                    "\n\t\t\tPost Content: " + news_dict[dict_name][key].content +
    #                    "\n\t\t\tCOVID Related?: " + str(news_dict[dict_name][key].relevant) +
    #                    "\n\t\t\tSource: " + str(news_dict[dict_name][key].sources) + "\n")
    #
    # file.write("========================================== r/Science Data ==========================================\n")
    # for dict_name in science_dict.keys():
    #     file.write("Sorted by: " + dict_name)
    #     for key in sorted(science_dict[dict_name].keys()):
    #         file.write("\n\t\t\tTitle: " + science_dict[dict_name][key].title +
    #                    "\n\t\t\tScore: " + str(science_dict[dict_name][key].score) +
    #                    "\n\t\t\tNumber of Comments: " + str(science_dict[dict_name][key].num_comm) +
    #                    "\n\t\t\tDate Created: " + science_dict[dict_name][key].created +
    #                    "\n\t\t\tPost Content: " + science_dict[dict_name][key].content +
    #                    "\n\t\t\tCOVID Related?: " + str(science_dict[dict_name][key].relevant) +
    #                    "\n\t\t\tSource: " + str(science_dict[dict_name][key].sources) + "\n")
    #
    # file.write(
    #     "========================================== r/WorldNews Data ==========================================\n")
    # for dict_name in worldnews_dict.keys():
    #     file.write("Sorted by: " + dict_name)
    #     for key in sorted(worldnews_dict[dict_name].keys()):
    #         file.write("\n\t\t\tTitle: " + worldnews_dict[dict_name][key].title +
    #                    "\n\t\t\tScore: " + str(worldnews_dict[dict_name][key].score) +
    #                    "\n\t\t\tNumber of Comments: " + str(worldnews_dict[dict_name][key].num_comm) +
    #                    "\n\t\t\tDate Created: " + worldnews_dict[dict_name][key].created +
    #                    "\n\t\t\tPost Content: " + worldnews_dict[dict_name][key].content +
    #                    "\n\t\t\tCOVID Related?: " + str(worldnews_dict[dict_name][key].relevant) +
    #                    "\n\t\t\tSource: " + str(worldnews_dict[dict_name][key].sources) + "\n")


if __name__ == '__main__':
    main()
