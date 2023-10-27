#! /usr/bin/env bash

for file in *.cpp
do
	sed -i 's@^//.*$@@g' $file
done
