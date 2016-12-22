#!/bin/bash

./scripts/prep-dir.sh
sunyata --deploy --template sunyata-blogless.json
rm -rf blogless-zipdir