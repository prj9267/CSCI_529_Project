class Post:

    def __init__(self):
        self.title = ""
        self.score = 0
        self.num_comm = 0
        self.created = ""
        self.content = ""

    def __eq__(self, other):
        if self.title == other.title and self.content == other.content:
            return True
        return False

def main():
    return 0


if __name__ == '__main__':
    main()