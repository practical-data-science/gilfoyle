"""
Example 1
"""

# Load packages
import pandas as pd
import seaborn as sns
from gilfoyle import report

# ====================================================================================================================
# Set up the report
# ====================================================================================================================

# Create a report
pdf = report.Report(output='example.pdf')

pdf.set_title('Gilfoyle example')
pdf.set_accent_background_color('#9f85ca')
pdf.set_accent_font_color('#fff')

# Create an empty payload
payload = pdf.get_payload()

# ====================================================================================================================
# Chapter cover
# ====================================================================================================================

payload = pdf.add_page(payload,
                       page_type='chapter',
                       page_title='Gilfoyle',
                       page_subheading='Various examples')

# ====================================================================================================================
# Simple layout with dataframe
# ====================================================================================================================

# Load a Pandas dataframe and return 13 rows
df = pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/monthly-ecommerce-data.csv',
                 skiprows=1,
                 names=['Period', 'Sessions', 'Transactions', 'Conversion Rate', 'Revenue', 'AOV']).head(13)

# Add the dataframe to the payload
payload = pdf.add_page(payload,
                       page_type='report',
                       page_layout='simple',
                       page_title='Simple layout, dataframe',
                       page_dataframe=df
                       )

# ====================================================================================================================
# Simple layout with dataframe and metrics comparing last month to last year
# ====================================================================================================================

# Load a Pandas dataframe and return 13 rows
df = pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/monthly-ecommerce-data.csv',
                 skiprows=1,
                 names=['Period', 'Sessions', 'Transactions', 'Conversion rate', 'Revenue', 'AOV']).head(13)

# Add metrics
metrics = [
    pdf.add_metric_tile(
        metric_title='Sessions',
        metric_value_now=df['Sessions'].loc[0],
        metric_value_before=df['Sessions'].loc[12],
        metric_name='year'
    ),
    pdf.add_metric_tile(
        metric_title='Conversion rate',
        metric_value_now=df['Conversion rate'].loc[0],
        metric_value_before=df['Conversion rate'].loc[12],
        metric_name='year',
        metric_suffix='%'
    ),
    pdf.add_metric_tile(
        metric_title='Transactions',
        metric_value_now=df['Transactions'].loc[0],
        metric_value_before=df['Transactions'].loc[12],
        metric_name='year'
    ),
    pdf.add_metric_tile(
        metric_title='AOV',
        metric_value_now=round(df['AOV'].loc[0], 2),
        metric_value_before=df['AOV'].loc[12],
        metric_name='year',
        metric_prefix='£'
    ),
    pdf.add_metric_tile(
        metric_title='Revenue',
        metric_value_now=df['Revenue'].loc[0],
        metric_value_before=df['Revenue'].loc[12],
        metric_name='year',
        metric_prefix='£'
    ),
]

# Add the dataframe to the payload
payload = pdf.add_page(payload,
                       page_type='report',
                       page_layout='simple',
                       page_title='Simple layout, dataframe, YoY metrics',
                       page_dataframe=df,
                       page_metrics=metrics,
                       )

# ====================================================================================================================
# Simple layout with dataframe and metrics comparing last month to previous month
# ====================================================================================================================

# Load a Pandas dataframe and return 13 rows
df = pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/monthly-ecommerce-data.csv',
                 skiprows=1,
                 names=['Period', 'Sessions', 'Transactions', 'Conversion rate', 'Revenue', 'AOV']).head(13)

# Add metrics
metrics = [
    pdf.add_metric_tile(
        metric_title='Sessions',
        metric_value_now=df['Sessions'].loc[0],
        metric_value_before=df['Sessions'].loc[1],
        metric_name='month'
    ),
    pdf.add_metric_tile(
        metric_title='Conversion rate',
        metric_value_now=df['Conversion rate'].loc[0],
        metric_value_before=df['Conversion rate'].loc[1],
        metric_name='month',
        metric_suffix='%'
    ),
    pdf.add_metric_tile(
        metric_title='Transactions',
        metric_value_now=df['Transactions'].loc[0],
        metric_value_before=df['Transactions'].loc[1],
        metric_name='month'
    ),
    pdf.add_metric_tile(
        metric_title='AOV',
        metric_value_now=round(df['AOV'].loc[0], 2),
        metric_value_before=df['AOV'].loc[1],
        metric_name='month',
        metric_prefix='£'
    ),
    pdf.add_metric_tile(
        metric_title='Revenue',
        metric_value_now=df['Revenue'].loc[0],
        metric_value_before=df['Revenue'].loc[1],
        metric_name='month',
        metric_prefix='£'
    ),
]

