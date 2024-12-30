# -*- coding: utf-8 -*-
import sys
import pickle
import itertools

sys.path.append("python-modules")

from tools.validate.validate import *
from tools.view.view import *
from tools.usuarios.usuarios import *
from tools.administrador.administrador import *

validating_existence_file("equipos.dat")
validating_existence_file("usuarios.dat")
validating_existence_file("fechas.dat")
validating_existence_file("resultados.dat")
validating_existence_file("predicciones.dat")
equipos = loading_file_into_memory("equipos.dat")
usuarios = loading_file_into_memory("usuarios.dat")
fechas = loading_file_into_memory("fechas.dat")
resultados = loading_file_into_memory("resultados.dat")
predicciones = loading_file_into_memory("predicciones.dat")


#  Función para ingresar nuevo user
def ingresar_usuario(base1, base2):
    cleaning()
    print "\nRegistrarse.\n\n"
    user = raw_input("\n\t\tIngrese el nombre de USUARIO: ")
    if user not in base1.keys():
        print u"\n\tRellene los campos con la información correspondiente al USUARIO.\n"
        temporal = []
        dato = raw_input("\n\t\t1. Nombre(s): ")
        temporal.append(dato)
        dato = raw_input("\n\t\t2. Apellido(s): ")
        temporal.append(dato)
        dato = raw_input("\n\t\t3. Contrasena: ")
        dato = validate_password(dato)
        temporal.append(dato)
        base1[user] = temporal
        saving_changes_to_the_file("usuarios.dat", base1)
        base2[user] = {}
        saving_changes_to_the_file("predicciones.dat", base2)
        cleaning()
        print "\n\t\tEl USUARIO ha sido registrado exitosamente."
    else:
        print "\n\t\tUsuario existente."
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

#  Función para modificar user existente
def modificar_usuario(base):
    cleaning()
    print "\n\tModificar usuario.\n\n"
    user = raw_input("\n\t\tIngrese el nombre de usuario a modificar: ")
    cleaning()
    if user in base.keys():
        temporal = base[user]
        print "\n\tLos datos del usuario", user, "a modificar son:\n"
        print "\n\t\t1. Nombre(s):", temporal[0]
        print "\n\t\t2. Apellido(s):", temporal[1]
        print u"\n\t\t3. Contraseña:", temporal[2]
        print "\n\n\n\t\t4. Salir SIN MODIFICAR DATOS del CLIENTE."
        atributo = raw_input("\n\n\t\tIngrese una opcion: ")
        atributo = validate_integer(atributo)
        atributo = validate_range(atributo, 1, 4)
        cleaning()
        if atributo != 4:
            msje = "\n\tIngrese "
            etiquetas = ["Nombre(s): ", "Apellido(s): ", "Contraseña: "]
            msje = msje + etiquetas[atributo - 1]
            dato = raw_input(msje)
            temporal[atributo - 1] = dato
            base[user] = temporal
            saving_changes_to_the_file("usuarios.dat", base)
            cleaning()
            print "\n\t\tUsuario modificado exitosamente."
        else:
            print "\n\t\tNO ha modificado el usuario."
    else:
        print u"\n\tEl usuario", user, "que desea modificar, NO ESTA REGISTRADO.\n"
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

#  Función de log in al sistema como user
def login(base):
    cleaning()
    print "\n\tLog in: "
    print "\n\tIngrese el nombre de usuario"
    usuario = raw_input("\n\tUsuario: ")
    print u"\n\tIngrese la contraseña"  
    contrasena = raw_input("\n\tContrasena: ")
    acceso = validate_user(base, usuario, contrasena)
    if acceso == True:
        print "\n\t\tAcceso correcto"
        raw_input("\n\t\tPresione enter para continuar")
        return True, usuario
    else:
        print u"\n\t\tUsuario y/o contraseña incorrecto"
        raw_input("\n\t\tPresione enter para continuar")
        return False, None

