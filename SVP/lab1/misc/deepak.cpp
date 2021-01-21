#include<bits/stdc++.h>
using namespace std;

#define pii pair<int, int>
#define res pair<pii, unordered_map<int, pii>>

class Graph{
    vector<string> G;
    int row, col; 
    //solution vars
    int num_visited;
    int path_length;
public:
    Graph(string filename);
    
    //helpers
    int hash(pii index);
    void showGraph();
    void markGraph(res result);
    vector<pii> moveGen(pii pos);
    bool goalTest(pii pos);

    res bfs();
    res dfs();
    pii dls_subroutine(pii source, unordered_map <int, pii> &closed, int db);
    res dfid();
};


Graph :: Graph(string filename){
    ifstream fin(filename);
    string str;
    int algo;
    fin>>algo;
    row = 0;
    num_visited = 0;
    path_length = 0;
    while(getline(fin, str))
        if(str.length()){
            col = str.length();
            G.push_back(str);
            row++;
        }
    fin.close();

    res result;
    if (algo==0) result = bfs();
    else if (algo == 1) result = dfs();
    else result = dfid();
    
    markGraph(result);
    
    //num states explored
    cout<<num_visited<<endl;
    //path_length
    cout<<path_length<<endl;
    showGraph();
}

/* helpers */
int Graph::hash(pii index){
    return index.first*row + index.second;
}

void Graph:: showGraph(){
    for(string Grow : G){
        cout<<Grow<<endl;
    }
}

void Graph:: markGraph(res result){
    pii index = result.first;
    pii parent;
    path_length = 0;
    while(index != make_pair(-1,-1)){
        path_length ++;
        G[index.first][index.second] = '0';
        parent = result.second[hash(index)];
        index = parent;
    }
}

vector<pii> Graph:: moveGen(pii pos){
                // down up right left
    int rot_x[] = {0, 0, 1, -1};
    int rot_y[] = {1, -1, 0, 0};
    vector<pii> neighbours;
    for(int i=0; i<4; i++){
        int y = pos.first + rot_y[i];
        int x = pos.second + rot_x[i];
        if(y>=0 && y<row && x>=0 && x<col)
            neighbours.push_back(make_pair(y, x));
    }
    return neighbours;
}

bool Graph:: goalTest(pii pos){
    if(pos.first<row && pos.first >=0 && pos.second <col && pos.second >=0)
        return G[pos.first][pos.second] == '*';
    return false;
}
/* end of helpers*/

res Graph:: bfs(){
    queue<pii> open;
    unordered_map <int, pii> closed;
    pii iter_index = make_pair(0,0);
    pii nullparent = make_pair(-1,-1);
    //check if goal and mark as visited
    num_visited = 1;
    closed[hash(iter_index)] = nullparent;
    if(goalTest(iter_index))
        return make_pair(iter_index, closed);
    
    while( !open.empty() ){
        //pop from stack and visit neighbours
        iter_index = open.front();
        open.pop();

        cout<<num_visited<<endl;

        //iter over neighbours
        for(pii neb_index : moveGen(iter_index)){
            char neb = G[neb_index.first][neb_index.second];
            bool isEmpty = (neb == ' ' || neb =='*');
            bool isVistable =  closed.find(hash(neb_index)) == closed.end();
            // can visit if node not visited or if this is depth bounded search 
            if(isEmpty && isVistable){
                //mark as visited
                closed[hash(neb_index)] = iter_index;
                //check if we reached goal
                if(goalTest(neb_index))
                    return make_pair(neb_index, closed);
                open.push(neb_index);
            }
        }
    }
    return make_pair(nullparent, closed);
}

res Graph:: dfs(){
    stack<pii> open;
    unordered_map <int, pii> closed;
    pii iter_index = make_pair(0,0);
    pii nullparent = make_pair(-1,-1);

    //push source to open and mark it as visited
    open.push(iter_index);
    //check if goal and mark as visited
    num_visited = 1;
    closed[hash(iter_index)] = nullparent;
    if(goalTest(iter_index))
        return make_pair(iter_index, closed);
    
    while( !open.empty() ){
        //pop from stack and visit neighbours
        iter_index = open.top();
        open.pop();

        cout<<num_visited<<endl;

        // vector<pii> iter_neighbours = moveGen(iter_index);
        //iter over neighbours
        for(pii neb_index : moveGen(iter_index)){
            char neb = G[neb_index.first][neb_index.second];
            bool isEmpty = (neb == ' ' || neb =='*');
            bool isVistable =  closed.find(hash(neb_index)) == closed.end();
            // can visit if node not visited or if this is depth bounded search 
            if(isEmpty && isVistable){
                //mark as visited
                closed[hash(neb_index)] = iter_index;
                //check if we reached goal
                if(goalTest(neb_index))
                    return make_pair(neb_index, closed);
                open.push(neb_index);
            }
        }
    }
    return make_pair(nullparent, closed);
}

pii Graph::dls_subroutine(pii source, unordered_map <int, pii> &closed, int db){
    pii nullparent = make_pair(-1,-1);
    if(db < 0) return nullparent;
    pii deep_index;
    for(pii neb_index : moveGen(source)){
        char neb = G[neb_index.first][neb_index.second];
        bool isEmpty = (neb == ' ' || neb =='*');
        bool isVistable =  closed.find(hash(neb_index)) == closed.end();
        if(isEmpty && isVistable){
            //mark as visited
            closed[hash(neb_index)] = source;
            //check if we reached goal
            if(goalTest(neb_index))
                return neb_index;
            //go deep
            deep_index = dls_subroutine(neb_index, closed, db-1);
        }
    }
}
pii Graph:: dfid(){
    pii goal = {-1, -1};
    int db = 0;
    while(! goalTest(goal)){
        goal = dfs(db++);
    }
    return goal;
}

int main(int argc, char** argv){
    if(argc != 2){
        cout<<"Usage ./run.sh <filename>"<<endl;
        return 1;
    }

    Graph G(argv[1]);
    return 0;
}