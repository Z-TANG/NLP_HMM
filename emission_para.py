# reading data\gene.counts and data\gene.train
# map infrequent words (counts<5) into symbol _RARE_
__author__ = 'TomTang'
import re


# primitive words counts dictionary
primitive_counts={}


def read_counts():
    file = open('data\\gene.counts')

    for line in file:
        words=line.strip().split(' ')
        if words[1] == 'WORDTAG':
            num=int(words[0])
            word=words[3]
            if primitive_counts.has_key(word):
                primitive_counts[word] = num+primitive_counts[word]
            else:
                primitive_counts[word] = num
    file.close()


def get_rare_category(word):
    numeric_pattern=re.compile('.*\d.*')
    allCap_pattern=re.compile('\A([A-Z])+\Z')
    lastCap_pattern=re.compile('.*[A-Z]\Z')
    if numeric_pattern.match(word):
        return '_NUMERIC_'
    else:
        if allCap_pattern.match(word):
            return '_ALL_CAPITALS_'
        else:
            if lastCap_pattern.match(word):
                return '_LAST_CAPITAL_'
            else:
                return '_RARE_'




def rewrite_train_data():
    rfile=open('data\\gene.train')
    wfile=open('data\\gene_replace_4rare.train','w')

    for line in rfile:
        line =line.strip()
        if not line:
            wfile.write('\n')
        else:
            words=line.split(' ')
            if primitive_counts[words[0]]<5:
                wfile.write(get_rare_category(words[0])+' '+words[1]+'\n')
            else:
                wfile.write(words[0]+' '+words[1]+'\n')

    rfile.close()
    wfile.close()

if __name__=="__main__":
    read_counts()
    rewrite_train_data()
