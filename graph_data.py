"""
authors: Parker, Anthony, Drake, Grace
description: Parses through tsv files and graphs data that was gathered from Reddit

Current Function: Parses through tsv files and stores the data in Post objects.
TODO: Improve data gathered (?) and set up graphs.
"""
import re


class Post:

    def __init__(self):
        self.id = None
        self.title = ""
        self.score = 0
        self.num_comm = 0
        self.created = ""
        self.content = ""
        self.relevant = False

    def __eq__(self, other):
        if self.title == other.title and self.content == other.content:
            return True
        return False


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
        file = open("data/original/" + file_name, encoding="utf8")
        cols = file.readline()

        line = file.readline()
        post_count = 0
        while line != "":
            post_data = line.strip().split("\t")

            # Skipping the blank lines generated by the TSV writer
            if len(post_data) > 1:
                post_count += 1
                post = Post()

                post.id = post_count
                post.title = post_data[0]
                post.score = post_data[1]
                post.num_comm = post_data[2]
                post.created = post_data[3]

                # All posts in r/Coronavirus are related to COVID-19
                if sub_reddit_name == "coronavirus":
                    post.relevant = True
                # Search the title for keywords
                elif re.search("coronavirus", post.title, re.IGNORECASE) or \
                     re.search("covid", post.title, re.IGNORECASE) or \
                     re.search("sars-cov-2", post.title, re.IGNORECASE) or \
                     re.search("pandemic", post.title, re.IGNORECASE) or \
                     re.search("virus", post.title, re.IGNORECASE):
                    post.relevant = True

                # If the post doesn't have text content.  Most likely an image.
                if len(post_data) == 5:
                    post.content = post_data[4]

                    # Search the content for keywords
                    if re.search("coronavirus", post.content, re.IGNORECASE) or \
                       re.search("covid", post.content, re.IGNORECASE) or \
                       re.search("sars-cov-2", post.content, re.IGNORECASE) or \
                       re.search("pandemic", post.content, re.IGNORECASE) or \
                       re.search("virus", post.content, re.IGNORECASE):
                        post.relevant = True

                if file_name == file_list[0]:
                    sub_reddit_dict["all_time"][post.id] = post
                elif file_name == file_list[1]:
                    sub_reddit_dict["day"][post.id] = post
                elif file_name == file_list[2]:
                    sub_reddit_dict["month"][post.id] = post
                elif file_name == file_list[3]:
                    sub_reddit_dict["week"][post.id] = post

            line = file.readline()


def main():
    coronavirus_dict = dict()
    news_dict = dict()
    science_dict = dict()
    worldnews_dict = dict()

    parse_data("coronavirus", coronavirus_dict)
    parse_data("news", news_dict)
    parse_data("science", science_dict)
    parse_data("worldnews", worldnews_dict)

    print("========================================== r/Coronavirus Data ==========================================\n")
    for dict_name in coronavirus_dict.keys():
        print("Sorted by: " + dict_name)
        for key in sorted(coronavirus_dict[dict_name].keys()):
            print("\n\t\t\tTitle: " + coronavirus_dict[dict_name][key].title +
                  "\n\t\t\tScore: " + str(coronavirus_dict[dict_name][key].score) +
                  "\n\t\t\tNumber of Comments: " + str(coronavirus_dict[dict_name][key].num_comm) +
                  "\n\t\t\tDate Created: " + coronavirus_dict[dict_name][key].created +
                  "\n\t\t\tPost Content: " + coronavirus_dict[dict_name][key].content +
                  "\n\t\t\tCOVID Related?: " + str(coronavirus_dict[dict_name][key].relevant))

    print("========================================== r/News Data ==========================================\n")
    for dict_name in news_dict.keys():
        print("Sorted by: " + dict_name)
        for key in sorted(news_dict[dict_name].keys()):
            print("\n\t\t\tTitle: " + news_dict[dict_name][key].title +
                  "\n\t\t\tScore: " + str(news_dict[dict_name][key].score) +
                  "\n\t\t\tNumber of Comments: " + str(news_dict[dict_name][key].num_comm) +
                  "\n\t\t\tDate Created: " + news_dict[dict_name][key].created +
                  "\n\t\t\tPost Content: " + news_dict[dict_name][key].content +
                  "\n\t\t\tCOVID Related?: " + str(news_dict[dict_name][key].relevant))

    print("========================================== r/Science Data ==========================================\n")
    for dict_name in science_dict.keys():
        print("Sorted by: " + dict_name)
        for key in sorted(science_dict[dict_name].keys()):
            print("\n\t\t\tTitle: " + science_dict[dict_name][key].title +
                  "\n\t\t\tScore: " + str(science_dict[dict_name][key].score) +
                  "\n\t\t\tNumber of Comments: " + str(science_dict[dict_name][key].num_comm) +
                  "\n\t\t\tDate Created: " + science_dict[dict_name][key].created +
                  "\n\t\t\tPost Content: " + science_dict[dict_name][key].content +
                  "\n\t\t\tCOVID Related?: " + str(science_dict[dict_name][key].relevant))

    print("========================================== r/WorldNews Data ==========================================\n")
    for dict_name in worldnews_dict.keys():
        print("Sorted by: " + dict_name)
        for key in sorted(worldnews_dict[dict_name].keys()):
            print("\n\t\t\tTitle: " + worldnews_dict[dict_name][key].title +
                  "\n\t\t\tScore: " + str(worldnews_dict[dict_name][key].score) +
                  "\n\t\t\tNumber of Comments: " + str(worldnews_dict[dict_name][key].num_comm) +
                  "\n\t\t\tDate Created: " + worldnews_dict[dict_name][key].created +
                  "\n\t\t\tPost Content: " + worldnews_dict[dict_name][key].content +
                  "\n\t\t\tCOVID Related?: " + str(worldnews_dict[dict_name][key].relevant))


if __name__ == '__main__':
    main()
