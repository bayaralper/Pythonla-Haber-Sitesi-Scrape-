from bs4 import BeautifulSoup
from bs4.element import NavigableString
import time
from bs4 import BeautifulSoup
import requests
def get_request(r):
   soup=BeautifulSoup(r.content,'html5lib')
   time.sleep(1)
   all_div=soup.find_all('div') #Tüm divleri buldur

   for div in all_div:
                  
      if len(div)>0:
         section=find_section(div) #Section classını bul
      
         if section!=None:  
            titles=find_title(section)#Section classının içinden başlıkları al

            break

   return titles

def find_child(div):
   child_div=div.findChild()
   return child_div

def find_section(div):
    if len(div)>0:
        section_class=div.findChild('section',{'id':'slide-manset'})#Divin altındaki section id'lere bakar.
        if section_class!=None:
           
           return section_class
        else:          
           temp=div.find()
           if temp!=None:
              return find_section(temp)
           else:              
               pass

def find_title(find_section):
   if len(find_section)>0:
      title=[]
      div_section=find_section.findChild('div') #Divleri arar 
      if div_section!=None:
         for i in div_section.find_all('a'):#Bütün a taglarını bulur
            a_title=i.get('href')   
            title.append(a_title)
         
         return title
   
      else:
        section_sub=find_child(find_section)
        return find_title(section_sub) #Recursive


def find_url(titles,site_url):#Haber başlıklarını url'e dönüştürür.
   all_url=[]
   for title in titles:
      all_url.append(site_url+title)
      
   return all_url
   

def find_sub_date(sub_url):   #Tarih buldurur.
    sub_r=requests.get(sub_url,verify=False)
    soup=BeautifulSoup(sub_r.content,'html5lib')#Html yapısını çeker
    span=soup.find_all('span',{'class':'tarih'})#Bütün span class:tarihleri buldurur.
    if span!=None:
      for i in span:
        date=i.text
    return date
                   


                   