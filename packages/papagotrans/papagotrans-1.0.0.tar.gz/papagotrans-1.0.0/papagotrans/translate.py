import json
from urllib.request import urlopen

def translate(text : str, target : str, source : str):
    """
    Papago 무제한 API를 사용하여 불러옵니다.
    """
    with urlopen(f"https://playentry.org/api/expansionBlock/papago/translate/nsmt?text={text.encode('utf8')}&target={target}&source={source}") as url:
        data = url.read()
    result = json.loads(data.decode('utf-8'))
    return result