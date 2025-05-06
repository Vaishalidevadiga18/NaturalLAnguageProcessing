#include<stdio.h>
#include<string.h>
#include<ctype.h>
#define MAX 50
char words[100][20];
int wordcount=0;
void toLowerStr(char *s){
    while(*s){
        *s=tolower(*s);
        s++;

    }
}
void Tokenize(char *s){
    char *tok=strtok(s, " .\n");
    while(tok){
        toLowerStr(tok);
        strcpy(words[wordcount++],tok);
        tok=strtok(NULL, " .\n");

    }
}
int getUnigram(char w){
    int count=0;
    for(int i=0;i<wordcount;i++){
        if(strcmp(words[i],w)==0)
        count++:
    return count;

    }
}
int getBigram(char w1,char w2){
    int count=0;
    for(int i=0;i<wordcount-1;i++){
        if(strcmp(words[i],w1)==0 && strcmp(words[i+1],w2)==0)
        count++:
    return count;
    
    }
}

int getvocabsize(){
    int vocab=0.0;
    char seen[2000][20];

    for(int i=0;i<wordcount;i++){
        int found=0;
        for(int j=0;i<vocab;j++){
            if(strcmp(seen[j],vocab[i])==0){
            found=1;
            break;
            }

        }
        if(!found){
            strcpy(seen[vocab++],words[i]);

        }
    }
    return vocab;

}
int main()
{
    int n;
    char line[MAX],input[MAX];
    printf("Enter no");
    scanf("%d",&n);
    getchar();
    printf("Enter each sentence");
    fgets(line,MAX,stdin);
    tokenize(line);
    printf("Enter test");
    fgets(input,MAX,stdin);
    toLowerStr(input);
    char *tokens[100];
    int tcount=0;
    char *tok=strtok(input, " .\n");
    while(tok){
        tok[wordcount++]=tok;
        tok=strtok(NULL, " .\n");

    }
    int v=getvocabsize();
    double prob=0.0;
    for(int i=0;i<tcount-1;i++){
        int uni=getUnigram(tokens[i]);
        int bi=getBigram(token[i],[i+1]);
        double smoothed=(double) bi+1/uni+v;
        printf("P(%s|%s)=count(%s,%s)+1/count(%s)+%d=%d+1/%d+v=%.4f\n",tokens[i+1],tokens[i],tokens[i],tokens[i+1],tokens[i],bi ,uni,v,smoothed);  
    }
}