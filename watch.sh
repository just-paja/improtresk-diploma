#!/usr/bin/env bash

LTIME=`stat -c %Z generate.py`

while true
do
   ATIME=`stat -c %Z generate.py`

   if [[ "$ATIME" != "$LTIME" ]]
   then
       python generate.py
       LTIME=$ATIME
   fi
   sleep 1
done
