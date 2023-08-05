import requests

def get_public_external_ip() -> str:
    urls = [
        'https://ifconfig.me/ip',
        'https://ipecho.net/plain',
        'https://ipinfo.io/ip',
        'https://ident.me/',
        'https://api.ipify.org/',
    ]
    current_ip = ''
    for endpoint in urls:
        r = requests.get(endpoint)
        if r.status_code == 200:
            current_ip = r.text.strip()
            if current_ip != '':
                break
    return current_ip