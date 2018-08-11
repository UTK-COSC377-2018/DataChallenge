#!/bin/bash

com="./virtualenv.sh ${@:1}"

scl enable python33 "${com}"
