$lines = cat .\test 
foreach($line in $lines) {
    echo $line
    echo $line | py dp_sol.py
    echo "$line`n1" | py .\ao_star.py
    echo "$line`n0" | py .\ao_star.py
    echo ""
}