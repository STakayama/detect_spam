
#-*- encoding: utf-8 -*-
import os,sys,time,json,requests,re
from collections import Counter

#user_f=open('../implement/user_from_1020_1022.txt','r')
#https://gist.github.com/kkosuge/1272304
#spam mailからdictionary作る

dictionary=[]
dic_f=open('dictionary.txt','r')
dic_word=dic_f.readline()#一行目はいらないので
dic_word=dic_f.readline()
while dic_word:
    dic_word=dic_word[dic_word.find('\t')+1:]#一行の先頭にタブがある
    dic_word=dic_word[:dic_word.find('\t')]
    dictionary.append(dic_word)
    dic_word=dic_f.readline()

new_f=open ('not_common.txt','w')
new_dicitonary=[]

def make_dictionary(file_name):
    f=open(file_name,'r')
    line=f.readline()
    while line:
        text=line[line.find('"text": "')+9:]
        text=text[text.find(' '):text.find('",')]
        word=text[:line.find(' ')]
        dic_candidates=re.split('[ \n\u]+',text)
        for j in range(0,len(dic_candidates)-1):
            if dic_candidates[j] not in dictionary:
                if dic_candidates[j] not in new_dicitonary:#初めて出てきた単語の時
                    #if re.search('[0-9]',dic_candidates[j]) is None:
                    if re.search('["\'~+\-=_.,/%\?!;:@#\*&\(\)\\\]+',dic_candidates[j]) is None:
                        new_dicitonary.append(dic_candidates[j])
                        print dic_candidates[j]
                        new_f.write(dic_candidates[j]+'\n')

        line=f.readline()

#detect_spam('../twitter_analysis_test/research/1021_en_2.txt')
make_dictionary('../twitter_analysis_test/research/1021_2_en_2.txt')
#detect_spam('../twitter_analysis_test/research/1021_3_en_2.txt')
