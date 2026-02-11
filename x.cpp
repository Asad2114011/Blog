#include <bits/stdc++.h>
using namespace std;
#define ll long long
const int N=2e5+5;
map<int,pair<int,set<int>>>m;
vector<int>v[N],dis(N,-1);
vector<bool>vis(N,false);
void bfs(int s){
  queue<int>q;
  q.push(s);
  vis[s]=true;
  dis[s]=0;
  while(!q.empty()){
    int cur=q.front();
    q.pop();
    for(int i:v[cur]){
       if(!vis[i]){
        q.push(i);
        vis[i]=true;
        dis[i]=dis[cur]+1;
        m[dis[i]].first++;
        m[dis[i]].second.insert(cur);
       }
    }
  }
  return;
}
int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);
    ll t;
    cin >> t;
    while (t--)
    {
      int n;
      cin>>n;
      for(int i=1;i<=n;i++){
        vis[i]=false;
        dis[i]=-1;
        v[i].clear();
      }
      m.clear();
      n--;
      while(n--){
        int l,r;
        cin>>l>>r;
        v[l].push_back(r);
        v[r].push_back(l);
      }
      bfs(1);
      int mx=-1;
      for(auto i:m){
        if(i.second.first>=mx){
          mx=i.second.first;
          if(i.second.second.size()==1)mx++;
        }
      }
      cout<<mx<<'\n';
      
    }
    return 0;
}