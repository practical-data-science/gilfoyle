# Gilfoyle
Gilfoyle is a report generation tool for Python which makes it quick and easy to create stylish looking reports or presentations using data. 

#### Installation
You can install Gilfoyle by entering `pip3 install gilfoyle` in your terminal. 

#### Usage
Gilfoyle can be used within a regular Python script or from inside a Jupyter notebook. 

```python
# Load packages
import pandas as pd
from gilfoyle import report

# Define output filename
pdf = report.Report(output='example.pdf')

# Set report title
pdf.set_title('Monthly ecommerce report')

# Create payload
payload = pdf.get_payload()

# Add a cover slide
payload = pdf.add_page(payload,
                       page_type='cover',
                       page_title='Monthly report',
                       page_subheading='Matt Clarke')

# Fetch your data
df = pd.read_csv('data.csv', 
                 skiprows=1,
                 names=['Period', 'Entrances', 'Sessions', 'Pageviews',
                        'Transactions', 'Conversion Rate', 'AOV']).head(13)

payload = pdf.add_page(payload,
                       page_type='report',
                       page_layout='simple',
                       page_title='Organic search',
                       page_dataframe=df
                       )

# Save to PDF
pdf.create_report(payload, verbose=True, output='pdf')
```


#### Dependencies

Gilfoyle is written in Python 3 and uses the Jinja 2 templating engine, the Bulma HTML and CSS framework, and the Weasyprint PDF generator package. Gilfoyle is compatible with Pandas and can automatically turn your dataframes into tables. 

