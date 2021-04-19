// n choose r combination
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;


struct c_unique {
    int current;
    c_unique() {current=0;}
    int operator()() {return ++current;}
} UniqueNumber;

vector<vector<int>> nCr(int n, int r){

    vector<vector<int>> combinations;
    vector<int> combination;
    std::vector<int> indices(r);
    std::vector<int>::iterator first = indices.begin(), last = indices.end();

    std::generate(first, last, UniqueNumber);

    // std::for_each(first, last, myfunction); 
    for(int i: indices)
        cout << i-1 <<  " ";

    std::cout << std::endl;

    while((*first) != n-r+1){
        std::vector<int>::iterator mt = last;

        while (*(--mt) == n-(last-mt)+1);
        (*mt)++;
        while (++mt != last) *mt = *(mt-1)+1;

        for(int i: indices)
            cout << i-1 << " ";
        std::cout << std::endl;
    }
}


int main()
{
    nCr(4, 3);
}