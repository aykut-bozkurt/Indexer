import operator
import re
import itertools
import sys

import time

import tokenizer

# lists 20 most frequent words in the dictionary
def list_top_20_frequent():
    index = get_inverted_index_object()

    length = {}

    for word_key in index.keys():
        sum = 0
        for doc_key in index[word_key].keys():
            for elem in index[word_key][doc_key]:
                sum += 1
        length.update({word_key: sum})

    length = sorted(length.items(), key=operator.itemgetter(1))

    last20pairs = {k[0]: k[1] for k in list(length)[len(length) - 22:]}
    print(last20pairs)


# converts inverted index file content into python object
def get_inverted_index_object():

    return eval( (open("inverted-index.txt").read()).replace("\n","") )


# converts dictionary file content into python object
def get_dictionary_object():

    return eval( (open("dictionary.txt").read()).replace("\n","") )


# returns list of document lists for each query word
def get_docs_of_words(query_words):

    word_keys = {}
    for word in query_words:
        if word in dictionary:
            word_keys.update({word: dictionary[word]})

    if len(word_keys.items()) > 0:

        #sorted in the order of query words
        sorted_keys = []
        for word in query_words:
            sorted_keys.append(word_keys[word])

        # list of list that contains document ids in which contains the word_key corresponding to query word
        doc_ids = []
        for key in sorted_keys:
            global inverted_index_dict
            doc_ids.append(list(inverted_index_dict[int(key)].keys()))

        return doc_ids
    else:
        return []


# returns inverted index rows for query words
def get_inverted_index_list(query_words):
    global inverted_index_dict

    word_keys = []

    for word in query_words:
        word_keys.append({dictionary[word] : inverted_index_dict[dictionary[word]]})

    # print(word_keys)
    if len(word_keys) == len(query_words):
        return word_keys
    else:
        return []


# finds matching documents upon conjunctive query
def conjunctive_matcher(query_words):

    doc_ids = get_docs_of_words(query_words)

    # find documents that contains each query word
    if len(doc_ids) > 0:
        intersect_docs = set(doc_ids[0])
        for i in range(0, len(doc_ids)):
            if i != len(doc_ids) - 1:
                intersect_docs = intersect_docs.intersection(set(doc_ids[i+1]))

        intersect_docs = list(intersect_docs)
        # inplace ascending sort returns none
        intersect_docs.sort()
        print("Results are " + str(intersect_docs))
        return intersect_docs
    else:
        print("No result after conjunction!!!")
        return []


# finds matching documents upon phrase query
def phrase_matcher(query_words):

    inverted_index_list_of_query_words = get_inverted_index_list(query_words)


    if len(inverted_index_list_of_query_words) > 0:
        # list of candidate lists that contain lists of positions of the query words of the same document e.g [ c0[ w0d1[1,5,9,23],w1d1[2,35,56], w2d1[4,6] ], c1[..] ]
        list_of_candidate_list = []
        for inverted_index in inverted_index_list_of_query_words:
            # extract document and positions mapping by removing word number(words already in sorted)
            list_of_candidate_list.append(list(inverted_index.values())[0])

        # sorted in query words
        possible_docs = get_docs_of_words(query_words)

        # print(list_of_candidate_list[0])
        # print(possible_docs)

        if len(possible_docs) > 0:
            candidate_docs = set(possible_docs[0])
            for i in range(0, len(possible_docs)):
                if i != len(possible_docs) - 1:
                    candidate_docs = candidate_docs.intersection(possible_docs[i + 1])
            # print (str(candidate_docs) + " candid")

            candidate_docs = list(candidate_docs)
            candidate_docs.sort()

            # candidate documents' positions' lists to apply merge
            candidates = []
            for x in range(0, len(candidate_docs)):
                candidates.append([])
            for elem in list_of_candidate_list:
                i = 0
                for candid in candidate_docs:
                    if candid in elem:
                        candidates[i].append(elem[candid])
                    i += 1

            print(str(candidates) + " candidates")
            print(str(candidate_docs) + " candid docs")

            i = 0
            doc_index = []
            for candidatelist in candidates:
                #[ [], [], [], ..  ]  merge lists in that list in findDoc function
                if find_doc_for_phrase(candidatelist):
                    doc_index.append(i)
                i += 1

            docs = []
            for index in doc_index:
                docs.append(candidate_docs[index])
            docs.sort()

        print (str(docs) + " founded docs")
        return docs
    else:
        print ("No result after phrase query!!!")
        return []

# returns true if consecutive positions exist when the position lists in the list are merged and are taken one position element
def find_doc_for_phrase(candidateList):
    print(candidateList)
    tuple_len = len(candidateList)
    # product function returns tuples consisting of all combinations in the lists
    tuple_list = list(itertools.product(*candidateList))

    for tuple in tuple_list:
        flag = True
        for i in range(0,tuple_len-1):
            if tuple[i] + 1 != tuple[i+1]:
                flag = False
                break
        if flag:
            return True

    return False

