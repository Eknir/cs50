/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

// First prime after 1.3* dictionary entries
#define M 186037

// implement a hashtable
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

int dictionarySize = 0;

// create an array of nodes with size M
node *hashtable[M];

// hash function https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/
int hash(const char* word)
    {
    unsigned int hash = 0;
    for (int i=0, n=strlen(word); i<n; i++)
        hash = (hash << 2) ^ word[i];
    return hash % M;
    }

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
        unload();
        fclose(fp);
        return false;
    }
    //array to store the word
    char word[LENGTH +1];

    while(fscanf(fp, "%s", word) != EOF)
    {
    int i = 0;
    while(word[i])
    {
        word[i] = tolower(word[i]);
        i++;
    }
        node *new_node = malloc(sizeof(node));
        if(new_node == NULL)
        {
            unload();
            fclose(fp);
            return false;
        }
        else
        {
            strcpy(new_node->word, word);
            new_node->next = hashtable[hash(word)];
            hashtable[hash(word)] = new_node;
            dictionarySize++;
        }
    }
    fclose(fp);
    return true;
}

/**
 * Returns true if word is in dictionary else false.
 */


bool check(const char *word)
{
    char temp[LENGTH];
    strcpy(temp, word);

    // make the word to lowercase (to have the correct value in the hash function)
    int i = 0;
    while(temp[i])
    {
    temp[i] = tolower(temp[i]);
    i++;
    }


    // put cursor to the head of the list
    node *cursor = hashtable[hash(temp)];

   // strcpy(new_node->word, cursor->word);
    // iterate
    while(cursor != NULL)
    {
        if(strcasecmp(cursor ->word,temp) == 0)
        {
            // word is in the list
            return true;
        }
        cursor = cursor -> next;
    }
    // word not in the list
    return false;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if(dictionarySize >0)
    {
        return dictionarySize;
    }
    else
    {
        return 0;
    }

}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for(int i = 0; i < M; i++)
    {
        node *cursor = hashtable[i];
            while(cursor != NULL)
            {
                node* temp = cursor;
                cursor = cursor -> next;
                free(temp);
            }
        }
    return true;
    return false;
}

