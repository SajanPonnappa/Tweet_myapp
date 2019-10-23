#include<stdio.h>
#include<string.h>

void main()
{
	char s[]="the quick brown fox jumps over the lazy dog";
	int used[26]={0};
	int i;
	for(i=0;i<=strlen(s);i++)
	{
		if(s[i]>='a' && s[i]<='z')
		used[s[i]-'a']= 1;
	}
	for(i=0;i<26;i++)
	{
		if(used[i]==0)
		printf("%c",(char)(i+'a'));
	}
}
	
