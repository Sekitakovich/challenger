[Howto]

import EventPlus

(simplecase)

sender thread: 
    EventPlus.set(value=1)  # value is any

waiter thread:
    result = EventPlust.wait()
    print(result.value)

(nextstep)

sender thread:
    EventPlus.set(value=['How', 'are', 'you?'], sender=100, channel='sample')

waiter thread:
    result = EventPlust.wait(timeout=5, channel='sample')
    if result.valid:
        data = result.value
    else:
        print('timeout!')
