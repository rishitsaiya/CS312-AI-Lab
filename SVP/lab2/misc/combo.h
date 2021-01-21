// n choose r combination
#ifndef COMBO_H
#define COMBO_H

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
    vector<int> myints(r);
    vector<int>::iterator first = myints.begin(), last = myints.end();

    std::generate(first, last, UniqueNumber);
    combinations.push_back(myints);

    while((*first) != n-r+1){
        std::vector<int>::iterator mt = last;

        while (*(--mt) == n-(last-mt)+1);
        (*mt)++;
        while (++mt != last) *mt = *(mt-1)+1;
        
        combinations.push_back(myints);

    }

    // Indexify to 0 -> n-1
    for(int i=0; i<combinations.size(); ++i)
        for(int j=0; j<combinations[i].size(); ++j)
            combinations[i][j] -= 1;
    return combinations;
}

// int main()
// {
//     vector<vector<int>> combos = nCr(5, 4);
//     for(vector<int> v: combos){
//         for(int i: v)
//             cout << i << " ";
//         cout << "\n";
//     }
// }
#endif