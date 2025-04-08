
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_WORDS 100
#define MAX_BIGRAMS 100

typedef struct {
    char word1[20];
    char word2[20];
    int count;
} Bigram;

int main() {
    // Corpus of sentences
    char *corpus[] = {
        "There is a big garden",
        "Children play in the garden",
        "They play inside  beautiful garden"
    };
    int corpus_size = sizeof(corpus) / sizeof(corpus[0]);

    // Array to store bigrams
    Bigram bigrams[MAX_BIGRAMS];
    int bigram_count = 0;

    // Count bigrams in the corpus
    for (int i = 0; i < corpus_size; i++) {
        char sentence[100];
        strcpy(sentence, corpus[i]); // Copy to a modifiable string
        char *token = strtok(sentence, " ."); // Tokenize by space and period
        char *prev_token = NULL;

        while (token != NULL) {
            if (prev_token != NULL) {
                // Check if the bigram already exists
                int found = 0;
                for (int j = 0; j < bigram_count; j++) {
                    if (strcmp(bigrams[j].word1, prev_token) == 0 && strcmp(bigrams[j].word2, token) == 0) {
                        bigrams[j].count++;
                        found = 1;
                        break;
                    }
                }
                // If not found, add new bigram
                if (!found) {
                    strcpy(bigrams[bigram_count].word1, prev_token);
                    strcpy(bigrams[bigram_count].word2, token);
                    bigrams[bigram_count].count = 1;
                    bigram_count++;
                }
            }
            prev_token = token;
            token = strtok(NULL, " .");
        }
    }

    // Calculate the probability of the sentence "They play in a big garden"
    char target_sentence[] = "They play in a big garden";  // Copy to avoid modifying the original
    char *target_token = strtok(target_sentence, " ");
    char *prev_target_token = NULL;
    double probability = 1.0;

    while (target_token != NULL) {
        if (prev_target_token != NULL) {
            // Find the count of the bigram
            int bigram_found = 0;
            int bigram_count_value = 0;
            for (int i = 0; i < bigram_count; i++) {
                if (strcmp(bigrams[i].word1, prev_target_token) == 0 && strcmp(bigrams[i].word2, target_token) == 0) {
                    bigram_found = 1;
                    bigram_count_value = bigrams[i].count;
                    break;
                }
            }

            // Find the count of the first word in the bigram
            int first_word_count = 0;
            for (int i = 0; i < bigram_count; i++) {
                if (strcmp(bigrams[i].word1, prev_target_token) == 0) {
                    first_word_count += bigrams[i].count;
                }
            }

            // Calculate the probability for the bigram
            if (first_word_count > 0) {
                probability *= (double)bigram_count_value / first_word_count;
            } else {
                probability *= 0; // If the first word count is zero, probability is zero
            }
        }
        prev_target_token = target_token;
        target_token = strtok(NULL, " ");
    }

    // Output the probability
    printf("Probability of the sentence 'They play in a big garden': %f\n", probability);

    return 0;
}
 