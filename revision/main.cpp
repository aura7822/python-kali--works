#include<iostream>
using namespace std;

int age;
string booktitle;
int main(){
    cout<<"Enter your age : ";
    cin>>age;
    cout<<"\n";
    cout<<(age <= 17 ? "Not allowed to vote!" : "Allowed to vote!\n");
    cin.ignore();
    cout<<"Enter the book title : ";
    getline(cin, booktitle);
    cout<<"\n";
    cout<<"Confirmed that you have choosen the following book : "<<booktitle<<endl;
    return 0;
}
