
#include <iostream>
#include <vector>
#include <string>
#include <iostream>
#include <stdio.h>
#include <fstream>
using namespace std;

string word;

struct node{
    node *left = NULL;
    node *right = NULL;
    int flag = 0;
    string content;
    string code;
    double frequency;

};
vector<node*> codes;
vector<node*> Arraynode;

void makeNodeArray(){
    node* dummy;
        while(word.length()!= 0){
        if(word.length()!= 0){
            dummy = new node;
            char a = word[0];
            dummy->frequency = 0;
            dummy->content = a;
            int i = 0;
            while(i < word.length()){
                if(word[i] == a){
                    word.erase(i, 1);
                    dummy->frequency= dummy->frequency + 1;
                } else{
                    i++;
                }
        }
         Arraynode.push_back(dummy);
    }
    }
};

node* extractMin()
{

double temp = Arraynode[0]->frequency;

unsigned int pos = 0;
node* tempNode = Arraynode[0];
if(Arraynode.size()==1){

}else{
 for(int i = 1; i < Arraynode.size(); i++)
 {

  if(temp > Arraynode[i]->frequency)
  {
     pos = i;
     temp = Arraynode[i]->frequency;
  }
 }
 tempNode = Arraynode[pos];
}

 Arraynode.erase(Arraynode.begin()+pos, Arraynode.begin()+pos+1);
 return tempNode;

};



vector<node*> makeHuffmanTreeNodes()
{
    node* insideNode;
    node* right;
    node* left;
    while(Arraynode.size() > 1){
        insideNode = new node;
        right = new node;
        left = new node;
        left = extractMin();
        insideNode -> left = left;
        if(!Arraynode.empty()){
        right = extractMin();
        insideNode -> right = right;
        insideNode->frequency = right->frequency + left->frequency;
        }else{
        insideNode-> frequency = left->frequency;
        }
        Arraynode.push_back(insideNode);
        }


};

void ultimatecoder(node* changed, string s){

    if(changed->right!=NULL){
    changed->right->code = s + "1";
    ultimatecoder(changed->right, s+ "1");
    }
    if(changed->left!=NULL){
        changed->left->code = s + "0";
        ultimatecoder(changed->left, s + "0");
    }
    if(changed->right == NULL && changed->left == NULL){
        codes.push_back(changed);
    }
};

void huffman_tree(string sentence){

    string english = sentence;
    ultimatecoder(Arraynode[0], "");
    string HMcode = "";
    ofstream encodetxt, codetxt;
    codetxt.open("code.txt");
    encodetxt.open("encodemsg.txt");

for(int i = 0; i < sentence.length(); i++){
    string firstletter(1, sentence[i]);
    for(int j = 0; j < codes.size(); j++){
        if(firstletter == codes[j]->content){
            HMcode+= codes[j]->code;
            break;
        }
    }
}
double average = 0;
for(int j = 0; j <codes.size(); j++){

    codetxt << codes[j]->content << " code is " <<codes[j]->code <<endl;
    average= average + codes[j]->code.length();
}
average= average/ codes.size();

codetxt << "average bits per symbols is: " << average;

codetxt.close();
encodetxt << HMcode;
encodetxt.close();
};





int main(int argc, char *argv[]){
string sentence;
fstream inFile;
inFile.open(argv[1]);

getline(inFile, sentence);
word = sentence;
while(!inFile.eof()){
    getline(inFile, sentence);
    word += sentence;
}

makeNodeArray();
makeHuffmanTreeNodes();
huffman_tree(sentence);

return 0;
}
