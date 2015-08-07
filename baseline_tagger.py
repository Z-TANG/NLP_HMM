__author__ = 'TomTang'
# for each word x,  tag y* = arg max e(x|y)= arg max count(x,y)/count(y)

dic={}
unigram={}
def read_count(count_file_path):
    count_file=open(count_file_path)
    for line in count_file:
        line=line.strip()
        if line:
            words=line.split(' ')
            if words[1]=='WORDTAG':
                if not dic.has_key(words[3]):
                    dic[words[3]]={}
                    dic[words[3]]['O']=0
                    dic[words[3]]['I-GENE']=0
                dic[words[3]][words[2]]=int(words[0])
            if words[1]=='1-GRAM':
               unigram[words[2]]=int(words[0])

def read_dev(dev_file_path,out_file_path):
    dev_file=open(dev_file_path)
    out_file=open(out_file_path,'w')
    for line in dev_file:
        line=line.strip()
        if line:
            if not dic.has_key(line):
                newline='_RARE_'
            else:
                newline=line
            max_e=float(0)
            max_tag=''
            for tag in unigram.keys():
                tmp=float(dic[newline][tag])/float(unigram[tag])
                if max_e<tmp:
                    max_e=tmp
                    max_tag=tag
            out_file.write(line+' '+max_tag+'\n')
        else:
            out_file.write('\n')

if __name__=="__main__":
    read_count('data\\gene_replace_rare.counts')
    read_dev('data\\gene.dev','data\\gene.dev.p1.out')
