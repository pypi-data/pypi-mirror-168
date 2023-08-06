from unittest import TestCase

from docpipe.html import TextToHtmlText, ParseHtml, SerialiseHtml, StripWhitespace
from docpipe.pipeline import PipelineContext


class HtmlTestCase(TestCase):
    maxDiff = None

    def run_html_stage(self, html_text, stage):
        context = PipelineContext(pipeline=None)
        context.html_text = html_text
        # parse html
        ParseHtml()(context)
        stage(context)
        SerialiseHtml()(context)
        return context.html_text

    def test_html_to_text(self):
        context = PipelineContext(pipeline=None)
        context.text = """
one
    two < three
  four & five
"""

        TextToHtmlText()(context)
        self.assertMultiLineEqual(
            """<div>
<p></p>
<p>one</p>
<p>    two &lt; three</p>
<p>  four &amp; five</p>
</div>""",
            context.html_text.strip())

    def test_strip_whitespace(self):
        self.assertMultiLineEqual(
            """<div>
<h1>text <sup>a </sup></h1>
<p>foo</p>
<p><b>bold</b></p>
</div>""",
            self.run_html_stage("""
<div>
<h1> text <sup>a </sup></h1>
<p> foo  </p>
<p> <b>bold</b>  </p>
</div>
""", StripWhitespace()).strip())
