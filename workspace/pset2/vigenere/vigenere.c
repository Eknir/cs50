#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // a user can only give one keyword
    int MAXNUMBEROFPASSWORDS = 2;

    string k = argv[1];
    // error message if more than 1 keyword is passed in command line
    if(argc != MAXNUMBEROFPASSWORDS)
    {
         printf("Please don't give a password in command line\n");
         return 1;
    }

    //error message if non-alphabetical characters are passed in command line
    for(int i = 0, n = strlen(k); i < n; i++)
    {
        if((k[i] >= 0 && k[i] <=64 )|| (k[i] >=91 && k[i] <= 96 )|| (k[i]>= 123))
        {

          printf("Please only give alphabetical characters\n");
         return 1;
        }

    }

    // prompt user for plaintext
    printf("plaintext: ");
    string s = get_string();
    printf("ciphertext: ");

    int counter = 0;
    for(int i=0, n = strlen(s); i < n; i++)
    {
        int unencrypted = s[i];
        int encrypted;
        int key;

        // makes alphabetical list if UPPERCASE
        if(unencrypted <= 90 && unencrypted >=65)
        {
            unencrypted = unencrypted - 65;

            // converts password char to key if key is UPPERCASE
            if(k[counter%strlen(k)] <= 90 && k[counter%strlen(k)] >=65)
                {
                    key = k[counter%strlen(k)] - 65;
                    encrypted = (unencrypted + key) % 26 + 65;
                    printf("%c", encrypted);
                    counter++;
                }
            // converts password char to key if key is lowercase
            else
                {
                    key = k[counter%strlen(k)] - 97;
                    encrypted = (unencrypted + key) % 26 + 65;
                    printf("%c", encrypted);
                    counter++;
                }

        }
        // makes alphabetical list if lowercase
        else if(unencrypted <= 122 && unencrypted >=97)
        {
            unencrypted = unencrypted -97;

            // converts password char to key if key is UPPERCASE
            if(k[counter%strlen(k)] <= 90 && k[counter%strlen(k)] >=65 )
                {
                    key = k[counter%strlen(k)] - 65;
                    encrypted = (unencrypted + key) % 26 + 97;
                    printf("%c", encrypted);
                    counter++;
                }
            // converts password char to key if key is lowercase
            else
                {
                    key = k[counter%strlen(k)] - 97;
                    encrypted = (unencrypted + key) % 26 + 97;
                    printf("%c", encrypted);
                    counter++;
                }
        }

        else
            {
                printf("%c", unencrypted);

            }

        }
        printf("\n");

}

