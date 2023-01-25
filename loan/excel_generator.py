import io
import xlsxwriter
from .models import Loan

def generate_excel():
    output = io.BytesIO()
    # Create a new Excel file
    # workbook = xlsxwriter.Workbook('loans_app_excel.xlsx')
    workbook = xlsxwriter.Workbook(output)

    # Add a "Data sheet"
    data_sheet = workbook.add_worksheet("Data sheet")

    # Add a "Chart sheet"
    chart_sheet = workbook.add_worksheet("Chart sheet")

    # ==============================
    # Add data to the "Data sheet"
    # ==============================
    # Get data from db
    data = list(Loan.objects.all().values_list('signature_date', 'title', 'country', 'sector', 'signed_amount'))
    headers = ['signature_date', 'title', 'country', 'sector', 'signed_amount']
    
    # Write the headers to the first row of the sheet
    for col, header in enumerate(headers):
        data_sheet.write(0, col, header)

    # Write the data to the sheet
    for row, loan in enumerate(data, start=1):
        for col, header in enumerate(headers):
            data_sheet.write(row, col, loan[col])

    # Apply styling to the headers
    header_format = workbook.add_format({'bold': True, 'align': 'center'})
    for col in range(len(headers)):
        data_sheet.set_column(col, col, 20)
        data_sheet.write(0, col, headers[col], header_format)


    # ===================================
    # Create a chart in the "Chart sheet"
    # ===================================
    chart = workbook.add_chart({'type': 'column'})

    # Add data to the chart
    # Assume the data is grouped by year, sector, and country
    chart.add_series({
         'name':       '=Data sheet!$B$1',
         'categories': '=Data sheet!$A$2:$A$100',
         'values':     '=Data sheet!$D$2:$D$100',
    })

    # Add a title to the chart
    chart.set_title ({'name': 'Loan Amount by Year, Sector, and Country'})

    # Add axis labels
    chart.set_x_axis({'name': 'Year'})
    chart.set_y_axis({'name': 'Loan Amount'})

    # Insert the chart into the "Chart sheet"
    chart_sheet.insert_chart('A1', chart)

    # Add a dropdown menu to the "Chart sheet" to allow user to select chart type
    chart_sheet.data_validation('A2', {'validate': 'list',
                                    'source': ['Year', 'Sector', 'Country']})

    
    # Save the Excel file
    workbook.close()

    output.seek(0)

    return output
