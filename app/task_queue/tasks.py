from app import celery
import random


@celery.task
def random_numbers():
    arr = []
    for i in range(10000):
        arr.append(random.randint(0, 100))

    return arr
