#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

const int maxn = 600100;
const int mod = 1e9+7;

ll fac[maxn+100],inv[maxn+100],power[maxn+100];

int a,b,c;

ll comb(int a,int b)
{
    return fac[a]*inv[b]%mod*inv[a-b]%mod;
}
ll comb(int a,int b,int c)
{
    return fac[a+b+c]*inv[a]%mod*inv[b]%mod*inv[c]%mod;
}
int calc(int k)
{
    int d = b - c;
    int res=0;
    for(int t1 = 0;2 * t1 + d <= k;t1++)
    {
        int t2 = t1 + d;
        int t3 = k - t1 - t2;
        if(c - t1 - t3 < 0) continue;
        res = (res + comb(t1,t2,t3) * comb(c - t1 - t3 + k-1,k-1) % mod * power[t3] % mod)%mod;
    }
    return res;
}
ll solve(int a)
{
    return ((2LL*calc(a)%mod + calc(a+1))%mod + calc(a-1))%mod;
}
int main()
{
    fac[0]=1;
    for(int i=1;i<=maxn;i++) {
      fac[i]=fac[i-1]*i%mod;
    }
    inv[1]=1;
    inv[0]=1;
    for(int i=2;i<=maxn;i++) {
      inv[i]=(mod-(mod/i)*inv[mod%i]%mod)%mod;
    }
    for(int i=1;i<=maxn;i++)  {
      inv[i]=inv[i-1]*inv[i]%mod;
    }
    power[0]=1;
    for(int i=1;i<=maxn;i++) {
      power[i]=(power[i-1]*2)%mod;
    }
    cin>>a>>b>>c;
    {
        if(a<c) swap(a,c);
        if(a<b) swap(a,b);
        if(b<c) swap(b,c);
        std::cout << solve(a) << '\n';
    }
    return 0;
}