# -*- coding: utf-8 -*-

# import Levenshtein

# from collections import defaultdict

def levenshtein_distance(costs, startword, endword):
    """

    Transform source word to target word using levenshtein distance w/ following rules

    Every interim step between the first and the last word must also be a word
    No interim step can be less than three letters
    The first line of input will contain the “cost” of each operation in order: insertion, deletion, substitution, and anagram
    The second line of input will contain the starting word
    The third line of input will contain the ending word

    1 3 1 5
    HEALTH
    HANDS
    (output: 7) (HEALTH - HEATH - HEATS - HENTS - HENDS - HANDS)
    (If your dictionary doesn’t have a couple of these words in there, don’t worry -- you’re scored on your code, not your word list.)

    1 9 1 3
    TEAM
    MATE
    (output: 3) (TEAM - MATE)
    
    7 1 5 2
    OPHTHALMOLOGY
    GLASSES
    (output: -1)

    """

    # get dictionary for anagrams 
    # word_anagrams = parse_dictionary('/usr/share/dict/words')

    if len(startword) < 3 or len(endword) < 3:
        raise Exception("The minimum number of letters for all interim steps must be at least three.")

    rows = len(startword)+1
    cols = len(endword)+1
    inserts, deletes, subs, ana =  costs.split(' ')

    # initialize matrix
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings by deletions:
    for i in range(1, rows):
        dist[i][0] = i * int(deletes)
    # target prefixes can be created from an empty source string by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i * int(inserts)
        
    for col in range(1, cols):
        for row in range(1, rows):

            # USE THIS FOR TRANSPORTATION COST CALC!!
            # doesPreviousMatch = (a[iA - 1] == b[iB - 1]

            possible_costs = []
            possible_costs.append(dist[row][col-1] + int(inserts))
            possible_costs.append(dist[row-1][col] + int(deletes))
            if startword[row-1] == endword[col-1]:
                possible_costs.append(dist[row-1][col-1])
            else:
                possible_costs.append(dist[row-1][col-1] + int(subs))
            # if new_word not in word_anagrams:
            #     ana = 0
            # else:
            #     ana = int(ana)
            

            # if startword[]

            # TRANSPORTATION (ANAGRAM) COST!!!! Convert to python
            val bCharIndexInA = mapCharAToIndex.getOrDefault(b[iB - 1], 0)
            if (bCharIndexInA != 0 && prevMatchingBIndex != 0) {
                possibleCosts.append(dist[bCharIndexInA - 1][prevMatchingBIndex - 1]
                        + (iA - bCharIndexInA - 1) + 1 + (iB - prevMatchingBIndex - 1))
            }

            dist[row][col] = min(possible_costs)
            # dist[row][col] = min(dist[row][col-1] + int(inserts), # insertion
            #                      dist[row-1][col] + int(deletes),  # deletion
            #                      dist[row-1][col-1] + sub_cost) # substitution
            #                      # dist[col-2][row-2] + ana) #anagram       
    # # read matrix
    # for r in range(rows):
    #     print(dist[r])
    
 
    return dist[row][col]

# should return -1 
# print levenshtein_distance(('7 1 5 2'), "opthamology", "glasses")
# should return 7
print levenshtein_distance(('1 3 1 5'), "health", "hands")
# should return 3
print levenshtein_distance(('1 9 1 3'), "team", "mate")
# should return invalid input
# print levenshtein_distance(('7 1 5 2'), 'so', 'os')
# should return 5
print levenshtein_distance(('1 1 2 1'), "kitten", "sitting")
# should return 8
print levenshtein_distance(('1 1 2 1'), "intention", "execution")


# def parse_dictionary(filename):
#     """

#     Parse dictionary 
    
#     """

#     word_anagrams = defaultdict(set)
#     with open(filename) as dictionary:
#         for word in dictionary:
#             word = word.rstrip()
#             word_anagrams[''.join(sorted(word))].add(word)

#     return word_anagrams

# if __name__ == "__main__":
#    main()


