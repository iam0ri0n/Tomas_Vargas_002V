def leer_opcion():
    try:
        opcion=int(input("Ingrese opción: "))
        return opcion
    except ValueError:
        return -1
def buscar_codigo(codigo, dict_prod):
    #if codigo existe returns true (insensible a mayúsculas), False en caso contrario
    codigo_upper=codigo.strip().upper()
    for key in dict_prod:
        if key.upper()==codigo_upper:
            return True
    return False
def obtener_clave_real(codigo, dict_prod):
    #suelta la clave tal cual está guardada en el diccionario, da lo mismo si son mayúsculas o minúsculas
    codigo_upper=codigo.strip().upper()
    for key in dict_prod:
        if key.upper()==codigo_upper:
            return key
    return None
def unidades_por_categoria(categoria, dict_prod, dict_stock):
    #calcula y da el total de unidades disponibles para una categoría dada
    cat_limpia=categoria.strip().lower()
    total_unidades=0
    for cod, datos in dict_prod.items():
        if datos[1].lower()==cat_limpia:
            if cod in dict_stock:
                total_unidades+=dict_stock[cod][1]
    print("El total de unidades disponibles es:", total_unidades)
def busqueda_precio(p_min, p_max, dict_prod, dict_stock):
    #da productos dentro del rango [p_min, p_max] con stock mayor a cero
    encontrados=[]
    for cod in dict_stock:
        try:
            datos_stock=dict_stock[cod]
            precio=datos_stock[0]
            unidades=datos_stock[1]
        except IndexError:
            print(f"Error: Al código {cod} le faltan datos de precio o unidades.")
        if p_min<=precio<=p_max and unidades > 0:
            if cod in dict_prod:
                nombre=dict_prod[cod][0]
                encontrados.append(nombre+"--"+cod)
    if len(encontrados)>0:
        n=len(encontrados)
        for i in range(n):
            for j in range(0,n-i-1):
                if encontrados[j]>encontrados[j+1]:
                    encontrados[j],encontrados[j+1]=encontrados[j+1],encontrados[j]
        print("Los productos encontrados son:", encontrados)
    else:
        print("No hay productos en ese rango de precios.")
def actualizar_precio(codigo, nuevo_precio, dict_prod, dict_stock):
    if buscar_codigo(codigo,dict_prod):
        clave_real=obtener_clave_real(codigo,dict_prod)
        dict_stock[clave_real][0]=nuevo_precio
        return True
    return False
def agregar_producto(codigo, nombre, categoria, marca, peso_kg, es_importado, es_para_cachorro, precio, unidades, dict_prod, dict_stock):
    if buscar_codigo(codigo, dict_prod):
        return False
    cod_clean=codigo.strip().upper()
    dict_prod[cod_clean]=[nombre.strip(), categoria.strip(), marca.strip(), peso_kg, es_importado, es_para_cachorro]
    dict_stock[cod_clean]=[precio, unidades]
    return True
def eliminar_producto(codigo, dict_prod, dict_stock):
    if buscar_codigo(codigo, dict_prod):
        clave_real=obtener_clave_real(codigo, dict_prod)
        del dict_prod[clave_real]
        del dict_stock[clave_real]
        return True
    return False
def validar_codigo(codigo, dict_prod):
    #valida que el código no sea vacío ni solo espacios y que no exista previamente
    if not codigo or codigo.strip()=="":
        return False
    if buscar_codigo(codigo,dict_prod):
        return False
    return True
def validar_texto_no_vacio(texto):
    if not texto or texto.strip()=="":
        return False
    return True
def validar_peso(peso_ingresado):
    try:
        val=float(peso_ingresado)
        return val>0
    except ValueError:
        return False
def validar_booleano_sn(respuesta):
    #valida que la respuesta sea 's' o 'n'(o 'S'/'N')
    r=respuesta.strip().lower()
    return r=='s' or r=='n'
def validar_precio(precio_ingresado):
    try:
        val=int(precio_ingresado)
        return val>0
    except ValueError:
        return False
def validar_unidades(unidades_ingresadas):
    try:
        val=int(unidades_ingresadas)
        return val>=0
    except ValueError:
        return False
