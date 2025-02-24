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
media_url = channel_id
