[Simple case]

import EventPlus

sender thread: EventPlus.set(value=1)  # value is any

waiter thread: result = EventPlust.wait()

see EventPlus.set and EventPlus.get!