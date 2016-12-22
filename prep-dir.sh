#!/bin/bash

rm -rf blogless-zipdir
mkdir blogless-zipdir
pip install jinja2 -t blogless-zipdir/
pip install setuptools -t blogless-zipdir/
cp -R blogless/* blogless-zipdir/
