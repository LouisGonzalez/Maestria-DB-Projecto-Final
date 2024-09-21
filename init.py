import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, and_
import mariadb
import unicodedata

def connection_to_db():
    connection = mariadb.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="tutorias",
        port=3307
    )

    return connection

conn = f"mysql+pymysql://root:root@localhost:3307/tutorias"

engine = create_engine(conn)
metadata = MetaData()

#Transforma las columnas del excel a minusculas separadas por guiones bajos eliminando posibles tildes
def column_names_to_lower_case(column_name):
    column_to_lower = column_name.lower()
    column_normalized = unicodedata.normalize('NFD', column_to_lower)
    column_normalized2 = ''.join(c for c in column_normalized if unicodedata.category(c) != "Mn")

    column_transformed = column_normalized2.replace(" ","_")

    return column_transformed

#Obtiene la primary key de un select simple
def get_primary_key_value(tableName, colName, value):
    table = Table(tableName, metadata, autoload_with=engine)
    pk_column_name = list(table.columns)[0].name
    query1 = select(table.c[pk_column_name]).where(table.c[colName] == value)
    with engine.connect() as connection:
        return connection.execute(query1).fetchone(),pk_column_name

#Obtiene la primary key de un select con condiciones
def get_primary_key_by_two_values(tableName, conditions):
    table = Table(tableName, metadata, autoload_with=engine)
    pk_column_name = list(table.columns)[0].name
    query1 = select(table.c[pk_column_name]).where(and_(*conditions))
    with engine.connect() as connection:
        return connection.execute(query1).fetchone(),pk_column_name

#Insert data for rol_persona table
def insert_data_rol_persona(sheet, data_frame):
    metadata.reflect(bind=engine)
    table = Table(sheet, metadata, autoload_with=engine)        #Conexion a la tabla rol_persona
    print(table)
    for i, row in data_frame.iterrows():    #recorriendo las filas del data frame
        my_tuple={}
        for col in data_frame.columns:      #recorriendo las columnas del data frame
            col_to_lower = column_names_to_lower_case(col)
            if(col == "ROL"):   #se usa el excel para este atributo
                fk_value = row[col]
                result,pk_name = get_primary_key_value("rol","nombre",fk_value)     #se usa la database para estos atributos
                my_tuple[col_to_lower] = result[0]
            else:
                my_tuple[col_to_lower] = row[col]
        insert_tuple = table.insert().values(**my_tuple)
        with engine.connect() as connection:
            try:
                connection.execute(insert_tuple)
                connection.commit()
            except Exception as e:
                raise e
            
#Insert data for materia_nivel table
def insert_data_materia_nivel(sheet, data_frame):
    metadata.reflect(bind=engine)
    table = Table(sheet, metadata, autoload_with=engine)    #Conexion a la tabla materia_nivel
    print(table)
    for i, row in data_frame.iterrows():    #recorriendo las filas del data frame
        my_tuple={}
        for col in data_frame.columns:  #recorriendo las columnas del data frame
            col_to_lower = column_names_to_lower_case(col)
            if(col == "Materia"):   #se usa el excel para este atributo
                fk_value = row[col]
                result,pk_name = get_primary_key_value("materia","materia",fk_value)    #se usa la database para estos atributos
                my_tuple[col_to_lower] = result[0]
            elif(col == "Nivel"):   #se usa el excel para este atributo
                fk_value = row[col]
                result,pk_name = get_primary_key_value("nivel","nivel", fk_value)   #se usa la database para estos atributos
                my_tuple[col_to_lower] = result[0]
            else:
                my_tuple[col_to_lower] = row[col]
        insert_tuple = table.insert().values(**my_tuple)
        with engine.connect() as connection:
            try:
                connection.execute(insert_tuple)
                connection.commit()
            except Exception as e:
                raise e        

#Insert data for alumno_nivel table
def insert_data_alumno_nivel(sheet, data_frame):
    metadata.reflect(bind=engine)
    table = Table(sheet, metadata, autoload_with=engine)    #Conexion a la tabla alumno_nivel
    print(table)
    for i, row in data_frame.iterrows():    #recorriendo las filas del data frame
        my_tuple={}
        concat=[]
        for col in data_frame.columns:      #recorriendo las columnas del data frame
            col_to_lower = column_names_to_lower_case(col)
            if(col == "Nivel"):   #se usa el excel para este atributo
                fk_value = row[col]
                result,pk_name = get_primary_key_value("nivel","nivel",fk_value)     #se usa la database para estos atributos
                my_tuple[col_to_lower] = result[0]
            else:
                my_tuple[col_to_lower] = row[col]
        insert_tuple = table.insert().values(**my_tuple)
        with engine.connect() as connection:
            try:
                connection.execute(insert_tuple)
                connection.commit()
            except Exception as e:
                raise e

