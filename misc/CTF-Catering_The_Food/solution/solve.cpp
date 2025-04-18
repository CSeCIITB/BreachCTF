#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

const ll maxn = 600100;
const ll MOD = 1e9+7;

ll a,b,c;
ll factorial[maxn+100],inverse_fact[maxn+100],power[maxn+100];

ll comb(ll a,ll b,ll c)
{
    return factorial[a+b+c]*inverse_fact[a]%MOD*inverse_fact[b]%MOD*inverse_fact[c]%MOD;
}

ll comb(ll a,ll b)
{
    return factorial[a]*inverse_fact[b]%MOD*inverse_fact[a-b]%MOD;
}


ll calc(ll k)
{
    ll d = b - c;
    ll res=0;
    for(ll t1 = 0;2 * t1 + d <= k;t1++)
    {
        ll t2 = t1 + d;
        ll t3 = k - t1 - t2;
        if(c - t1 - t3 < 0) continue;
        res = (res + comb(t1,t2,t3) * comb(c - t1 - t3 + k-1,k-1) % MOD * power[t3] % MOD)%MOD;
    }
    return res;
}
ll solve(ll a)
{
    return ((2LL*calc(a)%MOD + calc(a+1))%MOD + calc(a-1))%MOD;
}
int main()
{
    power[0]=1;
    for(ll i=1;i<=maxn;i++) {
      power[i]=(power[i-1]*2)%MOD;
    }

    factorial[0]=1;
    for(ll i=1;i<=maxn;i++) {
      factorial[i]=factorial[i-1]*i%MOD;
    }

    inverse_fact[1]=1;
    inverse_fact[0]=1;
    for(ll i=2;i<=maxn;i++) {
      inverse_fact[i]=(MOD-(MOD/i)*inverse_fact[MOD%i]%MOD)%MOD;
    }
    for(ll i=1;i<=maxn;i++)  {
      inverse_fact[i]=inverse_fact[i-1]*inverse_fact[i]%MOD;
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
