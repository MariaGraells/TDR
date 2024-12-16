# Descripció: Aquest script descarrega els articles i pàgines del web de l'institut Pere Vives i els guarda en un fitxer HTML

# Importem la llibreria os per a poder treballar amb el sistema operatiu  
import os
# Importem la llibreria requests per a poder fer peticions HTTP
import requests
# Importem la llibreria BeautifulSoup per a poder treballar amb HTML
from bs4 import BeautifulSoup

#Funcio per a obtenir la informació dels posts
def obtenir_info_posts():
    index_paginacio=1
    global data_titol_contigut

    # Configuració del navegador per a fer les peticions HTTP
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    #Mirem tot els posts, agafem el titol, data i contigut i els PDFs!
    while True: 
        
        try:
            # Accedim als serveis de Wordpress per a obtenir els posts. Els posts venen de 10 en 10.
            # Aquest procés s'anomena paginació, Wordpress ens retorna 10 posts per cada petició.
            # Per això fem servir la variable index de paginació. Quan el index de paginacio val 1, 
            # Wordpress ens retorna els 10 primers posts, quan val 2, ens retorna els 10 següents 
            # i així successivament. 
            response = requests.get(f"https://institutperevives.cat/wp-json/wp/v2/posts?page={index_paginacio}", headers=headers, verify=False)
            
            print(f"🔍 Accedint a la pàgina {index_paginacio}, status: {response.status_code}")
            #Si no hi ha més pàgines
            if response.status_code == 400:
                print(f"🚩 Ja no hi ha més posts")
                break
            
            #Si trobes algun error llença una excepció
            response.raise_for_status()
           
            #Agafem el contingut dels posts en format JSON
            posts_json = response.json()    
            
            #Per a cada post, agafem la data, el titol i el cos
            for post in posts_json:
                data_post = post['date']
                titol_post = post['title']['rendered']
                cos_post = post['content']['rendered']
                
                #Convertim el cos del post a text natural
                cos_text_natural = BeautifulSoup(cos_post, features="html.parser").get_text()

                # Eliminem les linies en blanc
                cos_text_natural = "\n".join(line for line in cos_text_natural.splitlines() if line.strip())
                
                #Guardem el titol, data i cos del post i ho acumulem en una variable en format HTML
                data_titol_contigut = data_titol_contigut + f"""
                    <h1>Titol: {titol_post}</h1>\n
                    <p>Data: {data_post}</p>\n
                    <p>URL: {post['link']}</p>\n
                    <p>Cos:{cos_text_natural}</p>
                """
                #Mostrem que hem llegit el post
                print(f"✅ He llegit la pàgina correctament: {titol_post}")
                
                #Descarreguem els PDFs del cos del post
                descarrega_pdfs_contingut(cos_post)

                #Mostrem que hem descarregat els PDFs
                print(f"✅ I també he guardat els PDFs d'aquesta pàgina, si ni havien: {titol_post}")
        
        #Si hi ha algun error, el mostrem
        except Exception as e:
            print(f"🚩 Hi ha hagut un error per aquest motiu: {str(e)}")
        
        #Incrementem el contador de pagines    
        index_paginacio = index_paginacio + 1


