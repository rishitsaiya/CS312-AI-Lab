// #include <iostream> 
// #include<fstream>
// #include <queue> 
// #include <vector>
// #include<stack>
// #include<string>
// #include<cstring>

#include<bits/stdc++.h>

using namespace std; 
int **input; //matrix to contain maze in binary form
bool **visited; //matrix to store visited cells
int **min_depth; //matrix to store the minimum depth at which the cells are visited
int **final_path; //matrix to store the final path
int states_explored = 0; //number of states explored before reaching the goal

/* struct to store coordinates of a cell */
struct Point { 
    int x; 
    int y; 
}; 

/* struct which contains the coordinates, distance from source and parent of the cell */
struct queueNode { 
    Point pt;
    int dist;
    queueNode* pptr; 
}; 
 
/* function to check if a cell is valid */  
bool isValid(int row, int col, int n, int m) { 
    return (row >= 0) && (row < n) && 
           (col >= 0) && (col < m); 
} 

/* arrays which contain the order in which next valid cells are to be explored */ 
int rowNum[] = {1, -1, 0, 0}; 
int colNum[] = {0, 0, 1, -1}; 

/* function to implement depth limited search */
int final_DFIS(int** mat, int n, int m, Point src, Point dest, int limit, queueNode* prev_ptr, bool** visited, int** min_depth) { 
    /* check to ensure that source and goal cells are valid */
    if (!mat[src.x][src.y] || !mat[dest.x][dest.y]) {
        return -1; 
    }
    /* if depth limit is reached, returns -1 */
    if (limit==0){
        return -1;
    }
    /* node to store details of the current cell */
    queueNode* root = new queueNode;
    root->pt.x = src.x;
    root->pt.y = src.y;
    root->dist = prev_ptr->dist + 1;
    root->pptr = prev_ptr;
    min_depth[src.x][src.y]=root->dist;

    /* checking if the current cell is goal, storing the path and returning the path distance */
    if (src.x == dest.x && src.y == dest.y){
        queueNode* curr = root;
        while(curr->pptr!=NULL){
            final_path[curr->pt.x][curr->pt.y]=1;
            curr = curr->pptr;
        }
        final_path[curr->pt.x][curr->pt.y]=1;
        return root->dist; 
    }
    states_explored++;
    visited[src.x][src.y] = true;

    /* checking for valid adjacent cells that can be explored */
    for (int i = 0; i < 4; i++) { 
        int row = src.x + rowNum[i]; 
        int col = src.y + colNum[i]; 
        Point curr_point;
        curr_point.x = row;
        curr_point.y = col;
        if (isValid(row, col, n, m) && mat[row][col] &&  
           (!visited[row][col] || min_depth[row][col]>root->dist+1)) { 
            int dist = final_DFIS(mat, n, m, curr_point, dest, limit - 1, root, visited, min_depth);
            if(dist > -1){
                return dist;
            }
        }
    }
    return -1;
} 

/* function to implement depth first search */
int final_DFS(int** mat, int n, int m, Point src, Point dest) { 
	states_explored=0;
    /* check to ensure that source and goal cells are valid */
    if (!mat[src.x][src.y] || !mat[dest.x][dest.y]) 
        return -1; 
    /* matrix to store visited cells */
    bool visited[n][m]; 
    memset(visited, false, sizeof visited); 
    visited[src.x][src.y] = true;  
    
    /* stack that maintains the cells that are to be explored next */
    stack <queueNode*> q; 
    queueNode* s = new queueNode;
    s->pt.x = src.x;
    s->pt.y = src.y;
    s->dist = 0;
    s->pptr = NULL;
   	q.push(s);

    while (!q.empty()) { 
    	states_explored++;
        queueNode* curr = q.top(); 
        Point pt = curr->pt; 

        /* checking if the current cell is goal, storing the path and returning the path distance */
        if (pt.x == dest.x && pt.y == dest.y) {
        	queueNode* root = curr;
        	while(root->pptr!=NULL){
        		final_path[root->pt.x][root->pt.y]=1;
        		root = root->pptr;
        	}
        	final_path[root->pt.x][root->pt.y]=1;
            return curr->dist; 
        }
        q.pop(); 
    
        /* checking for valid adjacent cells that can be explored and pushing them to the stack */
        for (int i = 0; i < 4; i++) { 
            int row = pt.x + rowNum[i]; 
            int col = pt.y + colNum[i]; 
            if (isValid(row, col, n, m) && mat[row][col] &&  
               !visited[row][col]) {  
                visited[row][col] = true; 
                queueNode* Adjcell = new queueNode;
                Adjcell->pt.x = row;
                Adjcell->pt.y = col;
                Adjcell->dist = curr->dist + 1;
                Adjcell->pptr = curr;
                q.push(Adjcell); 
            } 
        } 
    } 
    return -1; 
} 

