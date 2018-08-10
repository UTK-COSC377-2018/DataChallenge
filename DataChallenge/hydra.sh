#!/bin/bash

com="./run.sh ${@:1}"

scl enable python33 "${com}"
