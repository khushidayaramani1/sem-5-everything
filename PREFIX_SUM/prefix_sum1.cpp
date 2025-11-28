#include<iostream>
using namespace std;

int main(){
    int nums[]={1,2,3,5,8,4,9,7,6};
    int length=sizeof(nums)/sizeof(nums[0]);
    for(int i=1;i<length;i++){
        nums[i]=nums[i]+nums[i-1];
    }
    for(int elem:nums){
        cout<<elem<<" ";
    }
}
