#!/usr/bin/env bash

curl -iv -X PUT 'http://localhost:9444/models/default/samples' -d @samples.json