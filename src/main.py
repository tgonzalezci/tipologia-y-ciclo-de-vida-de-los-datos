"""
Museo del Prado – Artwork Scraper
=================================

This script orchestrates a two-phase web scraping pipeline against the
https://www.museodelprado.es/busqueda-obras website,

Output
------
A CSV file at the path supplied to ``Bot(output_file=...)``, containing
one row per successfully scraped artwork.

Dependencies
------------
- app.bot.Bot : Customized playwright class wrapper.

Usage
-----
Run directly::

    python main.py   # or whatever this file is named

Bot uses a context manager to handle browser lifecycle.
"""

from app.bot import Bot

with Bot(name="prado", output_file="../dataset/prado_artworks.csv") as bot:
            bot.check_user_agent()
            bot.goto(f"https://www.museodelprado.es/busqueda-obras")
            bot.wait(5)
            bot.accept_cookies()
            bot.wait(5)
            total_artworks = bot.get_num_artworks()
            bot.write_logs(f"Total artworks: {total_artworks}")
            while len(bot.get_pending_artworks_links_to_scrape()) > 0 and \
                    len(bot.get_pending_artworks_to_scrape()) < total_artworks * 0.9998:
                for link in bot.get_pending_artworks_links_to_scrape():
                    try:
                        bot.goto(f"{link}")
                        bot.click_compact_view()
                        num_artworks = bot.get_num_artworks()
                        bot.execute_infinite_scroll()
                        artwork_links = bot.extract_and_save_links()
                        bot.write_logs(f"Total links: {len(artwork_links)} of {num_artworks}")
                        if len(artwork_links) == num_artworks:
                            bot.register_scraped_artwork_link(link)
                    except Exception as e:
                        bot.write_logs(str(e))

            while len(bot.get_pending_artworks_to_scrape()) > 0 :
                for artwork_link in bot.get_pending_artworks_to_scrape():
                    try:
                        artwork = bot.get_artwork_info_from_link(artwork_link)
                        bot.write_artwork_to_csv(artwork)
                        bot.register_scraped_artwork(artwork_link)
                    except Exception as e:
                        bot.write_logs(str(e))
