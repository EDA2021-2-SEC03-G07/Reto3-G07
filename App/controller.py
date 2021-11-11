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
 """

from sys import int_info
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def InitCatalog():
    catalog = model.InitCatalog()
    return catalog

# Funciones para la carga de datos
def loadData(catalog, ufofile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    ufofile = cf.data_dir + ufofile
    input_file = csv.DictReader(open(ufofile, encoding="utf-8"),
                                delimiter=",")
    for ufo_event in input_file:
        model.addUFO(catalog, ufo_event)


def total_sightings(catalog):
    info= model.total_sightings(catalog)
    return info

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def sightings_by_city(catalog,city):
    info= model.sightings_by_city(catalog,city)
    return info

def size_city_tree(catalog):
    info= model.size_city_tree(catalog)
    return info

#Requerimiento 3

def older_hour(catalog):
    info = model.older_hour(catalog)
    return info
def hours_in_range(catalog, lowhour, highhour):
    info = model.hours_in_range(catalog, lowhour, highhour)
    return info

#Requerimiento 4

def older_sightings(catalog):
    info = model.older_sightings(catalog)
    return info
def dates_in_range(catalog, lowdate, highdate):
    info = model.dates_in_range(catalog, lowdate, highdate)
    return info
def size_in_range(lst):
    info = model.size_in_range(lst)
    return info

#Requerimiento 5

def sightings_by_zone(catalog,min_long,max_long,min_lat,max_lat):
    info= model.sightings_by_zone(catalog,min_long,max_long,min_lat,max_lat)
    return info
