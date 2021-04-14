import os
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
                 page_visualisation=None):
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
                'page_visualisation': page_visualisation
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