# Add the dataframe to the payload
payload = pdf.add_page(payload,
                       page_type='report',
                       page_layout='simple',
                       page_title='Simple layout, dataframe, MoM metrics',
                       page_dataframe=df,
                       page_metrics=metrics,
                       )

# ====================================================================================================================
# Simple layout with dataframe and no metrics comparison
# ====================================================================================================================

# Load a Pandas dataframe and return 13 rows
df = pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/monthly-ecommerce-data.csv',
                 skiprows=1,
                 names=['Period', 'Sessions', 'Transactions', 'Conversion rate', 'Revenue', 'AOV']).head(13)

# Add metrics
metrics = [
    pdf.add_metric_tile(
        metric_title='Sessions',
        metric_value_now=df['Sessions'].loc[0],
    ),
    pdf.add_metric_tile(
        metric_title='Conversion rate',
        metric_value_now=df['Conversion rate'].loc[0],
        metric_suffix='%'
    ),
    pdf.add_metric_tile(
        metric_title='Transactions',
        metric_value_now=df['Transactions'].loc[0],
    ),
    pdf.add_metric_tile(
        metric_title='AOV',
        metric_value_now=round(df['AOV'].loc[0], 2),
        metric_prefix='£'
    ),
    pdf.add_metric_tile(
        metric_title='Revenue',
        metric_value_now=df['Revenue'].loc[0],
        metric_prefix='£'
    ),
]

# Add the dataframe to the payload
payload = pdf.add_page(payload,
                       page_type='report',
                       page_layout='simple',
                       page_title='Simple layout, dataframe, metrics (no comparison)',
                       page_dataframe=df,
                       page_metrics=metrics,
                       )

# ====================================================================================================================
# Left commentary layout with dataframe and notification message
# ====================================================================================================================

# Load a Pandas dataframe and return 13 rows
df = pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/monthly-ecommerce-data.csv',
                 skiprows=1,
                 names=['Period', 'Sessions', 'Transactions', 'Conversion Rate', 'Revenue', 'AOV']).head(13)

# Define commentary
page_commentary = """
To add a commentary section to your report you need to define a block of text and use HTML to add markup.<br><br>
                       
There's quite a bit of room in the left-commentary layout to support adding lengthy commentary and also adding a 
notification message to alert readers to specific points.
"""

# Define message
page_message = {'message': 'This is a page message', 'style': 'warning'}

# Add the dataframe to the payload
payload = pdf.add_page(payload,
                       page_type='report',
                       page_layout='left-commentary',
                       page_title='Left-commentary layout, dataframe, commentary, notification, warning message',
                       page_dataframe=df,
                       page_commentary=page_commentary,
                       page_notification='This is a notification',
                       page_message=page_message,
                       )

# ====================================================================================================================
# Simple layout with dataframe
# ====================================================================================================================

# Load a Pandas dataframe and return 13 rows
df = pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/monthly-ecommerce-data.csv',
                 skiprows=1,
                 names=['Period', 'Sessions', 'Transactions', 'Conversion Rate', 'Revenue', 'AOV']).head(13)

# Define message
page_message = {'message': 'This is a page message', 'style': 'danger'}

# Add the dataframe to the payload
payload = pdf.add_page(payload,
                       page_type='report',
                       page_layout='simple',
                       page_title='Simple layout, dataframe, danger message',
                       page_dataframe=df,
                       page_message=page_message,
                       )

# ====================================================================================================================
# Simple layout with dataframe and visualisation
# ====================================================================================================================

# Load a Pandas dataframe and return 13 rows
df = pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/monthly-ecommerce-data.csv',
                 skiprows=1,
                 names=['Period', 'Sessions', 'Transactions', 'Conversion Rate', 'Revenue', 'AOV']).head(13)

# Define commentary
page_commentary = """
To add a visualisation you need to use either the "plot" or "left-commentary" layouts, save the image to a file and 
pass in the filename to the "page_visualisation" argument. You will want to tweak the image size so it sits perfectly on your report page.
"""

# Generate a visualisation and save the image
sns.set(rc={'figure.figsize': (15, 6)})
line_plot = sns.lineplot(x='Period', y='Sessions', data=df)
line_plot.figure.savefig("lineplot.png")

# Add the dataframe to the payload
payload = pdf.add_page(payload,
                       page_type='report',
                       page_layout='plot',
                       page_title='Plot layout, visualisation, commentary',
                       page_dataframe=df,
                       page_commentary=page_commentary,
                       page_visualisation='lineplot.png',
                       )

# ====================================================================================================================
# Render the report
# ====================================================================================================================

# Create the report
pdf.create_report(payload, verbose=False, output='pdf')
print('Created example.pdf')
