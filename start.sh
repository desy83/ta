#!/bin/bash

cdir=$(/bin/pwd)
export PYTHONPATH="${cdir}:${PYTHONPATH}"

exec "/usr/bin/python2.7" "${cdir}/main.py"
