
#-*- encoding: utf-8 -*-
import json
import os,sys,time,json,requests,re
from collections import Counter

#ツイートのデータ(改行されている)を読み込む
#python twitterで得られるツイートデータの構造：https://gist.github.com/kkosuge/1272304
#spam mailからdictionary作る

dictionary=[]
keys=[]
dic_f=open('dictionary.txt','r')
dic_word=dic_f.readline()#一行目はいらない
dic_word=dic_f.readline()

while dic_word:
    dic_word=dic_word[dic_word.find('\t')+1:]#一行の先頭にタブがある
    key=dic_word[dic_word.find('\t')+1:]
    dic_word=dic_word[:dic_word.find('\t')]
    key=key[key.find('\t')+1:]
    key=key[:key.find('\n')]
    dictionary.append(dic_word)#dictionaryの配列
    keys.append(int(key))#出現率
    dic_word=dic_f.readline()

keyword_points=[]#ツイートに含まれるキーワードの値の合計
users=[]#リンクありのユーザ
links=[]#リンク、対応ユーザと同じ位置
user_candidate=''#usersに入れたいuserの名前
reply_texts=[]#リプライの内容
just_texts=[]#ただのツイート
times=[]#タイムスタンプ
past_time=0#一つ前のツイートとの時間差を比べるための変数

def detect_spam(file_name): #リンク付きツイート
    f=open(file_name,'r')
    line=f.readline()
    while line:#name entitiesの順
        name_line=line[line.find('"screen_name": "')+16:]#名前を取り出すための文字列
        user_candidate=name_line[:name_line.find('"')]
        link_line=line[line.find('"url": ')+7:]#リンクを取り出すための文字列
        rep_line=line[line.find('"in_reply_to_status_id": ')+25:]#リプライ情報を取り出すための文字列
        time_line=line[line.find('"timestamp_ms": "')+17:]#タイムスタンプを取り出すための文字列
        if(len(time_line[:time_line.find('"')])>6):#タイムスタンプが6ケタ以上の時
            times.append(int(time_line[:time_line.find('"')]))
        else:#タイムスタンプがない場合もある
            times.append(1)
        if link_line[:4]=='null':#リンクがない場合
            users.append(user_candidate)
            links.append('')
        else:#リンクがある場合
            link_line=link_line[link_line.find('"')+1:]
            link=link_line[:link_line.find('"')]
            users.append(user_candidate)
            links.append(link)

        if rep_line[:4]=='null':#リプライがない場合
            reply_texts.append('')
            keyword_points.append(0)
        else:#リプライがある場合
            line=line[line.find('"text": "')+9:]#12
            text=line[:line.find('",')]
            reply_texts.append(text)
            keyword_points.append(0)
            word_num=len(re.findall(' +',text))+1.0#単語数
            for word in range(0,len(dictionary)):
                if text.find(dictionary[word])>0:#ツイート内にdictionaryの中身があれば
                    keyword_points[len(keyword_points)-1]+=keys[word]
                keyword_points[len(keyword_points)-1]=keyword_points[len(keyword_points)-1]/word_num#keyword_pointにはツイートの単語数に対するdictionary wordの出現率の和の割合を入れる

            #just_texts...リプライを除いた普通のツイート
        just_text=line[line.find('"text": "')+9:line.find('",')]
        just_texts.append(just_text)
        if user_candidate=='heyjayofficial':
            print just_text
        line=f.readline()

#detect_spam('../twitter_analysis_test/research/1021_en_2.txt')
detect_spam('../twitter_analysis_test/research/1021_2_en_2.txt')
#detect_spam('../twitter_analysis_test/research/1021_3_en_2.txt')

