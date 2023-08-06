from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
print (here)
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
    setup(
        name = "vcfvalidator",
        version = "1.0.0",
        author = "Junaid Memon",
        author_email = "jmemonisy@gmail.com",
        description = "VCF parser for header data",
        # other arguments omitted
        long_description=long_description,
        long_description_content_type='text/markdown'
    )