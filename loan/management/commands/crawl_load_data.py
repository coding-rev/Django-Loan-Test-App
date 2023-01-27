# Python/django imports
from django.core.management import BaseCommand
from datetime import datetime

# Local imports
from loan.utils.site_crawler import crawl_site
from loan.models.loan_model import Loan
from loan.models.country_model import Country
from loan.models.sector_model import Sector


class Command(BaseCommand):
    help = "Crawl site and populate DB with data (loans data)"

    def handle(self, *args, **options):
        self.stdout.write("crawling....")
        try:
            # Get crawled data
            data = crawl_site()

            # List definition for loan model instances
            loan_data_model_list = []

            for index, row in enumerate(data[1:101]):
                cleaned_row = row.text.split("\n")

                # Get or create country
                row_country = Country.objects.get_or_create(name=cleaned_row[2])
                # Get or create sector
                row_sector = Sector.objects.get_or_create(name=cleaned_row[3])
                # Sanitize row date to python date format
                row_signature_date = datetime.strptime(cleaned_row[0], "%d %B %Y")

                # Add current row data to loan model
                loan_data_model_list.append(
                    Loan(
                        signature_date=row_signature_date,
                        title=cleaned_row[1],
                        country=row_country,
                        sector=row_sector,
                        signed_amount=cleaned_row[4],
                    )
                )
            # Finally make a loan bulk create
            Loan.objects.bulk_create(loan_data_model_list)

            self.stdout.write(
                self.style.SUCCESS("Successfully crawled and uploaded records:)")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
