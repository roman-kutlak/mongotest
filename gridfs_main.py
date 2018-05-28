import os, gridfs, pymongo
from pprint import pprint

def main(connection_str):
    client = pymongo.MongoClient(connection_str)
    db = client.test  # use database test
    fs = gridfs.GridFS(db)
    a = fs.put(b"hello world", filename="test.txt", chunk_size=6)
    print(fs.get(a).read())
    pprint(list(db.fs.chunks.find()))


if __name__ == '__main__':
    host = os.environ['MONGO_HOST']
    username = os.environ['MONGO_USERNAME']
    password = os.environ['MONGO_PASSWORD']
    main(f'mongodb+srv://{username}:{password}@{host}/?retryWrites=true')
