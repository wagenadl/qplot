import numpy as np
import tempfile
import os
import re
import qplot_internal as qi
from core import *
from annotate import *
from axes import *
from plots import *



#======================================================================
if __name__ == '__main__':
    print('qplot test')
    figure('hello', 4, 3)
    pen('r')
    plot([1,2,3,4], [1,3,2,4])
    
    brush('555')
    patch([1,2,1,1],[1,1,2,1])