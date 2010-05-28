#!/bin/bash

./server.py 2> /dev/null &
./start.py
kill %%
