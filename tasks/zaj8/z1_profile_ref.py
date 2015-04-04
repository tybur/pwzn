import pstats, cProfile

#import pyximport
#pyximport.install()

import zadanie1_ref
from zadanie1_comp import *

cProfile.runctx("test2(zadanie1_ref.quicksort, 10000)", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
