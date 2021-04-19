#include "state.cpp"
int main(){
    vi jobs;
    for(int i=0; i< 4; i++)
        jobs.push_back(i+1);
    State init(jobs);
    string key = hash_value(jobs);
    ss closed;
    closed.insert(key);
    init.print();
    for( State S: init.moveGen(closed, 4) )
        S.print();
    cout<<closed.size()<<endl;
    return 0;
}