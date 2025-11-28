#include<iostream>
using namespace std;
int main(){
    int prefixSum=0,totalSum=0,suffixSum;
    int nums[]={2,5,1,6,2};
    int length=sizeof(nums)/sizeof(nums[0]);
    for(int elem:nums){
        totalSum+=elem;
    }

    for(int i=0;i<length;i++){
        prefixSum+=nums[i];
        suffixSum=totalSum-prefixSum;
        if(prefixSum==suffixSum){
            cout<<"yes";
            break;
        }
    }


}
