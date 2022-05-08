import sys
import os
from datetime import datetime

start_time = datetime.now()
def millis():
   dt = datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

def silent_exc(type,value,traceback):
    sys.exit(1)

#Package stuff
__version__ = "1.0.0"
__doc__ = """Diskspeedcheck is a small utility that checks your disk's write speed. It is highly customizeable."""

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

def average(ltba,errors="halt"):
    """Averages a list. errors halt means it will throw a typeerror. skip means it will skip over it and not throw an error"""
    t = 0
    success = 0
    for item in ltba:
        try:
            t += item
        except TypeError:
            if errors.lower()=="halt":
                raise TypeError("Invalid item in list!")
        else:
            success += 1
    avg = t / success
    return avg

if "-s" in args or "--silent" in args:
    us = False
    sys.excepthook = silent_exc
else:
    us = True
if uv and not us:
    raise RuntimeError("verbose and silent may not be used together!")

#Defining variables
pverb("Preparing variables")
wsize = 1000000 #Default of 1 MB but may change later
dir = os.getcwd()
fname = "__speedtest__"
assembledname = dir + "/" + fname #For ease of writing
diffval = 1 #Placeholder incase -s is not used

pverb("Scanning arguments")
#Scanning for args part 2
if "-d" in args:
    ndir = args[args.index("-d")+1]
    if os.path.isdir(ndir):
        dir = ndir
        assembledname = dir + "/" + fname #For ease of writing
    else:
        if us:
            print(f"ERROR provided directory {ndir} is not valid")
        sys.exit(3)

if "--directory" in args: #Seperate due to .replace() issues
    ndir = args[args.index("--directory")+1]
    if os.path.isdir(ndir):
        dir = ndir
        assembledname = dir + "/" + fname #For ease of writing
    else:
        if us:
            print(f"ERROR provided directory {ndir} is not valid")
        sys.exit(3)

if "-f" in args:
    fname = args[args.index("-f")+1]
    assembledname = dir + "/" + fname
if "--file" in args:
    fname = args[args.index("--file")+1]
    assembledname = dir + "/" + fname

if "-si" in args: #Avoid conflicts with -s silent
    nwsize = args[args.index("-si")+1]
    try:
        nwsize = int(nwsize)
    except:
        if us:
            print("Invalid size")
        sys.exit(5)
    else:
        wsize = nwsize
        diffval = 1000000/wsize

if "--size" in args:
    nwsize = args[args.index("--size")+1]
    try:
        nwsize = int(nwsize)
    except:
        if us:
            print("Invalid size")
        sys.exit(5)
    else:
        wsize = nwsize
        diffval = 1000000/wsize

writeable = "x"*wsize
pverb("Performing final checks")
if os.path.isfile(assembledname) and not "--surpressfile" in args:
    if us:
        print("ERROR File already exists. To surpress this and overwrite the file, run with --surpressfile")
    sys.exit(4)
pverb("Writing file")

if "-a" in args:
    try:
        aloop = int(args[args.index("-a")+1])
    except IndexError:
        pverb("No average value provided, going with 10")
        aloop = 10
    except ValueError:
        pverb("Invalid average value provided, going with 10")
        aloop = 10
    speeds = []
    dspeeds = []
    for i in range(aloop):
        pverb(f"Running test {i+1}/{aloop}")
        if os.path.isfile(assembledname) and not "--surpressfile" in args:
            os.remove(assembledname)
        if "--excludefmk" in args or "-e" in args:
            pverb("Excluding file make")
            try:
                with open(assembledname,"w+") as f:
                    start = datetime.now()
                    f.write(writeable)
                    end = datetime.now()
            except PermissionError:
                if us:
                    print("ERROR Permission denied")
                sys.exit(2)
        else:
            start = datetime.now()
            try:
                with open(assembledname,"w+") as f:
                    f.write(writeable)           
            except PermissionError:
                if us:
                    print("ERROR Permission denied")
                sys.exit(2)
            end = datetime.now() 
        speed = end - start
        speed = speed.total_seconds()*1000
        dspeed = 1000 / speed
        dspeed = dspeed / diffval
        speeds.append(speed)
        dspeeds.append(dspeed)
        if "--noround" in args:
            pverb(f"Speed is {dspeed} MB/s")
            pverb(f"Wrote {wsize/1000} KB to the disk in {speed} milliseconds.")
        else:
            pverb(f"Speed is {round(dspeed,3)} MB/s")
            pverb(f"Wrote {wsize/1000} KB to the disk in {round(speed,3)} milliseconds.")
    pverb("All tests done")
    print(f"Average speed is {round(average(dspeeds),3)} Mb/s")
    print(f"Average time is {round(average(speeds),3)} ms")
    print(f"Lowest time was {min(speeds)} ms ({max(dspeeds)} Mb/s)")
    print(f"Slowest time was {max(speeds)} ms ({min(dspeeds)} Mb/s)")
    if not "--noremove" in args:
        pverb("Removing file")
        os.remove(assembledname)

else:
    if "--excludefmk" in args or "-e" in args:
        pverb("Excluding file make")
        try:
            with open(assembledname,"w+") as f:
                start = datetime.now()
                f.write(writeable)
                end = datetime.now()
        except PermissionError:
            if us:
                print("ERROR Permission denied")
            sys.exit(2)
    else:
        start = datetime.now()
        try:
            with open(assembledname,"w+") as f:
                f.write(writeable)           
        except PermissionError:
            if us:
                print("ERROR Permission denied")
            sys.exit(2)
        end = datetime.now()

    if not "--noremove" in args:
        pverb("Removing file")
        os.remove(assembledname)
    pverb("Calculating")
    speed = end - start
    speed = speed.total_seconds()*1000
    dspeed = 1000 / speed
    dspeed = dspeed / diffval
    pverb("Printing results")

    if "--noround" in args:
        print(f"Speed is {dspeed} MB/s")
        print(f"Wrote {wsize/1000} KB to the disk in {speed} milliseconds.")
    else:
        print(f"Speed is {round(dspeed,3)} MB/s")
        print(f"Wrote {wsize/1000} KB to the disk in {round(speed,3)} milliseconds.")
pverb("Done")
sys.exit(0)