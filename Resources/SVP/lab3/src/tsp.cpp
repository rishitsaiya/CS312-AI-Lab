#include "state.cpp"
#include <chrono>
using namespace std::chrono; 


class TSP{
    edge_t edges;
    vp cities;
    string isEuclidean;
    ss open, closed; 
    int N;
    int num_states;
    int density;
    double k_max; // max iteration count
    double heuristic(State S);
    bool goalTest(State S);
    vector<vd> Tau;
/*
    Question 1:  Simulated Annealing
    *******************************************************
    Use priority queue as the OPEN set
*/
    bool validateMove(State &node, State &newNode, int k, double &temperature);
    State randomNeighbour(State S);
    State simulatedAnnealing();

/*
    Question 2: geneticAlgorithm
    *******************************************************
    consists of 2 functions
    * makeChild
    * geneticAlgorithm, the actual function that does the traversal
*/
    State makeChild(State &A, State &B, string crossover);
    vs selectParents(vs &population);
    State geneticAlgorithm();

/*
    Question 3: Ant Colony
    *******************************************************
    consists of 2 functions
    * makeChild
    * geneticAlgorithm, the actual function that does the traversal
*/
    
    State simulateAnt(int start);
    void updatePheromone(vs ants);
    State antColonyOptimization();


public:
    void input(char *filename);  
    void testPrint(string function_name);
};


void TSP::input(char *filename){
    // cout<<"Opening "<<filename<<endl;
    double cell_cost;
    ifstream fin;
    fin.open(filename);
    fin >> isEuclidean;
    fin >> N;
    cities = vp (N);

    k_max = 2000;
    for(point &city : cities)
        fin>>city.x>>city.y;

    // Input N x N cost matrix
    loop(i, N){
        vector<double> rowC;
        loop(j, N){
            fin >> cell_cost;
            rowC.push_back(cell_cost);
        }
        edges.push_back(rowC);
    }
    fin.close();
}

void TSP:: testPrint(string function_name){
    // Get starting timepoint 
    //init some vars
    auto start = high_resolution_clock::now(); 
    State sol = null_state;
    density = 2;
    if(function_name=="simann")
        sol = simulatedAnnealing();
    else if(function_name=="genAlg")
        sol = geneticAlgorithm();
    else if(function_name=="ant")
        sol = antColonyOptimization();
    else
        cout<<"Wrong function!!\n";
    

    // Get ending timepoint 
    auto stop = high_resolution_clock::now(); 
    auto duration = duration_cast<microseconds>(stop - start);

    // cout<<"Solution\t: ";
    printf("%lf\n", heuristic(sol));
    sol.print();
    // printf("Visited\t\t: %d\n", num_states);
    // printf("Time taken (micro s): %ld\n", duration.count());
}

double TSP:: heuristic(State S){
    /*
        @params
            * State S, having the order to visit places
        @return
            * integer representing the cost of this path
    */
    double path_cost = 0;
    for(int i=1; i<S.places.size(); i++){
        int u = S.places[i-1];
        int v = S.places[i];
        path_cost += edges[u][v];
    }
    path_cost += edges[S.places.back()][S.places.front()];
    return path_cost;
}


State TSP:: randomNeighbour(State S){
    /* 
     *  For a given node, this returns a random neighbour
     *      @Params: S(State): current state
     *      @Returns: State: a random neighbour of S
     */
    swap(S.places[rand()%N], S.places[rand()%N]);
    return S;
}


bool TSP:: validateMove(State &node, State &newNode, int k, double &temperature){
    /*
     *  Calculates whether next possible state (newNode) is taken using probability 
     *      temperature = k_max/(k+1)
     *      P = 1 - exp([h(node) - h(newNode)]/ k * temperature)
     * 
     *  @Params: node(State): current state
     *      newNode(State): next possible state
     *           k(int): iteration number
     *  @Returns: Boolean: whether to consider newNode for next move
     */
    // temperature = k_max/(k+1);
    // cout << "Temp: " << temperature << "\n";
    double deltaH = heuristic(node) - heuristic(newNode);

    if(deltaH > 0) // If newNode better, choose it
        return true;
    
    double prob = 1;
    double p = double(rand())/double((RAND_MAX));

    if(k != 0)
        prob = 1/(1 + exp( -deltaH / k * temperature ));

    return (p < prob);
}