#Insert data for sucursales
def insert_data_sucursal(sheet, data_frame):
    metadata.reflect(bind=engine)   
    table = Table(sheet, metadata, autoload_with=engine)    #Conexion a la tabla sucursal
    for i, row in data_frame.iterrows():    #recorriendo las filas del data frame
        can_insert = False
        my_tuple = {}
        for col in data_frame.columns:      #recorriendo las columnas del data frame
            col_to_lower = column_names_to_lower_case(col)
            if(col == "Salon"):
                print("No hago nada")
            else:
                fk_value = row[col]
                result,pk_name = get_primary_key_value("sucursal","sucursal", fk_value)
                if(result == None):
                    can_insert = True
                    my_tuple[col_to_lower] = row[col]
        if(can_insert == True):
            insert_tuple = table.insert().values(**my_tuple)
            with engine.connect() as connection:
                try:
                    connection.execute(insert_tuple)
                    connection.commit()
                except Exception as e:
                    raise e

#Insert data for salones
def insert_data_salon(sheet, data_frame):
    metadata.reflect(bind=engine)
    table = Table(sheet, metadata, autoload_with=engine) #Conexion a la tabla salon
    for i, row in data_frame.iterrows():    #recorriendo las filas del data frame
        my_tuple = {}
        for col in data_frame.columns:      #recorriendo las columnas del data frame
            col_to_lower = column_names_to_lower_case(col)
            if(col == "Sucursal"):       #Si la columna es sucursal hacer una busqueda del valor de la llave primaria en base al valor de la columna       
                fk_value = row[col]
                result,pk_name = get_primary_key_value("sucursal", "sucursal", fk_value)
                my_tuple[col_to_lower] = result[0]
            else:
                my_tuple[col_to_lower] = row[col]   #Inserta el valor de la columna tal cual esta hacia la base de datos
        insert_tuple = table.insert().values(**my_tuple)
        with engine.connect() as connection:
            try:
                connection.execute(insert_tuple)
                connection.commit()
            except Exception as e:
                raise e

#Insert data for tutor_puede_impartir
def insert_data_tutor_puede_impartir(sheet, data_frame):
    metadata.reflect(bind=engine)
    table = Table(sheet, metadata, autoload_with=engine)    #Conexion a la tabla tutor_puede_impartir
    print(table)
    for i, row in data_frame.iterrows():    #recorriendo las filas del data frame
        my_tuple={}
        conditions = []
        for col in data_frame.columns:      #recorriendo las columnas del data frame
            col_to_lower = column_names_to_lower_case(col)
            actual_table = Table("materia_nivel", metadata, autoload_with=engine) 
            if(col == "Materia"):
                #Encontrar la PK de materia
                fk_value = row[col]
                result,pk_name = get_primary_key_value("materia","materia",fk_value)
                conditions.append(actual_table.c["materia"] == result[0]) #Agrega una nueva condicional a la query (material == "row[col]")
            elif(col == "Nivel"):
                #Encontrar la PK de Nivel
                fk_value = row[col]
                result,pk_name = get_primary_key_value("nivel","nivel",fk_value)
                conditions.append(actual_table.c["nivel"] == result[0]) #Agrega una nueva condicional a la query (nivel == "row[col]")
            else:
                my_tuple[col_to_lower] = row[col]
        result,pk_name = get_primary_key_by_two_values("materia_nivel",conditions)
        my_tuple["materia_nivel"] = result[0]
        insert_tuple = table.insert().values(**my_tuple)
        with engine.connect() as connection:
            try: 
                connection.execute(insert_tuple)
                connection.commit()
            except Exception as e:
                raise e
            
