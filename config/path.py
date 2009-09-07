import os
import sys

join = os.path.join

APP_PATH = os.path.abspath(os.path.dirname(__file__))
APP_PATH = sys.path[0]

paths = ('lib', 'data', 'common')
for path in paths:
    globals()[path] = join(APP_PATH, path)
del(paths)

hardware = join(data, 'hardware')
tools = join(hardware, 'tools')
arduino = join(hardware, 'cores', 'arduino')

avr_tools_path = '/usr/bin'
avrdude_path = tools

if __name__ == '__main__':
    for key, value in globals().copy().iteritems():
        if not key.startswith('_'):
            print key, value
