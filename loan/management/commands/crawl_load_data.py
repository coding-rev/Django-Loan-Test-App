# Django imports
from django.core.management import BaseCommand

# Local imports
from loan.site_crawler import crawl_site
from loan.models import Loan

class Command(BaseCommand):
    help = "Crawl site and populate DB with data (loans data)"

    def handle(self, *args, **options):
        self.stdout.write("crawling....")
        try:
            # get crawled data
            data = crawl_site()

            loan_data_model_list = []
            for index, row in enumerate(data[1:101]):
                cleaned_row = row.text.split("\n")
                loan_data_model_list.append(
                    Loan(
                        signature_date = cleaned_row[0],
                        title = cleaned_row[1],
                        country = cleaned_row[2],
                        sector = cleaned_row[3],
                        signed_amount = cleaned_row[4]
                    )
                )
            # Finally make a builk create/save to db
            Loan.objects.bulk_create(loan_data_model_list)

            self.stdout.write(self.style.SUCCESS("Successfully crawled and uploaded records:)"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
