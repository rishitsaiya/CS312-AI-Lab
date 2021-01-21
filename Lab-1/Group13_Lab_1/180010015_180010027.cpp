#include <bits/stdc++.h>
using namespace std;

int **Binary_Maze;     // matrix to contain maze in binary form
int **Path_For_Pacman; // matrix to binary_Maze the final path

int NumOfStateExplored = 0; // number of states explored before reaching the goal

/* structure to binary_Maze coordinates of a cell */
struct Point{
    int x, y;
};

/* structure which contains the coordinates, distance from source and parent of the cell */
struct PointList{
    Point point;
    int point_distance;
    PointList *pointer;
};

/* function to check if a cell is valid */
bool validity(int row, int column, int n, int m){
    if ((row >= 0) && (row < n) && (column >= 0) && (column < m))
        return true;
    else
        return false;
}

/* arrays which contain the order in which next valid cells are to be explored */
// Order: DURL - Down > Up > Right > Left
int row_Shift[] = {1, -1, 0, 0};
int column_Shift[] = {0, 0, 1, -1};

/* function to implement depth first search */
int DFS(int **path, int n, int m, Point Food_destination){
    
    /* matrix to binary_Maze Visited_Cells cells */
    bool visited[n][m];
    memset(visited, false, sizeof visited); 
    visited[0][0] = true;

    /* stack that maintains the cells that are to be explored next */
    stack<PointList *> stac;
    PointList *start = new PointList;
    start->point.x = 0;
    start->point.y = 0;
    start->point_distance = 0;
    start->pointer = NULL;
    stac.push(start);

/*Checking if the stack is empty or not and pointing it to current cell*/
    while (!stac.empty()){
        PointList *current = stac.top();
        Point point = current->point;

        /* checking if the current cell is goal, storing the path and returning the path distance */
        if (point.x == Food_destination.x && point.y == Food_destination.y){
            NumOfStateExplored++;
            PointList *Source = current;
            while (Source->pointer != NULL){
                Path_For_Pacman[Source->point.x][Source->point.y] = 1;
                Source = Source->pointer;
            }
            Path_For_Pacman[Source->point.x][Source->point.y] = 1;
            return current->point_distance;
        }

        /* checking for valid adjacent cells that can be explored and pushing them to the stack */
        stac.pop();
        for (int i = 0; i < 4; i++){
            int hori = point.x + row_Shift[i];
            int verti = point.y + column_Shift[i];
            if (validity(hori, verti, n, m) && path[hori][verti] && !visited[hori][verti]){
                visited[hori][verti] = true;
                PointList *neibhouring_Cell = new PointList;
                neibhouring_Cell->point.x = hori;
                neibhouring_Cell->point.y = verti;
                neibhouring_Cell->point_distance = current->point_distance + 1;
                neibhouring_Cell->pointer = current;
                stac.push(neibhouring_Cell);
            }
        }
        NumOfStateExplored++;
    }
    return -1;
}

/* function to implement breadth first search */
int BFS(int **path, int n, int m, Point Food_destination){
    
    /* matrix to binary_Maze Visited cells */
    bool visited[n][m];
    memset(visited, false, sizeof visited); 
    visited[0][0] = true;

    /* queue that maintains the cells that are to be explored next */
    queue<PointList *> que;
    PointList *start = new PointList;
    start->point.x = 0;
    start->point.y = 0;
    start->point_distance = 0;
    start->pointer = NULL;
    que.push(start);

/*Checking if the queue is empty or not and pointing it to current cell*/
    while (!que.empty()){

        PointList *current = que.front();
        Point point = current->point;

        /* checking if the current cell is goal, storing the path and returning the path distance */
        if (point.x == Food_destination.x && point.y == Food_destination.y){
            NumOfStateExplored++;
            PointList *Source = current;
            while (Source->pointer != NULL){
                Path_For_Pacman[Source->point.x][Source->point.y] = 1;
                Source = Source->pointer;
            }
            Path_For_Pacman[Source->point.x][Source->point.y] = 1;
            return current->point_distance;
        }

/* checking for valid adjacent cells that can be explored and pushing them to the queue */

        que.pop();
        for (int i = 0; i < 4; i++){
            int hori = point.x + row_Shift[i];
            int verti = point.y + column_Shift[i];
            if (validity(hori, verti, n, m) && path[hori][verti] && !visited[hori][verti]){
                visited[hori][verti] = true;
                PointList *neibhouring_Cell = new PointList;
                neibhouring_Cell->point.x = hori;
                neibhouring_Cell->point.y = verti;
                neibhouring_Cell->point_distance = current->point_distance + 1;
                neibhouring_Cell->pointer = current;
                que.push(neibhouring_Cell);
            }
        }
        NumOfStateExplored++;
    }
    return -1;
}

/* function to implement depth limited search */

bool **Visited_Cells; // matrix to binary_Maze Visited cells
int **min_depth;      // matrix to binary_Maze the minimum depth at which the cells are Visited

