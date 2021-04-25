while 
    read line
do 
    echo $line
    echo $line | python3 dp_sol.py
    echo -e "$line\n1" | python3 ao_star.py
    echo -e "$line\n0" | python3 ao_star.py
    echo 
done < test