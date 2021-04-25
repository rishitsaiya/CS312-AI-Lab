echo "Simulated Annealing for $1"
echo $1 | python3 sim_ann.py > simulated_annealing_$1.txt
cat simulated_annealing_$1.txt
echo
echo "Genetic Algorithm for $1"
echo $1 | python3 gen_algo.py > genetic_algo_$1.txt
cat genetic_algo_$1.txt
cat genetic_algo_$1.txt | tail -n +2 | tail -n +2 | tail -n +2 | tail -n +2 > temp.txt
cat temp.txt >  genetic_algo_$1.txt
rm temp.txt
echo
echo "Ant Colony for $1"
echo $1 | python3 ant_col.py > ant_col_$1.txt
cat ant_col_$1.txt
echo
