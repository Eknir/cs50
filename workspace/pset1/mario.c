/**
 * water.c
 * 
 * Rinke Hendriksen
 * Rinkehendriksen@gmail.com
 * 
 * creates half a piramid, height specified by user by printing hashes and spaces
 */
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

//asks user for the desired height between 1 and 23
    do
        {
            printf("Height: ");
            height = GetInt();
        }
    
    while(height < 0 || height > 23);
    
// specifies the row number on which the hashes and spaces are printed
        
        for(int row = 0; row < height; row++)   
            {
            
//prints the desired amount of spaces  
            for(int spaces = height - row - 2; spaces >= 0; spaces --)
                {
                    printf(" ");
                }
            
//prints the desired amount of hashes followed by a new line
            for(int hashes = 0; hashes <= row + 1; hashes ++)
                {
                    printf("#");
                }
                printf("\n");
            }
return 0;
}
