import pyaudio
import wave
from threading import Thread, Lock, Event
from typing import List
from loguru import logger


class Recorder(object):

    def __init__(self, *, channels: int = 2, format: int = pyaudio.paInt16, freq: int = 48000, chunksize=1024):

        self.engine = pyaudio.PyAudio()

        self.format = format
        self.channels = channels
        self.rate = freq
        self.chunksize = chunksize

        self.buffer: List[bytes] = []

    def info(self):

        for index in range(self.engine.get_host_api_count()):
            logger.info(self.engine.get_host_api_info_by_index(index))

    def get(self, *, secs: int = 1):
        stream = self.engine.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  input_device_index=0,
                                  frames_per_buffer=self.chunksize)
        logger.info('Start')
        self.buffer.clear()
        for a in range(int(self.rate / self.chunksize * secs)):
            data = stream.read(self.chunksize)
            self.buffer.append(data)
            logger.debug(a)

        stream.stop_stream()
        stream.close()

        # print(result)

        with wave.open('sample.wav', 'wb') as f:
            f.setnchannels(self.channels)
            f.setsampwidth(self.engine.get_sample_size(self.format))
            f.setframerate(self.rate)
            sound = b''.join(self.buffer)
            f.writeframes(sound)
            logger.debug('saved %d bytes' % len(sound))


if __name__ == '__main__':

    '''
    48000Hz x 2ch = 96000(word) x 10 = 960000(word)
    '''

    recorder = Recorder(chunksize=1024)

    recorder.get(secs=10)
