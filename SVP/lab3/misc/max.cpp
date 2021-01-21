#include <bits/stdc++.h>
using namespace std;
#include "state.cpp"
int N=8;

State makeChild(State &A, State &B){
    vi child(N, -1);
    int index = 0;
    // search for B[index] in A and copy it
    while(child[index]==-1){
        child[index] = A.places[index];
        index = search(A.places, B.places[index]);
    }

    loop(i, N)
        if(child[i]==-1)
            child[i] = B.places[i];

    return State(child);
}

int main(){
    State A ({0,1,2,3,4,5,6,7});
    State B ({7,4,1,0,2,5,3,6});
    makeChild(B,A).print(); 
    return 0;
}