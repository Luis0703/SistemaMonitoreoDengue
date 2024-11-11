# noticia_routes.py
import requests
from flask import Blueprint, jsonify

noticia_routes = Blueprint('noticia_routes', __name__)

GNEWS_API_KEY = '7652a59e3c0354ce354d76c7fa48e31f'  # Reemplaza con tu clave de API

@noticia_routes.route('/api/noticias', methods=['GET'])
def obtener_noticias():
    url = (
        'https://gnews.io/api/v4/search?'
        'q=dengue%20Perú&'    # Términos de búsqueda
        'lang=es&'            # Idioma en español
        'country=pe&'         # Limita a noticias de Perú
        'max=5&'              # Número máximo de resultados
        f'token={GNEWS_API_KEY}'  # Clave de API de GNews
    )
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        articulos = datos.get('articles', [])
        
        # Extraer y estructurar los datos de cada artículo
        noticias = [
            {
                'titulo': articulo['title'],
                'descripcion': articulo['description'],
                'url': articulo['url'],
                'fuente': articulo['source']['name'],
                'fecha': articulo['publishedAt']
            }
            for articulo in articulos
        ]
        
        return jsonify(noticias)
    else:
        return jsonify({'error': 'No se pudieron obtener las noticias'}), 500