import re
from datetime import datetime

# Cambia el nombre si tu archivo limpio tiene diferente nombre
FILENAME = 'sarc_proyecto_tienda_limpio.sql'

# Regex para extraer los bloques de ventas e ingresos
VENTA_REGEX = r"INSERT INTO `app_ventas_venta` \([^)]+\) VALUES(.*?);"
INGRESO_REGEX = r"INSERT INTO `app_finanzas_ingreso` \([^)]+\) VALUES(.*?);"

# Regex para parsear cada fila
# Permite campos NULL y maneja comillas correctamente
VENTA_ROW = re.compile(r"\((\d+),\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*([\d.]+|NULL),\s*(NULL|'[^']*'|[^,]*),.*?\)")
INGRESO_ROW = re.compile(r"\((\d+),\s*'([^']+)',\s*([\d.]+|NULL),\s*'([^']*)',\s*(\d+),\s*'venta'\)")

def parse_ventas(block):
    ventas = {}
    for line in block.strip().split('\n'):
        m = VENTA_ROW.match(line.strip().rstrip(',').rstrip())
        if m:
            vid = int(m.group(1))
            fecha = m.group(2)
            total = float(m.group(5))
            obs = m.group(6).strip().strip("'") if m.group(6) else None
            ventas[vid] = {
                'fecha': fecha,
                'total': total,
                'obs': obs if obs != 'None' else None
            }
    return ventas

def parse_ingresos(block):
    ingresos = {}
    for line in block.strip().split('\n'):
        m = INGRESO_ROW.match(line.strip().rstrip(',').rstrip())
        if m:
            iid = int(m.group(1))
            fecha = m.group(2)
            monto = float(m.group(3))
            desc = m.group(4)
            venta_id = int(m.group(5))
            ingresos[venta_id] = {
                'fecha': fecha,
                'monto': monto,
                'desc': desc
            }
    return ingresos

def comparar_fechas(f1, f2):
    try:
        dt1 = datetime.fromisoformat(f1.split(',')[0].replace('"','').replace("'",''))
        dt2 = datetime.fromisoformat(f2.split(',')[0].replace('"','').replace("'",''))
        # Permite diferencia de segundos
        return abs((dt1 - dt2).total_seconds()) < 60
    except Exception:
        return f1 == f2

def main():
    with open(FILENAME, encoding='utf-8') as f:
        content = f.read()
    ventas_block = re.search(VENTA_REGEX, content, re.DOTALL)
    ingresos_block = re.search(INGRESO_REGEX, content, re.DOTALL)
    if not ventas_block or not ingresos_block:
        print('No se encontró el bloque de ventas o ingresos.')
        return
    ventas = parse_ventas(ventas_block.group(1))
    ingresos = parse_ingresos(ingresos_block.group(1))
    ok, errores = 0, 0
    for vid, v in ventas.items():
        ingreso = ingresos.get(vid)
        if not ingreso:
            print(f'[ERROR] Venta ID {vid} no tiene ingreso asociado.')
            errores += 1
            continue
        # Verifica monto/total
        if abs(v['total'] - ingreso['monto']) > 0.01:
            print(f'[ERROR] Venta ID {vid}: total venta ({v["total"]}) != monto ingreso ({ingreso["monto"]})')
            errores += 1
        # Verifica fecha
        if not comparar_fechas(v['fecha'], ingreso['fecha']):
            print(f'[ERROR] Venta ID {vid}: fecha venta ({v["fecha"]}) != fecha ingreso ({ingreso["fecha"]})')
            errores += 1
        # Si pasa ambas verificaciones
        if errores == 0:
            ok += 1
    print(f'\nRevisión terminada. Ventas correctas: {ok}, Errores: {errores}, Total ventas: {len(ventas)}')
    # Busca ingresos sin venta
    for venta_id in ingresos:
        if venta_id not in ventas:
            print(f'[ERROR] Ingreso con venta_id {venta_id} no tiene venta asociada.')

def generar_insert_ingresos(ventas, archivo_out="correccion_ingresos.sql"):
    lines = []
    lines.append('-- Script generado automáticamente para corregir los INSERT de app_finanzas_ingreso')
    lines.append('-- Asegura que cada ingreso tenga fecha y monto igual a la venta correspondiente, y elimina/omite ingresos huérfanos')
    lines.append('delete from app_finanzas_ingreso;')
    lines.append('INSERT INTO `app_finanzas_ingreso` (`id`, `fecha`, `monto`, `descripcion`, `venta_id`, `tipo`) VALUES')
    inserts = []
    for idx, (vid, v) in enumerate(ventas.items(), start=1):
        fecha = v['fecha']
        monto = v['total']
        descripcion = f'Ingreso por Venta ID {vid}'
        venta_id = vid
        tipo = 'venta'
        inserts.append(f"({idx}, '{fecha}', {monto:.2f}, '{descripcion}', {venta_id}, '{tipo}')")
    lines.append(',\n'.join(inserts) + ';')
    with open(archivo_out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Se generó el archivo {archivo_out} con los INSERT corregidos.')

if __name__ == '__main__':
    main()
    # Generar archivo de corrección de ingresos
    with open(FILENAME, encoding='utf-8') as f:
        content = f.read()
    ventas_block = re.search(VENTA_REGEX, content, re.DOTALL)
    if ventas_block:
        ventas = parse_ventas(ventas_block.group(1))
        generar_insert_ingresos(ventas)

