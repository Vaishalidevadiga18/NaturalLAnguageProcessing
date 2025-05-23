#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX 500
#define MAX_LEN 50

char words[MAX][MAX_LEN];
int wordCount = 0;
int freq[MAX][MAX] = {0};
int count[MAX] = {0};

// Function to find index of a word, or add it if not present (during training)
int find(const char* word) {
    for (int i = 0; i < wordCount; i++) {
        if (strcmp(words[i], word) == 0)
            return i;
    }
    if (wordCount >= MAX) {
        printf("Error: Exceeded maximum word limit.\n");
        exit(1);
    }
    strcpy(words[wordCount], word);
    wordCount++;
    return wordCount - 1;
}

// Function to only get index of a word (during testing)
int getIndex(const char* word) {
    for (int i = 0; i < wordCount; i++) {
        if (strcmp(words[i], word) == 0)
            return i;
    }
    return -1; // Not found
}

// Function to compute word transition frequencies from corpus
void computation(const char* set[], int n) {
    for (int s = 0; s < n; s++) {
        char copy[500];
        strcpy(copy, set[s]);

        char* token = strtok(copy, " ");
        int prev = find("<s>");
        count[prev]++;

        while (token != NULL) {
            int curr = find(token);
            count[curr]++;
            freq[prev][curr]++;
            prev = curr;
            token = strtok(NULL, " ");
        }

        int endix = find("</s>");
        freq[prev][endix]++;
        count[endix]++;
    }
}

// Function to calculate transition probability from one word to another
double prob(int prev, int curr) {
    if (count[prev] == 0) return 0.0;
    if (strcmp(words[curr], "</s>") == 0 && freq[prev][curr] > 0) {
        return 1.0;
    }
    return (double)freq[prev][curr] / count[prev];
}

// Main function
int main() {
    const char* corpus[] = {
        "there is a big garden",
        "children play in the garden",
        "they play inside beautiful garden"
    };

    computation(corpus, 3);

    const char* test[] = { "<s>", "they", "play", "in", "a", "big", "garden", "</s>" };
    int len = 8;

    double total = 1.0;
    for (int i = 1; i < len; i++) {
        int p = getIndex(test[i - 1]);
        int c = getIndex(test[i]);

        if (p == -1 || c == -1) {
            printf("Word not found in training data: %s or %s\n", test[i - 1], test[i]);
            total = 0.0;
            break;
        }

        double prob_val = prob(p, c);

        if (prob_val == 0.0) {
            printf("No transition found from %s to %s\n", test[i - 1], test[i]);
            total = 0.0;
            break;
        }

        total *= prob_val;
        printf("P(%s | %s) = %.4f\n", test[i], test[i - 1], prob_val);
    }

    printf("Total Probability: %.4f\n", total);
    return 0;
}
