#!/bin/bash
g++ main.cpp -o deploy.ai;
./deploy.ai $1 > output.txt;