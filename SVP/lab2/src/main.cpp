#include "TabuSet.cpp"
#include <chrono>
using namespace std::chrono; 

pii nil = {-1, -1};

class JobAllocation{
    vector<vector<int>> cost;
    ss open, closed; 
    int N, space_size;
    int constraint;
    int num_states;
    TabuSet T;
    int heuristic(State S);
    bool goalTest(State S);

/*
    Question 1:  Best First Search
    *******************************************************
    Use priority queue as the OPEN set
*/
    State bestFirstSearch();

/*
    Question 2: Beam search
    *******************************************************
    consists of 2 functions
    * makeBeam , for generating neighbours
    * beamSearch, the actual function that does the traversal
*/
    vector<State> makeBeam(State S, int K, int beamSize);
    State beamSearch(int beamSize);

/*
    Question 3: Hill Climbing
    *******************************************************
    consists of 2 functions
    * bestNeighbour , for generating neighbours
    * hillClimbing, calls bestNeighbour to go to the best node
*/
    State bestNeighbour(State S, int K);
    State hillClimbing(State node, int K);

/*
    Question 4: Variable NeighbourHood descent
    *******************************************************
    Only one function that does the job 
*/
    State variableNeighbourhoodDescent(int max_density);
/*
    Question 5: Tabu Search
    *******************************************************
    Only one function that does the job 
*/
    State tabuNextMove(State S, int K);
    State tabuSearch(int queue_size, int K, int iter_count);

public:
    void input(char *filename){
        // cout<<"Opening "<<filename<<endl;
        int cell_cost;
        ifstream fin;
        fin.open(filename);
        fin >> N >> constraint;
        space_size = 1;
        num_states = 0;
        for(int i=2; i<=N; i++)
            space_size *= i;
        // Input N x N cost matrix
        for(int i=0; i<N; ++i){
            vector<int> rowC;
            
            for(int j=0; j<N; ++j){
                fin >> cell_cost;
                rowC.push_back(cell_cost);
            }
            cost.push_back(rowC);
        }
        fin.close();
    }  


    void testPrint(){
        // Get starting timepoint 
        auto start = high_resolution_clock::now(); 
    
        // State sol = tabuSearch(10, 2, 20000);
        State sol = variableNeighbourhoodDescent(5);
        // State sol = bestFirstSearch();
        // State sol = beamSearch(2);
        // State sol = hillClimbing(State(N), 2);

        // Get ending timepoint 
        auto stop = high_resolution_clock::now(); 
        auto duration = duration_cast<microseconds>(stop - start);

        cout<<"Solution\t: ";
        sol.print();
        printf("H. value\t: %d\n", heuristic(sol));
        printf("Visited\t\t: %d\n", num_states);
        printf("Space size\t: %d\n", space_size);
        printf("Time taken (micro s): %ld\n", duration.count());
        printf("Frac visited\t: %.2f%%\n", (100.0*num_states)/space_size);
    }
};


int JobAllocation:: heuristic(State S){
    /*
        @params
            * State S, having the jobs allocated to people
        @return
            * integer representing the cost of this allocation
    */
    int sum = 0;
    for(int i=0; i<S.jobs.size(); i++)
        sum += cost[i][S.jobs[i]];
    return sum;
}

bool JobAllocation:: goalTest(State S){
    /* 
        *  Checks if the cost of the State is less than the constraint
        *   
        * @params:
        *          State S: having array of jobs assigned to ith person
        *          constraint(int): maximum bound constraint for path cost
        * @return:
        *          Boolean of whether state is equal to goal or not.
        */
    return (
        (S.jobs.size() == N) && 
        (heuristic(S) <= constraint)
    );
}

State JobAllocation::bestFirstSearch(){

    //declare empty priority queue
    priority_queue<State, vector<State>, function<bool(State, State)>> Q( [this](State l, State r) -> bool {// Lambda Comparator Constructor for function<>
            // Min Priority Queue based on score
            return (heuristic(l) > heuristic(r));
    });
    
    State S(N);
    // Push Source,
    Q.push(S);
    closed.insert(hash_value(S.jobs));
    while(!Q.empty()){
        S = Q.top();
        Q.pop();
        num_states++;

        if(goalTest(S)){
            cout << "Goal Found!!!!!!\n";
            return S;
        }

        // generate moves and update closed set too
        for(State T : S.moveGen(closed, 2))
            Q.push(T);

    }
    cout<<"Could not find any goal with constraint "<<constraint<<endl;
    return S;
}


