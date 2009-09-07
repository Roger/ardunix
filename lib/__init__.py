import os
import sys

import build
#import codebuffer

# add project to sys path
BASE_PATH = os.path.join(os.path.sep ,
     *os.path.dirname(os.path.realpath( __file__ )).split( os.path.sep )[:-1])
sys.path.append(BASE_PATH)
