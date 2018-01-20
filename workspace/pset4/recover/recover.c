/**
 * Copies a BMP piece by piece, just because.
 */

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover card.raw \n");
        return 1;
    }

    char *infile = argv[1];

    // open input file
    FILE* input = fopen(infile, "r");
    if (input == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }

    // create buffer
    unsigned char buffer[512];

    // filename counter
    int count = 0;

    FILE* picture = NULL;

    // check if we found jpg before
    int found = 0;

    // continue untill last picture
    while (fread(buffer, 512, 1, input) == 1)
    {
        // rcheck for signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            if (found == 1)
            {
                // close previous picture
                fclose(picture);
            }
            else
            {
                // first jpg discovered
                found = 1;
            }

            char filename[8];
            sprintf(filename, "%03d.jpg", count);
            picture = fopen(filename, "a");
            count++;

        }

       if (found == 1)
        {
            // write once we start finding jpg
            fwrite(&buffer, 512, 1, picture);
        }

    }

    // close files
    fclose(input);
    fclose(picture);

    return 0;
}






