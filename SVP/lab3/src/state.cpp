#include <bits/stdc++.h>
using namespace std;

//point library made xD
#define point pair<double, double>
#define x first
#define y second;
#define vi vector<int>
#define vd vector<double>
#define vp vector<point>
#define ss set<string>
#define edge_t vector<vector<double>>
#define vs vector<State>
#define loop(i, n) for(int i=0; i<n; i++)

string hash_value(vi &arr){
    string s = "";
    for(int num: arr)
        s = s + "," + to_string(num);
    return s;
}

int greatestLowerBound(vd &V, double p){
    int index = 0;
    int beg = 0, end =V.size()-1;
    while(beg<=end){
        int mid = (beg+end)/2;
        if(V[mid]==p){
            return mid;
        }
        else if(V[mid] < p){
            index = mid;
            beg = mid + 1;
        }
        else{
            end = mid - 1;
        }
    }
    return index;
}


int lub(vd &V, double p){
    int index = 0;
    int beg = 0, end =V.size()-1;
    while(beg<=end){
        int mid = (beg+end)/2;
        if(V[mid]==p){
            return mid;
        }
        else if(V[mid] > p){
            index = mid;
            beg = mid + 1;
        }
        else{
            end = mid - 1;
        }
    }
    return index;
}


int search(vi &arr, int key){
    loop(i, arr.size())
        if(arr[i] == key)
            return i;
    return -1;
}

class State{
public:
    vi places;
    int N;
    State(int n=5){
        N = n;
        for(int i=0; i<N; i++)
            places.push_back(i);
    }

    State(vi L){
        places = L;
        N = places.size();
    }

    vi Delta(State neb){
        vi delta;
        for(int i=0;i<N; i++)
            if(places[i] != neb.places[i])
                delta.push_back(i);
        return delta;
    }
    vs moveGen(ss &closed, int K){
        /*
            This function returns a list of states
            that has less or equal to K places perturbed.

            @params
                * set<string> closed : set of states already visited
                * int K : number of places to be perturbed

            @returns
                * vector<vector<int>> neighbours
        */
        
        vs neighbours;

        // Generate bitmask with K 1's and N-K 0's
        string bitmask(N-K, 0);
        bitmask.resize(N, 1);

        // permute bitmask to obtain every combo of indices
        do{
            vi shuffled;
            for (int i = 0; i < N; i++)
                if (bitmask[i])
                    shuffled.push_back(i);
            do{
                vi move_idx;
                for(int i = 0, j=0; i< N; i++){
                    if(bitmask[i])
                        move_idx.push_back(shuffled[j++]);
                    else
                        move_idx.push_back(i);
                }
                vi move = filter(move_idx);    
                string key = hash_value(move);
                if(closed.find(key) == closed.end()){
                    neighbours.push_back(State(move));
                    closed.insert(key);
                }
            }while(next_permutation(shuffled.begin(), shuffled.end()));
        }while (next_permutation(bitmask.begin(), bitmask.end()));
        return neighbours;
    }

    void print(){
        for(int j : places)
            cout<<j<<" ";
        cout<<endl;
    }

    vi filter(vi &indices){
        vi F;
        for(int i : indices)
            F.push_back(places[i]);
        return F;
    }

    bool isNil(){
        for(int num : places)
            if(num != 0)
                return false;
        return true;
    }
}null_state = State(vector<int> (2, 0));