import pymongo


class Client(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.db = self.client["eol"]
        self.collection = self.db["school_1"]

    def get_school(self):
        items = self.collection.find()
        schools = list(item.get("school_number") for item in items)
        return schools

    def close(self):
        self.client.close()

    def main(self):
        schools = self.get_school()
        self.close()
        return schools


def main():
    obj = Client()
    schools = obj.main()
    with open("schools", "w") as f:
        f.write(str(schools))


if __name__ == '__main__':
    main()