State TSP::simulatedAnnealing(){
    State node(N);
    State bestNode = node;
    double temperature = k_max;
    for(int k=0; k < k_max; k++){
        while(true){

            State newNode = randomNeighbour(node);
            num_states++;
            
            if(validateMove(node, newNode, k, temperature)){
                node = newNode;
                if(heuristic(node) <= heuristic(bestNode)){
                    bestNode = node;
                    printf("%lf\n", heuristic(bestNode));
                    bestNode.print();
                }
                temperature = k_max/(k+1);
                // temperature = k_max - k;
                // temperature = .999 * temperature;
                
                break;
            }
            
            
        }
    }
    return bestNode;
}


State TSP::makeChild(State &A, State &B, string crossover="cyclic"){
    vi child(N, -1);
    int index = 0;
    if(crossover == "cyclic"){
        // search for B[index] in A and copy it
        while(child[index]==-1){
            child[index] = A.places[index];
            index = search(A.places, B.places[index]);
        }

        loop(i, N)
            if(child[i]==-1)
                child[i] = B.places[i];
    } else if(crossover == "order"){
        int start = rand()%N; 
        int end = rand()%(N-start) + start;
        child = vi(A.places.begin() + start, A.places.begin() + end);
        loop(j, N){ // Add remaining cities in the order it occurs in B.
            if(find(child.begin(), child.end(), B.places[j]) == child.end()){
                child.push_back(B.places[j]);
            }
        }
    }
    return State(child);
}


vs TSP:: selectParents(vs &population){
    vd H;
    loop(i, population.size())
        H.push_back(1/heuristic(population[i]));

    int normalizer = accumulate(H.begin(), H.end(), 0);
    
    //normalize the probabilities
    loop(i, H.size())
        H[i] = H[i]/normalizer;
    
    //find the cummulative probabilities for random selection
    loop(i, H.size()-1){
        H[i+1] = H[i] + H[i+1];
    }   

    vs selected;
    loop(i, H.size()){
        //roll random number
        double p = double(rand())/double((RAND_MAX));
        //find the greatest lower bound of p in H
        int index = greatestLowerBound(H, p);
        //append that to the selected population
        selected.push_back(population[index]);
    }
    //Knuth shuffle
    for(int i=H.size()-1; i>0; i--){
        int r = rand()%i;
        swap(selected[i], selected[r]);
    }
    
    return selected;
}

State TSP:: geneticAlgorithm(){
    /*
        hyper_parameters
        * k_max : # of iterations  
        * P : population size
        * k : # of organisms to be replaced by children
    */
    k_max = 100;
    int P = 2500;
    int k = 25 * P/100;
    double mutation_prob = 0.005;
    vs population;

    loop(i, P){
        while(true){
            State node(N);
            //Knuth shuffle
            for(int j=N-1; j>0; j--){
                int r = rand()%j;
                swap(node.places[j], node.places[r]);
            }
            string key = hash_value(node.places);
            if(closed.find(key) != closed.end())
                continue;
            closed.insert(key);
            population.push_back(node);
            break;
        }
    }
    sort(population.begin(), population.end(), [this](const State &a, const State &b){
        return heuristic(a) < heuristic(b);
    });

    loop(i, k_max){
        vs selected = selectParents(population);
        
        vs children;
        loop(j, P/2){
            children.push_back(makeChild(selected[j], selected[P/2+j], "order"));
            children.push_back(makeChild(selected[P/2+j], selected[j], "order"));
        }

        //mutate a small portion of the population
        loop(j, children.size()){
            double p = double(rand())/double((RAND_MAX));
            if(p < mutation_prob){
                int mutation_extent = 1;
                loop(x, mutation_extent){
                    int a = rand() % N;
                    int b = rand() % N;
                    swap(children[j].places[a], children[j].places[b]);
                }
            }
        }

        sort(children.begin(), children.end(),[this](const State &a, const State &b){
            return heuristic(a) < heuristic(b);
        });
        
        //replace last k of population with first k children
        int k = P *15/100; 
        loop(j, k)
            population[P-1-j] = children[j];

        //sort the population according to heuristic
        sort(population.begin(), population.end(),[this](const State &a, const State &b){
            return heuristic(a) < heuristic(b);
        });
        double best = heuristic(population[0]);
        double worst = heuristic(population[P-1]);
        // printf("Loop %d/%d (%lf, %lf)\n", i+1, (int)k_max, best, worst);
        printf("%lf\n", best);
        population.begin()->print();
    }
    //return best among population
    return *population.begin();
}

