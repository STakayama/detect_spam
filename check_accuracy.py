#-*- encoding: cp932 -*-
import csv

def check_accuracy(file_name):
    texts=[]
    dic=[]
    spam_num=0
    data_num=0 
    #spam_num/data_num...P(C=c)
    #P(X1=x1|C=c)はだいたい0になるのでは? (各単語のhow_many)/spam_num

    how_many=[]#spamで、何回単語が出現したか
    dic_f=open('not_common.txt','r')
    dic_line=dic_f.readline()
    while dic_line:#dictionaryを読み込み
        dic.append(dic_line)
        dic_line=dic_f.readline()
        
    with open(file_name,'r') as csv_f:
        reader=csv.reader(csv_f)
        #writer.writerrow()
        line=f.readline()
        data_num+=1
        #print line

        #MIが高い


        while line:
            

            if line[2]==1:#判定がspam
                spam_num+=1

            for 
            line=f.readline()

make_csv_anotate('../twitter_analysis_test/research/1021_2_en_2.txt')


#P(X1=x1|C=c)...0のやつは
#MIが0になるxは消す
