#!/bin/sh

echo > zerses.tex

find ./2010 ./2011 ./2012 ./2013 -name '*.html' | sort - | while read FILENAME; do
	echo $FILENAME
	./grepzerses.py $FILENAME >> ./zerses.tex
done

