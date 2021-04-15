import os
import re
import numpy as np
import pandas as pd
from weasyprint import HTML
from jinja2 import Environment
from jinja2 import FileSystemLoader


class Report:
    def __init__(self,
                 output,
                 template='assets/template.html',
                 base_url='.'
                 ):
        self.template = template
        self.output = output
        self.base_url = base_url
        self.payload = ''
        self.title = ''

    """
    Report configuration
    """

    def set_title(self, title):
        self.title = title

    """
    Add pages
    """

    @staticmethod
    def get_payload():
        """Return the payload dictionary to append to.

        Returns:
            dict: Payload dictionary to pass to Jinja.
        """

        return {'report': {}, 'pages': []}

    def add_page(self,
                 payload,
                 page_type,
                 page_title,
                 page_layout=None,
                 page_subheading=None,
                 page_commentary=None,
                 page_message=None,
                 page_notification=None,
                 page_metrics=None,
                 page_dataframe=None,
                 page_visualisation=None,
                 page_background=None):
        """Add a new page to the payload for the report.

        Args:
            payload: Current payload.
            page_type: Page type, i.e. cover, chapter, report
            page_title: Page title
            page_layout: Page layout, i.e. simple, left-commentary
            page_subheading: Page subheading
            page_commentary: Page commentary text to appear with report
            page_message: Page message dictionary
            page_notification: Page notification text
            page_metrics: Dictionary of page metrics
            page_dataframe: Pandas dataframe with formatted headers
            page_visualisation: Image of data visualisation to include.
            page_background: Image path of cover background image.

        Returns:
            dict: Current payload with new data appended.
        """

        page = {'page_type': page_type,
                'page_layout': page_layout,
                'page_title': page_title,
                'page_subheading': page_subheading,
                'page_commentary': page_commentary,
                'page_message': page_message,
                'page_notification': page_notification,
                'page_metrics': page_metrics,
                'page_dataframe': self.format_dataframe(page_dataframe),
                'page_visualisation': page_visualisation,
                'page_background': page_background,
                }
        payload['pages'].append(page)
        return payload

    @staticmethod
    def format_dataframe(dataframe):
        """Returns the HTML of a reformatted dataframe for use in the report.

        Args:
            dataframe: Pandas dataframe.

        Returns:
            string: Pandas dataframe in HTML format.
        """

        if isinstance(dataframe, pd.DataFrame):
            formatted_df = dataframe.to_html(classes=['dataframe', 'table', 'is-striped', 'is-fullwidth'],
                                             max_rows=13,
                                             max_cols=10,
                                             index=False)
            return formatted_df

    """
    Load template
    """

    def _get_template(self):
        """Returns the defined Jinja template to populate.

        Returns:
            HTML template.
        """

        path = os.path.dirname(__file__)
        env = Environment(loader=FileSystemLoader(path))
        template = env.get_template(self.template)
        return template

    def _render_template(self, payload):
        """Renders the payload in the Jinja template.

        Args:
            payload: Payload dictionary.

        Returns:
            string: Rendered template.
        """

        template = self._get_template()
        return template.render(payload)

    def _extend_payload(self, payload):
        """Extends the payload by appending additional values.

        Args:
            payload: Payload dictionary.

        Returns:
            dict: Payload with appended values.
        """

        payload['report']['title'] = self.title
        return payload

    """
    Save to HTML
    """

    @staticmethod
    def to_html(html, filename):
        """Write a string of HTML to a file.

        Args:
            html: string of HTML.
            filename: filename and path.

        Returns:
            File.
        """

        f = open(filename, 'w')
        f.write(html)
        f.close()

    """
    Generate PDF
    """

    def create_report(self, payload, output='pdf', verbose=False):
        """Creates the report.

        Args:
            payload: Dictionary payload.
            output: Output format (optional). pdf or html.
            verbose: Set to true to see dictionary payload.

        Returns:
            file: Rendered file.
        """

        payload = self._extend_payload(payload)
        if verbose:
            print(payload)

        if output == 'html':
            self.to_html(self._render_template(payload), self.output)
        else:
            return HTML(string=self._render_template(payload),
                        base_url=self.base_url).write_pdf(self.output)

    """
    Metrics
    """

    @staticmethod
    def get_percentage_change(metric_now, metric_before):
        """Return the percentage change in a metric.

        Args:
            metric_now (float/int): Metric in current period.
            metric_before (float/int): Metric in previous period.

        Returns:
            change (float): Percentage change to two decimal places.
        """

        if metric_now == metric_before:
            return 0
        try:
            return (abs(metric_now - metric_before) / metric_before) * 100.0
        except ZeroDivisionError:
            return float('inf')

    @staticmethod
    def get_change_direction(metric_now, metric_before):
        """Return the direction of change in a metric.

        Args:
            metric_now (float/int): Metric in current period.
            metric_before (float/int): Metric in previous period.

        Returns:
            direction (string): Returns up, down, flat or nothing.
        """

        if metric_now > metric_before:
            direction = 'up'
        elif metric_now < metric_before:
            direction = 'down'
        elif metric_now == metric_before:
            direction = 'flat'
        else:
            direction = ''

        return direction

    @staticmethod
    def to_numeric(string):
        """Strip non-numeric characters and return a float or int depending on decimal.

        Args:
            string (string): Formatted number, i.e. £123,391

        Return:
            numeric (int/float): Numeric representation of string in int or float.
        """

        if isinstance(string, str):
            numeric = re.sub("[^0-9.]", "", string)

            if numeric.isdigit():
                numeric = int(numeric)
            else:
                numeric = float(numeric)

        else:
            numeric = string

        return numeric

    @staticmethod
    def format_number(metric, prefix=None, suffix=None):
        """Add a prefix or suffix to a number.

        Args:
            metric (int/float/string): The metric to prefix or suffix.
            prefix (optional, string): The prefix to add, i.e. £
            suffix (optional, string): The suffix to add, i.e. %

        Returns:
            metric (string): The metric with a prefix or suffix, i.e. £12.99 or 12.23%.
        """

        if prefix:
            metric = prefix + str(metric)
        elif suffix:
            metric = str(metric) + suffix
        else:
            metric

        return metric

    def add_metric_tile(self,
                        metric_title,
                        metric_value_now,
                        metric_value_before,
                        metric_prefix=None,
                        metric_suffix=None):
        """Create a metric tile dictionary to append to the metrics list payload.

        Args:
            metric_title (string): Title of metric tile, i.e. Revenue
            metric_value_now (int/float): Value of metric in current period.
            metric_value_before (int/float): Value of metric in same period 12 months ago.
            metric_prefix (optional, string): Optional prefix, i.e. £
            metric_suffix (optional, string): Optional suffix, i.e. %

        Returns:
            Dictionary containing metric tile data to be appended to the metrics list.

            {'metric_type': 'number',
             'metric_title': 'Transactions',
             'metric_value': 4076,
             'metric_label': 'Up 24% on last year'}

        Usage:
            metrics = []

            metrics.append(
                add_metric_tile(metric_title='Transactions',
                                metric_value_now=df_google_ads['Transactions'].loc[0],
                                metric_value_before=df_google_ads['Transactions'].loc[12]
                           )
            )

            metrics.append(
                add_metric_tile(metric_title='Revenue',
                                metric_value_now=df_google_ads['Revenue'].loc[0],
                                metric_value_before=df_google_ads['Revenue'].loc[12],
                                metric_prefix='£'
                           )
            )

            metrics.append(
                add_metric_tile(metric_title='Costs',
                                metric_value_now=df_google_ads['Costs'].loc[0],
                                metric_value_before=df_google_ads['Costs'].loc[12],
                                metric_prefix='£'
                           )
            )

            metrics.append(
                add_metric_tile(metric_title='Cost of Sale',
                                metric_value_now=df_google_ads['COS'].loc[0],
                                metric_value_before=df_google_ads['COS'].loc[12],
                                metric_suffix='%'
                           )
            )

        Output:
            [{'metric_title': 'Transactions',
          'metric_value': 4076,
          'metric_label': 'Up 24% on last year'},
         {'metric_title': 'Revenue',
          'metric_value': '£253659',
          'metric_label': 'Up 47% on last year'},
         {'metric_title': 'Costs',
          'metric_value': '£30244',
          'metric_label': 'Up 62% on last year'},
         {'metric_title': 'Cost of Sale',
          'metric_value': '11.92%',
          'metric_label': 'Up 10% on last year'}]

        """

        # Remove any formatting
        metric_value_now = self.to_numeric(metric_value_now)
        metric_value_before = self.to_numeric(metric_value_before)

        # Get percentage change and change direction
        percentage_change = self.get_percentage_change(metric_value_now, metric_value_before)
        change_direction = self.get_change_direction(metric_value_now, metric_value_before)
        metric_label = change_direction.capitalize() + ' ' + str(round(percentage_change)) + '% on last year'

        # Add prefix or suffix
        metric_value_now = self.format_number(metric_value_now, metric_prefix, metric_suffix)

        metric = {
            'metric_title': metric_title,
            'metric_value': metric_value_now,
            'metric_label': metric_label
        }

        return metric
