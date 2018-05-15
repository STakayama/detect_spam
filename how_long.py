#-*- encoding: cp932 -*-
import csv,io
import codecs#文字化け対策

def make_csv_anotate(file_name):
    texts=[]
    with codecs.open('1021_2.csv','wb','utf-8-sig') as csv_f:
        f=open(file_name,'r')
        writer=csv.writer(csv_f)
        #writer.writerrow()
        line=f.readline()
        print line
        while line:
            name=line[line.find('"screen_name": "')+16:]
            name=name[:name.find('"')]

            text=line[line.find('"text": "')+9:]
            text=text[text.find(' '):text.find('",')]

            #text=unicode(str(text),'cp932').encode('utf8')

            texts.append(text)
            texts.append(name)
            writer.writerow(texts)
            texts=[]
            #csv_f.write(text)
            line=f.readline()

make_csv_anotate('../twitter_analysis_test/research/1021_2_en_2.txt')