def main():
    productos={
    'M001':['Alimento Premium', 'comida', 'DogPlus', 10, True, False],
    'M002':['Arena Aglomerante', 'higiene', 'CatClean', 8, False, False],
    'M003':['Snack Dental', 'snack', 'BiteJoy', 1, True, True],
    'M004':['Shampoo Suave', 'higiene', 'PetCare', 0.5, False, True],
    'M005':['Correa Nylon', 'accesorio', 'WalkPro', 0.3, True, False],
    'M006':['Cama Mediana', 'accesorio', 'CozyPet', 2, False, False],
}
    stock={
    'M001':[32990, 12],
    'M002':[9990, 0],
    'M003':[5490, 25],
    'M004':[7990, 5],
    'M005':[11990, 7],
    'M006':[24990, 3],
}
    continuar=True
    while continuar:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Unidades por categoría")
        print("2. Búsqueda de productos por rango de precio")
        print("3. Actualizar precio de producto")
        print("4. Agregar producto")
        print("5. Eliminar producto")
        print("6. Salir")
        print("=====================================")
        opcion=leer_opcion()
        if opcion==1:
            cat=input("Ingrese categoría a consultar: ")
            unidades_por_categoria(cat, productos, stock)
        elif opcion==2:
            datos_correctos=False
            p_min=0
            p_max=0
            while not datos_correctos:
                min_ingresado=input("Ingrese precio mínimo: ")
                max_ingresado=input("Ingrese precio máximo: ")
                try:
                    p_min=int(min_ingresado)
                    p_max=int(max_ingresado)
                    
                    if p_min>=0 and p_max>=0 and p_min<=p_max:
                        datos_correctos=True
                    else:
                        print("Debe ingresar valores enteros válidos (mínimo <= máximo y >= 0)")
                except ValueError:
                    print("Debe ingresar valores enteros")
            busqueda_precio(p_min, p_max, productos, stock)
        elif opcion==3:
            repetir=True
            while repetir:
                cod=input("Ingrese código del producto: ")
                precio_valido=False
                n_precio=0
                while not precio_valido:
                    p_input=input("Ingrese nuevo precio: ")
                    try:
                        n_precio=int(p_input)
                        if n_precio>0:
                            precio_valido=True
                        else:
                            print("El precio debe ser un número entero positivo.")
                    except ValueError:
                        print("Debe ingresar un valor entero válido.")
                exito=actualizar_precio(cod, n_precio, productos, stock)
                if exito:
                    print("Precio actualizado")
                else:
                    print("El código no existe")
                resp=input("¿Desea actualizar otro precio (s/n)?: ").strip().lower()
                if resp!='s':
                    repetir=False
        elif opcion==4:
            in_codigo=input("Ingrese código del producto: ")
            in_nombre=input("Ingrese nombre: ")
            in_categoria=input("Ingrese categoría: ")
            in_marca=input("Ingrese marca: ")
            in_peso=input("Ingrese peso (kg): ")
            in_importado=input("¿Es importado? (s/n): ")
            in_cachorro=input("¿Es para cachorro? (s/n): ")
            in_precio=input("Ingrese precio: ")
            in_unidades=input("Ingrese unidades: ")
            #validación independiente de cada campo
            v_cod=validar_codigo(in_codigo, productos)
            v_nom=validar_texto_no_vacio(in_nombre)
            v_cat=validar_texto_no_vacio(in_categoria)
            v_mar=validar_texto_no_vacio(in_marca)
            v_pes=validar_peso(in_peso)
            v_imp=validar_booleano_sn(in_importado)
            v_cac=validar_booleano_sn(in_cachorro)
            v_pre=validar_precio(in_precio)
            v_uni=validar_unidades(in_unidades)
            if not v_cod:
                print("Error: El código ingresado está vacío, contiene solo espacios o ya existe.")
            elif not v_nom:
                print("Error: El nombre no puede estar vacío.")
            elif not v_cat:
                print("Error: La categoría no puede estar vacía.")
            elif not v_mar:
                print("Error: La marca no puede estar vacía.")
            elif not v_pes:
                print("Error: El peso debe ser un número mayor a cero.")
            elif not v_imp:
                print("Error: Debe ingresar 's' o 'n' en importado.")
            elif not v_cac:
                print("Error: Debe ingresar 's' o 'n' en cachorro.")
            elif not v_pre:
                print("Error: El precio debe ser un entero mayor a cero.")
            elif not v_uni:
                print("Error: Las unidades deben ser un entero mayor o igual a cero.")
            else:
                es_imp_bool=(in_importado.strip().lower()=='s')
                es_cac_bool=(in_cachorro.strip().lower()=='s')
                peso_float=float(in_peso)
                precio_int=int(in_precio)
                unidades_int=int(in_unidades)
                registrado=agregar_producto(
                    in_codigo, in_nombre, in_categoria, in_marca,
                    peso_float, es_imp_bool, es_cac_bool,
                    precio_int, unidades_int, productos, stock
                )
                if registrado:
                    print("Producto agregado")
                else:
                    print("El código ya existe")
        elif opcion==5:
            cod_elim=input("Ingrese código del producto a eliminar: ")
            eliminado=eliminar_producto(cod_elim, productos, stock)
            if eliminado:
                print("Producto eliminado")
            else:
                print("El código no existe")
        elif opcion==6:
            print("Programa finalizado.")
            continuar=False
        else:
            print("Debe seleccionar una opción válida")
if __name__=="__main__":
    main()