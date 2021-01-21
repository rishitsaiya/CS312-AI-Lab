#include<bits/stdc++.h>
using namespace std;

#define pii pair<int, int>

struct Node{
    static int stamp;
    char value;
    int visited;
    int depth;
    pii parent;
    Node(){
        depth = INT32_MAX;
        value = ' ';
        visited = false;
        parent = make_pair(-1, -1);
    }
    // int getColor(int db){
    //     if(db==stamp) return color;
    //     return 0;
    // }
    // int getDepth(int db){
    //     if(db==stamp) return depth;
    //     return INT32_MAX;
    // }
};

int Node:: stamp = -1;
class Graph{
    vector<vector<Node>> G;
    int row, col; 
    //solution vars
    int num_visited;
    int path_length;
public:
    Graph(string filename);
    
    pii bfs();
    pii dfs();
    pii dfid();
    pii dfid_subroutine(pii source, int db, int stamp);
    
    //helpers
    void showGraph();
    void markGraph(pii index);
    vector<pii> moveGen(pii pos, bool rev);
    bool goalTest(pii pos);
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
            G.push_back(vector<Node>(col));
            for(int j = 0; j<col; j++)
                G[row][j].value = str[j];
            row++;
        }
    fin.close();

    pii goal;
    if (algo==0) goal = bfs();
    else if (algo == 1) goal = dfs();
    else goal = dfid();
    
    markGraph(goal);
    
    //num states explored
    cout<<num_visited<<endl;
    //path_length
    cout<<path_length<<endl;
    showGraph();
}

/* helpers */
void Graph:: showGraph(){
    for(vector<Node> Grow : G){
        for(Node iter: Grow)
            if(iter.visited && iter.value != '0')
                cout << '1';
            else
                cout<<iter.value;
        cout<<endl;
    }
}

void Graph:: markGraph(pii index){
    path_length = 0;
    while(index != make_pair(-1,-1)){
        path_length ++;
        G[index.first][index.second].value = '0';
        index = G[index.first][index.second].parent;
    }
}

vector<pii> Graph:: moveGen(pii pos, bool rev=false){
                // down up right left
    int rot_x[] = {0, 0, 1, -1};
    int rot_y[] = {1, -1, 0, 0};
    vector<pii> res;
    for(int i=0; i<4; i++){
        int y = pos.first + rot_y[i];
        int x = pos.second + rot_x[i];
        if(y>=0 && y<row && x>=0 && x<col)
            res.push_back(make_pair(y, x));
    }
    if(rev) // reverse order
            std::reverse(res.begin(), res.end());
    return res;
}

bool Graph:: goalTest(pii pos){
    if(pos.first<row && pos.first >=0 && pos.second <col && pos.second >=0)
        return G[pos.first][pos.second].value == '*';
    return false;
}
/* end of helpers*/

pii Graph:: bfs(){
    queue<pii> Q;
    Q.push(make_pair(0,0));
    G[0][0].visited = true;
    while( !Q.empty() ){
        // pop and mark visited
        pii iter_index = Q.front();
        Q.pop();
        Node &iter = G[iter_index.first][iter_index.second];
        // cout<<iter_index.first<<" "<<iter_index.second<<endl;
        num_visited ++;

        // check if we reached goal!
        if(goalTest(iter_index)) return iter_index;
        
        //otherwise iter over neighbours
        vector<pii> iter_neighbours = moveGen(iter_index);
        for(pii neighbour : iter_neighbours){
            Node &neighbour_node = G[neighbour.first][neighbour.second];

            if( !neighbour_node.visited &&  //not visited
                (neighbour_node.value == ' ' || neighbour_node.value=='*') //free node
            ){
                neighbour_node.visited = true;
                neighbour_node.parent = iter_index;
                Q.push(neighbour);
            }
        }
    }
    return {-1,-1};
}

pii Graph:: dfs(){
    stack<pii> S;
    S.push(make_pair(0,0));
    G[0][0].visited = true;
    while( !S.empty() ){
        // pop and mark visited
        pii iter_index = S.top();
        S.pop();
        Node &iter = G[iter_index.first][iter_index.second];
        // printf("index (%d, %d)-> %c, depth:%d\n", iter_index.first, iter_index.second, iter.value, iter.depth);
        num_visited ++;
        // check if we reached goal!
        if(goalTest(iter_index)) return iter_index;

        //otherwise iter over neighbours
        for(pii neb_index : moveGen(iter_index, true)){
            Node &neb = G[neb_index.first][neb_index.second];
            // printf("At (%d %d)\n", neb_index.first, neb_index.second );
            //check if the node is boundary
            bool isEmpty = (neb.value == ' ' || neb.value=='*');
            if(!isEmpty) continue;

            // printf("Isvisitable: %d for (%d %d)\n", isVisitable, neb_index.first, neb_index.second );
            if(!neb.visited){
                neb.visited = true;
                neb.parent = iter_index;
                S.push(neb_index);
            }
        }
    }
    return {-1,-1};
}

pii Graph:: dfid(){
    pii goal = {-1, -1};
    int db = 0;
    while(! goalTest(goal)){
        G[0][0].depth = 0;
        goal = dfid_subroutine({0,0}, db, db++);
        // break;
    }
    return goal;
}

pii Graph::dfid_subroutine(pii source, int db, int stamp){
    num_visited++;
    // source is closed
    // mark stamp to know the val of depth bound at root function call
    Node & iter =  G[source.first][source.second];
    iter.visited = stamp;
    if(goalTest(source))
        return source;
    
    if(db!=0)
    for(pii neb_index : moveGen(source)){
        Node &neb = G[neb_index.first][neb_index.second];

        //continue if you cant go there
        if(!(neb.value == ' ' || neb.value=='*')) continue; 

        if(neb.visited == stamp && iter.depth + 1 >= neb.depth) continue;
        neb.depth = iter.depth + 1;
        neb.parent = source;
        
        pii goal = dfid_subroutine(neb_index, db-1, stamp);
        if(goalTest(goal))return goal;
    }
    return {-1,-1};
}

int main(int argc, char** argv){
    if(argc != 2){
        cout<<"Usage ./run.sh <filename>"<<endl;
        return 1;
    }

    Graph solve(argv[1]);
    return 0;
}

// //show stack
// pii *end = &S.top() + 1;
// pii *beg = end - S.size(); 
// vector<pii> stack_contents(beg, end);
// for(pii index : stack_contents)
//     printf("(%d %d), ", index.first, index.second);
// cout<<endl;
// fflush(stdout);