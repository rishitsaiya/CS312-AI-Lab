javac Main.java

ts=$(date +%s%N)

if [ $# -eq 0 ]
  then
    echo "
    
        Four command line arguments
    
            # input.txt     - input file
            # BFS/HillTop   - Best for search or Hill Climbing
            # 1/2/3         - Heuristic function
            # output.txt    - output file
    "
    else 
        java Main $1 $2 $3 > $4
        echo $((($(date +%s%N) - $ts)/1000000))' Mili-Seconds'

fi
