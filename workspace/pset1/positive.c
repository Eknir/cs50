#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        printf("please give me a positive int: ");
        n = GetInt();
    }
    while (n<1);
    printf("Thanks for the positve int!\n");
}