
#-*- encoding: utf-8 -*-
import json
import os,sys,time,json,requests
from collections import Counter

#user_f=open('../implement/user_from_1020_1022.txt','r')
#https://gist.github.com/kkosuge/1272304
#spam mailからdictionary作る

dictionary=[]
keys=[]
dic_f=open('dictionary.txt','r')
dic_word=dic_f.readline()#一行目はいらないので
dic_word=dic_f.readline()
while dic_word:
    dic_word=dic_word[dic_word.find('\t')+1:]#一行の先頭にタブがある
    key=dic_word[dic_word.find('\t')+1:]
    dic_word=dic_word[:dic_word.find('\t')]
    key=key[key.find('\t')+1:]
    key=key[:key.find('\n')]
    dictionary.append(dic_word)
    keys.append(int(key))
    #print key
    dic_word=dic_f.readline()

keyword_points=[]#ツイートに含まれるキーワードの値の合計
users=[]#リンクありのユーザ
links=[]#リンク、対応ユーザと同じ位置
use=''
texts=[]#リプライの内容
just_text=[]#ただのツイート
times=[]#タイムスタンプ
points=[]
past_time=0
'''
ex=[1,1,2,3]
con=Counter(ex)
print con.most_common()[0]
'''
def detect_spam(file_name): #リンク付きツイート
    global use
    f=open(file_name,'r')
    line=f.readline()
    while line:#name entitiesの順
        name_line=line[line.find('"screen_name": "')+16:]
        use=name_line[:name_line.find('"')]
        link_line=line[line.find('"url": ')+7:]
        rep_line=line[line.find('"in_reply_to_status_id": ')+25:]
        time_line=line[line.find('"timestamp_ms": "')+17:]
        if(len(time_line[:time_line.find('"')])>6):
            times.append(int(time_line[:time_line.find('"')]))
        else:
            times.append(1)
        if link_line[:4]=='null':
            users.append(use)
            links.append('')
        else:
            link_line=link_line[link_line.find('"')+1:]
            link=link_line[:link_line.find('"')]
            users.append(use)
            links.append(link)
            
        if rep_line[:4]=='null':
            texts.append('')#リプライなし
            keyword_points.append(0)
        else:
            text=line[line.find('"text": "')+9:]#12
            text=text[line.find(' '):line.find('",')]
            texts.append(text)
            keyword_points.append(0)
            word_num=texts.count(' ')-1.0#簡易な単語数数え
            for word in range(0,len(dictionary)):
                if text.find(dictionary[word])>0:
                    keyword_points[len(keyword_points)-1]+=keys[word]
                keyword_points[len(keyword_points)-1]=keyword_points[len(keyword_points)-1]/word_num
        if use=='noufal_rifqi':
            print text
            
            #キーワードが文中にいくつあるか
        just_text.append(line[line.find('"text": "')+9:line.find('",')])
        line=f.readline()

#1900ret scrnひとつめ"users"ふたつめretstatus

#detect_spam('../twitter_analysis_test/research/1021_en_2.txt')
detect_spam('../twitter_analysis_test/research/1021_2_en_2.txt')
#detect_spam('../twitter_analysis_test/research/1021_3_en_2.txt')

one_users=[]
tweet_num=[]
rep_num=[]
links_num=[]
same_rep=[]
same_tweet_with_link=[]
same_link=[]
same_time=[]
same_same_tweet=[]
same_keyword=[]#同じユーザのキーワードの値
delete=[]
passed_users=[]
domains=[]
result_rep=[]
result_link=[]
result_time=[]
result_same_tweet=[]
result_tweet_with_link=[]
result_keyword=[]
for user in range(0,len(users)):
    if users[user] in passed_users:
        continue
    else:
        if(links[user].find('.gov')>-1|links[user].find('.jp')>-1|links[user].find('.edu')>-1):### should be not ".gov." / or ''
            domains.append(1)
            #elif(link.find('.cm')>-1|link.find('.com')>-1|link.find('.cn')>-1):
            # points.append(0.1)
        else:
            one_users.append(users[user])
            domains.append(0)
        same_rep.append(texts[user])
        same_link.append(links[user])
        same_keyword.append(keyword_points[user])
        same_time.append(10000000000000000000)#ダミー
        same_same_tweet.append(just_text[user])
        past_time=int(times[user])
        tweet_num.append(0)
        if texts[user]!='':
            rep_num.append(0)
        else:
            rep_num.append(1)
        if links[user]!='':
            links_num.append(0)
            same_tweet_with_link.append(texts[user])
        else:
            links_num.append(1)
            same_tweet_with_link.append('')
                
        delete_rep=[]
        delete_link=[]
        for obj in range(user+1,len(users)-1):
            if(users[user]==users[obj]):#ユーザーが重複
                #print len(tweet_num)
                tweet_num[len(tweet_num)-1]+=1
                same_same_tweet.append(just_text[user])
                same_rep.append(texts[obj])
                same_link.append(links[obj])
                same_time.append(times[obj]-past_time)
                same_keyword.append(keyword_points[obj])
                past_time=times[obj]
                #print user
                if texts[user]!='':
                    rep_num[len(rep_num)-1]+=1#リプライの数
                if links[user]!='':
                    links_num[len(links_num)-1]+=1#リンクの数
                    same_tweet_with_link.append(texts[user])
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
'''
counter=Conter(link_point)
counter2=Conter()
counter3=Conter()
counter4=Conter()
counter5=Conter()
common=counter.
common2=counter2.
common3=counter3.
common4=counter4.
common5=counter5.
'''
result=[]
for word in result_keyword:
    print word
for i in range(100):
    #print one_users[link_points.index(max(link_points))]
    #print one_users[same_points.index(max(same_points))]
    #print one_users[rep_points.index(max(rep_points))]
    #print one_users[domain_points.index(max(domain_points))]
    #print one_users[result_time.index(min(result_time))]
    result.append(one_users[link_points.index(max(link_points))])
    result.append(one_users[same_points.index(max(same_points))])
    result.append(one_users[rep_points.index(max(rep_points))])
    result.append(one_users[domain_points.index(max(domain_points))])
    result.append(one_users[result_time.index(min(result_time))])
    #一度見たやつはダミーを入れる(消すとindexが変わってしまうので)
    link_points[link_points.index(max(link_points))]=link_points[link_points.index(min(link_points))]
    same_points[same_points.index(max(same_points))]=same_points[same_points.index(min(same_points))]
    rep_points[rep_points.index(max(rep_points))]=rep_points[rep_points.index(min(rep_points))]
    domain_points[domain_points.index(max(domain_points))]=domain_points[domain_points.index(min(domain_points))]
    result_time[result_time.index(min(result_time))]=result_time[result_time.index(max(result_time))]
    

print '\n'
for j in range(100):
#(range 5)500:8件 400:3件
#(range 100) 
    if one_users[result_keyword.index(max(result_keyword))] in result:
        print one_users[result_keyword.index(max(result_keyword))]
    result_keyword[result_keyword.index(max(result_keyword))]=result_keyword[result_keyword.index(min(result_keyword))]

#print link_points
#print rep_points
#print domain_points

'''
user_f=open('spam_user.txt','w')
user_f2=open('spam_link.txt','w')
for user in range(0,len(users)):
    user_f.write(users[user]+'\n')
    user_f2.write(links[user]+'\n')
print users
print links
user_f.close()
'''
