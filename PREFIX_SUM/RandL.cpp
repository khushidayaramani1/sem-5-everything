#include<iostream>
using namespace std;
int main(){
    int nums[]={1,2,3,4,5,6,7,8,9};
    for(int i=1;i<9;i++){
        nums[i]=nums[i]+nums[i-1];
    }
    for(int elem:nums){
        cout<<elem<<" ";
    }
}
