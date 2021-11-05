from bs4 import BeautifulSoup
import requests


from .dbaseql import *

class TableBuilder:

    @staticmethod
    def build_table(url):
        html_doc = requests.get(url)
        html_content = BeautifulSoup(html_doc.content, 'html.parser')
        
        raw = html_content.find('thead')
        data = raw.find_all('tr')
        headers = data[0]
        rows = data[1:]

        table = Table([header.text for header in headers.find_all("th")])

        convert = lambda txt: float(txt) if txt.isnumeric() else txt

        for cols in rows:
            col = cols.find_all("td")
            table.insert([convert(txt.text) for txt in cols])

        return table