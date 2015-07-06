import urllib.request
import urllib.error

from bs4 import BeautifulSoup
from database import LiaoXueFengDirectorManager

user_agent = r"Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D)" \
             r" AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36"

python_url_2_7 = (14, 'http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000')
python_url = (9, 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000')
git_url = (11, 'http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000')
js_url = (10, 'http://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000')


def get_directory(*url):
    req = urllib.request.Request(url[1], headers={'User-Agent': user_agent})
    response = None
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))

    if response:
        # the_page = response.read().decode("UTF-8")
        the_page = response.read()
        soup = BeautifulSoup(the_page, "html.parser", from_encoding="utf-8")
        parent_ul = soup.find('ul', {"class": "uk-nav uk-nav-side", "style": "margin-right:-15px;"})
        all_li = parent_ul.find_all('li')

        root_id = None
        root_title = None

        item_map = []  # (id,title)
        current_item_id = None
        current_child_item_id = None

        child_item_map = {}  # pid:(id,title)
        sub_child_item_map = {}  # pid:(id,title)

        for li in all_li:
            style = li.attrs.get('style')
            if style is None:
                root_id = li.attrs['id']
                root_title = str(li.a.string)
            elif style == "margin-left:2em;":
                if child_item_map.get(current_item_id) is None:
                    child_item_map[current_item_id] = []
                current_id = li.attrs['id']
                current_title = str(li.a.string)
                child_item_map[current_item_id].append((current_id, current_title))
                current_child_item_id = current_id
            elif style == "margin-left:3em;":
                if sub_child_item_map.get(current_child_item_id) is None:
                    sub_child_item_map[current_child_item_id] = []
                current_id = li.attrs['id']
                current_title = str(li.a.string)
                sub_child_item_map[current_child_item_id].append((current_id, current_title))
            else:
                current_id = li.attrs['id']
                current_title = str(li.a.string)
                item_map.append((current_id, current_title))
                current_item_id = current_id

        # print(root_id + " " + root_title)
        # print(item_map)
        # print(child_item_map)

        # 插入数据库
        sql_manager = LiaoXueFengDirectorManager.LiaoXueFengDirectorManager()
        sql_manager.create_connection()
        sql_manager.create_director()

        insert_values = [[url[0], root_id, root_id, 0, root_title]]

        for parent_key, title in item_map:
            insert_values.append([url[0], root_id, parent_key, 0, title])
            child_item_array = child_item_map.get(parent_key)
            if child_item_array is not None:
                for child_key, child_title in child_item_array:
                    insert_values.append([url[0], root_id, child_key, 1, child_title])
                    sub_child_item_array = sub_child_item_map.get(child_key)
                    if sub_child_item_array is not None:
                        for sub_child_key, sub_child_title in sub_child_item_array:
                            insert_values.append([url[0], root_id, sub_child_key, 2, sub_child_title])

        sql_manager.insert_into_director(*insert_values)
        print(sql_manager.fetch_from_director())
        sql_manager.close_conn()


if __name__ == "__main__":
    get_directory(*python_url)
    get_directory(*python_url_2_7)
    get_directory(*git_url)
    get_directory(*js_url)
