import requests
from bs4 import BeautifulSoup, ResultSet, Tag

def get_soup(url: str) -> BeautifulSoup:
    """
    :type: str
    :rtype: BeautifulSoup
    """
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    return soup

def get_next_page(soup: BeautifulSoup) -> str:
    """
    This function extracts
    the url of the next page
    if it exists.
    :type: BeautifulSoup
    :rtype: str
    """
    page = soup.find_all('a', {'rel': 'next'})
    if page:
        return page[0].get('href')
    return None

def pcs(soup: BeautifulSoup) -> list[dict]:
    """
    :type: BeautifulSoup
    :rtype: dict
    """
    pcs_soups = get_pcs_soups(soup)
    pcs_informations_keys = ['id', 
                             'name', 
                             'description', 
                             'store-availability-list', 
                             'brand', 
                             'price', 
                             'in-stock',
                             'url'
                            ]
    pcs_informations = []
    for pc_soup in pcs_soups:
        pcs_informations.append(
            dict(
                zip(
                    pcs_informations_keys,
                    get_pc_informations(pc_soup)
                )
            )
        )
    return pcs_informations

def get_pcs_soups(soup: BeautifulSoup) -> ResultSet:
    """
    :type: BeautifulSoup
    :rtype: ResultSet
    """
    return soup.find_all('div', {'class': 'item-product'})

def get_pc_informations(pc_soup: Tag) -> list[str]:
    """
    :type: Tag
    :rtype: list[str]
    """
    pcs_informations = []
    pcs_informations.append(get_pc_id(pc_soup))
    pcs_informations.append(get_pc_name(pc_soup))
    pcs_informations.append(get_pc_description(pc_soup))
    pcs_informations.append(get_store_availability_list(pc_soup))
    pcs_informations.append(get_brand(pc_soup))
    pcs_informations.append(get_price(pc_soup))
    pcs_informations.append(get_in_stock(pc_soup))
    pcs_informations.append(get_url(pc_soup))
    return pcs_informations

def get_pc_id(pc_soup: Tag) -> str:
    """
    :type: Tag
    :rtype: list[str]
    """
    id_soup = pc_soup.find('span', {'class': 'product-reference'})
    return id_soup.text

def get_pc_name(pc_soup: Tag) -> str:
    """
    :type: Tag
    :rtype: str
    """
    name_soup = pc_soup.find('h2', {'class': 'h3 product-title'})
    return name_soup.text

def get_pc_description(pc_soup: Tag) -> str:
    """
    :type: Tag
    :rtype: str
    """
    description_soup = pc_soup.find('div', {'itemprop': 'description'})
    description_text = "".join(s for s in description_soup.stripped_strings)
    return description_text

def get_store_availability_list(pc_soup: Tag) -> list[str]:
    """
    :type: Tag
    :rtype: list[str]
    """
    stores_soup = pc_soup.find_all('div', {'class': 'store-availability-list'})
    store_availability = [store_soup.get('title')
                          for store_soup in stores_soup
                          if store_soup.parent.parent.get('id') == 'productList-availability-store' 
                        ]
    return store_availability

def get_brand(pc_soup: Tag) -> str:
    """
    :type: Tag
    :rtype: str
    """
    img_soup = pc_soup.find('img', {'class': 'img img-thumbnail manufacturer-logo'})
    return img_soup.get('alt')

def get_price(pc_soup: Tag) -> str:
    """
    :type: Tag
    :rtype: str
    """
    price_soup = pc_soup.find('span', {'class': 'price'})
    return price_soup.text

def get_in_stock(pc_soup: Tag) -> str:
    """
    :type: Tag
    :rtype: str
    """
    in_stock_soup = pc_soup.find('div', {'id': 'stock_availability'})
    return in_stock_soup.text

def get_url(pc_soup: Tag) -> str:
    """
    :type: Tag
    :rtype: str
    """
    url_soup = pc_soup.find('h2', {'class': 'h3 product-title'})
    return url_soup.find('a').get('href')

def main():
    """
    This function find all the pcs
    available for sale and their 
    informations in Tunisianet
    website.
    """
    url = "https://www.tunisianet.com.tn/301-pc-portable-tunisie?order=product.price.asc"
    pcs_informations = []
    while url:
        soup = get_soup(url)
        pcs_informations.extend(pcs(soup))
        url = get_next_page(soup)
        print(url)
    print(pcs_informations[0])
    print(pcs_informations[1])
    print(pcs_informations[2])
    print(pcs_informations[3])
    print(pcs_informations[4])
    print(pcs_informations[10])
    print(pcs_informations[822])
    print(len(pcs_informations))
if __name__ == '__main__':
    main()
