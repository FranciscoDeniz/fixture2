# -*- coding: utf-8 -*-
import pickle

#  Función que valida, que el valor ingresado sea entero
def validate_integer(opcion):
    loop = True
    while loop:
        try:
            opcion = int(opcion)
            loop = False
        except ValueError:
            print u"\n\n\tERROR. Debe ingresar sólo valores ENTEROS."
            opcion = raw_input("\n\n\t\tIngrese nuevamente una opcion: ")
            loop = True
    return opcion

#  Función que valida, que el valor ingresado pertenezca a un rango de valores que estará determinado por las variables start y end
def validate_range(opcion, start, end):
    while opcion < start or opcion > end:
        print u"\n\n\tERROR. Debe ingresar sólo valores VÁLIDOS."
        print u"\n\n\tLos valores deben estar comprendidos entre", start, "y", end, "para considerarse una opción válida."
        opcion = raw_input("\n\n\t\tIngrese nuevamente una opcion: ")
        opcion = validate_integer(opcion)
    return opcion

#  Función que valida la existencia de un archivo
def validating_existence_file(file_name):
    try:
        object_type_file = open(file_name, "r+")
    except IOError:
        object_type_file = open(file_name, "w+")
    object_type_file.close()

#  Función que valida la contraseña
def validate_password(dato):
    while len(dato)<8:
            print u"\n\n\tLa contraseña debe tener al menos 8 caracteres."
            dato = raw_input("\n\tContrasena: ")
    return dato

#  Función que valida el usuario
def validate_user(base,usuario,contrasena):
    if usuario in base.keys():
        temporal = base[usuario] 
        if temporal[2] == contrasena:
            acceso = True
        else:
            acceso = False
    else:
        acceso = False
    return acceso

#  Función que valida al administrador
def validate_admin():
    keys_admin = (1905, 1983,1999)
    cod_admin = raw_input("\n\tIngrese codigo de administrador: ")
    cod_admin = validate_integer(cod_admin)
    while cod_admin not in keys_admin:
        print(u"\n\tCódigo de administrador incorrecto")
        print(u"\n\tIngrese un codigo de administrador válido o 0 para volver al menú principal: ")
        cod_admin = raw_input("\n\t")
        cod_admin = validate_integer(cod_admin)
        if cod_admin == 0:
            return False
    return True