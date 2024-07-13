import re
import requests
from bs4 import BeautifulSoup
import os.path

trash_list = {
    "2_Anime_Saitama_OK.png",
    "2_Anime_zero_cansado.png",
    "1514-gendo-hmm.png",
    "2810-schoolgirlgod.png",
    "4352_DiCaprioLaugh.png",
    "4742-pika-luffy-face.png",
    "47910middle.jpg",
    "crying-pepe-1024x1024-1.jpg",
    "home.png",
    "laugh_naruto.png",
    "log1.png",
    "nyaKnife.png",
    "PeepoSignbruh.png",
    "SaitamaSerious.png",
    "ZeroTwo_Heart.png",
    "ZeroTwo1.png",
    "ZeroTwoFightMe.png"
}

def main():

    # title_page = 'https://www.mangaread.org/manga/golden-kamui/'
    print("enter manga chapter list on mangaread url (for example, https://www.mangaread.org/manga/golden-kamui/): ")
    title_page = input()
    manga_name = title_page.strip("/").split("/")[-1][:50]
    title_response = requests.get(title_page)
    title_soup = BeautifulSoup(title_response.text, 'html.parser')

    pages = title_soup.findAll("li", {"class":"wp-manga-chapter"})

    for p in pages:
        a = p.find('a') 
        try: 
            
            # looking for href inside anchor tag 
            if 'href' in a.attrs: 
                
                # storing the value of href in a separate  
                # variable 
                url = a.get('href') 
                download_chapter(manga_name, url)
        except:
            pass
    
    print(f"download complete. enjoy your manga in folder {manga_name}")

def download_chapter(manga_name, chapter_url:str):

    chapter_dir = os.path.join(manga_name, chapter_url.strip('/').split('/')[-1])
    print(f"downloading {chapter_dir}")
    if not os.path.exists(chapter_dir):
        os.makedirs(chapter_dir)

    response = requests.get(chapter_url)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]


    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|jpeg|png))$', url)

        if not filename:
            continue

        if str(filename.group(1)) in trash_list:
            continue

        save_path = os.path.join(chapter_dir, filename.group(1))

        if os.path.exists(save_path):
            continue

        with open(save_path, 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative 
                # if it is provide the base url which also happens 
                # to be the site variable atm. 
                url = '{}{}'.format(chapter_url, url)

            response = requests.get(url)
            f.write(response.content)

if __name__ == "__main__":
    main()