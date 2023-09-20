import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main():
    base_site = "https://en.wikipedia.org/wiki/Music"
    response = requests.get(base_site)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    div_notes =soup.find_all('div', {'role': 'note'})
    div_links = []
    for div in div_notes:
        anchors = div.find_all('a')
        div_links.extend(anchors)
    
    note_urls = [urljoin(base_site, l.get('href')) for l in div_links]
    par_text = []

    for url in note_urls:
        note_resp = requests.get(url)
        if note_resp.status_code != 200:
            continue
        note_html = note_resp.content
        note_soup = BeautifulSoup(note_html, 'lxml')
        note_pars = note_soup.find_all('p')
        text = [p.text for p in note_pars]
        par_text.append(text)

    page_text = ["".join(text) for text in par_text]
    url_to_text = dict(zip(note_urls, page_text))
    print(url_to_text['https://en.wikipedia.org/wiki/Music_theory'])

if __name__ == "__main__":
    main()