#Funcio per a obtenir la informació de les pàgines
def obtenir_info_pagines():
    index_paginacio=1
    global data_titol_contigut

    # Configuració del navegador per a fer les peticions HTTP
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # Mirem totes les pàgines, agafem el titol, data i contigut i els PDFs
    while True:
        try:
            # Accedim als serveis de Wordpress per a obtenir les pàgines. Les pàgines venen de 10 en 10.
            # Aquest procés s'anomena paginació. Wordpress ens retorna 10 pàgines per cada petició.
            # Per això fem servir la variable index de paginació. Quan el index de paginacio val 1, 
            # Wordpress ens retorna les 10 primeres pàgines, quan val 2, ens retorna les 10 següents 
            # i així successivament. 
            response = requests.get(f"https://institutperevives.cat/wp-json/wp/v2/pages?page={index_paginacio}", 
                                    headers=headers, verify=False)
            
            #Si no hi ha més pàgines
            if response.status_code == 400:
                print(f"🚩 Ja no hi ha més pàgines")
                break
            
            #Si trobes algun error llença una excepció
            response.raise_for_status()

            #Agafem el contingut de la pagina en format JSON
            pagines_json = response.json()

            #Per a cada pagina, agafem la data, el titol i el cos
            for pagina in pagines_json:
                data_pagina = pagina['date_gmt']
                titol_pagina = pagina['title']['rendered']
                cos_pagina = pagina['content']['rendered']
                
                #Convertim el cos de la pagina a text natural   
                pagina_text_natural = BeautifulSoup(cos_pagina, features="html.parser").get_text()

                #Eliminem les linies en blanc
                pagina_text_natural = "\n".join(line for line in pagina_text_natural.splitlines() if line.strip())

                #Guardem el titol, data i cos de la pagina i ho acumulem en una variable en format HTML
                data_titol_contigut = data_titol_contigut + f"""
                    <h1>Titol: {titol_pagina}</h1>\n
                    <p>Data: {data_pagina}</p>\n
                    <p>URL: {pagina['link']}</p>\n
                    <p>Cos: {pagina_text_natural}</p>
                    """
                #Mostrem que hem llegit la pagina i hem agafat la informació que ens interessa
                print(f"✅ He llegit la pàgina correctament: {titol_pagina}")

                #Descarreguem els PDFs del cos de la pagina
                descarrega_pdfs_contingut(cos_pagina)

                #Mostrem que hem descarregat els PDFs de la pagina
                print(f"✅ I també he guardat els PDFs d'aquesta pàgina, si ni havien: {titol_pagina}")

        #Si hi ha algun error, el mostrem
        except Exception as e:
            print(f"🚩 Hi ha hagut un error per aquest motiu: {str(e)}")

        #Incrementem el contador de pagines    
        index_paginacio = index_paginacio + 1


#Funcio per descarregar els PDFs    
def descarrega_pdfs_contingut(cos):
    soup = BeautifulSoup(cos, 'html.parser')
    enllacos_trobats = soup.find_all('a', href=True)

    #Per a cada enllaç, si és un PDF, el descarreguem
    for enllaç in enllacos_trobats:
        if enllaç['href'].endswith('.pdf'):
            pdf_url = enllaç['href']

            try:
                #Descarregar el PDF
                pdf_obtingut = requests.get(pdf_url, verify=False)
                
                #Si la descarrega falla, per algun motiu, com per exemple, si perdem la connexió, aquesta funcio produeix una excepció
                pdf_obtingut.raise_for_status()

                #Donar un nom al fitxer PDF
                nom_fitxer_pdf = os.path.join(carpeta_fitxers, pdf_url.split('/')[-1])
                
                #Escriure el fitxer pdf amb el nom creat al disc de l'ordinador
                with open(nom_fitxer_pdf, 'wb') as f:
                    f.write(pdf_obtingut.content)
                
                #Mostrem que hem descarregat el PDF
                print(f"✅ Fitxer PDF descarregat correctament: {nom_fitxer_pdf}")
            
            #Si hi ha algun error, el mostrem
            except Exception as e:
                print(f"🚩 El PDF amb l'enllaç {pdf_url} ha fallat per aquest motiu: {str(e)}")  


#Funcio principal i AMB LA QUE COMENÇA EL PROGRAMA 
if __name__ == "__main__":

    #Inicialitzem les variables

    #Carpeta on guardarem els PDFs
    carpeta_fitxers = "fitxers"
                
    #Si la carpeta on guardarem els pdfs no existeix, llavors cal crear-la
    os.makedirs(carpeta_fitxers, exist_ok=True)

    #Variable per a guardar la informació dels posts i pàgines 
    data_titol_contigut = ""
    #Nom del fitxer on es guardarà tota la informació
    nom_fitxer_data_titol_cos = "1.contiguts_descarregats_junts.html"

    #Creem la carpeta on guardarem els PDFs
    obtenir_info_posts()
    obtenir_info_pagines()

    #Guardem tota la informació en un fitxer HTML en el directori de fitxers
    nom_fitxer_data_titol_cos = os.path.join(carpeta_fitxers, nom_fitxer_data_titol_cos)
    with open(nom_fitxer_data_titol_cos, 'w', encoding='utf-8') as f:
        f.write(data_titol_contigut)
    
    #Mostrem que hem acabat
    print(f"💫 Acabat")