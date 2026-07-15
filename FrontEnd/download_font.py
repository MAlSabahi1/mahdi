import requests
from bs4 import BeautifulSoup
import re
import os
import zipfile
import io

def download_samt_font():
    # Attempt to download from arbfonts.com
    # url = "https://arbfonts.com/samt-7017-font-download.html"
    
    # Actually let's try a direct search on duckduckgo for raw ttf URLs
    search_url = "https://html.duckduckgo.com/html/?q=samt+7017+filetype:ttf"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("Searching for direct TTF links...")
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('.ttf') and 'samt' in href.lower():
                print(f"Found TTF link: {href}")
                font_res = requests.get(href, headers=headers)
                if font_res.status_code == 200:
                    with open('/home/mahdi/Desktop/n/mahdi/FrontEnd/public/fonts/samt7017.ttf', 'wb') as f:
                        f.write(font_res.content)
                    print("Successfully downloaded TTF!")
                    return True
    except Exception as e:
        print(e)
        
    # If direct TTF fails, let's search for zip files
    search_url_zip = "https://html.duckduckgo.com/html/?q=samt+7017+filetype:zip"
    try:
        print("Searching for direct ZIP links...")
        res = requests.get(search_url_zip, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('.zip') and 'samt' in href.lower():
                print(f"Found ZIP link: {href}")
                zip_res = requests.get(href, headers=headers)
                if zip_res.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(zip_res.content)) as z:
                        for info in z.infolist():
                            if info.filename.endswith('.ttf'):
                                with open('/home/mahdi/Desktop/n/mahdi/FrontEnd/public/fonts/samt7017.ttf', 'wb') as f:
                                    f.write(z.read(info.filename))
                                print("Successfully downloaded and extracted TTF from ZIP!")
                                return True
    except Exception as e:
        print(e)
        
    print("Could not find direct download link without captchas.")
    return False

download_samt_font()
