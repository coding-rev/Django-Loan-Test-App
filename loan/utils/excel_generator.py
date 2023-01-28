import io
import xlsxwriter
from loan.models.loan_model import Loan
from django.db.models import Sum, Count


def generate_excel():
    output = io.BytesIO()
    # Create a new Excel file
    # workbook = xlsxwriter.Workbook('loans_app_excel.xlsx')
    workbook = xlsxwriter.Workbook(output)
    
    # Add a "Data sheet"
    data_sheet = workbook.add_worksheet("Data sheet")

    # Add a "Chart sheet"
    chart_sheet = workbook.add_worksheet("Chart sheet")

    # Add a "Aggregated hidden sheet"
    agg_sheet = workbook.add_worksheet(name="aggregation")

    # Add data to the "Data sheet"

    # Get data from db
    data = list(
        Loan.objects.all().values_list(
            "signature_date", "title", "country__name", "sector__name", "signed_amount", "currency__symbol"
        )
    )
    headers = ["Signature Date", "Title", "Country", "Sector", "Signed Amount"]

    # Write the headers to the first row of the sheet
    for col, header in enumerate(headers):
        data_sheet.write(0, col, header)

    # Write the data to the sheet
    for row, loan in enumerate(data, start=1):
        for col, header in enumerate(headers):
            # Concatenating signed amount symbol to the amount
            if col == len(headers)-1:
                data_sheet.write(row, col, str(loan[len(loan)-1])+str(loan[col])) 
            # other fields
            else:
                data_sheet.write(row, col, str(loan[col]))

    # Apply styling to the headers
    header_format = workbook.add_format({"bold": True, "align": "center"})
    for col in range(len(headers)):
        data_sheet.set_column(col, col, 20)
        data_sheet.write(0, col, headers[col], header_format)

    # Creating CHART SHEET DATA
    loan_dataset = Loan.objects.select_related("country", "sector", "currency").all()

    loan_by_year = loan_dataset.values("signature_date__year").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("id"),
    )

    loan_by_country = loan_dataset.values("country__name").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("id"),
    )

    loan_by_sector = loan_dataset.values("sector__name").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("id"),
    )
    # Add drop down
    chart_sheet.data_validation(
        "C2",
        {
            "validate": "list",
            "source": ["By Country", "By Year", "By Sector"],
        },
    )
    # Setting default value to the cell
    chart_sheet.write("C2", "By Country")

    chart = workbook.add_chart({"type": "column"})
    chart2 = workbook.add_chart({"type": "column"})

    # Creating aggregated sheet
    agg_by_year = [
        [data["signature_date__year"], data["total_amount"], data["count"]]
        for data in loan_by_year
    ]
    agg_by_country = [
        [data["country__name"], data["total_amount"], data["count"]]
        for data in loan_by_country
    ]

    agg_by_sector = [
        [data["sector__name"], data["total_amount"], data["count"]]
        for data in loan_by_sector
    ]

    agg_sheet.add_table(
        f"B1:D{1+len(agg_by_year)}",
        {
            "data": agg_by_year,
            "name": "DataAggregationbyyear",
            "total_row": False,
            "autofilter": False,
            "columns": [
                {"header": "Year"},
                {"header": "Loan Amount"},
                {"header": "Quantity"},
            ],
        },
    )

    agg_sheet.add_table(
        f"F1:H{1+len(agg_by_country)}",
        {
            "data": agg_by_country,
            "name": "DataAggregationbycountry",
            "autofilter": False,
            "columns": [
                {"header": "Country"},
                {"header": "Loan Amount"},
                {"header": "Quantity"},
            ],
        },
    )

    agg_sheet.add_table(
        f"J1:L{1+len(agg_by_sector)}",
        {
            "data": agg_by_sector,
            "name": "DataAggregationbySector",
            "total_row": False,
            "autofilter": False,
            "columns": [
                {"header": "Country"},
                {"header": "Loan Amount"},
                {"header": "Quantity"},
            ],
        },
    )

    # Creating dynamic data (excel formula) to be used for the chart series as defined names
    chart_y_series = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$G$2:$G${1+len(loan_by_country)},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$C$2:$C${1+len(loan_by_year)},\
                aggregation!$K$2:$K${1+len(loan_by_sector)}\
            )\
        )'
    chart_x_label = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$F$2:$F${1+len(loan_by_country)},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$B$2:$B${1+len(loan_by_year)},\
                aggregation!$J$2:$J${1+len(loan_by_sector)}\
            )\
        )'

    chart2_y_series = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$H$2:$H${1+len(loan_by_country)},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$D$2:$D${1+len(loan_by_year)},\
                aggregation!$L$2:$L${1+len(loan_by_sector)}\
            )\
        )'

    # defining names that can be used to represent excel functions and formulas: returns range of cells
    workbook.define_name("chart_series", chart_y_series)
    workbook.define_name("chart_labels", chart_x_label)
    workbook.define_name("chart2_series", chart2_y_series)
    workbook.define_name("chart2_labels", chart_x_label)

    # Adding chart series (y-axis values as 'values' and x-axis values as 'categories')
    chart.add_series(
        {
            "values": "=aggregation!chart_series",
            "categories": "=aggregation!chart_labels"
        }
    )

    chart2.add_series(
        {
            "values": "=aggregation!chart2_series",
            "categories": "=aggregation!chart2_labels"
        }
    )

    # setting addition info
    chart.set_style(25)
    chart.set_size({"width": 600})
    chart.set_title({"name": "Loan Amount"})
    chart.set_style(25)
    chart2.set_size({"width": 600})
    chart2.set_title({"name": "Loan Quantity"})

    # Inserting the charts into the chart sheet
    chart_sheet.insert_chart("B4", chart)
    chart_sheet.insert_chart("B20", chart2)

    # auto fitting the cells to the width of the contents
    chart_sheet.autofit()
    data_sheet.autofit()

    # Hide the sheet
    agg_sheet.hide()

    # Save the Excel file
    workbook.close()

    output.seek(0)

    return output
