import gevent
import random

def task(pid):
    """
    some task
    """
    gevent.sleep(random.randint(0, 2)*0.001)
    print 'Task', pid, 'done'


def syn():
    for i in xrange(1, 10):
        task(i)


def asy():
    threads = [gevent.spawn(task, i) for i in xrange(10)]
    gevent.joinall(threads)

print 'syn'
syn()

print 'asy'
asy()