tweet_num=[]
rep_num=[]
links_num=[]
same_rep=[]#same~...同一ユーザの情報をまとめたもの
same_tweet_with_link=[]
same_link=[]
same_time=[]
same_same_tweet=[]
same_keyword=[]#同じユーザのキーワードの値
delete=[]
passed_users=[]#登録済ユーザ
domains=[]
result_rep=[]#各ユーザ毎の結果
result_link=[]
result_time=[]
result_same_tweet=[]
result_tweet_with_link=[]
result_keyword=[]
for user in range(0,len(users)-1):
    if users[user] in passed_users:#ユーザを既に配列に登録済み(重複を避けたい)
        continue
    else:
        if(links[user].find('.gov')>-1 or links[user].find('.jp')>-1 or links[user].find('.edu')>-1):### should be not ".gov." / or ''　安全ドメイン
            domains.append(1)
        else:
            domains.append(0)
        same_rep.append(reply_texts[user])
        same_link.append(links[user])
        same_keyword.append(keyword_points[user])
        same_time.append(10000000000000000000)#ダミー
        same_same_tweet.append(just_texts[user])
        past_time=int(times[user])
        tweet_num.append(0)
        if reply_texts[user]!='':
            rep_num.append(0)
        else:
            rep_num.append(1)
        if links[user]!='':
            links_num.append(0)
            same_tweet_with_link.append(just_texts[user])
        else:
            links_num.append(1)
            same_tweet_with_link.append('')

        delete_rep=[]
        delete_link=[]
        for obj in range(user+1,len(users)-1):
            if(users[user]==users[obj]):#ユーザーが重複
                #print len(tweet_num)
                tweet_num[len(tweet_num)-1]+=1
                same_same_tweet.append(just_texts[user])
                same_rep.append(reply_texts[obj])
                same_link.append(links[obj])
                same_time.append(times[obj]-past_time)
                same_keyword.append(keyword_points[obj])
                past_time=times[obj]
                #print user
                if reply_texts[user]!='':
                    rep_num[len(rep_num)-1]+=1#リプライの数
                if links[user]!='':
                    links_num[len(links_num)-1]+=1#リンクの数
                    same_tweet_with_link.append(just_texts[user])
                else:
                    same_tweet_with_link.append('')
                delete.append(obj)
                if(links[user].find('.gov')>-1|links[user].find('.jp')>-1|links[user].find('.edu')>-1):
                    domains[len(domains)-1]+=1


        counter=Counter(same_rep)
        result_rep.append(counter.most_common()[0])
        counter=Counter(same_link)
        common=counter.most_common()
        counter2=Counter(same_tweet_with_link)
        common2=counter2.most_common()
        link_result=('',0)
        with_result=('',0)
        for i in range(len(common)):
            if common[i][0]!='':
                link_result=common[i]
                with_result=common2[i]
                break
        counter=Counter(same_same_tweet)
        common=counter.most_common()
        same_result=('',0)
        for i in range(len(common)):
            if common[i][0]!='':
                same_result=common[i]
                break
        result_same_tweet.append(same_result)
        result_link.append(link_result)
        result_time.append(min(same_time))#特徴値5
        result_tweet_with_link.append(with_result)

        result_keyword.append(sum(same_keyword))

        delete=[]
        same_rep=[]
        same_link=[]
        same_tweet=[]
        same_time=[]
        passed_users.append(users[user])
link_points=[]
rep_points=[]
domain_points=[]
same_points=[]
for i in range(0,len(passed_users)):
    if result_link[i][0]!='' and tweet_num[i]!=0:#特徴値1
        link_points.append(float(result_link[i][1])/float(tweet_num[i]))
    else:
        link_points.append(-1)
    if result_rep[i][0]!=''and rep_num[i]!=0:#特徴値3
        rep_points.append(float(result_rep[i][1])/float(rep_num[i]))
    else:
        rep_points.append(-1)
    #特徴値4
    if links_num[i]!=0 and links_num[i]!=0:
        domain_points.append(float(domains[i])/float(links_num[i]))
    else:
        domain_points.append(-1)
     #特徴値2
    if result_same_tweet[i][0]!='' and result_same_tweet[i][1]!=0:
        same_points.append(float(result_tweet_with_link[i][1])/float(result_same_tweet[i][1]))
    else:
        same_points.append(-1)

result=[]
#for word in result_keyword:
 #   print word
for i in range(100):
    result.append(passed_users[link_points.index(max(link_points))])
    result.append(passed_users[same_points.index(max(same_points))])
    result.append(passed_users[rep_points.index(max(rep_points))])
    result.append(passed_users[domain_points.index(max(domain_points))])
    result.append(passed_users[result_time.index(min(result_time))])
    #一度見たやつはダミーを入れる(消すとindexが変わってしまうので)
    link_points[link_points.index(max(link_points))]=link_points[link_points.index(min(link_points))]
    same_points[same_points.index(max(same_points))]=same_points[same_points.index(min(same_points))]
    rep_points[rep_points.index(max(rep_points))]=rep_points[rep_points.index(min(rep_points))]
    domain_points[domain_points.index(max(domain_points))]=domain_points[domain_points.index(min(domain_points))]
    result_time[result_time.index(min(result_time))]=result_time[result_time.index(max(result_time))]


print '\n'
for j in range(20):
    if passed_users[result_keyword.index(max(result_keyword))] in result:
        print passed_users[result_keyword.index(max(result_keyword))]
    result_keyword[result_keyword.index(max(result_keyword))]=result_keyword[result_keyword.index(min(result_keyword))]

#print link_points
#print rep_points
#print domain_points
