#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./copy infile outfile\n");
        return 1;
    }

    //resizing factor
    int n = atoi(argv[1]);
    if(n > 100)
    {
        fprintf(stderr, "number too large.\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 1;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 1;
    }


    BITMAPINFOHEADER binew;
    BITMAPFILEHEADER bfnew;
    binew =bi;
    bfnew = bf;
    binew.biWidth = bi.biWidth * n;
    binew.biHeight = bi.biHeight * n;
    binew.biSizeImage = bi.biSizeImage * n;
    bfnew.bfSize = binew.biSizeImage  + 54;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfnew, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&binew, sizeof(BITMAPINFOHEADER), 1, outptr);

    // determine padding for scanlines
    int padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int newpadding =  (4 - (binew.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    char array[binew.biWidth + newpadding];

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            // write RGB triple n times to array
            for(int x = 0; x < n; x++)
            {
                array[j+x] = triple;
                //fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
        }
        //write padding
        if(newpadding != 0)
        {
            for(int y = 1; y <= newpadding; y++)
            {
                array[j+x+y] = 0x00;

            }
                fwrite(&array, sizeof(array), n, outptr);
        }

        {
        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
        }
    }
    }


    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