/* function to implement breadth first search */
int final_BFS(int** mat, int n, int m, Point src, Point dest) { 
	states_explored=0;
    /* check to ensure that source and goal cells are valid */
    if (!mat[src.x][src.y] || !mat[dest.x][dest.y]) 
        return -1; 
  
    /* matrix to store visited cells */
    bool visited[n][m]; 
    memset(visited, false, sizeof visited); 
    visited[src.x][src.y] = true;  

    /* queue that maintains the cells that are to be explored next */
    queue <queueNode*> q; 
    queueNode* s = new queueNode;
    s->pt.x = src.x;
    s->pt.y = src.y;
    s->dist = 0;
    s->pptr = NULL;
    q.push(s); 
    while (!q.empty()) { 
    	states_explored++;
        queueNode* curr = q.front(); 
        Point pt = curr->pt; 

        /* checking if the current cell is goal, storing the path and returning the path distance */
        if (pt.x == dest.x && pt.y == dest.y) {
        	queueNode* root = curr;
        	while(root->pptr!=NULL){
        		final_path[root->pt.x][root->pt.y]=1;
        		root = root->pptr;
        	}
        	final_path[root->pt.x][root->pt.y]=1;
            return curr->dist; 
        }
        q.pop(); 
  
        /* checking for valid adjacent cells that can be explored and pushing them to the queue */
        for (int i = 0; i < 4; i++) { 
            int row = pt.x + rowNum[i]; 
            int col = pt.y + colNum[i]; 
            if (isValid(row, col, n, m) && mat[row][col] &&  
               !visited[row][col]) { 
                visited[row][col] = true; 
                queueNode* Adjcell = new queueNode;
                Adjcell->pt.x = row;
                Adjcell->pt.y = col;
                Adjcell->dist = curr->dist + 1;
                Adjcell->pptr = curr;
                q.push(Adjcell); 
            } 
        } 
    } 
    return -1; 
} 

int main(int argc, char* argv[]) { 	
    int mode; //defines the type of search to be implemented
    int n, m; //row and column size of the maze
    int counter = 0; //keeps track of the input file contents in terms of number of lines
    int dest_x, dest_y; // stores the coordinates of goal cell
    vector<string>store; //helps in converting maze into binary matrix
    vector<char>maze; //stores contents of maze 

    /* opening input file stream and reading input file */
    ifstream in_file(argv [1]);
    string s;
    while (getline(in_file, s)) {
        if(counter==0){
            mode=stoi(s);
            counter++;
            continue;
        }
        if(counter==1){
        	m = s.size(); //fetching column size
        }
        string l;
        bool is_empty = true;
        for (int i = 0; i < s.size(); i++) {
            char c = s[i];
            if (isblank(c)) {
                l += "1";
                store.push_back("1");
                maze.push_back(s[i]);
            }
            else if (c == '*') {
                l += "*";
                 store.push_back("*");
                 maze.push_back(s[i]);
                 dest_x = counter-1;
                 dest_y = i;
            }
            else if (c == '-'){
                l += "0";
                 store.push_back("0");
                 maze.push_back(s[i]);
            }
            else if (c == '|'){
                l += "0";
                 store.push_back("0");
                 maze.push_back(s[i]);
            }
            else{
            	l += "0";
                 store.push_back("0");
                 maze.push_back(s[i]);
            }
            is_empty = false;
        }
        if(!is_empty){
        	counter++;
        }
    }
    if(s.size()!=0){
    	m = s.size(); //fetching column size
    }
    n = counter-1; //fetching row size
    input = new int *[m]; //creating matrix to contain maze in binary form
    final_path = new int *[m]; //creating matrix to store the final path
    /* processing maze into binary format */
    store[0]="1";
    for(int i = 0; i <n; i++){
    	input[i] = new int[m];
    }
    for(int i = 0; i <n; i++){
    	final_path[i] = new int[m];
    }
    int feed = 0;
    for(int i=0;i<n;i++){
       for(int j=0;j<m;j++){
            if(store[feed]=="1" || store[feed]=="*"){
                input[i][j]=1;
            }
            else{
                input[i][j]=0;
            }
            feed++;
       }
    }
    input[0][0]=1;
    input[dest_x][dest_y]=1;
	Point source = {0, 0}; 
    Point dest = {dest_x, dest_y};
    int dist; //stores distance of goal from source
    
    if(mode == 0) /* BFS mode */{
    	dist = final_BFS(input, n, m, source, dest); 
    }
    else if(mode == 1) /* DFS mode */{
    	dist = final_DFS(input, n, m, source, dest); 
    }
    else if(mode == 2) /* DFIS mode */{
    	int iter=0;
        int limit = 1;
        int prev_states_explored = 0;
        queueNode* root = new queueNode;
        root->pt.x = source.x;
        root->pt.y = source.y;
        root->dist = 0;
        root->pptr = NULL;
        while(true){
            visited = new bool *[m];
            for(int i = 0; i <n; i++){
                visited[i] = new bool[m];
            }
            min_depth = new int *[m];
            for(int i = 0; i <n; i++) {
            //iteratively increase depth until goal is found
                min_depth[i] = new int[m];
            }
            dist = final_DFIS(input, n, m, source, dest, limit, root, visited, min_depth);
            prev_states_explored = states_explored;
            iter++;
            if(dist == -1){
                limit++;
            }
            else{
                break;
            }
        }
        dist--;
    }
    /* printing output to file */
    ofstream out;
    out.open("output.txt");
    out<<states_explored<<endl;
    if (dist)  
        out<< dist+1<<endl; 
    else
        out<<-1<<endl;
    int temp = 0; 
    for(int i=0;i<n;i++){
    	for(int j=0;j<m;j++){
    		if(final_path[i][j]==1){
                out<<0;
            }
    		else{
                out<<maze[temp];
            }
    		temp++;
    	}
        if(i!=n-1)
            out<<endl;
    }
    out.close();
	return 0; 
} 