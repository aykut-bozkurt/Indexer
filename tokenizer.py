import porter_stemmer


# takes string and tokenize it after preprocessing(remove punctuations, stop words, case folding)
def tokenize(x):

    # tokenize
    init_list = x.split(" ")

    stop_word_set = []
    token_set = []

    # remove stop words from tokens
    stop_word_set.append("")
    stop_word_set.append("reuter")
    stop_word_set.append("\x03")
    for line in open("stopwords.txt"):
        stop_word_set.append(line.strip("\n"))

    # case folding and further normalization tokens
    for word in init_list:
        word = word.strip('[?,;.!,+"()[]{}<>]').lower()
        if (word != "") and (word not in stop_word_set):
            word = word.replace("'s","").replace("-","").replace("'","").replace('"',"")
            token_set.append(word)

    ''''#
    init_list = [x for x in init_list if x != ""]
    token_set = init_list
    #'''
    #print(token_set)
    return token_set


# stems given tokens in the word list
def stem(word_list):

    stemmed_list = []
    p = porter_stemmer.PorterStemmer()
    if len(word_list) > 0:
        for x in word_list:
            output = ''
            word = ''
            line = x + "\n"
            if line == '':
                break
            for c in line:
                if c.isalpha():
                    word += c.lower()
                else:
                    if word:
                        output += p.stem(word, 0, len(word) - 1)
                        word = ''
                    output += c.lower()
            stemmed_list.append(output.strip("\n"))

    #print(stemmed_list)
    return stemmed_list
