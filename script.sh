#!/bin/bash

echo "starting computation..." \
&&
  while true
  do
     /bin/bash -c "python3 /app/test.py"
  done \
&& echo "finish?"

