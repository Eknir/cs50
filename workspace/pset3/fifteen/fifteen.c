/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */

#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <math.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();
    //draw();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();

        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }
        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(50);
        }

        // sleep thread for animation's sake
        usleep(500);
    }

    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(200);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).
 */
void init(void)
{
    // initialize counter, starting at d^2 -1
    int counter = d*d-1;
    for(int i = 0; i<d; i++)
    {
       for(int j = 0; j<d; j++)
       {
           // assign value to array
           board[i][j] = counter;
           counter--;
        }
    }
    // check number of tiles and replace last two tiles if d is even
    if(d%2 == 0)
    {
        int replace = board[d-1][d-3];
        board[d-1][d-3] = board[d-1][d-2];
        board[d-1][d-2] = replace;
    }
}

/**
 * Prints the board in its current state.
 */
void draw(void)
{
   for(int i=0; i<d; i++)
   {
       for(int j=0; j<d; j++)
       {
           if(j == 0)
           {
               // print top row
               if(i == 0)
               {
                  printf(" ------------------");
                  // extra spaces for top row
                  if(d >3)
                  {
                    printf("------");
                  }
                  printf("\n");
               }
            // right side of the board
            printf("|");
           }
           // print underscore if 0
           if(board[i][j] == 0)
           {
               printf("   _  ");
           }
           // right side of the board
           else
           {
           // print values
           printf("  %2d  ", board[i][j]);
           }

           // print right side of the board
           if(j == d-1)
           {
               // edge + new line
               printf("| \n");

               // edge + last row
               if(i == d-1)
               {
                printf(" ------------------");

                    // longer last row
                    if(d >3)
                    {
                        printf("------");
                    }
                printf("\n\n");
                }
            }
        }
   }
}


/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false.
 */
bool move(int tile)
{
int tx;
int ty;
int zx;
int zy;
    // find the location of tile

    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        {
            if(board[i][j] == tile)
            {
            tx = j;
            ty = i;
            }
        }
    }
    // find the location of 0
    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        {
            if(board[i][j] == 0)
            {
            zx = j;
            zy = i;
            }
        }
    }

    // check for false moves
    if(ty == zy)
    {
        if(tx != zx +1 && tx != zx -1)
        {
            // y the same, but not next to 0
            return false;
        }
    }
    else if (ty == zy + 2 || ty == zy -2)
    {
        // too far away
        return false;
    }
    else if(tx != zx)
    {
        // not directly above or below
        return false;
    }


    board[zy][zx] = tile;
    board[ty][tx] = 0;
    return true;
}


/**
 * Returns true if game is won (i.e., board is in winning configuration),
 * else false.
 */
bool won(void)
{
    int counter = 1;

    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            if (board[i][j] == counter)
                counter++;
        }
    }

    if (counter == d*d && board[d-1][d-1] == 0)
        return true;
    else
        return false;
}