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

    # Chart Sheet Creation
    # Fetch loan data for aggregation
    loans = (
        Loan.objects.all()
        .select_related("country", "sector")
        
    )

    agg_by_year = loans.values("signature_date__year").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("id"),
    )

    agg_by_country = loans.values("country__name").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("id"),
    )

    agg_by_sector = loans.values("sector__name").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("id"),
    )
    # Dropdown list
    chart_sheet.data_validation(
        "A2",
        {
            "validate": "list",
            "source": ["Agg By Country", "Agg By Year", "Agg By Sector"],
        },
    )
    # Setting default value to the cell
    chart_sheet.write("A2", "Agg By Country")

    # Adding chart objects
    chart = workbook.add_chart({"type": "column"})
    chart_2 = workbook.add_chart({"type": "column"})

    # Preparing data for hidden sheet table to be used for the chart series
    agg_by_year = [
        [data["signature_date__year"], data["total_amount"], data["count"]]
        for data in agg_by_year
    ]
    agg_by_country = [
        [data["country__name"], data["total_amount"], data["count"]]
        for data in agg_by_country
    ]

    agg_by_sector = [
        [data["sector__name"], data["total_amount"], data["count"]]
        for data in agg_by_sector
    ]
    # Add aggregation sheet
    agg_sheet = workbook.add_worksheet(name="aggregation")
    agg_sheet.add_table(
        f"A1:D{len(agg_by_year)+1}",
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
        f"G1:I{len(agg_by_country)+1}",
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
        f"K1:M{len(agg_by_sector)+1}",
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

    # Creating/generating dynamic data for chart
    chart_y_series = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$G$2:$G${len(agg_by_country)+1},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$C$2:$C${len(agg_by_year)+1},\
                aggregation!$K$2:$K${1+len(agg_by_sector)}\
            )\
        )'
    chart_x_label = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$F$2:$F${len(agg_by_country)+1},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$B$2:$B${len(agg_by_year)+1},\
                aggregation!$J$2:$J${len(agg_by_sector)+1}\
            )\
        )'

    chart_2_y_series = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$H$2:$H${len(agg_by_country)+1},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$D$2:$D${len(agg_by_year)+1},\
                aggregation!$L$2:$L${len(agg_by_sector)+1}\
            )\
        )'

    
    workbook.define_name("chart_series", chart_y_series)
    workbook.define_name("chart_labels", chart_x_label)
    workbook.define_name("chart_2_series", chart_2_y_series)
    workbook.define_name("chart_2_labels", chart_x_label)

    # Adding chart series
    chart.add_series(
        {
            "values": "=aggregation!chart_series",
            "categories": "=aggregation!chart_labels",
        }
    )
    # Adding chart 2 series
    chart_2.add_series(
        {
            "values": "=aggregation!chart_2_series",
            "categories": "=aggregation!chart_2_labels",
        }
    )

    # Adding style and other settings
    chart.set_size({"width": 600})
    chart.set_style(25)
    chart.set_title({"name": "Loan Amount"})
    
    chart_2.set_size({"width": 600})
    chart_2.set_style(25)
    chart_2.set_title({"name": "Loan Quantity"})
    

    # Insert charts
    chart_sheet.insert_chart("A4", chart)
    chart_sheet.insert_chart("A20", chart_2)

    # making sheets fit 
    chart_sheet.autofit()
    data_sheet.autofit()

    # Hidding the agg_sheet on default
    agg_sheet.hide()

    # Save the Excel file
    workbook.close()

    output.seek(0)

    return output
