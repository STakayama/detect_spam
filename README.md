# detect_spam
This is an  attempt to detrect spams on twitter.  
Refered http://ci.nii.ac.jp/naid/110009623087 and https://ipsj.ixsq.nii.ac.jp/ej/?action=repository_action_common_download&item_id=151505&item_no=1&attribute_id=1&file_no=1  
All of them are written in python2.7.  
  
API...TwitterStreamAPI(python/twitter)   
Main program...detect_spam.py  
Previous attempt...make_dic.py, new_dic.py  
dictonary...not_common.txt(created using dictionary.txt(Word Frequencies in Written and Spoken English) and tweet data)  
program for making a dictionary...check_accuracy.py  
change txt to csv...make_csv.py  
  
  <main program>
  
  1. make of an array of dictionary on not_common.txt  
  
  2. read tweet datas and keep user data. score each tweet datas.(If possibility of spam is high, the point is large.)  
  
  3. delete information of user who has already registered to passed_users[].count points or numbers of each items.  
  
  4. show users' names whose accounts are judged as spam account.
