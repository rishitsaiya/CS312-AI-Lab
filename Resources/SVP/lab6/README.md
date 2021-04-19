# Code for AO* Algorithm implemented on Optimal Matrix Multiplication Problem

## Steps to Run

'./run.sh <input_file>'

Sample inputs are in tests/

Example:
'./run.sh tests/input1'

## For changing heuristic function 

For overestimating heuristic, replace line 38 in node.py with
'return h1(self, dims)'

For underestimating heuristic, replace line 38 in node.py with
'return h2(self, dims)'