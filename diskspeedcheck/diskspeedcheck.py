import sys
import os
from datetime import datetime
from datetime import timedelta

start_time = datetime.now()
def millis():
   dt = datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

#Package stuff
__version__ = "0.0.1"

#Getting arguments and removing filename
args = sys.argv
del args[0]

#Scanning args phase 1
if "-v" in args or "--verbose" in args:
    uv = True
else:
    uv = False

def pverb(data):
    global uv
    if uv:
        print(millis(),end=" ")
        print(data)
pverb("Checking arguments")
if "-s" in args or "--silent" in args:
    us = True
else:
    us = False
if uv and us:
    raise RuntimeError("verbose and silent may not be used together!")

#Defining variables
pverb("Preparing variables")
wsize = 1000000 #Default of 1 MB but may change later
dir = os.getcwd()
fname = "__speedtest__"
assembledname = dir + "/" + fname #For ease of writing
writeable = "x"*wsize
pverb("Performing final checks")
if os.path.isfile(assembledname):
    os.remove(assembledname)
pverb("Writing file")
start = datetime.now()
try:
    with open(assembledname,"x") as f:
        f.write(writeable)
except FileExistsError:
    if us:
        print("ERROR File already exists")
    sys.exit("-1")
except PermissionError:
    if us:
        print("ERROR Permission denied")
    sys.exit(-1)
end = datetime.now()
pverb("Removing file")
os.remove(assembledname)
pverb("Calculating")
speed = end - start
speed = speed.total_seconds()*1000
dspeed = 1000 / speed
pverb("Printing results")
print(f"Wrote {wsize/1000} KB to the disk in {speed} milliseconds.")
print(f"Speed is {dspeed} MB/s")
pverb("Done")
sys.exit(0)