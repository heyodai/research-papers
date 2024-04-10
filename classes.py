import re
import datetime
from bs4 import BeautifulSoup

class Paper:
    def __init__(self, article_id, soup, notes=None):
        self.article_id = article_id
        self.soup = soup
        self.notes = notes

        self.title = self.get_title()
        self.abstract = self.get_abstract()
        self.date = self.get_date()

        self.arxiv_url = self.get_arxiv_url()
        self.em_url = self.get_em_url()

    def get_title(self):
        pass

    def get_abstract(self):
        pass

    def get_date(self):
        pass

    def get_arxiv_url(self):
        return f"https://arxiv.org/abs/{self.article_id}"

    def get_em_url(self):
        return f"https://www.emergentmind.com/papers/{self.article_id}"
    
class ArxivPaper(Paper):
    def get_title(self):
        title = self.soup.find("h1", class_="title mathjax").text.strip()
        title = title.replace("Title:", "").strip()
        return title

    def get_abstract(self):
        abstract = self.soup.find("blockquote").text.strip()
        abstract = abstract.replace("Abstract:", "").strip()
        return abstract

    def get_date(self):
        dateline = self.soup.find("div", class_="dateline")
        date = dateline.text.split("Submitted on ")[1]

        date = date.split(" ")
        return f"{date[2]}-{date[1]}-{date[0]}"
    
class EmPaper(Paper):
    def get_title(self) -> str:
        return self.soup.find("h1").text.strip()

    def get_abstract(self):
        # To get the abstract, find the H3 tag with the text "Abstract"
        # The next sibling is the actual abstract
        abstract = None
        for h3 in self.soup.find_all("h3"):
            if h3.text.strip() == "Abstract":
                abstract = h3.find_next_sibling("div").text.strip()
                return abstract

    def get_date(self):
        # For the date, we can look for the text "Published" and extract the date
        date = None
        for div in self.soup.find_all("div"):
            if "Published" in div.text:
                match = re.search(r"Published (\w+\s+\d{1,2}, \d{4})", div.text)
                if match:
                    date = match.group(1)
                break

        # This comes out like 'Mar 21, 2024', so we can parse it with datetime
        try:
            date = datetime.datetime.strptime(date, "%b %d, %Y").date()
            date = date.strftime("%Y-%m-%d")
        except:
            print("Could not parse date")

        return date