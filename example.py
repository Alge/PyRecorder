import soundrecorder
import time

r = soundrecorder.Recorder()
print("Starting to record now")
r.record("out.wav")
time.sleep(5)
r.stop_recording()
print("done")
