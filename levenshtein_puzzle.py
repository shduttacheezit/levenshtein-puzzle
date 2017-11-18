# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple
from heapq import heappush, heappop
from itertools import product
from collections import deque
import string
import os


def lowest_cost_word_change(costs, startword, endword):
    """
    Transform source word to target word in path where every interim step is a word 
    and cannot be less than 3 letters. 
    Return lowest cost using given cost for each operation in order:
    insertion, deletion, substitution, and anagram

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
    # split the cost input 
    inserts, deletes, subs, ana =  costs[0], costs[1], costs[2], costs[3]

    # HANDLE EXCEPTION ERROR FOR LENGTH
    # if len(startword) or len(endword) == 3:
    #     Ra
    
    # first check start and end words are anagrams 
    if isAnagram(startword, endword) == True:
        print ana, [startword, endword]
    else:
        words = get_words('/usr/share/dict/words', startword, endword)
        print traverse(words, startword, endword, inserts, deletes, subs)

    # for vertex, path in traverse():  
        # if vertex == endword:
        #     print ' -> '.join(path)

def isAnagram(word1, word2):

    word1 = word1.lower()
    word2 = word2.lower()
    word1 = sorted(word1)
    word2 = sorted(word2)
    if word1 == word2:
        return True

# ATTEMPTED: did not use (was going to be for BFS)
def build_graph(words):
    buckets = defaultdict(list)
    graph = defaultdict(set)
    letters = string.lowercase

    # more efficient method of creating word graph
    for word in list(words):
        for i in range(len(word)):
            bucket = '{}_{}'.format(word[:i], word[i + 1:])
            buckets[bucket].append(word)
            # 
    for bucket, mutual_neighbors in buckets.items():
        for word1, word2 in product(mutual_neighbors, repeat=2):
            if word1 != word2:
                graph[word1].add(word2)
                graph[word2].add(word1)

    # ATTEMPTED: individually putting word in graph from delete, insert, and sub 
    #     remove=word[:i]+word[i+1:]
    #     if remove in words:
    #         graph[word].append(remove)
    #     #change 1 character
    #     for char in letters:
    #         change=word[:i]+char+word[i+1:]
    #         if change in words and change!=word:
    #             graph[word].append(change)
    # #add 1 character
    # for i in range(len(word)+1):
    #     for char in letters:
    #         add=word[:i]+char+word[i:]
    #         if add in words:
    #             graph[word].append(add)

    return graph

def get_words(filename, s, t):
    dictionary = [w.strip() for w in open(filename) if w == w.lower() and len(w) >= 3]
    s_length = len(s)
    t_length = len(t)

    # only get words of necessary length 
    if s_length > t_length: 
        words = [w for w in dictionary if len(w) <= s_length and len(w) >= t_length]
    elif s_length < t_length:
        words = [w for w in dictionary if len(w) >= s_length and len(w) <= t_length]
    elif s_length == t_length: 
        words = [w for w in dictionary if len(w) == s_length]
    return words

def traverse(words, startword, endword, ins_score, del_score, sub_score):

    # ATTEMPTED: BFS
    # paths = deque([ [startword] ])
    # extended=set()
    # #Breadth First Search
    # while len(paths) != 0:
    #     currentPath =paths.popleft()
    #     currentWord=currentPath[-1]
    #     if currentWord==endword:
    #         return currentPath
    #     elif currentWord in extended:
    #         #already extended this word
    #         continue
 
    #     extended.add(currentWord)
    #     transforms=graph[currentWord]
    #     for word in transforms:
    #         if word not in currentPath:
    #             #avoid loops
    #             paths.append(currentPath[:]+[word])
    # return -1

    # neighbors of word
    placeholder = object()
    matches = defaultdict(list)
    neighbours = defaultdict(list)
    for word in words:
        for i in range(len(word)):
            pattern = tuple(placeholder if i == j else c
                            for j, c in enumerate(word))
            m = matches[pattern]
            m.append(word)
            neighbours[word].append(m)

    # find cost using levenshtein edit distance & admissible heuristic
    def h_score(word):

        # return sum(a != b for a, b in zip(startword, endword))

        # USE LEVENSHTEIN DISTANCE MATRIX
        rows = len(startword)+1
        cols = len(endword)+1
        # initialize matrix
        dist = [[0 for x in range(cols)] for x in range(rows)]
        # deletions stay within columns 
        for i in range(1, rows):
            dist[i][0] = i * del_score
        # insertions stay within rows
        for i in range(1, cols):
            dist[0][i] = i * ins_score
            
        for col in range(1, cols):
            for row in range(1, rows):
                possible_costs = []
                possible_costs.append(dist[row][col-1] + int(ins_score))
                possible_costs.append(dist[row-1][col] + int(del_score))
                if startword[row-1] == endword[col-1]:
                    possible_costs.append(dist[row-1][col-1])
                else:
                    possible_costs.append(dist[row-1][col-1] + int(sub_score))
                dist[row][col] = min(possible_costs)
                hscore = dist[row][col]

        return hscore


    # words visited in the search.
    visited = set()

    # search nodes using A* algorithm 
    # used min-heap of 4-tuples (f-score, g-score, word, previous-node) to find lowest cost.
    Node = namedtuple('Node', 'f g word previous')
    open_set = set([startword])
    hscore = h_score(startword)
    open_heap = [Node(h_score(startword), 0, startword, None)]
    while open_heap:
        node = heappop(open_heap)
        if node.word == endword:
            result = []
            while node:
                result.append(node.word)
                node = node.previous
            return result[::-1], hscore
        open_set.remove(node.word)
        visited.add(node.word)
        g = node.g + 1
        for neighbourhood in neighbours[node.word]:
            for w in neighbourhood:
                if w not in visited and w not in open_set:
                    next_node = Node(h_score(w) + g, g, w, node)
                    heappush(open_heap, next_node)
                    open_set.add(w)

    return -1


    # ATTEMPTED: Using another type of Deque
    # visited = set()
    # paths = deque([[startword]])
    # while len(paths) > 0:
    #     curr_path = paths.popleft()
    #     curr_word = curr_path[-1]
    #     yield curr_word, curr_path

    #     neighbors = graph[curr_word]  

    #     for neighbor in neighbors - visited:
    #         visited.add(neighbor)
    #         paths.append(curr_path + [neighbor])


# def main():
#     print "Find lowest cost between two words by entering the cost of operation and two words"
#     while True:

        # NEED TO HANDLE TYPE ERROR FOR INVALID INPUT
#         try:
#             costs = map(int, raw_input('Cost of operations: ').split())
#             startword = raw_input('Starting Word: ')
#             endword = raw_input('Ending Word: ')
#         except EOFError:
#             break

#         lowest_cost_word_change(costs, startword, endword)

if __name__ == "__main__":
    # main()
    # print lowest_cost_word_change([7, 1, 5, 2], "opthamology", "glasses") # returns -1
    # print lowest_cost_word_change([1, 1, 2, 1], "kitten", "sitting") # returns -1
    print lowest_cost_word_change([1, 3, 1, 5], "health", "hands") # returns -1 
    # print lowest_cost_word_change([1, 4, 2, 3], "above", "below")
    # print lowest_cost_word_change([1, 9, 1, 3], "team", "mate")
    # print lowest_cost_word_change([1, 1, 1, 1], "damp", "like")
    print lowest_cost_word_change([2, 2, 2, 2], "at", "cat")

