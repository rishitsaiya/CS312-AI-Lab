javac Main.java

# if [ $# -eq 0 ]
#   then
#     echo "No arguments supplied"
# fi

java Main input.txt BFS 2 > output.txt

# input.txt - input file
# BFS or HillTop
# Heuristic function - 1/2/3