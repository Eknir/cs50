/**
 * water.c
 * 
 * Rinke Hendriksen
 * Rinkehendriksen@gmail.com
 * 
 * gives the minimal amount of coins needed for change
 */
#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // asks for an amount to change
    float amount_float;
    do
        {
            printf("O hai! How much change is owed?\n");
            amount_float = GetFloat();
        }
    
    while(amount_float < 0);
    
    //converts amount to a rounded integer
    float amount = (amount_float * 100);
    int amount_round = round (amount);
    
    // counting starts here
    int quarter = 0;
    int dime = 0;
    int nickel = 0;
    int pennie = 0;
    
    //counts amounts of quarters
    for(int q = 0; q < amount_round / 25; q ++)
        {
            quarter = quarter +1;
        }
    //residual 
    int amount_round_1 = amount_round - (quarter * 25);
    
    //counts amount of dimes
    for(int d = 0; d < amount_round_1 / 10; d ++)
        {
            dime = dime +1;
        }
    // residual   
    int amount_round_2 = amount_round_1 - (dime * 10);
    
    //counts amount of nickels
    for(int n = 0; n < amount_round_2 / 5; n ++)
        {
            nickel = nickel +1;
        }
    // residual s   
    int amount_round_3 = amount_round_2 - (nickel * 5);
    
     //counts amount of pennies
    for(int p = 0; p < amount_round_3 / 1; p ++)
        {
            pennie = pennie +1;
        }
   
    // counts total coins used
    int total_coins = quarter + dime + nickel + pennie;
    
    // prints total coins used
    printf("%d\n", total_coins);

}