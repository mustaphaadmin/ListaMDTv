import requests
from bs4 import BeautifulSoup

# Configurar sesión para mantener cookies y headers
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Referer': 'https://rotana.net/',
    'Origin': 'https://rotana.net',
    'Content-Type': 'application/x-www-form-urlencoded'
})

def get_kwik_key():
    """Obtiene el kwik_key desde la página de Rotana."""
    url = "https://rotana.net/en/channels"
    response = session.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    channel_div = soup.find("a", {"id": "rotana-lbc"})
    
    if channel_div:
        kwik_key = channel_div.get('onclick').split("'")[-2]
        return kwik_key
    else:
        print("Channel ID not found on the page")
        return None

def get_acl_token(kwik_key, media_url):
    """Obtiene el ACL Token desde la API de Rotana."""
    url = "https://rotana.net/channels/generateAclToken"
    data = {'kwik_key': kwik_key, 'mediaUrl': media_url}
    
    response = session.post(url, data=data)
    response.raise_for_status()
    
    try:
        response_json = response.json()
        return response_json.get('data')
    except ValueError:
        print("Failed to parse JSON response")
        return None

def get_m3u8_url(media_url, acl_token):
    """Genera la URL M3U8 con el token ACL."""
    return f"https://live.kwikmotion.com/{media_url}live/{media_url}.smil/playlist.m3u8?hdnts={acl_token}"

# Configuración de canal
media_url = "rlbc"
kwik_key = get_kwik_key()

if kwik_key:
    acl_token = get_acl_token(kwik_key, media_url)
    if acl_token:
        m3u8_url = get_m3u8_url(media_url, acl_token)
        print("M3U8 URL:", m3u8_url)
        
        # Obtener el contenido del archivo M3U8
        m3u8_response = session.get(m3u8_url)
        if m3u8_response.status_code == 200:
            with open("rotlbc.m3u8", "w", encoding="utf-8") as f:
                f.write(m3u8_response.text)
            print("Archivo M3U8 guardado correctamente.")
        else:
            print("Error al obtener el M3U8:", m3u8_response.status_code)
    else:
        print("No se pudo obtener el ACL Token.")
else:
    print("No se pudo obtener el kwik_key.")
