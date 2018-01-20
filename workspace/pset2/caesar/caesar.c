#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if(argc != 2)
    {
        printf("Please don't give more than 1 input\n");
        return 1;
    }

    string k = argv[1];
    int key = atoi(k);

    printf("plaintext: ");
    string s = get_string();
    printf("ciphertext: ");
    //printf("%s", s);

    for(int i=0, n = strlen(s); i < n; i++)
    {
        int unencrypted = s[i];
        int encrypted;

        // makes alphabetical list if UPPERCASE
        if(unencrypted <= 90 && unencrypted >=65)
        {
            unencrypted = unencrypted - 65;

            // apply key
            encrypted = (unencrypted + key) % 26 + 65;

        }
         // makes alphabetical list if lowercase
        else if(unencrypted <= 122 && unencrypted >=97)
        {
            unencrypted = unencrypted - 97;

            //apply key
            encrypted = (unencrypted + key) % 26 + 97;
        }
        //error if neither lowercase or uppercase
        else
        {
            encrypted = unencrypted;
        }
        printf("%c", encrypted);

    }
    printf("\n");


}