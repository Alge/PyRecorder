#!/usr/bin/env python3

import sounddevice as sd
import soundfile as sf
import queue
import os
import threading

class Recorder:

    def __init__(self):
        self.is_recording = False
        self.message_queue = queue.Queue()
        self.rt = None

    def record(self, filename):
        if self.is_recording:
            raise Exception("Already recording")
        self.rt = self.RecorderThread(self.message_queue, outfile=filename)
        self.rt.start()
        self.is_recording = True

    def stop_recording(self):
        if not self.is_recording:
            raise Exception("Not recording at the moment")
        self.message_queue.put("plz stop or something...")
        self.rt.join()
        self.is_recording = False


    class RecorderThread(threading.Thread):
        def __init__(self, message_queue, sample_rate=44100, channels=2, q=queue.Queue(), outfile = "out.wav", ):
            threading.Thread.__init__(self)
            self.sample_rate = sample_rate
            self.channels = channels
            self.q = q
            self.outfile = outfile
            self.message_queue = message_queue

        def run(self):
            # Delete the output file if it exists
            if os.path.isfile(self.outfile):
                os.remove(self.outfile)

            with sf.SoundFile(self.outfile, mode='x', samplerate=self.sample_rate, channels=self.channels) as file:
                with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self.recording_callback) as input_stream:
                    while self.message_queue.empty():
                        #print("queue empty")
                        file.write(self.q.get())
                    print("got something in the queue")
                    input_stream.stop()
                    print("streamed supposed to be stopped now")

        def recording_callback(self, indata, frames, time, status):
            #print("got something! frames: {} time: {}, status: {}".format(frames, time, status))
            self.q.put(indata.copy())
            return False
