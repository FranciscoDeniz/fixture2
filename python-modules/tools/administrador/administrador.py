# -*- coding: utf-8 -*-
# Importando librerías
import sys
import pickle
import itertools

sys.path.append("python-modules")

from tools.validate.validate import *
from tools.view.view import *
from tools.usuarios.usuarios import *
from tools.administrador.administrador import *

# Validando la existencia de los archivos
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


#  Función para ingresar un equipo
def ingresar_equipo(base):
    cleaning()
    if len(base) < 10:
        print "\n\tIngresar equipo.\n\n"
        equipo = raw_input("\n\tIngrese el nombre del equipo: ").upper()
        cantidad = len(base.values())
        if cantidad == 0:
            key = 1
            base[key] = equipo
            saving_changes_to_the_file("equipos.dat", base)
            print "\n\tEl equipo ha sido registrado exitosamente."
        elif equipo not in base.values():
            ultima_clave = list(base.keys())[-1]
            key = ultima_clave + 1
            base[key] = equipo
            saving_changes_to_the_file("equipos.dat", base)
            print "\n\tEl equipo ha sido registrado exitosamente."
        else:
            print "\n\tEquipo existente."
        if len(base)==10:
            print "\n\tSe completaron los 10 equipos."
    else:
        print "\n\tNo se pueden agregar mas equipos."
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

#  Función para eliminar un equipo
def eliminar_equipo(base1, base2):
    cleaning()
    if len(base2)== 0:
        if len(base1) != 0:
            print "\n\tEliminar equipo.\n\n"
            equipo = raw_input("\n\tIngrese el nombre de equipo que desea eliminar: ").upper()
            cleaning()
            if equipo in base1.values():
                for clave, valor in base1.items():
                    if valor == equipo:
                        clave_del = clave
                del base1[clave_del]
                saving_changes_to_the_file("equipos.dat", base1)
                cleaning()
                print "\n\t\tEquipo eliminado exitosamente."
            else:
                print "\n\tEl equipo", equipo, "no existe.\n"
        else:
            print "\n\tNo hay equipos ingresados"
    else:
        print u"\n\tNo se pueden eliminar equipos cuando el fixture ya está generado"
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

#  Función para generar fixture
def generar_fixture(base1, base2, base3):
    cleaning()
    if len(base3) == 0:
        contador = 1
        for i in range (9):
            base3[contador] = []
            contador +=1
        saving_changes_to_the_file("resultados.dat", base3)
    if len(base2) == 0:
        nombres_equipos = list(base1.values())
        if len(base1) == 10:
            contador = 1
            for i in range (9):
                base2[contador] = []
                contador +=1
            saving_changes_to_the_file("fechas.dat", base2)
            # Calcular todas las combinaciones posibles de enfrentamientos
            enfrentamientos_posibles = list(itertools.combinations(nombres_equipos, 2))
            base2[1].append(enfrentamientos_posibles[0])
            base2[1].append(enfrentamientos_posibles[17])
            base2[1].append(enfrentamientos_posibles[30])
            base2[1].append(enfrentamientos_posibles[39])
            base2[1].append(enfrentamientos_posibles[44])
            base2[2].append(enfrentamientos_posibles[2])
            base2[2].append(enfrentamientos_posibles[9])
            base2[2].append(enfrentamientos_posibles[31])
            base2[2].append(enfrentamientos_posibles[38])
            base2[2].append(enfrentamientos_posibles[42])
            base2[3].append(enfrentamientos_posibles[1])
            base2[3].append(enfrentamientos_posibles[10])
            base2[3].append(enfrentamientos_posibles[32])
            base2[3].append(enfrentamientos_posibles[37])
            base2[3].append(enfrentamientos_posibles[41])
            base2[4].append(enfrentamientos_posibles[3])
            base2[4].append(enfrentamientos_posibles[12])
            base2[4].append(enfrentamientos_posibles[20])
            base2[4].append(enfrentamientos_posibles[28])
            base2[4].append(enfrentamientos_posibles[43])
            base2[5].append(enfrentamientos_posibles[4])
            base2[5].append(enfrentamientos_posibles[11])
            base2[5].append(enfrentamientos_posibles[23])
            base2[5].append(enfrentamientos_posibles[27])
            base2[5].append(enfrentamientos_posibles[40])
            base2[6].append(enfrentamientos_posibles[5])
            base2[6].append(enfrentamientos_posibles[16])
            base2[6].append(enfrentamientos_posibles[22])
            base2[6].append(enfrentamientos_posibles[24])
            base2[6].append(enfrentamientos_posibles[36])
            base2[7].append(enfrentamientos_posibles[6])
            base2[7].append(enfrentamientos_posibles[15])
            base2[7].append(enfrentamientos_posibles[19])
            base2[7].append(enfrentamientos_posibles[26])
            base2[7].append(enfrentamientos_posibles[34])
            base2[8].append(enfrentamientos_posibles[8])
            base2[8].append(enfrentamientos_posibles[13])
            base2[8].append(enfrentamientos_posibles[21])
            base2[8].append(enfrentamientos_posibles[25])
            base2[8].append(enfrentamientos_posibles[33])
            base2[9].append(enfrentamientos_posibles[7])
            base2[9].append(enfrentamientos_posibles[14])
            base2[9].append(enfrentamientos_posibles[35])
            base2[9].append(enfrentamientos_posibles[18])
            base2[9].append(enfrentamientos_posibles[29])
            saving_changes_to_the_file("fechas.dat", base2)
            print "\n\tFixture generado exitosamente"
        else:
            print "\n\tDebe haber 10 equipos registrados para generar los enfrentamientos"
    else:
        print "\n\tFixture existente"
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

