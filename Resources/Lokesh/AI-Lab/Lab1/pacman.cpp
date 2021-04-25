#include <iostream>
#include <string>
#include <vector>
#include <queue> 
#include <stack>
#include <fstream>

using namespace std;
int states = 1;
int arpit;
bool flag = false;

struct position {
    int data;
    position* parent;
    int depth;
    bool visited;
    position() {
        parent = NULL;
        visited = false;
        depth = 99999;
    }
};

struct adj {
    vector<position*> arr;
    void disp() {
        for(int i = 0;i < arr.size();i++) {
            cout << arr[i]->data << " ";
        }
        cout << endl;
    }
};

void dfid(position* start,adj* adj_list,int depth,int dest,position* node) {
    if(start->depth < depth) {
        start->visited = true;
        if (start->data == dest) {
            arpit = states;
        }
        states++;
        for(int i = 0;i < adj_list[start->data].arr.size();i++) {
            if((adj_list[start->data].arr[i]->depth > start->depth + 1)) {
                adj_list[start->data].arr[i]->parent = start;
                adj_list[start->data].arr[i]->depth = start->depth + 1;
                dfid(adj_list[start->data].arr[i],adj_list,depth,dest,node);
            }
        }
    }
    return;
}

int main(int argc, char* argv[]) {
    ifstream inp;
    inp.open(argv[1]);
    vector<string> input;
    string temp;
    getline(inp,temp);
    int algo = stoi(temp);
    while(getline(inp,temp)) {
        input.push_back(temp);
    }

    int m = input.size();
    int n = input[0].length();

    int source = 0;
    int dest;

    position node[99999];
    adj adj_list[99999];

    for(int i = 0;i < input.size();i++) {
        for(int j = 0;j < input[i].size();j++) {
            int pos = n*i + j;
            node[pos].data = pos;
            if(input[i][j] == '*') dest = pos;
            if(input[i][j] == ' ' or ( i == 0 && j == 0)) {
                if(i < m && (input[i+1][j] == ' ' or input[i+1][j] == '*')) adj_list[pos].arr.push_back(&node[pos + n]);
                if(i > 0 && (input[i-1][j] == ' ' or input[i-1][j] == '*')) adj_list[pos].arr.push_back(&node[pos - n]);
                if(j < n && (input[i][j+1] == ' ' or input[i][j+1] == '*')) adj_list[pos].arr.push_back(&node[pos + 1]);
                if(j > 0 && (input[i][j-1] == ' ' or input[i][j-1] == '*')) adj_list[pos].arr.push_back(&node[pos - 1]);
            }
        }
    }
    int length = 1;

    //BFS
    if(algo == 0) {
        queue<position*> que;
        node[source].depth = 0;
        que.push(&node[source]);
        
        while(!que.empty()) {
            int que_front_index = que.front()->data;
            for(int i = 0;i < adj_list[que_front_index].arr.size();i++) {
                int pos = adj_list[que_front_index].arr[i]->data;
                if(node[pos].visited == false) {
                    node[pos].visited = true;
                    node[pos].parent = &node[que_front_index];
                    que.push(&node[pos]);
                }
            }
            if(que.front()->data == dest) break;
            que.pop();
            states++;
        }
    }

    //DFS
    if(algo == 1) {
        stack<position*> que;
        node[source].depth = 0;
        que.push(&node[source]);
        
        while(!que.empty()) {
            int que_front_index = que.top()->data;
            que.pop();
            states++;
            for(int i = 0;i < adj_list[que_front_index].arr.size();i++) {
                int pos = adj_list[que_front_index].arr[i]->data;
                if(node[pos].visited == false) {
                    node[pos].visited = true;
                    node[pos].parent = &node[que_front_index];
                    que.push(&node[pos]);
                }
            }
            if(que.top()->data == dest) break;
        }
    }

    //DFID
    if(algo == 2) {
        node[source].depth = 0;
        for(int i = 0;i < m*n;i++) {
            
            dfid(&node[source],adj_list, i,dest,node);
            for(int j = 0;j < m*n;j++) {
                node[j].depth = 99999;
                node[i].visited = false;
                node[i].parent = NULL;
            }
            node[source].depth = 0;
            if(node[dest].visited == true) break;
        }
    }

    position* path = &node[dest];

    while(path->parent != NULL) {
        int x = path->data / n;
        int y = path->data % n;
        input[x][y] = '0';
        path = path->parent;
        length++;
    }
    input[0][0] = '0';
    if(algo == 2) states= arpit - 1;
    cout << states << endl << length << endl;
    for(int i = 0;i < input.size(); i++) cout << input[i] << endl;
}