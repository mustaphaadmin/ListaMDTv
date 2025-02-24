import sys
import requests
from bs4 import BeautifulSoup

def get_kwik_key_from_page(channel_id):
    url = "https://rotana.net/en/live"
    headers = {
        'Referer': 'https://rotana.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Content-Type': 'application/x-mpegURL',
        'Origin': 'https://rotana.net',
        'X-Forwarded-For': '216.239.80.141'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    channel_div = soup.find("a", {"id": channel_id})
    
    if channel_div:
        kwik_key = channel_div.get('onclick').split("'")[-2]
        return kwik_key
    else:
        print(f"Channel ID {channel_id} not found on the page")
        return None

def get_channel_token(kwik_key, media_url):
    url = "https://rotana.net/channels/generateAclToken"
    data = {
        'kwik_key': kwik_key,
        'mediaUrl': media_url
    }
    headers = {
        'Referer': 'https://rotana.net/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://rotana.net',
        'X-Forwarded-For': '216.239.80.141'
    }
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    
    try:
        response_json = response.json()
        return response_json['data']
    except ValueError:
        print("Failed to parse JSON response")
        return None

def construct_m3u8_link(media_url, acl_token):
    return f"https://live.kwikmotion.com/{media_url}live/{media_url}.smil/playlist.m3u8?hdnts={acl_token}"

if len(sys.argv) != 2:
    print("Usage: python rotlbc.py <channel_id>")
    sys.exit(1)

channel_id = sys.argv[1]
media_url = channel_id.replace("-", "")
kwik_key = get_kwik_key_from_page(channel_id)

if kwik_key:
    acl_token = get_channel_token(kwik_key, media_url)
    if acl_token:
        m3u8_link = construct_m3u8_link(media_url, acl_token)
        with open(f"ressources/kuw/{media_url}.m3u8", "w") as file:
            file.write("#EXTM3U\n")
            file.write("#EXT-X-VERSION:3\n")
            file.write(f"#EXT-X-STREAM-INF:BANDWIDTH=4265866,RESOLUTION=1920x1080,CODECS=\"avc1.640029,mp4a.40.2\",CLOSED-CAPTIONS=NONE\n{m3u8_link}\n")
        print("M3U8 file updated successfully")
    else:
        print("Failed to retrieve ACL token")
else:
    print(f"Failed to retrieve kwik_key for channel {channel_id}")
