from django.core.management.base import BaseCommand
from core.scraper import scrape_jumia, scrape_ebrahims

class Command(BaseCommand):
    help = 'Re-scrape products from Jumia and Ebrahims, updating or creating as needed.'

    def handle(self, *args, **kwargs):
        queries = ["bag", "shoes", "laptop", "school"]  # Add your search terms here

        for query in queries:
            self.stdout.write(self.style.SUCCESS(f"Scraping Jumia for '{query}'..."))
            scrape_jumia(query, update_existing=True)
            self.stdout.write(self.style.SUCCESS(f"Scraping Ebrahims for '{query}'..."))
            scrape_ebrahims(query, update_existing=True)

        self.stdout.write(self.style.SUCCESS("Re-scraping and updating complete!"))