import time


class Timer(object):

    def __init__(self, method_name):
        self.start = time.time()
        self.method_name = method_name

    def reset(self):
        self.start = time.time()

    def print_end(self):
        end = time.time()
        difference = end - self.start
        print(self.method_name, " : ", difference, " seconds")

    def get_difference(self):
        end = time.time()
        difference = end - self.start
        return difference
