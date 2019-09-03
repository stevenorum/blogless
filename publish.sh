#!/bin/bash

rm -rf src/toco
rm -rf src/sneks
cp -r /Users/norums/Dropbox/personal/repos/toco/src/toco src/
cp -r /Users/norums/Dropbox/personal/repos/sneks/src/sneks src/

sneks publish-sam-stack
rm -rf src/toco
rm -rf src/sneks