State TSP:: antColonyOptimization(){
    int l = N;
    // k_max = 500;
    srand(time(0));
    State bestTour(N);
    loop(i, N)
        Tau.push_back(vd(N, 0.1));
    loop(t, k_max){
        vs ants;
        loop(i, l){
            ants.push_back(simulateAnt(i*10));
            if(heuristic(bestTour) > heuristic(ants.back()))
                bestTour = ants.back();
        }
        updatePheromone(ants);
        printf("i: %d: %lf\n", t, heuristic(bestTour));
    }
    return bestTour;
}

State TSP:: simulateAnt(int start){
    int alpha = 1, beta = 1;
    State ant(N);
    
    ant.places[0] = rand()%(N/3);
    set<int> visited;
    for(int i=1; i<N; i++){
    //choose ith city in the tour
        visited.insert(ant.places[i-1]);
        int u = i-1;
        // make allowed vertices
        vi allowed_vertices;
        loop(v, N){ 
            if(visited.find(v) != visited.end()) continue;
            allowed_vertices.push_back(v);
        }

        vd cummulative_prob;
            // find the density
        for(int v : allowed_vertices){
            if( edges[u][v] != 0){
                cummulative_prob.push_back(
                    pow(Tau[u][v], alpha) * pow(1/edges[u][v], beta)
                );
            }
        }
        
            // find the cummulative probs

        // for(int v=1; v<cummulative_prob.size(); v++)
        //     cummulative_prob[v] += cummulative_prob[v-1];
        double sum = accumulate(cummulative_prob.begin(), cummulative_prob.end(), 0);
            // normalize
        // printf("Tau");
        loop(v,cummulative_prob.size()){
            // cummulative_prob[v] /= cummulative_prob.back();
            cummulative_prob[v] /= sum;
            // printf("%lf,  ", cummulative_prob[v]);
        }

        //roll and find an edge
        
        double p = (double)rand()/RAND_MAX;
        int index = 0; 
        if(cummulative_prob.size() != 0)
        while(true){
            int r = rand()% cummulative_prob.size();
            double pp = (double)rand()/RAND_MAX;
            if(pp < cummulative_prob[r]){
                index = r;
                break;
            }
        }
        // printf("\nRolled: %lf\n", p);
        // int index = lub(cummulative_prob, p);
        ant.places[i] = allowed_vertices[index];
    }
    // ant.print();
    return ant;
}

void TSP :: updatePheromone(vs ants){
    double rho = 0.8;
    double Q = 1;
    loop(i, N)
        loop(j, N){
            //calculate delta Tau
            double delta = 0;
            for(State &ant : ants){ //ant is antk
                int left = search(ant.places, i);
                int right = (left+1)%N;
                if(ant.places[right]==j)
                    delta += Q / heuristic(ant);
            }
            Tau[i][j] = rho*Tau[i][j] + delta;
        }
}