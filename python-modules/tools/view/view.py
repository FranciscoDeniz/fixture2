# -*- coding: utf-8 -*-


import os
import pickle


#  Función que sirve para limpiar la pantalla
def cleaning():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")

#  Función que carga los datos de un archivo a un diccionario
def loading_file_into_memory(file_name):
    dictionary = {}
    object_type_file = open(file_name, "r+")
    loop = True
    while loop:
        try:
            dictionary = pickle.load(object_type_file)
        except EOFError:
            loop = False
    object_type_file.close()
    return dictionary

#  Función que guarda los datos de un diccionario en un archivo
def saving_changes_to_the_file(file_name, dictionary):
    object_type_file = open(file_name, "w+")
    pickle.dump(dictionary, object_type_file)
    object_type_file.close()
