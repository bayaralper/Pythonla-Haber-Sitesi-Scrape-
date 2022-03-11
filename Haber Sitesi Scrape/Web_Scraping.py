from firebase_admin import firestore
from requests.api import request
from archivepng import driver_find_height, screenshot_with_driver,driver_chrome_settings
import archivepng
import requests,ssl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import Child as ch
import savedb 
import os.path 
from os import name, path
import compare_change as cp_ch
url_main='' #Url üzerinden siteye request atma 
collection_title=url_main[12:17] #İsimlendirmede kullanmak için urlden kesit alındı.
with open(""+url_main[12:17]+".txt","a") as control_txt:#Uygulama kapandığı zaman tekrar çalışsın diye
                                                                           #İlk kez çalıştığında database collection olmadığı için 
                                                                           #Kontrol txt üzerinden yapıldı.
    if os.path.getsize(""+url_main[12:17]+".txt")==0:       
       control_txt.write(url_main)
       calistirildi_mi=False
    else:       
       calistirildi_mi=True

if calistirildi_mi==False:
    r=requests.get(url_main,verify=False)
    time.sleep(3)
    first_titles=ch.get_request(r)#İstek atar,başlıkları döndürür.
    all_url=ch.find_url(first_titles,url_main)#Başlıkları url ile birleştir        
    name_counter=0
    print("İlk girişte "+str(len(all_url))+" sayfanın kaç tanesinin bilgisini tutmak istersiniz")
    x=int(input())
    if x>len(all_url):
        raise Exception("Daha küçük bir sayı giriniz")
    else:
        
        all_url=all_url[0:x]
        for url in all_url:  
                        
                driver=webdriver.Chrome()
                height=driver_find_height(url,driver) #Sayfa yüksekliğini bul
                driver=driver_chrome_settings(height)#Chrome  ve driver ayarlarını yap,driver döndür
                name_counter=screenshot_with_driver(url,driver)#Ss al , url sayısını döndür 
                date=ch.find_sub_date(url)
                savedb.data_identify(url,name_counter,date)#Database üzerinde değişiklik yap,db.collection(collection title) döndür
                name_counter+=1
docs=savedb.db.collection(collection_title).get()    #dökümanları alır            
sorted_db=savedb.sort_data(url_main)         #databasedeki veriler sıralı gelir.       


sayac=1
while sayac>0:    #Yeni veriyi al ve databasedeki verilerle karşılaştır 
    sorted_db=savedb.sort_data(url_main)  
    Karsilastirma=True
    new_r=requests.get(url_main,verify=False)     
    time.sleep(120)
    new_titles=ch.get_request(new_r)
    new_all_url=ch.find_url(new_titles,url_main)#istekten sonra yeni urlleri bulur.

    for i in range(len(sorted_db)-1):   
       if(new_all_url[0]==sorted_db[i].get('url')):
           Karsilastirma=False
           print('Yeni gelen haber yok')
    
    if Karsilastirma==True:#Yeni gelenlerin sayısını bul,Ss al,Eski gelenlerin sayfalarını değiştir db üstünden,yeni gelenlere unique_id ekle ve sayfalarını güncelle.
        if calistirildi_mi==True:
           sorted_db=savedb.sort_data(url_main)  #database sıralar
           savedb.unique_id=sorted_db[len(sorted_db)-1].get('unique_id')+1#Unique_id atar
           print(savedb.unique_id)
           archivepng.name_counter=savedb.unique_id
           print(archivepng.name_counter)
            
        number_new_url=cp_ch.counter_new_url(new_all_url,sorted_db[0].get('url'))
        cp_ch.change_page(docs,collection_title,savedb.db,number_new_url)#Eski gelenlerin sayfalarını değiştirir.
        for i in range(number_new_url):
           driver=webdriver.Chrome()
           height=driver_find_height(new_all_url[i],driver) #Sayfa yüksekliğini bul
           driver=driver_chrome_settings(height)#Chrome ayarlarını yap
           screenshot_with_driver(new_all_url[i],driver)#SS al
           date=ch.find_sub_date(new_all_url[i])
           savedb.data_identify(new_all_url[i],i+1,date)#Yeni gelenlere unique_id eklendi ve sayfası eklendi.
           time.sleep(1)
           sorted_db=savedb.sort_data(url_main)  
                           
           print('Yeni sayfa kaydedildi')


   
