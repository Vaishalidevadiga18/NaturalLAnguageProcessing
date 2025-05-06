#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#define MAX 50
char words[1000][20];
int wordcount=0;
void toLowerStr(char *s){
    while(*s){
        *s=tolower(*s);
        s++;

    }
}
void tokenize(char *s){
    char *tok=strtok(s," .\n");
    while(tok){
        toLowerStr(tok);
        strcpy(words[wordcount++],tok);
        tok=strtok(NULL," .\n");

    }
}
int getUnigram(char *w){
    int count=0;
    for(int i=0;i<wordcount;i++)
    {
        if(strcmp(words[i],w)==0)
        count++;
    return count;

    }
}
int getBigram(char *w1,char *w2){
    int count=0;
    for(int i=0;i<wordcount-1;i++)
    {
        if(strcmp(words[i],w1)==0 &&strcmp(words[i+1],w2)==0)
        count++;
    return count;
    
    }
}
int main()
{
    int n;
    int line[MAX],input[MAX];
    printf("enter no");
    scanf("%d",&n);
    getchar();
    printf("Enter ech sentenc");
    for(int i=0;i<n;i++)
    {
        fgets(line,MAX,stdin);
        tokenize(line);

    }
    printf("Enter text senetence");
    fgets(input,MAX,stdin);
    toLowerStr(input);
    char * tokens[100];
    int tcount=0;
    tokens=strtok(input,"  .\n");
    while(tok){
        tokens[tcount++,tok]=tok;
        tok=strtok(NULL," .\n");
        double prob=1.0;
        for(int i=0;i<tcount-1;t++)
        {
        int uni=getUnigram(tokens[i]);
        int bi=getBigram(tokens[i],tokens[i+1]);
        printf("P(%s|%s)=count(%s,%s)/count(%s)=%d",tokens[i+1],tokens[i],tokens[i],tokens[i+1],tokens[i],bi/uni);
        if(uni==0||bi==0)
        prob=0.0;
    break;


    }
    total_prob*=prob;
    printf("Total probability=%.4f",total_prob);
}