# finds matching documents upon proximity query
def proximity_matcher(query_words, proximity_index_dict):

    inverted_index_list_of_query_words = get_inverted_index_list(query_words)

    if len(inverted_index_list_of_query_words) > 0:
        # list of candidate lists that contain lists of positions of the query words of the same document e.g [ c0[ w0d1[1,5,9,23],w1d1[2,35,56], w2d1[4,6] ], c1[..] ]
        list_of_candidate_list = []
        for inverted_index in inverted_index_list_of_query_words:
            # extract document and positions mapping by removing word number(words already in sorted)
            list_of_candidate_list.append(list(inverted_index.values())[0])

        # sorted in query words
        possible_docs = get_docs_of_words(query_words)

        # print(list_of_candidate_list[0])
        # print(possible_docs)

        if len(possible_docs) > 0:
            candidate_docs = set(possible_docs[0])
            for i in range(0, len(possible_docs)):
                if i != len(possible_docs) - 1:
                    candidate_docs = candidate_docs.intersection(possible_docs[i + 1])
            # print (str(candidate_docs) + " candid")

            candidate_docs = list(candidate_docs)
            candidate_docs.sort()

            # candidate documents' positions' lists to apply merge
            candidates = []
            for x in range(0, len(candidate_docs)):
                candidates.append([])
            for elem in list_of_candidate_list:
                i = 0
                for candid in candidate_docs:
                    if candid in elem:
                        candidates[i].append(elem[candid])
                    i += 1

            print(str(candidates) + " candidates")
            print(str(candidate_docs) + " candid docs")

            i = 0
            doc_index = []
            for candidatelist in candidates:
                # [ [], [], [], ..  ]  merge lists in that list in findDoc function
                if find_doc_for_proximity(candidatelist,proximity_index_dict):
                    doc_index.append(i)
                i += 1

            docs = []
            for index in doc_index:
                docs.append(candidate_docs[index])
            docs.sort()

        print(str(docs) + " founded docs")
        return docs
    else:
        print("No result after phrase query!!!")
        return []


def process_query(query_words):
    query_type = query_words[:1]
    query_words = query_words[1:]
    if query_type == "1":
        # call tokenizer
        query_words = tokenizer.tokenize(query_words.replace("\n", " "))
        # call stemmer(stem tokens)
        query_words = tokenizer.stem(query_words)
        # take set of query words to remove duplicates
        docs = conjunctive_matcher(list(sorted(set(query_words), key=query_words.index)))
        open("results.txt", "a").write(str(docs) + "\n")
    elif query_type == "2":
        # call tokenizer
        query_words = tokenizer.tokenize(query_words.replace("\n", " "))
        # call stemmer(stem tokens)
        query_words = tokenizer.stem(query_words)
        docs = phrase_matcher(query_words)
        open("results.txt", "a").write(str(docs) + "\n")
    elif query_type == "3":
        # call tokenizer
        query_words = tokenizer.tokenize(query_words.replace("\n", " "))
        # call stemmer(stem tokens)
        query_words = tokenizer.stem(query_words)

        # maps proximity index to proximity value e.g( 0 => /3 means proximity value after 0.th word )
        proximity_index_dict = {}
        proximity_index = 0
        for word in query_words:
            match = re.match("^\/\d+$", word)
            if match:
                proximity_index_dict.update({(proximity_index - 1): int(match.group(0).replace("/", ""))})
            else:
                proximity_index += 1

        query_words = [word for word in query_words if not re.match("^\/\d+$", word)]
        for i in range(0, len(query_words)):
            if i not in proximity_index_dict.keys():
                proximity_index_dict.update({i: 0})

        docs = proximity_matcher(query_words, proximity_index_dict)
        open("results.txt", "a").write(str(docs) + "\n")

    else:
        print("Unsupported query type is given!!!")

# returns true if proximity positions holds when the position lists in the list are merged and are taken one position element
def find_doc_for_proximity(candidateList, proximity_index_dict):

    tuple_len = len(candidateList)
    tuple_list = list(itertools.product(*candidateList))

    for tuple in tuple_list:
        flag = True
        for i in range(0,tuple_len-1):
            if tuple[i+1] <= tuple[i] or tuple[i+1] - tuple[i] > proximity_index_dict[i] + 1 :
                flag = False
                break
        if flag:
            return True

    return False





if len(sys.argv) != 2:
    print("Please give a filename for queires as your argument!!!")
else:
    start = time.time()
    dictionary = get_dictionary_object()
    inverted_index_dict = get_inverted_index_object()
    end = time.time()
    print("Total time for dictionary and inverted index retrieval :%d sec" % (end - start))
    start = time.time()
    query_words = sys.argv[1]
    for line in open(sys.argv[1],"r"):
        process_query(line.replace("\n",""))
    end = time.time()
    print("Total time for query processing :%.4f sec" % (end-start))



