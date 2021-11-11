﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.ADT import orderedmap as om
import datetime
import time
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def InitCatalog():
    catalog = {'UFO_sightings': None,
                'duration_UFO': None,
                'datetime_UFO': None,
                'cities': None}
    catalog['UFO_sightings'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['duration_UFO'] = om.newMap(omaptype='RBT', comparefunction=cmpFloats)
    catalog['datetime_UFO'] = om.newMap(omaptype='RBT')
    catalog['cities'] = om.newMap(omaptype="RBT")

    return catalog

# Funciones para agregar informacion al catalogo
def addUFO(catalog, ufo_event):
    lt.addLast(catalog['UFO_sightings'], ufo_event)
    updateDuration(catalog['duration_UFO'], ufo_event)
    updateDatetime(catalog['datetime_UFO'], ufo_event)
    addCity(catalog['cities'], ufo_event)

def updateDuration(orderedmap, ufo_event):
    #EN ESTA FUNCIÓN LA VARIABLE DURATION_EVENT TOMA LA DURACIÓN EN SEGUNDOS
    duration_event = ufo_event['duration (seconds)']
    duration_entry = om.get(orderedmap, duration_event)
    if duration_entry is None:
        duration_list = lt.newList()
        lt.addLast(duration_list, ufo_event)
        om.put(orderedmap, duration_event, duration_list)
    else: 
        value_entry = me.getValue(duration_entry)
        lt.addLast(value_entry, ufo_event)
    return orderedmap

def updateDatetime(orderedmap, ufo_event):
    occurreddate = ufo_event['datetime']
    ufodate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    time_entry = om.get(orderedmap, ufodate.date())
    if time_entry is None:
        ufodate_list = lt.newList()
        lt.addLast(ufodate_list, ufo_event)
        om.put(orderedmap,ufodate.date(),ufodate_list)
    else:
        value_entry = me.getValue(time_entry)
        lt.addLast(value_entry, ufo_event)
    return orderedmap

def addCity(map, ufo_event):
    city= ufo_event["city"]
    if om.contains(map,city) == False:
        lista_ciudad= lt.newList("ARRAY_LIST")
        lt.addLast(lista_ciudad,ufo_event)
        om.put(map,city,lista_ciudad)
    else:
        lista_ciudad= om.get(map,city)["value"]
        lt.addLast(lista_ciudad,ufo_event)

    return map
    
# Funciones para creacion de datos

# Funciones de consulta
######## carga de datos
def total_sightings(catalog):
    total= lt.size(catalog["UFO_sightings"])
    primeros5= lt.subList(catalog["UFO_sightings"],1,5)
    ultimos5= lt.subList(catalog["UFO_sightings"],-4,5)

    return total, primeros5, ultimos5
#########

def datetimesize(catalog): #no
    return om.size(catalog['datetime_UFO'])

def durationsize(catalog): #no
    return om.size(catalog['duration_UFO'])

######### requerimiento 1
def sightings_by_city(catalog,city): 
    list_sightings_city= om.get(catalog["cities"],city)["value"] #o(logn)
    merge.sort(list_sightings_city,cmpByDatetime) #o(nlogn)
    primeros3= lt.subList(list_sightings_city,1,3) #o(1)
    ultimos3= lt.subList(list_sightings_city,-2,3) #o(1)
    
    return om.size(catalog["cities"]),lt.size(list_sightings_city),primeros3,ultimos3

def size_city_tree(catalog):
    elementos= om.size(catalog["cities"]) #o(1)
    altura= om.height(catalog["cities"]) #o(1)

    return elementos, altura
##################

########### requerimiento 2 NICHOLAS
def sightings_by_duration(catalog,min,max):
    max_duration= om.maxKey(catalog["duration_UFO"]) #o(1)
    total_max= lt.size(me.getValue(om.get(catalog["duration_UFO"],max))) #o(logn)+o(1)+o(1)

    duraciones= om.values(catalog["duration_UFO"],min,max) #o(logn)
    total_max_rango= lt.size(lt.lastElement(duraciones)) #o(1)
    
    sightings_in_range= lt.newList("ARRAY_LIST")
    for duracion in lt.iterator(duraciones): #o(m)
        merge.sort(duracion,cmpByCity) #o(klogk)
        for sighting in lt.iterator(duracion): #o(k)
            lt.addLast(sightings_in_range,sighting) #o(1)

    total_rango= lt.size(sightings_in_range) #o(1)

    return max_duration, total_max, total_rango, total_max_rango, sightings_in_range
###########




# Funciones de comparación
def cmpByDatetime(sighting1, sighting2): #para mergesort
    datetime1= time.strptime(sighting1["datetime"], "%Y-%m-%d %H:%M:%S")
    datetime2= time.strptime(sighting2["datetime"], "%Y-%m-%d %H:%M:%S")
    return datetime1 < datetime2

def cmpFloats(duration1,duration2): #para mapas
    num1= float(duration1)
    num2= float(duration2)
    if num1 == num2:
        return 0
    elif num1 > num2:
        return 1
    else:
        return -1

def cmpByCity(city1,city2): #para mergesort
    str1= city1["city"]
    str2= city2["city"]
    return str1 < str2

# Funciones de ordenamiento
