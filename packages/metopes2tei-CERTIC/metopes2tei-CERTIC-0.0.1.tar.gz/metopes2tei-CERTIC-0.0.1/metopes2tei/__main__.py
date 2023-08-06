import logging
import argh
from metopes2tei import _process_doc
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def _convert_file(input_file_path: str):
    """
    Converts a *.docx file to XML TEI.
    """
    _process_doc(input_file_path, os.getcwd(), logger)


argh.dispatch_command(_convert_file)
