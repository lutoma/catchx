#!/bin/sh

cd $(dirname $0)
mkdir -p locale

cd i18n

for f in *.po
do
	f=$(basename $f .po)
	mkdir -p ../locale/$f/LC_MESSAGES
	msgfmt $f.po -o ../locale/$f/LC_MESSAGES/catchx.mo
done