int DFIS(int **path, int n, int m, Point Previous, Point Food_destination, int limit, PointList *prev_ptr){
    /* if depth limit is reached, returns -1 */
    if (limit == 0)
        return -1;

    /* node to binary_Maze details of the current cell */
    PointList *Current = new PointList;
    Current->point.x = Previous.x;
    Current->point.y = Previous.y;
    Current->point_distance = prev_ptr->point_distance + 1;
    Current->pointer = prev_ptr;
    min_depth[Previous.x][Previous.y] = Current->point_distance;

    /* checking if the current cell is goal, storing the path and returning the path distance */
    if (Previous.x == Food_destination.x && Previous.y == Food_destination.y){
        PointList *Prev = Current;
        while (Prev->pointer != NULL){
            Path_For_Pacman[Prev->point.x][Prev->point.y] = 1;
            Prev = Prev->pointer;
        }
        Path_For_Pacman[Prev->point.x][Prev->point.y] = 1;
        return Current->point_distance;
    }
/*Increamenting the states explored and marking the visiting cells in maze*/
    NumOfStateExplored++;
    Visited_Cells[Previous.x][Previous.y] = true;

    /* checking for valid adjacent cells that can be explored */
    for (int i = 0; i < 4; i++){
        int row = Previous.x + row_Shift[i];
        int column = Previous.y + column_Shift[i];

        Point curr_point;
        curr_point.x = row;
        curr_point.y = column;

        if (
            validity(row, column, n, m) 
            && path[row][column] 
            && (!Visited_Cells[row][column] || min_depth[row][column] > Current->point_distance + 1)
        ){
            int dist = DFIS(path, n, m, curr_point, Food_destination, limit - 1, Current);

            if (dist > -1)
                return dist;
        }
    }
    return -1;
}

int main(int argc, char *argv[]){
    int ALGO_CODE; // defines the type of search to be implemented

    vector<char> Maze; // binary_Mazes contents of Maze

    int n = 0, m = 0;   // row and column size of the Maze
    int food_X, food_Y; // the coordinates of goal cell

    ifstream inout_File(argv[1]); // opening Binary_Maze file stream and reading Binary_Maze file

/*String input for algorithm code*/
    string firstLine;
    getline(inout_File, firstLine);
    ALGO_CODE = stoi(firstLine);

/*Maze input*/
    string eachLine;
    while (getline(inout_File, eachLine)){
        m = 0;

        while (char ch = eachLine[m]){
            Maze.push_back(ch);

            if (ch == '*'){
                food_X = n, food_Y = m;
            }
            m++; // column size
        }
        n++; // row size
    }

    Binary_Maze = new int *[m];     // creating matrix to contain maze in binary form
    Path_For_Pacman = new int *[m]; // creating matrix to binary_Maze the final path

    for (int i = 0; i < n; i++){
        Binary_Maze[i] = new int[m];
        Path_For_Pacman[i] = new int[m];
    }

    int index = 0;
    for (int i = 0; i < n; i++){
        for (int j = 0; j < m; j++){
            if (Maze[index] == ' ')
                Binary_Maze[i][j] = 1;
            else
                Binary_Maze[i][j] = 0;

            index++;
        }
    }

    Binary_Maze[0][0] = 1;
    Binary_Maze[food_X][food_Y] = 1;

    Point initial_pos = {0, 0};
    Point Food_destination = {food_X, food_Y};
    int distance = -1; // distance of goal from source

    if (!Binary_Maze[0][0] || !Binary_Maze[Food_destination.x][Food_destination.y]){
        distance = -1;
    }
    else if (ALGO_CODE == 0) /* BFS */{
        distance = BFS(Binary_Maze, n, m, Food_destination);
    }
    else if (ALGO_CODE == 1) /* DFS */{
        distance = DFS(Binary_Maze, n, m, Food_destination);
    }
    else if (ALGO_CODE == 2) /* DFIS */{

/*Boundary Condition for depth and visited cells*/
        Visited_Cells = new bool *[m];
        min_depth = new int *[m];

        int limit = 0;

        PointList *Source = new PointList;

        Source->point.x = 0;
        Source->point.y = 0;
        Source->point_distance = 0;
        Source->pointer = NULL;

        while (distance == -1){
            limit++;

            for (int i = 0; i < n; i++){
                Visited_Cells[i] = new bool[m];
                min_depth[i] = new int[m]; //iteratively increase depth until goal is found
            }

            distance = DFIS(Binary_Maze, n, m, initial_pos, Food_destination, limit, Source);
        }
        distance--;
    }

    /* Printing output to file */

    ofstream out;
    out.open("output.txt");

/* Output no.of states and path distance */
    out << NumOfStateExplored << endl;
    out << ++distance;

/* Printing maze to output file */
    index = 0;
    for (int i = 0; i < n; i++){
        out << "\n";
        for (int j = 0; j < m; j++){
            if (Path_For_Pacman[i][j] == 1)
                out << 0;
            else
                out << Maze[index];
            index++;
        }
    }

    out.close();

    return 0;
}