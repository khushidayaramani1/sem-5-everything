#include<iostream>
using namespace std;

int fact(int n){
     if(n==0){
        return 1;
     }
     else if(n==1){
        return 1;
     }
    else{
        return n*fact(n-1);
    }
}

int ncr(int n,int r){
return fact(n)/(fact(r)*fact(n-r));
}
 int main(){
    int n=5;
    for(int i=0;i<n;i++){
            for(int j=0;j<=i;j++){
                cout<<ncr(i,j)<<" ";
            }
        cout<<"\n";
    }
}
