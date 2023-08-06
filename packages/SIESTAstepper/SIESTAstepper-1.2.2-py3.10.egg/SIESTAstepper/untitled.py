import os
import re
files = ['/home/egezer/Desktop/SIESTAstepper_tutorial/Carbon/i1/log', '/home/egezer/Desktop/SIESTAstepper_tutorial/Carbon/i2/log', '/home/egezer/Desktop/SIESTAstepper_tutorial/Carbon/i3/log', '/home/egezer/Desktop/SIESTAstepper_tutorial/Carbon/i3/continue/log', '/home/egezer/Desktop/SIESTAstepper_tutorial/Carbon/i3/continue_2/log', '/home/egezer/Desktop/SIESTAstepper_tutorial/Carbon/i4/log', '/home/egezer/Desktop/SIESTAstepper_tutorial/Carbon/i5/log']
path = "i*"
cwd = "/home/egezer/Desktop/SIESTAstepper_tutorial/Carbon"
log = "log"
cont = "continue"

repath = path.replace("*", "[0-9]+")

active_log = {}
to_remove = []
for filename in files:
    logmatch = re.search(
            f"({cwd}{os.sep}({repath})({os.sep}{cont}(_([0-9]+)){{0,1}}){{0,1}}{os.sep}{log})", filename
        
    )
    if not logmatch:
        continue
    _, instance, extended, _, increment = logmatch.groups()
    lognumber = 0
    if extended is not None:
        lognumber = 1 if increment is None else int(increment)
    if instance not in active_log:
        active_log[instance] = (lognumber, filename)
    else:
        if active_log[instance][0] > lognumber:
            to_remove.append(filename)
        else:
            to_remove.append(active_log[instance][1])
            active_log[instance] = (lognumber, filename)

for filename in to_remove:
    files.remove(filename)