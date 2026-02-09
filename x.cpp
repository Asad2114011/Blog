#include <bits/stdc++.h>
using namespace std;
#define ll long long
int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);
    ll t;
    cin >> t;
    while (t--)
    {
      ll n,m,k;
      cin>>n>>m>>k;
      ll x=0,y=0;
      if(k-1>n-k)k=n-k+1;

      while(true){
        ll cur_x=x+y+max(x+1,y);
        if(x<k-1&&cur_x<=m)x++;
        
        ll cur_y=x+y+max(x,y+1); 
        if(y<n-k&&cur_y<=m)y++;
        else break;
      }
      cout<<x+y+1<<'\n';
      
    }
    return 0;
}