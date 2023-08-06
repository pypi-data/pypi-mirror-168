import os
import re

### ============================================================================
## Resource managements
### ============================================================================
def memory_usage():
	"""return the memory usage in MB"""
	import psutil
	process = psutil.Process(os.getpid())
	mem = process.memory_info()[0] / float(2 ** 20)
	return mem
## --------



def natSorted(mylist):
	"https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort"
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key) ]
	return sorted(mylist, key = alphanum_key)
##--------



def float2str(floatnum, decimal=6):
	"""convert float number to str"""
	s = "{:.%if}" % decimal
	return s.format(floatnum)