import pickle

def create_or_load_pickle(data_path, create_func, create_new=False):
    try:
        if create_new: raise FileNotFoundError
        with open(data_path, "rb") as f:
            obj = pickle.load(f)
            print(data_path, "was loaded from the pickle file.")
    except FileNotFoundError:
        obj = create_func()
        with open(data_path, "wb") as f:
            pickle.dump(obj, f)
        print(f"New pickle file {data_path} created.")
    
    return obj

import warnings
def ignore_warnings():
    warnings.filterwarnings('ignore')

def p(*args):
    print(*args)

import platform
def play_beep(self, dur=1, freq=880):
    if platform.system() == "Windows":
        # Windowsの場合は、winsoundというPython標準ライブラリを使います.
        import winsound
        winsound.Beep(freq, dur * 1000)
    else:
        # Macの場合には、soxをbrewでインストールすることで使えるようになるplayコマンドを使います.
        import os
        os.system(f'play -n synth {dur} sin {freq}')


import threading, time
import numpy as np
from IPython.display import clear_output

class ProgressReporter: 
    def start(self, iterator, iter_func, interval=5.0, progress=1, finish_sound=True):
        self.start_time = time.time()
        self.iterator = iterator
        self.iter_func=iter_func
        self.current_progress = 0
        self.complete_progress = len(iterator)
        self.interval = interval
        self.progress = progress
        self.finish_sound = finish_sound
        
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._report)
        self._thread.setDaemon(True)
        self._thread.start()
        
        self._iteration()
    
    def stop(self):
        self._stop_event.set()
        
    def complete(self):
        self.current_progress = self.complete_progress

    # override if you prefer
    def _display(self):
        elapsed = (time.time() - self.start_time)
        speed = self.current_progress / elapsed
        try:
            rest = self.complete_progress / speed - elapsed
        except ZeroDivisionError:
            rest = np.nan
        
        print(f"Current progress: {self.current_progress} / {self.complete_progress}, {elapsed:.2f} [sec] elapsed")
        print(f"Speed of the progress: {speed:.2f} [item/sec]. The task will be finished in {rest:.2f} [sec]")

    # override if you prefer    
    def _report_finish_time(self):
        elapsed = time.time() - self.start_time
        clear_output()
        print(f"The task completed in {elapsed:.2f} [sec]")
        print(f"Speed of the progress: {(self.current_progress / elapsed):.2f} [item/sec]")
        if self.finish_sound: play_beep()

    def _report(self):
        print("Start Iteration")
        time.sleep(self.interval)
        while not self._stop_event.is_set() and self.current_progress < self.complete_progress:
            clear_output()
            self._display()
            time.sleep(self.interval)
    
    def _iteration(self):
        try:
            for item in self.iterator:
                self.iter_func(item)
                self.current_progress += self.progress
                if self.current_progress >= self.complete_progress: 
                    self._report_finish_time()
                    self.stop()
                    break
        except Exception as e:
            self.stop()
            raise e
        