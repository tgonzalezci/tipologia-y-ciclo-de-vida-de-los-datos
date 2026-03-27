import json
import random
import time
import os
import pandas as pd
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page
from playwright_stealth import Stealth
from log import Log
from bs4 import BeautifulSoup
import re
from pathlib import Path

class Bot:
    ARTWORK_FIELDS = [
        "Número de catálogo",
        "Autor",
        "Autores",
        "Título",
        "Fecha",
        "Técnica",
        "Soporte",
        "Dimensión",
        "Serie",
        "Procedencia",
    ]

    ARTWORK_LINKS = [
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_20",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_6",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_155",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_154",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_25",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_3",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_8",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_221",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_230",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_179",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_31",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_180",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=asc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_9",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_20",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_6",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_155",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_154",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_25",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_3",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_8",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_221",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_230",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_179",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_31",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_180",
        f"https://www.museodelprado.es/busqueda-obras?searchObras=&ordenarPor=ecidoc:p62_E52_p79_has_time-span_beginning,ecidoc:p62_E52_p80_has_time-span_end,gnoss:hasfechapublicacion&orden=desc&cidoc:p2_has_type@@@pm:objectTypeNode=http://museodelprado.es/items/objecttype_9",
    ]
    ARTWORK_LINKS_FILE = "artwork_links.txt"
    ARTWORK_FILE_REGISTER = "scraped_artworks_register.txt"
    ARTWORK_LINKS_FILE_REGISTER = "scraped_artwork_links_register.txt"

    def __init__(self, name: str = "prado", output_file: str = "prado_artworks.csv", wait_default: int = 3):
        self.name: str = name
        self.wait_default: int = wait_default
        self.dataset_dir = Path("dataset")
        self.dataset_dir.mkdir(exist_ok=True)
        self.output_file = str(self.dataset_dir / output_file)
        self.ARTWORK_LINKS_FILE = str(self.dataset_dir / self.ARTWORK_LINKS_FILE)
        self.ARTWORK_FILE_REGISTER = str(self.dataset_dir / self.ARTWORK_FILE_REGISTER)
        self.ARTWORK_LINKS_FILE_REGISTER = str(self.dataset_dir / self.ARTWORK_LINKS_FILE_REGISTER)
        self._log: Log = Log(name)
        self._create_files()
        self._launch_browser()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

    def write_logs(self, message: str, level: str = None):
        self._log.write(message, level)

    def close(self):
        if self.browser:
            self.write_logs("Stopping bot")
            self.browser.close()
        if self.playwright:
            self.write_logs("Closing bot")
            self.playwright.stop()

    def _create_files(self):
        filepath = Path(self.ARTWORK_LINKS_FILE)
        filepath.touch(exist_ok=True)
        filepath = Path(self.ARTWORK_FILE_REGISTER)
        filepath.touch(exist_ok=True)
        filepath = Path(self.ARTWORK_LINKS_FILE_REGISTER)
        filepath.touch(exist_ok=True)

    def _launch_browser(self):
        self.write_logs("Starting bot, using chromium browser")
        try:
            self.playwright: Playwright = sync_playwright().start()
            self.browser: Browser = self.playwright.chromium.launch(headless=False)
            self.context: BrowserContext = self.browser.new_context(viewport={"width": 3840, "height": 2160},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/122.0.0.0 Safari/537.36")
            self.page: Page = self.context.new_page()
            Stealth().apply_stealth_sync(self.page)
        except Exception as e:
            self.write_logs(f"Failed to launch chromium browser: {e}", "error")

    def wait(self,start: float = None, end: float = None) -> None:
        if end is None:
            if start is None:
                start = self.wait_default
            time.sleep(start)
        else:
            if start is None:
                start = 0
            time.sleep(random.uniform(start, end))

    def goto(self, url: str) -> str | None:
        try:
            self.write_logs(json.dumps({'navigating to':url}))
            self.page.goto(url)
            return self.page.content()
        except Exception as e:
            self.write_logs(f"Error opening url: {e}", "error")
            return None

    def accept_cookies(self):
        self.write_logs("Accepting cookies")
        self.find_element_by_id_and_click("onetrust-accept-btn-handler")

    def check_user_agent(self) -> str:
        user_agent = self.page.evaluate("navigator.userAgent")
        self.write_logs(f"Current user agent: {user_agent}")
        return user_agent

    def find_element_by_id_and_click(self, html_id: str) -> None:
        try:
            self.write_logs(json.dumps({'find_element_by_id_and_click':html_id}))
            self.page.locator(f"#{html_id}").click()
        except Exception as e:
            self.write_logs(f"Error clicking page: {e}", "error")

    def find_element_by_css_class_and_click(self, css_class: str) -> None:
        try:
            self.write_logs(json.dumps({'find_element_by_class_and_click': css_class}))
            self.page.locator(f".{css_class}").click()
        except Exception as e:
            self.write_logs(f"Error clicking page: {e}", "error")

    def click_compact_view(self) -> None:
        self.find_element_by_css_class_and_click("compacto")

    def get_text_by_selector(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def get_num_artworks(self) -> int:
        articles = self.get_text_by_selector("#filter1 > ul > li.label-tab.selected > a > span")
        return int(re.sub(r"[^\d]", "", articles))

    def execute_infinite_scroll(self):
        self.write_logs("Executing infinite scroll using JS")
        while True:
            scroll_step = random.randint(1800, 2000)
            pos_antes = self.page.evaluate("window.scrollY")
            self.page.evaluate(f"window.scrollBy(0, {scroll_step})")
            self.wait(5,6)
            pos_despues = self.page.evaluate("window.scrollY")
            self.write_logs(f"Loaded {self.page.locator('article.card-piece-gallery').count()} elements on the web")
            if pos_despues == pos_antes:
                self.write_logs("Reached end of page.")
                break

    def extract_and_save_links(self) -> list:
        self.write_logs(f"Extracting and saving media links to {self.ARTWORK_LINKS_FILE}")
        html = self.page.content()
        soup = BeautifulSoup(html, "html.parser")
        links = [
            a["href"]
            for a in soup.select("article.card-piece-gallery a.media")
            if a.get("href")
        ]
        with open(self.ARTWORK_LINKS_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join(links))
            f.write("\n")
        return links

    def get_artwork_description(self, soup) -> str:
        self.write_logs("getting artwork description")
        div = soup.find("div", class_="summary")
        if div:
            for span in div.find_all("span", class_="read-more"):
                span.decompose()
            return div.get_text(" ", strip=True)
        div = soup.find("div", attrs={"property": "cidoc:p3_has_note"})
        if div:
            return div.get_text(" ", strip=True)
        return ""

    def get_artwork_info_from_link(self, link:str) -> dict:
        self.write_logs(f"navigating to link {link}")
        self.goto(link)
        self.wait(1,1.8)
        self.write_logs("fetching artwork info")
        soup = BeautifulSoup(self.page.content(), "html.parser")
        fields_found = set()
        tech_specs = {field: "" for field in self.ARTWORK_FIELDS}
        for dt in soup.find_all("dt"):
            key = dt.get_text(strip=True)
            if key in self.ARTWORK_FIELDS and key not in fields_found:
                dd = dt.find_next_sibling("dd")
                if dd:
                    tech_specs[key] = dd.get_text(" ", strip=True)
                    fields_found.add(key)
        tech_specs.update({"descripcion": f"{self.get_artwork_description(soup)}"})
        tech_specs.update({"url":f"{link}"})
        return tech_specs

    def write_artwork_to_csv(self, artwork: dict) -> None:
        self.write_logs(f"Writing artwork to csv")
        header = False if os.path.exists(self.output_file) else True
        df = pd.DataFrame.from_dict([artwork])
        df.to_csv(self.output_file, index=False, encoding="utf-8", header=header, mode="w" if header else "a")

    def register_scraped_artwork(self, link: str) -> None:
        self.write_logs("Registering scraped artwork")
        with open(self.ARTWORK_FILE_REGISTER, "a", encoding="utf-8") as f:
            f.write(link + "\n")

    def register_scraped_artwork_link(self, link: str) -> None:
        self.write_logs("Registering scraped artwork link")
        with open(self.ARTWORK_LINKS_FILE_REGISTER, "a", encoding="utf-8") as f:
            f.write(link + "\n")

    def get_pending_artworks_to_scrape(self) -> list[str]:
        self.write_logs("Getting pending artwork")
        with open(self.ARTWORK_FILE_REGISTER, "r", encoding="utf-8") as f:
           scraped = [line.strip() for line in f.readlines()]
        with open(self.ARTWORK_LINKS_FILE, "r", encoding="utf-8") as f:
            total = [line.strip() for line in f.readlines()]
        return list(set(total) - set(scraped))

    def get_pending_artworks_links_to_scrape(self) -> list[str]:
        self.write_logs("Getting pending artwork links")
        with open(self.ARTWORK_LINKS_FILE_REGISTER, "r", encoding="utf-8") as f:
            scraped = [line.strip() for line in f.readlines()]
        return list(set(self.ARTWORK_LINKS) - set(scraped))