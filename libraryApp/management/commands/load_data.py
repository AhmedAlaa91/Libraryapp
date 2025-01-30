import json
from libraryApp.models import Author , Book
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Insert dummy data into the database'

    
    def handle(self, *args, **kwargs):

        with open('fixed_books.json', 'r', encoding='utf-8') as file:

            data = json.load(file)  # Load the entire JSON array


        for author_data in data:  # Iterate over each author in the array

            author, created = Author.objects.get_or_create(name = author_data.get("name") , biography= author_data.get("about"))
            title = author_data.get("name")
            rating=author_data.get("average_rating")

            #for book_id in author_data["book_ids"]:  # Iterate over each book ID for the author

            Book.objects.get_or_create(title=f"Book {title}", author=author , ratings=rating , genre=str(author_data.get("about"))[:90])

            print(f"Imported author {author.name} with books")

