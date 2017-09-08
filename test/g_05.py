import gevent
from gevent.event import AsyncResult

a = AsyncResult()


def setter():
    gevent.sleep(3)
    a.set()


def waiter():
    a.get()
    print 'I live!'

gevent.joinall([
    gevent.spawn(setter),
    gevent.spawn(waiter),
])
