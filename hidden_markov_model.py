__author__ = 'TomTang'
# implementation of hidden markov model

from collections import defaultdict
import emission_para
# parameter  q[Yi-2, Yi-1, Yi] = q(Yi| Yi-2, Yi-1)=count(Yi-2, Yi-1, Yi)/count(Yi-2, Yi-1)
q = defaultdict(float)

# parameter e[y,x]=e(x|y)=count(x,y)/count(y) where x is the word and y is the tag
e = defaultdict(float)

# possible tags set
s_set = set()

# vocabulary
vocabulary = set()


def read_corpus_count(corpus_count_file_path):
    counts = [defaultdict(int) for i in xrange(4)]
    count_file = open(corpus_count_file_path)
    for line in count_file:
        line = line.strip()
        if line:
            words = line.split(' ')
            if words[1] == 'WORDTAG':
                counts[0][tuple(words[2:])] = int(words[0])
                vocabulary.add(words[3])
            if words[1].endswith('-GRAM'):
                num = int(words[1].replace('-GRAM', ''))
                counts[num][tuple(words[2:])] = int(words[0])
                if num == 1:
                    s_set.add(words[2])

    count_file.close()

    for tag3 in counts[3].keys():
        for tag2 in counts[2].keys():
            if cmp(tag2, tag3[:-1])==0:
                q[tag3] = float(counts[3][tag3]) / counts[2][tag2]
                #print tag2, tag3,q[tag3]

    for word in counts[0].keys():
        #print tuple([word[0]])
        for tag1 in counts[1].keys():
            #print tuple([word[0]]),tag1,cmp(tuple([word[0]]),tag1)
            if cmp(tuple([word[0]]),tag1)==0:
                e[word] = float(counts[0][word]) / counts[1][tag1]
                #print word,tag1, e[word]
                # print tuple(word[0]), tag1
        #print '\n'


def get_sentence(file_path):
    mfile = open(file_path)
    sentence = []
    for line in mfile:
        line = line.strip()
        if line:
            sentence.append(line)
        else:
            yield sentence
            sentence = []
    if sentence:
        yield sentence

    mfile.close()


def s(index):
    if index < 1:
        return set('*')
    else:
        return s_set


def viterbi(sentences, out_file_path):
    out_file = open(out_file_path, 'w')
    for sentence in sentences:
        n = len(sentence)
        pi = [defaultdict(float) for i in xrange(n + 1)]
        bp = [defaultdict(str) for i in xrange(n + 1)]
        tags = ['' for i in xrange(n + 1)]

        pi[0][tuple(['*', '*'])] = 1
        for k in xrange(1, n + 1):
            for u in s(k - 1):
                for v in s(k):
                    max_pi = float(0)
                    max_bp = str('')
                    for w in s(k - 2):
                        word = sentence[k - 1]
                        if word not in vocabulary:
                            #word='_RARE_'
                            word = emission_para.get_rare_category(word)
                            #print word
                        tmp = pi[k - 1][tuple([w, u])] * q[tuple([w, u, v])] * e[tuple([v, word])]
                        #print pi[k - 1][tuple([w, u])],q[tuple([w, u, v])] ,e[tuple([v, word])],tmp
                        if tmp > max_pi:
                            max_pi = tmp
                            max_bp = w
                    pi[k][tuple([u, v])] = max_pi
                    bp[k][tuple([u, v])] = max_bp

        max_pi = float(0)
        max_u, max_v = str(''), str('')
        for u in s(n - 1):
            for v in s(n):
                tmp = pi[n][tuple([u, v])] * q[tuple([u, v, 'STOP'])]
                if tmp > max_pi:
                    max_u = u
                    max_v = v
                    max_pi=tmp
        tags[n - 1], tags[n] = max_u, max_v

        for k in xrange(n - 2, 0, -1):
            tags[k] = bp[k + 2][tuple([tags[k + 1], tags[k + 2]])]

        for i in xrange(n):
            out_file.write(sentence[i] + ' ' + tags[i + 1] + '\n')
        out_file.write('\n')

    out_file.close()


if __name__ == "__main__":
    read_corpus_count('data\\gene_replace_4rare.counts')
    viterbi(get_sentence('data\\gene.dev'),'data\\gene.dev.p3.out')