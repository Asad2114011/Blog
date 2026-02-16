#include <bits/stdc++.h>
using namespace std;
#define ll long long
int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);
    int t;
    cin >> t;
    while (t--)
    {
      int n;
      cin>>n;
      vector<int>v(n);
      for(int i=0;i<n;i++)cin>>v[i];
      int cnt=0;
      for(int i=0;i<n-1;i++){
        if(v[i]+v[i+1]==7||v[i]==v[i+1]){cnt++;i++;}        
      }
      cout<<cnt<<'\n';

    }
    return 0;
}