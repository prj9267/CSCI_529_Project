"""
authors: Parker, Anthony, Drake, Grace
description: Parses through tsv files and graphs data that was gathered from Reddit

Current Function: Parses through tsv files and stores the data in Post objects.
TODO: Improve data gathered (?) and set up graphs.
"""
import re
import csv


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


def main():
    coronavirus_dict = dict()
    news_dict = dict()
    science_dict = dict()
    worldnews_dict = dict()

    parse_data("coronavirus", coronavirus_dict)
    parse_data("news", news_dict)
    parse_data("science", science_dict)
    parse_data("worldnews", worldnews_dict)

    file = open("data/data_dictionary.txt", mode="w", encoding="utf8")

    file.write(
        "========================================== r/Coronavirus Data ==========================================\n")
    for dict_name in coronavirus_dict.keys():
        file.write("Sorted by: " + dict_name)
        for key in sorted(coronavirus_dict[dict_name].keys()):
            file.write("\n\t\t\tTitle: " + coronavirus_dict[dict_name][key].title +
                       "\n\t\t\tScore: " + str(coronavirus_dict[dict_name][key].score) +
                       "\n\t\t\tNumber of Comments: " + str(coronavirus_dict[dict_name][key].num_comm) +
                       "\n\t\t\tDate Created: " + coronavirus_dict[dict_name][key].created +
                       "\n\t\t\tPost Content: " + coronavirus_dict[dict_name][key].content +
                       "\n\t\t\tCOVID Related?: " + str(coronavirus_dict[dict_name][key].relevant) +
                       "\n\t\t\tSources: " + str(coronavirus_dict[dict_name][key].sources) + "\n")

    file.write("========================================== r/News Data ==========================================\n")
    for dict_name in news_dict.keys():
        file.write("Sorted by: " + dict_name)
        for key in sorted(news_dict[dict_name].keys()):
            file.write("\n\t\t\tTitle: " + news_dict[dict_name][key].title +
                       "\n\t\t\tScore: " + str(news_dict[dict_name][key].score) +
                       "\n\t\t\tNumber of Comments: " + str(news_dict[dict_name][key].num_comm) +
                       "\n\t\t\tDate Created: " + news_dict[dict_name][key].created +
                       "\n\t\t\tPost Content: " + news_dict[dict_name][key].content +
                       "\n\t\t\tCOVID Related?: " + str(news_dict[dict_name][key].relevant) +
                       "\n\t\t\tSource: " + str(news_dict[dict_name][key].sources) + "\n")

    file.write("========================================== r/Science Data ==========================================\n")
    for dict_name in science_dict.keys():
        file.write("Sorted by: " + dict_name)
        for key in sorted(science_dict[dict_name].keys()):
            file.write("\n\t\t\tTitle: " + science_dict[dict_name][key].title +
                       "\n\t\t\tScore: " + str(science_dict[dict_name][key].score) +
                       "\n\t\t\tNumber of Comments: " + str(science_dict[dict_name][key].num_comm) +
                       "\n\t\t\tDate Created: " + science_dict[dict_name][key].created +
                       "\n\t\t\tPost Content: " + science_dict[dict_name][key].content +
                       "\n\t\t\tCOVID Related?: " + str(science_dict[dict_name][key].relevant) +
                       "\n\t\t\tSource: " + str(science_dict[dict_name][key].sources) + "\n")

    file.write(
        "========================================== r/WorldNews Data ==========================================\n")
    for dict_name in worldnews_dict.keys():
        file.write("Sorted by: " + dict_name)
        for key in sorted(worldnews_dict[dict_name].keys()):
            file.write("\n\t\t\tTitle: " + worldnews_dict[dict_name][key].title +
                       "\n\t\t\tScore: " + str(worldnews_dict[dict_name][key].score) +
                       "\n\t\t\tNumber of Comments: " + str(worldnews_dict[dict_name][key].num_comm) +
                       "\n\t\t\tDate Created: " + worldnews_dict[dict_name][key].created +
                       "\n\t\t\tPost Content: " + worldnews_dict[dict_name][key].content +
                       "\n\t\t\tCOVID Related?: " + str(worldnews_dict[dict_name][key].relevant) +
                       "\n\t\t\tSource: " + str(worldnews_dict[dict_name][key].sources) + "\n")


if __name__ == '__main__':
    main()
