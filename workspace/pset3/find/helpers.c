/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // to make sure that user inputs at least one number in the array
    if(n <= 0)
    {
    return false;
    }
    else
    {
        // initialize i to be middle of array values
        int mid = n/2;

        // stop searching if value is found
        while(values[mid] != value)
        {
            // stop searching and return false if value is not found
            if(mid == 0 || mid == n-1)
            {
                return false;
            }
            // increment i if value we are looking for > value[i]
            if(values[(n -mid)] > value)
            {
                mid = mid - (n-mid)/2;
            }
            // decrement i if value we are looking for < value[i]
            else
            {
                mid = mid + (n-mid)/2;
            }
        }
        //return true if value is found
        return true;
    }

}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    for(int j = 0; j < n-1; j++)
    {

        for(int i = 0; i < n-1; i++)
        {
        if(values[i] > values[i+1])
        {
            int v = values[i+1];
            values[i+1] = values[i];
            values[i] = v;
        }
    }

}
    return;
}
