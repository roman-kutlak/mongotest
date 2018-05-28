import os
import pymongo


def main(connection_str):
    client = pymongo.MongoClient(connection_str)
    db = client.test  # use database test
    print(list(db.person.find()))
    r = db.person.insert_one({
        "name": "Roman",
        "address": {
            "town": "Oxford"
        }
    })
    print(r.inserted_id)
    print(list(db.person.find({"address.town": "Oxford"})))
    r = db.person.delete_one({"name": "Roman"})
    print(r.deleted_count)


if __name__ == '__main__':
    host = os.environ['MONGO_HOST']
    username = os.environ['MONGO_USERNAME']
    password = os.environ['MONGO_PASSWORD']
    main(f'mongodb+srv://{username}:{password}@{host}/?retryWrites=true')
