#!/bin/bash
cd `dirname $0`/..
./server.py -p 20211 2> /dev/null &
#./start.py -lcr test -s localhost -p 20211 -k test -u CatchX\ Developer
./start.py -s localhost -p 20211 -n CatchX\ Developer
kill %%