#  Función que muestra resultados en cada fecha
def ver_resultados(base1,base2):
    cleaning()
    if len(base2) != 0:
        if len(base1) != 0:
            print"\n\tSeleccione la fecha que quiere ver los resultados (1 a 9): "
            opcion = raw_input("\n\n\t\tIngrese una opcion: ")
            opcion = validate_integer(opcion)
            opcion = validate_range(opcion, 1, 9)
            partidos = base1[opcion]
            mostrar = []
            if len(partidos)>0:
                for partido in partidos:
                # Obtener los nombres de los equipos y los resultados
                    equipo1, res_1 = partido.items()[0]
                    equipo2, res_2 = partido.items()[1]
                    # Formatear la cadena
                    resultado_str = "{} {} VS {} {}".format(equipo1, res_1, res_2, equipo2)
                    mostrar.append(resultado_str)
                print "\n\tEstos son los resultados de la fecha " + str(opcion)+":"
                for partidos in mostrar:
                    print "\n\t\t\t\t", partidos
            else:
                print "\n\tNo hay resultados cargados en esa fecha"
            raw_input("\n\tPresione enter para continuar")
        else:
            print u"\n\tAún no se han cargado resultados, por favor intente luego"
            raw_input("\n\tPresione enter para continuar")
    else:
        print u"\n\tAún no se han generado los enfrentamientos, por favor intente luego"
        raw_input("\n\tPresione enter para continuar")

#  Función que permite predecir los resultados
def prediccion(base1, base2,base3, usuario):
    cleaning()
    if len(base2[usuario]) == 0:
        contador = 1
        for i in range (9):
            base2[usuario][contador] = []
            contador +=1
        saving_changes_to_the_file("predicciones.dat", base2)
    if len(base1) != 0:
        opcion = raw_input("\n\tIngrese la fecha que quiere realizar la prediccion (1 a 9): ")
        opcion = validate_integer(opcion)
        opcion = validate_range(opcion, 1, 9)
        if len(base3[opcion]) == 0:
            cleaning()
            if len(base2[usuario][opcion]) == 0:
                for equipo1, equipo2 in base1[opcion]:
                    print "\n\tFecha numero:" , opcion, ":"
                    print "\n\t" ,equipo1, "vs", equipo2
                    res_1 = raw_input("\t\t" +equipo1+ ": ")
                    res_1 = validate_integer(res_1)
                    res_2 = raw_input("\t\t" +equipo2+ ": ")
                    res_2 = validate_integer(res_2)
                    resultado = {equipo1: res_1, equipo2: res_2}
                    base2[usuario][opcion].append(resultado)
                print "\n\tLa prediccion de la fecha ", opcion, "  fue realizada exitosamente, suerte!"
            else:
                print "\n\tLa prediccion de la fecha ", opcion, " ya fue realizada"
            saving_changes_to_the_file("predicciones.dat", base2)
        else:
            print "\n\tNo se puede hacer la prediccion de una fecha disputada."
    else:
        print u"\n\tAún no se han generado los enfrentamientos, por favor intente luego."
    raw_input("\n\tPresione enter para continuar")

