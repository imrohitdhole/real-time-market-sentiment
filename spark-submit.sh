#!/bin/bash
docker build -t spark-sentiment .
docker run --network host spark-sentiment