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

acceso_admin = False

def generar_tabla_promedios(equipos, resultados):
    if not equipos or not resultados:
        print("\nNo hay datos suficientes para generar la tabla de promedios.")
        raw_input("\nPresione Enter para continuar...")
        return False  # Indica que no se generó la tabla

    tabla = {nombre: {"Pts": 0, "PJ": 0} for _, nombre in equipos.items()}

    for fecha, partidos in resultados.items():
        for partido in partidos:
            for equipo, goles in partido.items():
                rival = [e for e in partido if e != equipo][0]
                goles_rival = partido[rival]

                if goles > goles_rival:
                    puntos = 3
                elif goles == goles_rival:
                    puntos = 1
                else:
                    puntos = 0

                tabla[equipo]["Pts"] += puntos
                tabla[equipo]["PJ"] += 1

    tabla_ordenada = []
    for equipo, datos in tabla.items():
        pj = datos["PJ"]
        promedio = datos["Pts"] / float(pj) if pj > 0 else 0
        tabla_ordenada.append({
            "Equipo": equipo,
            "Pts": datos["Pts"],
            "PJ": pj,
            "Prom": promedio
        })

    tabla_ordenada.sort(key=lambda x: x["Prom"], reverse=True)

    print("\nTabla de Promedios Generada:")
    print("{:<25} {:<5} {:<5} {:<5}".format("Equipo", "Pts", "PJ", "Prom"))
    print("-" * 45)
    for fila in tabla_ordenada:
        print("{:<25} {:<5} {:<5} {:.3f}".format(fila["Equipo"], fila["Pts"], fila["PJ"], fila["Prom"]))

    print (u"\nLa tabla de promedios se generó exitosamente.")
    raw_input("\nPresione Enter para continuar...")
    return True  # Indica que la tabla se generó correctamente



def calcular_promedio_predicciones(predicciones, usuario):
    # Verifica si hay predicciones para el usuario
    if usuario not in predicciones or not isinstance(predicciones[usuario], list):
        print(u"No hay predicciones válidas para el usuario '{}'.".format(usuario))
        return 0
    

    total_predicciones = len(predicciones[usuario])
    aciertos = sum(1 for prediccion in predicciones[usuario] if prediccion.get('acierto', False))

    if total_predicciones > 0:
        return aciertos / float(total_predicciones) * 100
    else:
        return 0
    


def ver_historial_resultados(equipos, resultados):
    equipo = raw_input("Ingrese el nombre del equipo en mayuscula: ")
    if equipo in equipos.values():
        print("\nHistorial de resultados para {}:".format(equipo))
        for fecha, partidos in resultados.items():
            for partido in partidos:
                if equipo in partido:
                    print("{}: {}".format(fecha, partido))
    else:
        print("El equipo no existe.")
    raw_input("\nPresione Enter para continuar...")    

def ranking_usuarios(usuarios, predicciones):
    ranking = {}
    for usuario in usuarios:
        promedio = calcular_promedio_predicciones(predicciones, usuario)
        ranking[usuario] = promedio
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    print("\nRanking de usuarios:")
    for i, (usuario, promedio) in enumerate(ranking_ordenado, 1):
        print("{}. {}: {:.2f}% de aciertos".format(i, usuario, promedio))
    raw_input("\nPresione Enter para continuar...")
    
# Menús
def menu_principal():
    cleaning() 
    print u"\n\tFixture y predicción."
    print u"\n\tMenú Principal.\n\n"
    print "\n\t1. Acceder como administrador."
    print "\n\t2. Registrar usuario nuevo."
    print "\n\t3. Ingresar como usuario existente."
    print "\n\t4. Salir."
    opcion = raw_input("\n\n\t\tIngrese una opcion: ")
    opcion = validate_integer(opcion)
    opcion = validate_range(opcion, 1, 4)
    return opcion
    
def menu_administrador(cod_admin):
    cleaning()
    if cod_admin == True:
        print u"\n\tMenú administrador.\n\n"
        print "\n\t1. Ingresar equipos."
        print "\n\t2. Eliminar equipos."
        print "\n\t3. Generar fixture."
        print "\n\t4. Cargar resultado."
        print "\n\t5. Modificar resultado."
        print "\n\t6. Generar tabla de promedios."
        print u"\n\t7. Retornar al Menú Principal."
        opcion = raw_input("\n\n\t\tIngrese una opcion: ")
        opcion = validate_integer(opcion)
        opcion = validate_range(opcion, 1, 7)
        return opcion

def menu_usuario():
    cleaning()
    print u"\n\tMenú Usuario.\n\n"
    print "\n\t1. Ver resultados."
    print u"\n\t2. Hacer predicción."
    print u"\n\t3. Resultados de predicción."
    print "\n\t4. Ver tabla de posiciones."
    print "\n\t5. Modificar usuario."
    print "\n\t6. Ver tabla de promedios."
    print "\n\t7. Ver historial de resultados de equipo."
    print "\n\t8. Ver ranking de usuarios."
    print u"\n\t9. Retornar al Menú Principal."
    opcion = raw_input("\n\n\t\tIngrese una opcion: ")
    opcion = validate_integer(opcion)
    opcion = validate_range(opcion, 1, 9)
    return opcion

selec = menu_principal()
while selec != 4:
    if selec == 1:
        cod_admin = validate_admin()
        while cod_admin == True:
            admin = menu_administrador(cod_admin)
            if admin == 1:
                ingresar_equipo(equipos)
            elif admin == 2:
                eliminar_equipo(equipos, fechas)
            elif admin == 3:
                generar_fixture(equipos, fechas, resultados)
                admin = 6
            elif admin == 4:
                cargar_resultados(fechas, resultados)
                admin = 6
            elif admin == 5:
                modificar_resultados(fechas, resultados)
                admin = 6
            elif admin == 6:  # Generar tabla de promedios
                resultado = generar_tabla_promedios(equipos, resultados)
                if resultado:
                    print(u"\nLa tabla de promedios ya estaba generada o se generó correctamente.")
                else:
                    print("\nNo se pudo generar la tabla de promedios.")
                raw_input("\nPresione Enter para continuar...")

            else:
                cod_admin = False
        if cod_admin == False:
            selec = menu_principal()
    elif selec == 2:
        ingresar_usuario(usuarios, predicciones)
        selec = menu_principal()
    elif selec == 3:
        acceso_user, usuario = login(usuarios)
        if acceso_user == False:
            selec = menu_principal()
        while acceso_user == True:
            cod_user = menu_usuario()
            if cod_user == 1:
                ver_resultados(resultados, fechas)
            elif cod_user == 2:
                prediccion(fechas, predicciones, resultados, usuario)
            elif cod_user == 3:
                resultado_predicc(resultados, predicciones, usuario)
            elif cod_user == 4:
                ver_posiciones(resultados, equipos)
            elif cod_user == 5:
                modificar_usuario(usuarios)
            elif cod_user == 6:
                generar_tabla_promedios(equipos, resultados)
            elif cod_user == 7:
                ver_historial_resultados(equipos, resultados)
            elif cod_user == 8:
                ranking_usuarios(usuarios, predicciones)
            else:
                acceso_user = False
                selec = menu_principal()
