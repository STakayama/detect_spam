#-*- encoding: cp932 -*-
import csv

def check_accuracy(file_name):
    texts=[]
    dic=[]
    spam_num=0
    data_num=0 
    #spam_num/data_num...P(C=c)
    #P(X1=x1|C=c)�͂�������0�ɂȂ�̂ł�? (�e�P���how_many)/spam_num

    how_many=[]#spam�ŁA����P�ꂪ�o��������
    dic_f=open('not_common.txt','r')
    dic_line=dic_f.readline()
    while dic_line:#dictionary��ǂݍ���
        dic.append(dic_line)
        dic_line=dic_f.readline()
        
    with open(file_name,'r') as csv_f:
        reader=csv.reader(csv_f)
        #writer.writerrow()
        line=f.readline()
        data_num+=1
        #print line

        #MI������


        while line:
            

            if line[2]==1:#���肪spam
                spam_num+=1

            for 
            line=f.readline()

make_csv_anotate('../twitter_analysis_test/research/1021_2_en_2.txt')


#P(X1=x1|C=c)...0�̂��
#MI��0�ɂȂ�x�͏���
