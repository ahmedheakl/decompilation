#! /usr/bin/env bash

for file in *.cpp
do
	sed -i 's@#include@//#include@g' $file
	sed -i 's@using namespace@//using namespace@g' $file
	sed -i 's@int main@//int main@g' $file
done
