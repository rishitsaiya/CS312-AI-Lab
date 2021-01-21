#include <bits/stdc++.h>
#define pii pair<int, int>
using namespace std;

pii zero = {0, 0};
pii nil = {-1, -1};

struct node{
    char value;
    bool visited;
    bool explored;
    pii parent;
    int depth;
    node(){
        parent = zero;
        depth = 0;
        explored = false;
        visited = false;
        value = -1;
    }
};


class Maze{
    vector<vector<node>> G; //Graph
    int M, N; //Dimensions
    int algo; //0 -> bfs, 1 -> dfs, 2 -> dfid  
    int nodes_visited; // no. nodes visited in i'th iteration of dfid
    int max_bound; // dfid bound on i'th iteration

    node* get_node(pii pos){
        return &(G[pos.first][pos.second]);
    }


    void reset_nodes(){
        for(int i=0; i<M; ++i)
            for(int j=0; j<N; ++j){
                G[i][j].parent = zero;
                G[i][j].depth = 0;
                G[i][j].visited = false;
                G[i][j].explored = false;
            }
    }


    vector<pii> moveGen(pii pos, bool rev=false){
        vector<pii> neighbours; 
        int x, y;
        // Rotation -> DOWN < UP < RIGHT < LEFT
        int rot_x[] = {1, -1, 0, 0};
        int rot_y[] = {0, 0, 1, -1};
        for(int i=0; i<4; ++i){
            x = pos.first + rot_x[i]; 
            y = pos.second + rot_y[i];
            if(x >= 0 && x < M && y >= 0 && y < N){// if valid x, y co-ordinates
                if(G[x][y].value == ' ' || G[x][y].value == '*'){
                    neighbours.push_back(make_pair(x, y));
                }
            }
        }
        if(rev) // reverse order
            std::reverse(neighbours.begin(), neighbours.end());
        return neighbours;
    }


    bool goalTest(pii pos){
        if(pos==nil)
            return false;
        return (G[pos.first][pos.second].value == '*');
    }


    pii bfs(){

        queue<pii> Q;

        // Push Source
        Q.push(zero);    
        nodes_visited = 0;
        get_node(zero)->visited = true;
        while(!Q.empty()){

            // Pop source
            pii source = Q.front();
            Q.pop();

            nodes_visited ++;
            // Mark source visited
            // get_node(source)->visited = true;

            // Goal test
            if(goalTest(source))
                return source;

            // Check neighbours
            vector<pii> neighbours = moveGen(source);
            for(pii n: neighbours){
                if(!get_node(n)->visited){
                    get_node(n)->visited = true;
                    G[n.first][n.second].parent = source;
                    Q.push(n);
                }
            }
        }
        return {-1, -1};        
    }


    pii dfs(){

        stack<pii> S;

        // Push Source
        S.push(zero);    

        while(!S.empty()){

            // Pop source
            pii source = S.top();
            S.pop();

            // Mark source visited
            get_node(source)->visited = true;
            get_node(source)->explored = true;

            // Mark depth of node using parent
            if(source != zero)
                get_node(source)->depth = get_node(get_node(source)->parent)->depth + 1;
            
            // Goal test
            if(goalTest(source))
                return source;

            // Check neighbours
            vector<pii> neighbours = moveGen(source, true);
            for(pii n: neighbours){
                if(!G[n.first][n.second].explored){
                    get_node(n)->parent = source;
                    get_node(n)->explored = true;
                    S.push(n);
                }
            }
        }
        return {-1, -1};        
    }


    pii dls(pii source, int bound){
        nodes_visited ++;
        node* src = get_node(source);
        src->visited = true;
        
        if(goalTest(source))
            return source;

        if(bound > 0){
            for(pii n: moveGen(source)){
                node* nb = get_node(n); 
                if(nb->visited && src->depth + 1 >= nb->depth)
                    continue;
                nb->depth = src->depth + 1;
                nb->parent = source;

                pii goal = dls(n, bound-1);
                if(goal != nil)
                    return goal;                
            }
        }
        return nil;
    }

    pii dfid(){
        int bound = 0;
        nodes_visited = 0;
        while(true){
            reset_nodes();
            max_bound = bound;
            pii goal = dls(zero, bound);
            if(goalTest(goal)){
                return goal;
            }
            bound++;
        } 
    }

    bool is_boundary(string line){
        line.erase(std::remove(line.begin(), line.end(), '\n'), line.end());
        if(line.empty() || line[0]!='+')
            return false;
        for(int i=1; i<line.size()-2; i = i+3){
            if(line[i] != '-' || line[i+1] != '-')
                return false;
            if(line[i+2] != '+')
                return false;
        }
        return true;
    }

public:
    void input(string filename){
        string line;
        vector<string> lines;
        ifstream fin(filename);

        fin >> algo;
        fin.ignore();
        // read first line
        getline(fin, line, '\n');
        lines.push_back(line);
        
        while(true){
            getline(fin, line, '\n');
            lines.push_back(line);
            if(is_boundary(line))
                break;
        }

        M = lines.size();
        N = line.size();
        for(string line: lines){
            vector<node> v;
            for(char c: line){
                node n;
                n.value = c;
                v.push_back(n);
            }
            G.push_back(v);
        }
    }

    void printOutput(string filename){
        ofstream fout(filename);
        pii goal;
        int num_states = 0; // number of states
        switch(algo){
            case 0: {
                goal = bfs();   
                num_states = nodes_visited;       
                break;
            }
            case` 1: {
                goal = dfs();
                //count number of states
                for(int i=0; i<M; ++i)
                    for(int j=0; j<N; ++j)
                        if(G[i][j].visited)
                            num_states ++;
                break;
            }
            case 2: {
                goal = dfid();  
                num_states = nodes_visited -1;
                break;
            }
            default: cout << "Invalid input.\n";    break;
        }

        // Print num_states
        fout << num_states << "\n" ;

        // length of path found
        int len = 1;
        pii pos = goal;
        get_node(pos)->value = '0';
        while(pos != zero){
            pos = get_node(pos)->parent;
            get_node(pos)->value = '0'; // colour Graph
            len ++;
        }
        fout << len << "\n";

        // maze
        for(int i=0; i<M; ++i){
            for(int j=0; j<N; ++j){
                fout << G[i][j].value;
                if(G[i][j].value == '0')
                    G[i][j].value = ' ';
            }
            fout << "\n";
        }
    }
};

int main(int argc, char** argv){
    
    if(argc != 2){
        cout<<"Usage ./run.sh <filename>"<<endl;
        return 1;
    }

    Maze M;
    M.input(argv[1]);
    M.printOutput("output.txt");
    
    return 0;
}
