/**
 * water.c
 * 
 * Rinke Hendriksen
 * Rinkehendriksen@gmail.com
 * 
 * Prompts an equivalent amount of bottles of water,
 * conditionally on the amount of minutes spent in the shower
 */
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // asks the user how long his shower was this morning
    printf("For how long did you have a shower this morning?\n");
    int (min_shower) = GetInt();
    
    //converts minutes to bottles
    int (bottles) = min_shower * 12;
    
    // displays equivalent amount of bottles
    printf(" This was about %d bottles of water\n", bottles);
}