#Insert data for tutoria
def insert_data_tutoria(sheet, data_frame):
    metadata.reflect(bind=engine)
    table = Table(sheet, metadata, autoload_with=engine) #Conexion a la tabla tutoria
    print(table)
    for i, row in data_frame.iterrows():    #recorriendo las filas del data frame
        my_tuple={}
        conditions1=[]
        conditions2=[]
        for col in data_frame.columns:      #recorriendo las columnas del data frame
            col_to_lower = column_names_to_lower_case(col)
            materia_nivel_table = Table("materia_nivel", metadata, autoload_with=engine)
            salon_table = Table("salon", metadata, autoload_with=engine)
            if(col == "Materia"):
                #Encontrar la PK de Materia
                fk_value = row[col]
                result,pk_name = get_primary_key_value("materia","materia",fk_value)
                conditions1.append(materia_nivel_table.c["materia"] == result[0])   
            elif(col == "Nivel"):
                #Encontrar la PK de Nivel
                fk_value = row[col]
                result,pk_name = get_primary_key_value("nivel","nivel",fk_value)
                conditions1.append(materia_nivel_table.c["nivel"] == result[0])
            elif(col == "Sucursal"):
                #Encontrar la PK de sucursal
                fk_value = row[col]
                result,pk_name = get_primary_key_value("sucursal","sucursal", fk_value)
                conditions2.append(salon_table.c["sucursal"] == result[0])
            elif(col == "Salon"):
                fk_value = row[col]
                conditions2.append(salon_table.c["salon"] == fk_value)
            else:
                my_tuple[col_to_lower] = row[col]
        result,pk_name = get_primary_key_by_two_values("materia_nivel", conditions1)
        result2,pk_name2 = get_primary_key_by_two_values("salon", conditions2)
        my_tuple["id_materia_nivel"] = result[0]
        my_tuple["salon"] = result2[0]
        insert_tuple = table.insert().values(**my_tuple)
        with engine.connect() as connection:
            try: 
                connection.execute(insert_tuple)
                connection.commit()
            except Exception as e:
                raise e
        


#Insert data for general tables
def insert_data(sheet, data_frame):
    metadata.reflect(bind=engine)
    table = Table(sheet, metadata, autoload_with=engine)
    print(table)
    for i, row in data_frame.iterrows():    #recorriendo las filas del data frame
        my_tuple={}
        for col in data_frame.columns:      #recorriendo las columnas del data frame
            col_to_lower = column_names_to_lower_case(col)
            my_tuple[col_to_lower] = row[col]
        insert_tuple = table.insert().values(**my_tuple)
        with engine.connect() as connection:
            try: 
                connection.execute(insert_tuple)
                connection.commit()
            except Exception as e:
                raise e

def load_from_excel(file_path):
    sheets = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    return sheets

def main():
    file_path="20240914 - Data.xlsx"
    sheets=load_from_excel(file_path)

    for sheet_name, df in sheets.items():
        print(f"Insertando datos en la hoja {sheet_name}")
        if sheet_name == "TutoriaEstado":                           #1
            insert_data("estado_tutoria", df)
        if sheet_name == "rol":                                     #2
            insert_data(sheet_name, df)
        if sheet_name == "Personas":                                #3
            insert_data("persona",df)
        if sheet_name == "Telefonos":                               #4
            insert_data("telefono",df)
        if sheet_name == "emails":                                  #5
            insert_data("email",df)
        if sheet_name == "Materias":                                #6
            insert_data("materia", df)
        if sheet_name == "Niveles":                                 #7
            insert_data("nivel", df)
        if sheet_name == "EncargadoAlumno":                         #8
            insert_data("encargado_alumno", df)
        if sheet_name == "TutorHorario":                            #9
            insert_data("horario_tutor", df)
        if sheet_name == "Rol Persona":                             #10
            insert_data_rol_persona("rol_persona", df)  
        if sheet_name == "Materia Nivel":                           #11
            insert_data_materia_nivel("materia_nivel", df)
        if sheet_name == "Alumno Nivel":                            #12
            insert_data_alumno_nivel("alumno_nivel", df)
        if sheet_name == "TutorPuedeImpartir":                      #13
            insert_data_tutor_puede_impartir("tutor_puede_impartir", df)
        if sheet_name == "Sucursales":      
            insert_data_sucursal("sucursal", df)                    #14
            insert_data_salon("salon", df)                          #15 
        if sheet_name == "Tutoria":                                 #16
            insert_data_tutoria("tutoria", df)

main()