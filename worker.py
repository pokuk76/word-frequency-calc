import os

import redis

from rq import Worker, Queue, Connection

listen = ['default']    # Listen for a queue called default

''' Establish connection to Redis server on localhost:6379 '''
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