vector<State> JobAllocation::makeBeam(State S, int K, int beamSize){
    ss dummy;
    vector<State> beam;
    priority_queue<State, vector<State>, function<bool(State, State)>> Q( [this](State l, State r) -> bool {// Lambda Comparator Constructor for function<>
        // Min Priority Queue based on score
        return (heuristic(l) > heuristic(r));
    });
    for(State T: S.moveGen(dummy, K)) Q.push(T);

    int cost = INT_MAX, newCost;
    while(!Q.empty()){
        State T = Q.top();
        Q.pop();

        //continue if state has been visited
        string t_key = hash_value(T.jobs);
        if(closed.find(t_key)!=closed.end()) continue;

        //if not found in closed, add it to beam and closed
        beam.push_back(T);
        closed.insert(t_key);
        
        /*
            We would generally stop at beam.size() == beamSize
            But we keep on adding elements if elements past beamsize
            have the same heuristic value as the last element in the beam
        */
        newCost = heuristic(T);
        if(cost!=newCost &&  beam.size()>=beamSize) // hence this condition
            break;
    }
    return beam;
}

State JobAllocation::beamSearch(int beamSize){
    //declare empty priority queue
    priority_queue<State, vector<State>, function<bool(State, State)>> Q( [this](State l, State r) -> bool {// Lambda Comparator Constructor for function<>
            // Min Priority Queue based on score
            return (heuristic(l) > heuristic(r));
    });
    
    State S(N);
    // Push Source,
    Q.push(S);
    closed.insert(hash_value(S.jobs));
    while(!Q.empty()){
        S = Q.top();
        Q.pop();
        num_states++;
        
        if(goalTest(S)){
            cout << "Goal Found!!!!!\n";
            return S;
        }

        // generate moves and update closed set too
        for(State T : makeBeam(S, 2, beamSize))
            Q.push(T);
    }
    cout<<"Could not find any goal with constraint "<<constraint<<endl;
    return S;
}


State JobAllocation:: bestNeighbour(State S, int K=2){
    /* 
        for a give node, this returns the best neighbour
        The best neighbour is the one with minimum cost
    */
    vector<State> neighbours = S.moveGen(closed, K);
    State bestNeb = neighbours[0];
    int minCost = INT_MAX;
    for(State T : neighbours){
        int cost = heuristic(T);
        if(cost < minCost){
            bestNeb = T;
            minCost = cost;
        }
    }
    return bestNeb;
}

State JobAllocation::hillClimbing(State node, int K=2){
    State newNode = bestNeighbour(node, K);
    while(heuristic(node) >= heuristic(newNode)){
        num_states++;
        node = newNode;
        newNode = bestNeighbour(node);
    }
    return node;
}

State JobAllocation:: variableNeighbourhoodDescent(int max_density){
    State node = State(N);
    for(int k = 2; k<=max_density && k<=N; k++){
        // printf("Density: %d\n", k);
        node = hillClimbing(node, k);
        // printf("Num visited: %d\n\n", num_states);
    }
    return node;
}

State JobAllocation :: tabuNextMove(State S, int K){
    /*
        Returns next move after updating tabuset
    */
    ss dummy;//dummy empty set
    vector<State> nonTabu;
    vector<State> tabu;

    //partition the neighbours into tabu and non tabu
    T.partition(S, S.moveGen(dummy, K), nonTabu, tabu);
    
    //try to find the best node in nontabu 
    int curr_cost = INT_MAX;
    State bestNode = null_state;
    for(State &neb: nonTabu){
        int new_cost = heuristic(neb);
        if(new_cost <= curr_cost){
            curr_cost = new_cost;
            bestNode = neb;
        }
    }

    // once we get the best neighbour, update T.best
    if(! bestNode.isNil() ){
        if( T.best.isNil() || heuristic(bestNode) < heuristic(T.best)){
            T.best = bestNode;
            //surely, if bestNode is better than T.best, we must return this move
            return bestNode;         
        }
    }

    if(curr_cost <= heuristic(S))
    //best neighbour is better than current node
        return bestNode;

    // check for aspiration
    curr_cost = heuristic(T.best);
    bestNode = null_state;
    for(State &neb: tabu){
        int new_cost = heuristic(neb);
        if(new_cost < curr_cost){
            curr_cost = new_cost;
            bestNode = neb;
        }
    }
    return bestNode;
}

State JobAllocation:: tabuSearch(int queue_size, int K=2, int iter_count=5000){
    TabuSet T(queue_size);
    State node(N);
    State newNode = tabuNextMove(node, K);

    for(int i=0; i<iter_count && !newNode.isNil(); i++ ){
        num_states++;
        node = newNode;
        printf("Iteration %d: ", i);
        node.print();
        newNode = tabuNextMove(node, K);
        T.insert(node, newNode);
        vi change = newNode.Delta(node);
        State D(change);
        if(D.isNil())
            return node;
    }
    return T.best;
}

int main(int argc, char** argv){
    if(argc!=2){
        cout<<"Error: "<<argv[0]<<" <input_file_path>\n";
        return 0;
    }
    JobAllocation solver;
    solver.input(argv[1]);
    solver.testPrint();
    return 0;
}

