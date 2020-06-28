import os
from shutil import copyfile
import subprocess
import time
from mido import MidiFile
from multiprocessing import Process, Queue
import music21
import signal
import queue

class MIDIRecorder:
    playing = False
    recording = False
    looping = False
    Factor = 1
    playid = 0
    n_track = 0

    playing_process = None
    looping_process = None
    looping_popen_queue = None
    recording_process = None
    recording = False

    def __init__(self, mididir, midiplayport, midirecordport, maxtracks, \
            loop_tweak, test_mode=False):
        # TODO: assert mididir is a valid path, and the
        # ports are described by valid strings

        self.mididir = mididir
        self.midiplayport = midiplayport
        self.midirecordport = midirecordport
        self.maxtracks = maxtracks
        self.loop_tweak = loop_tweak
        self.test_mode = test_mode

        # TODO: parse music21 scores here
        def generate_score(n):
            path = os.path.join(self.mididir, f'track-{n}.mid')
            if os.path.isfile(path):
                try:
                    return music21.converter.parse(path)
                except:
                    return None
            else:
                return None
        
        # (score, scale_factor) tuple
        self.scores = [(generate_score(n), 1) for n in range(maxtracks)]

    def _is_playing(self):
        if self.playing_process is None:
            return False
        return self.playing_process.poll() is None

    def _play_file(self):
        current_file = os.path.join(self.mididir, f'track-{self.n_track}.mid')
        if self.test_mode:
            command = ['vlc', '/home/edd/tmp/output2.mp4']
        else:
            command = ['aplaymidi', '-p', str(self.midiplayport), \
                    str(current_file)]
        self.playing_process = subprocess.Popen(command)
                
    def _stop_play_file(self):
        if self.playing_process is not None:
            self.playing_process.terminate()
            self.playing_process = None

    def _is_recording(self):
        if self.recording_process is None:
            return False
        
        recording = self.recording_process.poll() is None
        if not recording and self.recording:
            # Reparse the score
            try:
                self.scores[self.n_track] = (music21.converter.parse(path), 1)
            except:
                pass
            self.recording = False
        return recording

    def _record_file(self):
        path = f'track-{self.n_track}.mid'
        current_file = os.path.join(self.mididir, path)
        if self.test_mode:
            command = ['vlc', '/home/edd/tmp/output1.mp4']
        else:
            command = ['arecordmidi', '-p', str(self.midiplayport), \
                    str(current_file)]
        self.recording_process = subprocess.Popen(command)
        self.recording = True

    def _stop_record_file(self):
        path = os.path.join(self.mididir, f'track-{self.n_track}.mid')
        if self.recording_process is not None:
            self.recording_process.terminate()
            self.recording_process = None

            # Reparse the score
            self.scores[self.n_track] = (music21.converter.parse(path), 1)
            self.recording = False

    def _is_looping(self):
        return self.looping_process is not None

    def _loop_file(self):
        path = os.path.join(self.mididir, f'track-{self.n_track}.mid')
        time_to_sleep = MidiFile(path).length + self.loop_tweak
        command = ['aplaymidi', '-p', str(self.midiplayport), \
                str(path)]

        def loop(t, command, q):
            while True:
                time.sleep(t)
                q.put(subprocess.Popen(command).pid)

        # Create some shared memory
        self.looping_popen_queue = Queue()
        self.looping_process = Process(target=loop, args=(time_to_sleep, \
                command, self.looping_popen_queue))
        self.looping_popen_queue.put(subprocess.Popen(command).pid)
        self.looping_process.start()

    def _stop_loop_file(self):
        if self.looping_process is not None:
            self.looping_process.kill()
            # Dequeue and stop all Popens
            while True:
                try:
                    popen = self.looping_popen_queue.get(block=False)
                except queue.Empty:
                    break
                else:
                    os.kill(popen, signal.SIGTERM)

            self.looping_process = None

    def toggle_play(self, channel):
        if self._is_playing():
            self._stop_play_file()
        elif not self._is_recording() and not self._is_looping():
            self._play_file()

    def toggle_record(self, channel):
        if self._is_recording():
            self._stop_record_file()
        elif not self._is_playing() and not self._is_looping():
            self._record_file()

    def toggle_loop(self, channel):
        if self._is_looping():
            self._stop_loop_file()
        elif not self._is_playing() and not self._is_recording():
            self._loop_file()

    def change_track(self, n_track):
        if n_track < 0 or n_track >= self.maxtracks:
            raise ValueError("Track number out of range")
        if not self._is_playing() and not self._is_recording() \
                and not self._is_looping():
            self.n_track = n_track

    def change_speed(self, factor):
        (score, existing_factor) = self.scores[self.n_track]
        new_factor = existing_factor * factor
        self.scores[self.n_track] = (score, new_factor)

        if score is not None:
            new_score = score.scaleOffsets(new_factor).scaleDurations(new_factor)
            new_score.write('midi', \
                os.path.join(self.mididir, f'track-{self.n_track}.mid'))
        
    def change_absolute_speed(self, factor):
        (score, existing_factor) = self.scores[self.n_track]
        self.scores[self.n_track] = (score, factor)

        if score is not None:
            new_score = score.scaleOffsets(factor).scaleDurations(factor)
            new_score.write('midi', \
                os.path.join(self.mididir, f'track-{self.n_track}.mid'))
