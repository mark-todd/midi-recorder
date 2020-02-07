import os
from shutil import copyfile
import subprocess
import time
from mido import MidiFile
from multiprocessing import Process
import music21
import sys


class MIDIRecorder:
        playing = False
        recording = False
        looping = False
        Factor = 1
        playid = 0
        ntrack = 0
        ntrackcurrent = 0

        mididir = None
        midiplayport = None
        midirecordport = None
        maxtracks = None
        looptweak = None
        scores = None

        playingprocess = None
        loopprocess = None

        # mididir - directory midi files are saved and transformed in
        # midiplayport - 
        # midirecordport -


        def __init__(self, mididir, midiplayport, midirecordport, maxtracks, looptweak):
                # TODO: assert mididir is a valid path, and the
                # ports are described by valid strings

                self.mididir = mididir
                self.midiplayport = midiplayport
                self.midirecordport = midirecordport
                self.maxtracks = maxtracks
                self.looptweak = looptweak
                self.scores = [None]*maxtracks

        # Return the path to the file we care about
        def _currentfile(self, basefile):
                if basefile:
                        return os.path.join(self.mididir, "track-" + str(self.ntrack) + ".mid")
                else:
                        return os.path.join(self.mididir, "output.mid")

        def _run(self, command):
                return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

        def _kill(self, process):
                try:
                        os.killpg(os.getpgid(process.pid), signal=SIGTERM)
                except:
                        pass


        def _playfile(self):
                playingprocess = self._run("aplaymidi -p " + self.midiplayport + " " + self._currentfile(False))


        def _stopfile(self):
                self._kill(playingprocess)
                playingprocess = None

        def _recordfile(self):
                playingprocess = self._run("arecordmidi -p " + self.midirecordport + " " + self._currentfile(True))
                # Generate the score
                score[self.ntrack] = music21.converter.parse(self._currentfile(True))
                newscore.write("midi", self._currentfile(False))

        def _sleepandcall(self, t):
                while True:
                        time.sleep(t)
                        self._playfile()

        def _getmidilength(self, basefile):
                return MidiFile(self._currentfile(basefile)).length


        def _loopfile(self):
                timetosleep = self._getmidilength(False) - self.looptweak
                self.loopprocess = Process(target=self._sleepandcall, args=(timetosleep,))
                self.loopprocess.start()

        def _stoploopfile(self):
                self.loopprocess.terminate()
                self._stopfile()


        def toggleplay(self):
                if self.playing:
                        self._stopfile()
                        self.playing = False
                        self.ntrack = self.ntrackcurr
                elif not self.recording and not self.looping:
                        self._playfile()
                        self.playing = True

        def togglerecord(self):
                if self.recording:
                        self._stopfile()
                        self.recording = False
                        self.ntrack = self.ntrackcurr
                elif not self.playing and not self.looping:
                        self._recordfile()
                        self.recording = True

        def toggleloop(self):
                if self.looping:
                        self._stoploopfile()
                        self.looping = False
                        self.ntrack = self.ntrackcurr
                elif not self.playing and not self.recording:
                        self._loopfile()
                        self.looping = True

        def changetrack(self, ntrack):
                assert(ntrack => 0 and ntrack < self.maxtracks)
                if not self.playing and not self.recording and not self.looping:
                        self.ntrack = ntrack

                self.ntrackcurr = ntrack

        def changespeed(self, factor):
                if scores == None:
                        print("Can't import empty score!")
                        sys.exit(1)

                self.scores[self.ntrack].scaleOffsets(factor).scaleDurations(factor)
                newscore.write("midi", self._currentfile(False))
                
