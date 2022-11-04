import Funciones.SQLConnect as F_sql
import Funciones.DataStructure as F_ds
import Funciones.ExportCSV as F_csv

def main():
    propiedadesUsuario = ["localhost", "root", "MySQLRootPass2021", "enfermedadesrespiratorias"]

    # JOIN 5 STUDY-Valores MYSQL----------------------------------------------------------------------------------------
    estudio='hematologia'
    listJOINselect = ['nota_inicial.*', 'laboratorio.folio_orden', 'laboratorio.fecha_orden',
                      'laboratorio.edad', 'laboratorio.servicio_solicita','nota_egreso.fecha_egreso',
                      estudio+'.determinacion',estudio+'.resultado','nota_egreso.diagnostico_final']
    listJOINfrom = ['nota_inicial', 'laboratorio','nota_egreso', estudio]
    listJOINon = ['nota_inicial.nss=laboratorio.nss',
                  'nota_inicial.nss=nota_egreso.nss ',
                  'laboratorio.folio_orden='+estudio+'.folio_orden']

    db_conexion = F_sql.openDBconect(propiedadesUsuario)
    union_datos = F_ds.join_valores_study_data_from_MYSQL(db_conexion, listJOINselect, listJOINfrom, listJOINon,estudio)
    F_csv.export_dataframe_to_csv(union_datos, 'Join_Nota-Labs-'+estudio+'-Determinacion-Valores_MYSQL')
    F_sql.closeDBconect(db_conexion)

    #__________________________________________________________________________________________________________________
    estudio='coagulaciones'
    listJOINselect = ['nota_inicial.*', 'laboratorio.folio_orden', 'laboratorio.fecha_orden',
                      'laboratorio.edad', 'laboratorio.servicio_solicita','nota_egreso.fecha_egreso',
                      estudio+'.determinacion',estudio+'.resultado','nota_egreso.diagnostico_final']
    listJOINfrom = ['nota_inicial', 'laboratorio','nota_egreso', estudio]
    listJOINon = ['nota_inicial.nss=laboratorio.nss',
                  'nota_inicial.nss=nota_egreso.nss ',
                  'laboratorio.folio_orden='+estudio+'.folio_orden']

    db_conexion = F_sql.openDBconect(propiedadesUsuario)
    union_datos = F_ds.join_valores_study_data_from_MYSQL(db_conexion, listJOINselect, listJOINfrom, listJOINon,estudio)
    F_csv.export_dataframe_to_csv(union_datos, 'Join_Nota-Labs-'+estudio+'-Determinacion-Valores_MYSQL')
    F_sql.closeDBconect(db_conexion)

    #__________________________________________________________________________________________________________________
    estudio='inmuno_infecto'
    listJOINselect = ['nota_inicial.*', 'laboratorio.folio_orden', 'laboratorio.fecha_orden',
                      'laboratorio.edad', 'laboratorio.servicio_solicita','nota_egreso.fecha_egreso',
                      estudio+'.determinacion',estudio+'.resultado','nota_egreso.diagnostico_final']
    listJOINfrom = ['nota_inicial', 'laboratorio','nota_egreso', estudio]
    listJOINon = ['nota_inicial.nss=laboratorio.nss',
                  'nota_inicial.nss=nota_egreso.nss ',
                  'laboratorio.folio_orden='+estudio+'.folio_orden']

    db_conexion = F_sql.openDBconect(propiedadesUsuario)
    union_datos = F_ds.join_valores_study_data_from_MYSQL(db_conexion, listJOINselect, listJOINfrom, listJOINon,estudio)
    F_csv.export_dataframe_to_csv(union_datos, 'Join_Nota-Labs-'+estudio+'-Determinacion-Valores_MYSQL')
    F_sql.closeDBconect(db_conexion)

    #__________________________________________________________________________________________________________________
    estudio='inmunologia'
    listJOINselect = ['nota_inicial.*', 'laboratorio.folio_orden', 'laboratorio.fecha_orden',
                      'laboratorio.edad', 'laboratorio.servicio_solicita','nota_egreso.fecha_egreso',
                      estudio+'.determinacion',estudio+'.resultado','nota_egreso.diagnostico_final']
    listJOINfrom = ['nota_inicial', 'laboratorio','nota_egreso', estudio]
    listJOINon = ['nota_inicial.nss=laboratorio.nss',
                  'nota_inicial.nss=nota_egreso.nss ',
                  'laboratorio.folio_orden='+estudio+'.folio_orden']

    db_conexion = F_sql.openDBconect(propiedadesUsuario)
    union_datos = F_ds.join_valores_study_data_from_MYSQL(db_conexion, listJOINselect, listJOINfrom, listJOINon,estudio)
    F_csv.export_dataframe_to_csv(union_datos, 'Join_Nota-Labs-'+estudio+'-Determinacion-Valores_MYSQL')
    F_sql.closeDBconect(db_conexion)

    #__________________________________________________________________________________________________________________
    estudio='quimica_clinica'
    listJOINselect = ['nota_inicial.*', 'laboratorio.folio_orden', 'laboratorio.fecha_orden',
                      'laboratorio.edad', 'laboratorio.servicio_solicita','nota_egreso.fecha_egreso',
                      estudio+'.determinacion',estudio+'.resultado','nota_egreso.diagnostico_final']
    listJOINfrom = ['nota_inicial', 'laboratorio','nota_egreso', estudio]
    listJOINon = ['nota_inicial.nss=laboratorio.nss',
                  'nota_inicial.nss=nota_egreso.nss ',
                  'laboratorio.folio_orden='+estudio+'.folio_orden']

    db_conexion = F_sql.openDBconect(propiedadesUsuario)
    union_datos = F_ds.join_valores_study_data_from_MYSQL(db_conexion, listJOINselect, listJOINfrom, listJOINon,estudio)
    F_csv.export_dataframe_to_csv(union_datos, 'Join_Nota-Labs-'+estudio+'-Determinacion-Valores_MYSQL')
    F_sql.closeDBconect(db_conexion)

    # JOIN 6 Multiples-Studies-Values MYSQL---------------------------------------------------------------------------
    ListEstudios=['hematologia','coagulaciones','inmuno_infecto','inmunologia','quimica_clinica']


    db_conexion = F_sql.openDBconect(propiedadesUsuario)
    union_datos = F_ds.join_multiple_study_data_from_MYSQL(db_conexion,ListEstudios)
    F_csv.export_dataframe_to_csv(union_datos, 'Join_Nota-Labs-MULTIPLE-Estudios-Valores_MYSQL')
    F_sql.closeDBconect(db_conexion)

    # JOIN 7.1 Multiples-Studies-Values MYSQL por DXFinal Embolia------------------------------------------------------
    ListEstudios=['hematologia','coagulaciones','inmuno_infecto','inmunologia','quimica_clinica']
    dx_final='embolia'

    db_conexion = F_sql.openDBconect(propiedadesUsuario)

    union_datos = F_ds.join_multiple_study_data_from_MYSQL_dxFinal(db_conexion,ListEstudios,dx_final)
    NombreArchivoCSV='Mutilple_estudios_'+str(dx_final)

    F_csv.export_dataframe_to_csv(union_datos, NombreArchivoCSV)
    F_sql.closeDBconect(db_conexion)


    # JOIN 7.2 Multiples-Studies-Values MYSQL por DXFinal Embolia------------------------------------------------------
    ListEstudios=['hematologia','coagulaciones','inmuno_infecto','inmunologia','quimica_clinica']
    dx_final='neumonia'

    db_conexion = F_sql.openDBconect(propiedadesUsuario)

    union_datos = F_ds.join_multiple_study_data_from_MYSQL_dxFinal(db_conexion,ListEstudios,dx_final)
    NombreArchivoCSV='Mutilple_estudios_'+str(dx_final)

    F_csv.export_dataframe_to_csv(union_datos, NombreArchivoCSV)
    F_sql.closeDBconect(db_conexion)

    # JOIN 7.3 Multiples-Studies-Values MYSQL por DXFinal Embolia------------------------------------------------------
    ListEstudios=['hematologia','coagulaciones','inmuno_infecto','inmunologia','quimica_clinica']
    dx_final='control'

    db_conexion = F_sql.openDBconect(propiedadesUsuario)

    union_datos = F_ds.join_multiple_study_data_from_MYSQL_dxFinal(db_conexion,ListEstudios,dx_final)
    NombreArchivoCSV='Mutilple_estudios_'+str(dx_final)

    F_csv.export_dataframe_to_csv(union_datos, NombreArchivoCSV)
    F_sql.closeDBconect(db_conexion)


    return None

main()
