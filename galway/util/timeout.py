import signal

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        if self.seconds is not None:
            signal.signal(signal.SIGALRM, self.handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,self.seconds)
            #signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        if self.seconds is not None:
            signal.alarm(0)