#  Función para cargar resultados de las fechas
def cargar_resultados(base1,base2):
    cleaning()
    if len(base1) != 0:
        opcion = raw_input("\n\tIngrese la fecha que quiere cargar el resultado (1 a 9): ")
        opcion = validate_integer(opcion)
        opcion = validate_range(opcion, 1, 9)
        if len(base2[opcion]) == 0:
            for equipo1, equipo2 in base1[opcion]:
                print "\n\tFecha numero" , opcion, ":"
                print "\n\t",equipo1, "vs", equipo2
                res_1 = raw_input("\t" +equipo1+ ": ")
                res_1 = validate_integer(res_1)
                res_2 = raw_input("\t" +equipo2+ ": ")
                res_2 = validate_integer(res_2)
                resultado = {equipo1: res_1, equipo2: res_2}
                base2[opcion].append(resultado)
        else:
            print "\tLos resultados de la fecha ", opcion, " ya fueron cargados"
        saving_changes_to_the_file("resultados.dat", base2)
    else:
        print u"\n\tAún no se genero el fixture"
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

#  Función para modificar resultados ya ingresados
def modificar_resultados(base1,base2):
    cleaning()
    bandera = True
    if len(base1) != 0:
        if len(base2) != 0:
            opcion = raw_input("\n\tIngrese la fecha que quiere modificar el resultado (1 a 9): ")
            opcion = validate_integer(opcion)
            opcion = validate_range(opcion, 1, 9)
            if len(base2[opcion]) != 0:
                base2[opcion] = []
                for equipo1, equipo2 in base1[opcion]:
                    print "\n\tFecha numero" , opcion, ":"
                    print "\n\t",equipo1, "vs", equipo2
                    res_1 = raw_input("\t" +equipo1+ ": ")
                    res_1 = validate_integer(res_1)
                    res_2 = raw_input("\t" +equipo2+ ": ")
                    res_2 = validate_integer(res_2)
                    resultado = {equipo1: res_1, equipo2: res_2}
                    base2[opcion].append(resultado)
                print "\n\tResultados modificados exitosamente"
            else:
                print "\n\n\tLos resultados de la fecha ", opcion, " no fueron cargados"
            saving_changes_to_the_file("resultados.dat", base2)
        else:
            print u"\n\tAún no se cargaron resultados"
    else:
        print u"\n\tAún no se genero el fixture"
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")