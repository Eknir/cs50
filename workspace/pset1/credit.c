/**
 * credit.c
 *
 * Rinke Hendriksen
 * Rinkehendriksen@gmail.com
 *
 * Promts the user for a credit card number and answers what type of credit card it is, if valid
 */

#include <cs50.h>
#include <stdio.h>

int main(void){

    long cc_number;
    long number = 0;
    bool even = false;
    int checksum = 0;
    int checksum1=0;
    int checksumfinal;
    int remainder;
    int counter = 0;

    // asks user for a positve number
    printf("Number:");
    cc_number = get_long_long();

    while(cc_number <= 0){
    printf("Retry: ");
    cc_number = get_long_long();
    }

    // adds all even numbers (from right) and multiplies by 2
    number=cc_number;
    while(number != 0)
    {
        counter ++;
    if(even==false){
        remainder = number%10;
        number = number/10;
        even = true;
        checksum = checksum + remainder;


    }
    else
    {
        remainder = number%10*2;
        number = number/10;

        even = false;

        if(remainder == 10)
        {
        checksum1 = checksum1 + 1;

        }

        else
        {
        if (remainder / 10 ==0)
        {
            checksum1 = checksum1 + remainder;

        }
        else
        {
                checksum1 = checksum1+ remainder%10;
                checksum1 = checksum1 + remainder/10;

        }


            }
    }
        }

    checksumfinal = checksum + checksum1;

  if(checksumfinal %10 == 0){
    if(counter ==15){
        if(cc_number / 10000000000000 == 34 || cc_number/10000000000000==37){
        printf("AMEX\n");
        }}
    else if(counter == 16){
        if(cc_number/100000000000000 == 51 || cc_number/100000000000000 == 52 || cc_number/100000000000000 == 53 || cc_number/100000000000000 == 54 || cc_number/100000000000000 ==55)
        {
        printf("MASTERCARD\n");
        }
        if(cc_number/ 1000000000000000 == 4)
        printf("VISA\n");
    }

    else if (counter == 13){
        if(cc_number /1000000000000 == 4){
        printf("VISA");
        }}
}
else{
    printf("INVALID\n");
}

}