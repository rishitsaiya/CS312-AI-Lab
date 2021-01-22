javac Group12.java

# ts=$(date +%s%N)

if [ $# -eq 0 ]
  then
    echo "
        Format - 4 command line arguments
    
            1. input.txt     - select input file
            2. BFS/HillTop   - select one of - Best for search or Hill Climbing
            3. 1/2/3         - select one of the Heuristic function among
            4. output.txt    - select output file
    "
    else 
        java Group12 $1 $2 $3 > $4
        # echo $((($(date +%s%N) - $ts)/1000000))' Mili-Seconds'

fi

echo "
  Successful...
"