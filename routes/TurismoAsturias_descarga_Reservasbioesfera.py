#importamos librerias
from bs4 import BeautifulSoup
import requests
import urllib.request
import re ##para trabajar con strings

#Variables
enlaces_rutas = [] #enlaces de las rutas a las paginas web donde se encuentran los kml
nombres_archivos = []
cabecera_url = ['https://www.turismoasturias.es','']
url_separadas_archivos = '' #url de los archivos kml separados sin cabecera
url_descarga_archivo = '' #url completa para descargar el archivo

##variables para los strings de los nombres
nombres_limpios = []
nombres = []


#-- OBTENCION ENLACES DE PAGINAS --#
#Enlace de rutas 
url_reservas_biosfera = 'https://www.turismoasturias.es/naturaleza/reservas-de-la-biosfera'

#Obtenemos el contenido de la url
contenido_url_biosfera = requests.get(url_reservas_biosfera)

#Hacemos un parseo para obtener el contenido en formato html
html_biosfera = BeautifulSoup(contenido_url_biosfera.content, 'html.parser')

#Obtenemos los enlaces a las paginas donde se encuentran los archivos kml con las rutas 
#que se encuentran dentro de las etiquetas html <a></a>
etiquetas_rutas = html_biosfera.find_all('a', class_='link')

#obtemos las url de cada una de las rutas 
for enlaces in etiquetas_rutas:
    enlaces_rutas.append(enlaces.get("href"))


# ---> Obtencion de nombres para los archivos
#Obtenemos las etiquetas con los nombres de los archivos
etiquetas_nombre = html_biosfera.find_all('span', class_="title")
for names in etiquetas_nombre:
     nombres_archivos.append(names.text)

for i in range(len(nombres_archivos)):
    nombres_limpios.append(re.sub("\\n|\\t","",nombres_archivos[i]))

for j in range(len(nombres_limpios)):
    nombres.append(re.sub(" ","",nombres_limpios[j]))
#@comprueba que la lista de nombres no tiene espacios ni carácteres raros
print(nombres)




#-- DESCARGA DE ARCHIVOS --#
contador = 0
while contador <= len(nombres):
    #descargamos los contenidos de las paginas donde se encuentran los kml para posteriormente descargarlo
    for i in range(len(enlaces_rutas)):
        #@--> comprueba que entran correctamente los enlaces
        #@print("enlace entra: ", enlaces_rutas[i])

        #realizamos un get a la url
        paginas_rutas_biosfera = requests.get(enlaces_rutas[i])
        #@--> comprueba que la conexion se realiza correctamente, resultado: response[200]
        #@print("paginas todas: ", paginas_rutas_biosfera)

        #transformamos a formato BeautifulSoup para poder identificar diferentes elementos del documento html y acceder a ellos
        ##le pasamos la pagina y hacemo un parse a html 
        pagina_unica = paginas_rutas_biosfera
        #@--> comprueba que la conexion se realiza correctamente, resultado: response[200]
        #@print("pagina unica: ", pagina_unica)

        #parseo del contenido de la pagina a html
        html_pag_rutas = BeautifulSoup(pagina_unica.content, 'html.parser')

        #especificar el barra baja en clase para que no interprete que se está creando una clase
        #obtenemos la extenson, altitud maxima y coordenadas 
        datos = html_pag_rutas.find_all('div', class_="datos")
        etiqueta_extension = html_pag_rutas.find_all('div', class_='col-md-4 col-sm-6')
        extension = etiqueta_extension[0].div.text
        etiqueta_altitudMax = html_pag_rutas.find_all('div', class_='col-md-8 col-sm-6')
        altitud_max = etiqueta_altitudMax[0].div.text
        etiqueta_coord = html_pag_rutas.find_all('span', class_='infowindow-text coordinates title12')
        coordenadas = etiqueta_coord[0].text
        #@comprobacion
        print("extension: ",extension)
        print("Altmax: ",altitud_max)
        print("coord: ",coordenadas)

        #escribimos el archivo de texto
        with open('reservasBiosfera.txt','a') as reservasBiosfera:
            reservasBiosfera.write(nombres[contador] + "\nExtension: " + extension + "\nAltitudMax: " + altitud_max + "\nCoord: " + coordenadas + "\n\n")
            contador = contador + 1

    
    
