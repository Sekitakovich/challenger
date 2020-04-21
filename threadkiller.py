from threading import Thread
import time


class Sample(Thread):

    def __init__(self):

        super().__init__()
        self.daemon = True

    def __del__(self):

        print('Bye!')

    def run(self) -> None:
        counter: int = 0
        while True:
            try:
                print(self.name, counter)
            except KeyboardInterrupt as e:
                print(e)
                break
            else:
                counter += 1
                time.sleep(1)


if __name__ == '__main__':

    s = Sample()
    s.start()

    for t in range(6):
        time.sleep(1)

    # del s

    try:
        raise (KeyboardInterrupt)
    except KeyboardInterrupt as e:
        pass
    else:
        time.sleep(3)
