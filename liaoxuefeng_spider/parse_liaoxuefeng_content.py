import urllib.request
import urllib.error

from bs4 import BeautifulSoup
from database.LiaoXueFengContentManager import LiaoXueFengContentManager
from database.LiaoXueFengDirectorManager import LiaoXueFengDirectorManager

user_agent = r"Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D)" \
             r" AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36"

base_url = 'http://www.liaoxuefeng.com/wiki/'
python_url = base_url + '0014316089557264a6b348958f449949df42a6d3a2e542c000' \
                        '/0014316724772904521142196b74a3f8abf93d8e97c6ee6000'

def get_content_from_url(key1, key2):
    url = base_url + key1
    if key1 != key2:
        url += "/" + key2
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
    response = None
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf-8"))

    if response:
        the_page = response.read().decode("UTF-8").replace("\n", "")
        soup = BeautifulSoup(the_page, "html.parser", from_encoding="utf-8")
        content_div = soup.find('div', {"class": "x-content"})
        wiki_content_div = content_div.find('div', {"class": "x-wiki-content"})
        for img in wiki_content_div.find_all('img'):
            if not img.attrs['src'].startswith("http"):
                img.attrs['src'] = 'http://www.liaoxuefeng.com' + img.attrs['src']
        content = str(content_div.h4)
        content += str(wiki_content_div)
        return content
    return None


sql_manager = LiaoXueFengDirectorManager()
sql_manager.create_connection()
directors = sql_manager.fetch_from_director()
sql_manager.close_conn()

sql_manager = LiaoXueFengContentManager()
sql_manager.create_connection()
for item in directors:
    print(item[1], item[2])
    ret_content = get_content_from_url(item[1], item[2])
    if ret_content:
        sql_manager.insert_into_content(*[item[1], item[2], ret_content])

sql_manager.close_conn()

# get_content_from_url('0014316089557264a6b348958f449949df42a6d3a2e542c000', '001431658624177ea4f8fcb06bc4d0e8aab2fd7aa65dd95000')
