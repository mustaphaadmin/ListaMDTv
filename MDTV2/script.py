import requests

# Configuración de TMDB
API_KEY = "493351c02d78997848da30e6bae16575"
URL_BASE = "https://api.themoviedb.org/3"

# Función para cargar IDs de películas desde un archivo
def cargar_ids_peliculas(archivo="MDTV2/peliculas.txt"):
    with open(archivo, "r") as f:
        return [linea.strip() for linea in f.readlines()]

# Función para obtener detalles de una película
def obtener_detalles_pelicula(id_pelicula):
    url = f"{URL_BASE}/movie/{id_pelicula}?api_key={API_KEY}&language=es-ES&append_to_response=videos"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        detalles = respuesta.json()
        # Construir la URL del póster
        base_url_imagen = "https://image.tmdb.org/t/p/w500"  # Cambia w500 por otro tamaño si lo prefieres
        detalles["poster_url"] = f"{base_url_imagen}{detalles.get('poster_path')}" if detalles.get("poster_path") else "http://enlace_placeholder"
        return detalles
    else:
        print(f"Error al obtener detalles para la película con ID {id_pelicula}")
        return None

# Generar archivo M3U
def generar_m3u(ids_peliculas, archivo_salida="MDTV2/lista.m3u", grupo="VOD"):
    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        archivo.write("#EXTM3U\n")
        for id_pelicula in ids_peliculas:
            detalles = obtener_detalles_pelicula(id_pelicula)
            if detalles:
                titulo = detalles["title"]
                descripcion = detalles["overview"]
                poster_url = detalles.get("poster_url", "http://enlace_placeholder")
                # Obtener enlace del trailer de YouTube
                videos = detalles.get("videos", {}).get("results", [])
                trailer_url = next(
                    (f"https://www.youtube.com/watch?v={video['key']}" for video in videos if video["site"] == "YouTube" and video["type"] == "Trailer"),
                    "http://enlace_placeholder"  # Enlace por defecto si no hay trailer
                )
                # Añadir entrada al archivo M3U con grupo
                archivo.write(f"#EXTINF:-1 tvg-logo=\"{poster_url}\" group-title=\"{grupo}\", {titulo}\n")
                archivo.write(f"# Descripción: {descripcion}\n")
                archivo.write(f"{trailer_url}\n")
        print(f"Lista M3U generada con éxito: {archivo_salida}")

# Ejecutar el script
if __name__ == "__main__":
    ids_peliculas = cargar_ids_peliculas()
    generar_m3u(ids_peliculas)
