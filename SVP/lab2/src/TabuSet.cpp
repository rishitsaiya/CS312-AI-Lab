#include "state.cpp"

class TabuSet{
    queue<vi> Q;
    set<string> S;
    int MAXSIZE;
public:
    State best;

    TabuSet(int size=10){
        MAXSIZE = size;
        best = null_state;
    }

    int size(){
        return Q.size();
    }

    bool insert(State current, State neb){
        vi delta = current.Delta(neb);
        string key = hash_value(delta);
        /* insert into set only if key not present*/
        if(S.find(key)==S.end()){
            if(S.size() == MAXSIZE){
                S.erase(S.find(key));
                Q.pop();
            }
            Q.push(delta);
            S.insert(key);
            return true;
        }
        return false;
    }

    bool isTabu(State &current, State &neb){
        vi delta = current.Delta(neb);
        string key = hash_value(delta);
        return ! (S.find(key)==S.end()) ;
    }

    void partition(State current, vector<State> moveGen, vector<State> &nonTabu, vector<State> &tabu){
        for(State move : moveGen){
            if(isTabu(current, move))
                tabu.push_back(move);
            else
                nonTabu.push_back(move);
        }
    }
};