#  Función que permite consultar los resultados de la prediccion
def resultado_predicc(base1,base2, usuario):
    cleaning()
    bandera = True
    if len(base1)!=0:
        for i in range(9):
            if len(base1[i+1]) != 0:
                bandera = False
    if bandera == False:
        opcion = raw_input("\n\tIngrese la fecha que quiere consultar el resultado de la prediccion (1 a 9): ")
        opcion = validate_integer(opcion)
        opcion = validate_range(opcion, 1, 9)
        if opcion not in base1:
            print "\n\tAun no hay resultados disponibles para la fecha ", opcion, ", por favor intente luego"
            raw_input("\n\tPresione enter para continuar")
        elif len(base1[opcion]) == 0:
            print "\n\tAun no hay resultados disponibles para la fecha ", opcion, ", por favor intente luego"
            raw_input("\n\tPresione enter para continuar")
        elif len(base2[usuario][opcion]) == 0:
            print "\n\tEl usuario ", usuario, " no realizo la prediccion de la fecha ", opcion
            raw_input("\n\tPresione enter para continuar")
        else:
            puntos = 0
            reales_mostrar = []
            prediccion_mostrar = []
            partidos = base1[opcion]
            partidos_predic = base2[usuario][opcion]
            for i in range(5):
                partido = partidos[i]
                prediccion = partidos_predic[i]
                equipo1 = ""
                equipo2 = ""
                res_real1 = 0
                res_real2 = 0
                for equipo in partido.items():
                    if equipo1 == "":
                        equipo1 = equipo[0]
                        res_real1 = equipo[1]
                    else:
                        equipo2 = equipo[0]
                        res_real2 = equipo[1]
                res_predic1 = 0
                res_predic2 = 0
                bandera = True
                for resultado in prediccion.values():
                    if bandera == True:
                        res_predic1 = resultado
                        bandera = False
                    else:
                        res_predic2 = resultado
                partido_real = "{} {} VS {} {}".format(equipo1, res_real1, res_real2, equipo2)
                partido_prediccion = "{} {} VS {} {}".format(equipo1, res_predic1, res_predic2, equipo2)
                reales_mostrar.append(partido_real)
                prediccion_mostrar.append(partido_prediccion)
                if res_real1 == res_predic1 and res_real2 == res_predic2:
                    puntos += 3
                    partido = "{} {} VS {} {}".format(equipo1, res_real1, res_real2, equipo2)
                elif res_real1 > res_real2 and res_predic1 > res_predic2:
                    puntos += 1
                elif res_real1 < res_real2 and res_predic1 < res_predic2:
                    puntos += 1
                elif res_real1 == res_real2 and res_predic1 == res_predic2:
                    puntos += 1
    
            print "\n\tPor cada resultado exacto se suma 3 puntos, por acertar el resultado (si es empate o quien gana) se suma 1 punto"
            print "\n\tLos resultados de la fecha numero:", opcion, " fueron: "
            for partidos in reales_mostrar:
                print "\n\t\t", partidos
            print u"\n\tLa prediccion de la fecha numero", opcion, " de", " '",usuario,"' " ,"fue: "
            for partidos in prediccion_mostrar:
                print "\n\t\t", partidos
            print u"\n\tLos puntos obtenidos por el usuario:", " '",usuario,"' " ,"en la fecha numero:", opcion, "son: ", puntos
            raw_input("\n\tPresione enter para continuar")
    else:
        print u"\n\tAún no se han generado los enfrentamientos o no se ha disputado ninguna fecha, por favor intente luego."
        raw_input("\n\tPresione enter para continuar")

#  Función para mostrar tabla de posiciones
def ver_posiciones(base1, base2):
    cleaning()
    if len(base2) > 0:
        posiciones = {}
        for equipos in base2.values():
            posiciones[equipos] = 0
        for clave, valor  in base1.items():
                if len(valor) != 0:
                    for partido in valor:
                        equipo1 = ""
                        equipo2 = ""
                        res1 = 0
                        res2 = 0
                        bandera = True
                        for clave, valor in partido.items():
                            if bandera == True:
                                equipo1 = clave
                                res1 = valor
                                bandera = False
                            else:
                                equipo2 = clave 
                                res2 = valor
                        if res1 > res2:
                            posiciones[equipo1] += 3
                        elif res1 < res2:
                            posiciones[equipo2] += 3
                        else:
                            posiciones[equipo1] += 1
                            posiciones[equipo2] += 1
        posiciones = sorted(posiciones.items(), key=lambda x: x[1], reverse = True)
        print "\n\t\tTabla de posiciones: "
        print "\n\t\t\tEquipos: ","\tPuntos: "
        print"\n"
        for equipo, puntos in posiciones:
            print"\t\t\t{:<15}\t\t{:<10}".format(equipo, puntos)
    else:
        print u"\n\tAún no se ingrsaron equipos"
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
