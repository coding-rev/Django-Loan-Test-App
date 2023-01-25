# Django imports
from django.core.management import BaseCommand

# Local imports
from crawler.excel_generator import generate_excel

class Command(BaseCommand):
    help = "Generate excel with Data Sheet and Chart Sheet"

    def handle(self, *args, **options):
        self.stdout.write("generating....")
        try:
            generate_excel()
            self.stdout.write(self.style.SUCCESS("Done :)"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
