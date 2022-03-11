def counter_new_url(new_all_url,first_url_db):
    number=0
    for url in new_all_url: #Yeni gelen sayfa ile dbnin en yeni elemanını karşılaştırır.
        if url!=first_url_db:
            number+=1
        else:
            break

    return number

def change_page(docs,collection_title,db,number):   #Sayfaları değiştirir.(Yeni gelen sayfa sayısına göre ) 
    for doc in docs:
        old_page=doc.get('page')
        new_page=number+old_page
        db.collection(collection_title).document(doc.id).update({'page':new_page})
        


    