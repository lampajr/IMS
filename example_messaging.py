from pubsub import pub

topic = "main"


def listener1(arg1, arg2, arg3):
    print('Function listener1 received:')
    print('  arg1 =', arg1)
    print('  arg2 =', arg2)
    arg3()


def listener2(arg1, arg2, arg3):
    print('Function listener2 received:')
    print('  arg1 =', arg1)
    print('  arg2 =', arg2)
    arg3()


pub.subscribe(listener1, topic)
pub.subscribe(listener2, topic)

print('Publishing something on ', topic, ' topic:')
an_obj = dict(a=435, b='proof')


def print_hello():
    print('hello')


pub.sendMessage(topic, arg1=12, arg2=an_obj, arg3=print_hello)
