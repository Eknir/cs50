#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    // asks the user for a name and stores name in s
    string s = get_string();

    // to be sure that user put's in a name
    while(s == NULL)
    {
        s = get_string();

    }
   // Runs over i'th character of s
    for(int i = 0, n = strlen(s); i < n; i++)
    {
        // if i equals space
        if(s[i] == ' ' || i == 0 )
        {
            // counts number of spaces
            while(s[i] == ' ')
            {
                i++;
            }

            if(s[i] != '\0')
            {
            char c = toupper(s[i]);
            // print the first letter after space
            printf("%c", c);
            }
        }
    }
    printf("\n");

}

