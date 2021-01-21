#include "tsp.cpp"
using namespace std;

int main(int argc, char** argv){
    if(argc!=3){
        cout<<"Error: "<<argv[0]<<" <input_file_path>\n";
        return 0;
    }
    TSP solver;
    solver.input(argv[1]);
    solver.testPrint(argv[2]);
        return 0;
}