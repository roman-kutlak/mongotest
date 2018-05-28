import os
import pymongo
import threading
import time


class Tailer(threading.Thread):
    terminated = False

    def __init__(self, connection_str):
        super().__init__()
        self.lock = threading.Lock()
        self.connection_str = connection_str

    def run(self):
        client = pymongo.MongoClient(self.connection_str)
        db = client.test
        cursor = db.logs.watch(max_await_time_ms=1000)
        print('Tailing collection logs"')
        while True:
            with self.lock:
                if self.terminated:
                    break
            entry = next(cursor)
            if entry:
                print('{}: {}'.format(entry['operationType'], entry['fullDocument']))

    def stop(self):
        with self.lock:
            self.terminated = True


def main(connection_str):
    client = pymongo.MongoClient(connection_str)
    db = client.test  # use database test
    tailer = Tailer(connection_str)
    tailer.setDaemon(True)
    tailer.start()
    time.sleep(5)
    print('Inserting first')
    db.logs.insert_one({"message": "First log message"})
    print('Inserting second')
    db.logs.insert_one({"message": "Second log message"})
    print('Inserting third')
    db.logs.insert_one({"message": "Third log message"})
    tailer.stop()
    db.logs.insert_one({"message": "flush"})
    tailer.join()


if __name__ == '__main__':
    host = os.environ['MONGO_HOST']
    username = os.environ['MONGO_USERNAME']
    password = os.environ['MONGO_PASSWORD']
    main(f'mongodb+srv://{username}:{password}@{host}/?retryWrites=true')
