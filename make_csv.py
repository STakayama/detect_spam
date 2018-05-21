
#-*- encoding: utf-8 -*-
import os,sys,time,json,requests,re
from collections import Counter
import csv

#ダウンロードしたcommon_wordの辞書、ツイートのデータをcsvに書く
#user_f=open('../implement/user_from_1020_1022.txt','r')
#https://gist.github.com/kkosuge/1272304
#spam mailからdictionary作る

#f=open('not_common.txt','r')
f=open('dictionary.txt','r')
line=f.readline()
dictionary=[]
numeric=[]
for i in range(0,100):#while line:
    line=line[line.find('\t')+1:]
    line=line[:line.find('\t')]
    line=re.sub('["\'~+\-=_.,/%\?!;:@#\*&\(\)\\\]+','',line)
    dictionary.append(line)
    numeric.append('Numeric')
    line=f.readline()
#ファイル一行目に'Numeric'と書き込む。二行目にdictionaryのword
numeric.append('Category')
dictionary.append('Class')

def make_csv(file_name):
    tweet_result=[]#not_commonのwordがない:0
    with open('common_word.csv','wb') as new_f:#,ncoding='shift_jis'
        writer=csv.writer(new_f)
        writer.writerow(numeric)
        writer.writerow(dictionary)
        f_2=open(file_name,'r')#ツイートデータ読み込み
        line=f_2.readline()#一行一ツイート
        while line:#各ツイートごとにdicitonary wordが幾つあるか数える
            text=line[line.find('"text": "')+9:]
            text=text[text.find(' '):text.find('",')]
            #word=text[:line.find(' ')]
            for j in range(0,len(dictionary)-1):
                count=(float)(len(re.findall(' +',text)))+1.0
                tweet_result.append(text.count(dictionary[j]))#/count)
            tweet_result.append(1)
            writer.writerow(tweet_result)
            tweet_result=[]
            print text
            line=f_2.readline()

#detect_spam('../twitter_analysis_test/research/1021_en_2.txt')
make_csv('../twitter_analysis_test/research/1021_2_en_2.txt')
#detect_spam('../twitter_analysis_test/research/1021_3_en_2.txt')
