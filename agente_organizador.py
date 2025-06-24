import os
import hashlib
import shutil

ROOT = r"C:\Users\Dario\Nextcloud"
REPORTE = os.path.join(ROOT, "reporte_organizador.txt")

def hash_file(filepath):
    """Devuelve el hash md5 de un archivo."""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def sugerir_carpeta(filename):
    """Sugerencia simple de subcarpeta por extension"""
    nombre, ext = os.path.splitext(filename.lower())
    if ext in [".jpg", ".jpeg", ".png"]:
        return "Imágenes"
    elif ext in [".pdf", ".docx", ".doc", ".xls", ".xlsx"]:
        return "Documentos"
    elif ext in [".mp4", ".avi", ".mov"]:
        return "Videos"
    elif ext in [".mp3", ".wav"]:
        return "Audio"
    else:
        return "Otros"

# Recorre carpeta y obtiene info de archivos
archivos = []
hashes = {}
duplicados = []

for dirpath, _, files in os.walk(ROOT):
    for fname in files:
        path = os.path.join(dirpath, fname)
        try:
            fhash = hash_file(path)
        except Exception as e:
            print(f"Error leyendo {path}: {e}")
            continue
        archivos.append({"ruta": path, "nombre": fname, "hash": fhash})
        if fhash in hashes:
            duplicados.append((path, hashes[fhash]))  # (nuevo, original)
        else:
            hashes[fhash] = path

# Escribir reporte
with open(REPORTE, "w", encoding="utf-8") as rep:
    rep.write("===== REPORTE ORGANIZADOR CARPETAS =====\n\n")
    rep.write("== Archivos encontrados ==\n")
    for f in archivos:
        rep.write(f"{f['ruta']} [hash:{f['hash']}]\n")
    rep.write("\n== Duplicados encontrados ==\n")
    for dup, orig in duplicados:
        rep.write(f"{dup}   --> DUPLICADO DE: {orig}\n")

print(f"\nReporte generado en: {REPORTE}\n")

# Interacción por consola para duplicados
for dup, orig in duplicados:
    print(f"\nArchivo duplicado encontrado:")
    print(f"  {dup}\n  DUPLICADO DE:\n  {orig}")
    op = input("¿Qué deseas hacer? [b]orrar / [n]ada: ").strip().lower()
    if op == "b":
        try:
            os.remove(dup)
            print(f"Borrado: {dup}")
        except Exception as e:
            print(f"Error al borrar: {e}")

# Sugerencias de movimiento por “regla”:
for f in archivos:
    sugerida = sugerir_carpeta(f["nombre"])
    carpeta_dest = os.path.join(ROOT, sugerida)
    if not f["ruta"].startswith(carpeta_dest):
        print(f"\nArchivo: {f['ruta']}")
        print(f"Sugerencia: Mover a: {carpeta_dest}")
        op = input("¿Mover archivo? [s]í / [n]o: ").strip().lower()
        if op == "s":
            try:
                os.makedirs(carpeta_dest, exist_ok=True)
                shutil.move(f["ruta"], os.path.join(carpeta_dest, f["nombre"]))
                print("¡Archivo movido!")
            except Exception as e:
                print(f"Error al mover: {e}")

print("\n=== Operación completada. Puedes revisar el reporte para ver el resumen. ===")
