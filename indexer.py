import operator
import bs4
import time

import tokenizer

#
word_count = 0
#

start = time.time()

dictionary = {}
inverted_index = {}

f1 = open("dictionary.txt", "a")
f2 = open("inverted-index.txt", "a")

id_count = 1

# now try for first file (contains 1000 articles in total)
total_file = 22
for file_count in range(0, total_file):
    ids = []
    titles = []
    bodies = []

    soup = None
    if file_count < 10:
        soup = bs4.BeautifulSoup(open(r"./Dataset/reut2-00" + str(file_count) + ".sgm", 'r', encoding = "ISO-8859-1"), "html.parser")
    else:
        soup = bs4.BeautifulSoup(open(r"./Dataset/reut2-0" + str(file_count) + ".sgm", 'r', encoding = "ISO-8859-1"), "html.parser")
    # get all reuters tags in the file
    reuters = soup.find_all('reuters')

    for reuter in reuters:
        soup = bs4.BeautifulSoup(str(reuter), "html.parser")
        # extract all bodies in the file
        bodies.append(soup.find("body"))
        # extract all titles in the file
        titles.append(soup.find("title"))
        # extract all newids in the file
        ids.append(reuter['newid'])

    for article_count_in_file in range(0, len(ids)):
        # call tokenizer(get the union of title and body tokens of the article)
        title = []
        body = []
        if titles[article_count_in_file] is not None:
            title = tokenizer.tokenize(titles[article_count_in_file].text.replace("\n", " "))
        if bodies[article_count_in_file] is not None:
            body = tokenizer.tokenize(bodies[article_count_in_file].text.replace("\n", " "))
        word_list = title + body

        # call stemmer(stem tokens)ids
        word_list = tokenizer.stem(word_list)

        #
        word_count += len(word_list)
        #


        # make indexing
        position_count = 1
        for word in word_list:
            if word not in dictionary:
                dictionary[word] = id_count
                # map of maps {(wordid)1 => { docid(12) => (pos list)[1,2 ,6,8] , docid(17) => (poslist) [4,5,7,8]  }, (wordid)2 => ... }
                inverted_index[dictionary[word]] = {ids[article_count_in_file]:[position_count]}
                id_count += 1
            else:
                if ids[article_count_in_file] in inverted_index[dictionary[word]]:
                    inverted_index[dictionary[word]][ids[article_count_in_file]].append(position_count)
                else:
                    inverted_index[dictionary[word]][ids[article_count_in_file]] = [position_count]
            position_count += 1

f1.write("{\n")
for key, val in sorted(dictionary.items(), key=operator.itemgetter(1)):
    f1.write( "'" +str(key) + "' : " + str(val) + ",\n")
f1.write("}")

f2.write("{\n")
for key, val in sorted(inverted_index.items(), key=operator.itemgetter(0)):
    f2.write(  str(key) + " : " + str(val) + ",\n")
f2.write("}")

f1.close()
f2.close()

end = time.time()
print(end - start)

#print(str(word_count) + " word count")
