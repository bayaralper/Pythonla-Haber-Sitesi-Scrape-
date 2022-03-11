import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
unique_id=0

cred = credentials.Certificate("")#json ismi yazılır
firebase_admin.initialize_app(cred)
db=firestore.client()

def data_identify(url,counter_url,date):
    global unique_id
    data={'url':url,'page':counter_url,'unique_id':unique_id,'date':date}
    collection_title=url[12:17]
    db.collection(collection_title).document('scrap_'+str(unique_id)).set(data)#Veri setler ve isimlendirme yapar.
    unique_id+=1
    
def sort_data(url):
    collection_title=url[12:17]
    docs=[]
    collec=db.collection(collection_title)
    query=collec.order_by('page',direction=firestore.Query.ASCENDING)#Azalan bir şekilde veri sıralatır.
    results=query.get()
    for result in results:
        result=result.to_dict()#Sözlük yapısına dönüştürür.
        docs.append(result)#Verileri array'e ekler.
    return docs
