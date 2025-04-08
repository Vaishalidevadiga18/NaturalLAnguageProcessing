
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_WORDS 200
#define MAX_WORD_LEN 50

typedef struct {
    char first[MAX_WORD_LEN];
    char second[MAX_WORD_LEN];
    int count;
} Bigram;

void tokenize(char *text, char words[MAX_WORDS][MAX_WORD_LEN], int *word_count) {
    char *token = strtok(text, " ");
    *word_count = 0;
   
    while (token != NULL && *word_count < MAX_WORDS) {
        strcpy(words[*word_count], token);
        (*word_count)++;
        token = strtok(NULL, " ");
    }
}

int find_bigram(Bigram bigrams[], int bigram_count, char *first, char *second) {
    for (int i = 0; i < bigram_count; i++) {
        if (strcmp(bigrams[i].first, first) == 0 && strcmp(bigrams[i].second, second) == 0) {
            return i;
        }
    }
    return -1;
}

int find_unigram_count(char words[MAX_WORDS][MAX_WORD_LEN], int word_count, char *target) {
    int count = 0;
    for (int i = 0; i < word_count; i++) {
        if (strcmp(words[i], target) == 0) {
            count++;
        }
    }
    return count;
}

void calculate_bigrams(char words[MAX_WORDS][MAX_WORD_LEN], int word_count, Bigram bigrams[], int *bigram_count) {
    *bigram_count = 0;
    for (int i = 0; i < word_count - 1; i++) {
        int index = find_bigram(bigrams, *bigram_count, words[i], words[i + 1]);
        if (index != -1) {
            bigrams[index].count++;
        } else {
            strcpy(bigrams[*bigram_count].first, words[i]);
            strcpy(bigrams[*bigram_count].second, words[i + 1]);
            bigrams[*bigram_count].count = 1;
            (*bigram_count)++;
        }
    }
}

double apply_laplace_smoothing(Bigram bigrams[], int bigram_count, char words[MAX_WORDS][MAX_WORD_LEN], int word_count, char *first, char *second) {
    int vocabulary_size = word_count; // Approximating V as the number of unique words
    int unigram_count = find_unigram_count(words, word_count, first);
   
    int bigram_index = find_bigram(bigrams, bigram_count, first, second);
    int bigram_count_value = (bigram_index != -1) ? bigrams[bigram_index].count : 0;

    double probability = (bigram_count_value + 1) / (double)(unigram_count + vocabulary_size);
    return probability;
}

double calculate_sentence_probability(char test_sentence[], Bigram bigrams[], int bigram_count, char words[MAX_WORDS][MAX_WORD_LEN], int word_count) {
    char test_words[MAX_WORDS][MAX_WORD_LEN];
    int test_word_count = 0;
    tokenize(test_sentence, test_words, &test_word_count);

    double sentence_probability = 1.0;
    for (int i = 0; i < test_word_count - 1; i++) {
        double prob = apply_laplace_smoothing(bigrams, bigram_count, words, word_count, test_words[i], test_words[i + 1]);
        sentence_probability *= prob;
    }
    return sentence_probability;
}

int main() {
    // Four corpus sentences
    char corpus1[] = "I am from vellore";
    char corpus2[] = "I am a teacher";
    char corpus3[] = "students are good and are from various cities";
    char corpus4[] = "students from vellore do engineering"; // ✅ Fixed (semicolon added)

    char corpus[MAX_WORDS * MAX_WORD_LEN] = ""; // Merging corpus sentences
    snprintf(corpus, sizeof(corpus), "%s %s %s %s", corpus1, corpus2, corpus3, corpus4);

    char words[MAX_WORDS][MAX_WORD_LEN];
    int word_count = 0;

    tokenize(corpus, words, &word_count);

    Bigram bigrams[MAX_WORDS];
    int bigram_count = 0;
    calculate_bigrams(words, word_count, bigrams, &bigram_count);

    printf("Bigram Counts:\n");
    for (int i = 0; i < bigram_count; i++) {
        printf("(%s, %s): %d\n", bigrams[i].first, bigrams[i].second, bigrams[i].count);
    }

    // Test sentence
    char test_sentence[] = "students are from vellore";

    double sentence_prob = calculate_sentence_probability(test_sentence, bigrams, bigram_count, words, word_count);
    printf("\nProbability of test sentence  after Laplace Smoothing: %.10f\n",sentence_prob);

    return 0;
}
