from os import mkdir
from collections import deque
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


class Browser:
    def __init__(self, save_dir):
        self.save_dir = save_dir
        self.saved_page = {}
        self.page_now = ""
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"}
        try:
            mkdir(self.save_dir)
        except FileExistsError:
            # print("The dir already existed!")
            pass

    @staticmethod
    def __open_file(file_path: str):
        with open(file_path, 'r') as f:
            print(f.read())
        f.close()

    @staticmethod
    def __save_page(file_path: str, page_content: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            print(page_content, file=f)
            f.close()

    @staticmethod
    def __process_page(content: bytes) -> str:
        page = ""
        soup = BeautifulSoup(content, 'html.parser')
        body = soup.find('body')  # get body by tag <body></body>
        descendants = body.descendants
        for descendant in descendants:
            if descendant.name in ["p", 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']:
                try:
                    if descendant.name == 'a':
                        page += Fore.BLUE + descendant.get_text().strip()
                    else:
                        page += Style.RESET_ALL + descendant.get_text().strip()  # try to get descendants content.

                except:
                    pass
            else:
                pass
        return page

    def run(self):
        open_stack = deque()
        while True:
            web_url = input().strip()
            if web_url.find(".") == -1:
                if web_url == "exit":
                    break
                elif web_url == "back":
                    if len(open_stack) > 0:
                        print(open_stack.pop())
                    else:
                        print("No open page!")
                    continue
                elif web_url in self.saved_page.keys():
                    self.__open_file(self.saved_page[web_url])
                else:
                    pass
            else:
                if web_url.find("https") == -1 or web_url.find("http") == -1:
                    web_url = "https://" + web_url
                r = requests.get(web_url, headers=self.header)
                if not r.status_code:
                    print("GET ERROR")
                    continue
                web_page = self.__process_page(r.content)
                print(web_page)
                if self.page_now != "":
                    open_stack.append(self.page_now)
                self.page_now = web_page
                file_name = web_url[:web_url.rfind('.')]
                if file_name.find('https') != -1:
                    file_name = file_name[7:]
                elif file_name.find('http') != -1:
                    file_name = file_name[6:]
                file_path = self.save_dir + "\\" + file_name
                self.__save_page(file_path, web_page)
                self.saved_page[file_name] = file_path


if __name__ == '__main__':
    new_browser = Browser(sys.argv[1])
    new_browser.run()
    sys.exit()



