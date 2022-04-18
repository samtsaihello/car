#include <iostream>
using namespace std;
#include <queue>
int adj[100][4] = {};
int pred[100] = {};
int dis[100] = {};
int level[100] = {};
int num_of_adj[100] = {};
bool counted[100] = {};
bool cannotfind = 0;


int main(){
    int num;
    int start, end;
    cin >> num >> start >> end;
    for (int i = 1; i <= num; i++){
        cin >> num_of_adj[i];
        if(num_of_adj[i] == 0) continue;
        else{
            for (int j = 0; j < num_of_adj[i]; j++){
                cin >> adj[i][j];
            }
        }
    }
    queue <int> que;
    que.push(end);
    dis[end] = 0;
    level[end] = 0;
    int lv = 1;
    bool start_appear = 0;
    while(true){
        for(int i = 0; i < num_of_adj[que.front()]; i++){
            if(counted[(adj[que.front()][i])] == 0){
                level[adj[que.front()][i]] = lv;
                counted[(adj[que.front()][i])] = 1;
                que.push(adj[que.front()][i]);
                dis[adj[que.front()][i]] = dis[que.front()] + 1;
                if(pred[adj[que.front()][i]] == 0){
                    pred[adj[que.front()][i]] = que.front();
                }
                if(adj[que.front()][i] == start){
                    start_appear = 1;
                    break;
                }
            }
        }
        if(start_appear == 1) break;
        if(que.size() == 1) {
            cannotfind = 1;
            break;
        }
        else que.pop();
        lv++;
    }
    int present = start;
    cout << level[start] <<'\n';
    if(cannotfind == 1) cout << "We can't find a path!" << '\n';
    else{
        for(int i = level[start]; i > 0; i--){
            cout<< pred[present] << " ";
            present = pred[present];
        }
    }


    return 0;
}