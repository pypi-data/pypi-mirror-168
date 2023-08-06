import logging
import re
import fnmatch
from typing import List, Tuple, Union
import os
import os.path
import sys
from subprocess import Popen, PIPE
import shutil

SOFFICE_PATH = shutil.which("soffice")
JAVA_PATH = shutil.which("java")
RESOURCES_PATH = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
SAXON_PATH = os.getenv("SAXON_PATH") or (RESOURCES_PATH + "saxon9.jar")

if not SOFFICE_PATH:
    sys.exit("Could not find soffice. Is it in your PATH ?")
if not JAVA_PATH:
    sys.exit("Could not find java. Is it in your PATH ?")
if not SAXON_PATH:
    sys.exit(
        "Could not find the Saxon jar. Please set SAXON_PATH environment variable."
    )
if not os.path.isfile(SAXON_PATH):
    sys.exit(
        "Could not find the Saxon jar. Please check your SAXON_PATH environment variable."
    )


def _silent_remove(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def _union_java_output(std_out: bytes, std_err: bytes) -> Union[bytes, str]:
    """
    Java outputs errors to STDOUT ???
    """
    if std_err:
        try:
            out = std_err.decode("utf-8")
            out = out.strip()
            if out:
                return out
        except UnicodeDecodeError:
            return std_err
    if std_out:
        try:
            out = std_out.decode("utf-8")
            out = out.strip()
            if out:
                return out
        except UnicodeDecodeError:
            return std_out
    return "subprocess provided no error output"


def _find_files(what: str, where: str = ".") -> List[str]:
    rule = re.compile(fnmatch.translate(what), re.IGNORECASE)
    return [
        "{}{}{}".format(where, os.path.sep, name)
        for name in os.listdir(where)
        if rule.match(name)
    ]


def _process_doc(
    doc_file,
    working_dir: str,
    logger: logging.Logger,
) -> Tuple[bool, Union[str, bytes]]:
    doc_file_no_extension = os.path.splitext(doc_file)[0]
    #
    # CONVERSION  Flat XML
    #
    cli_args = [
        SOFFICE_PATH,
        "--invisible",
        "--convert-to",
        "xml:OpenDocument Text Flat XML",
        "--outdir",
        working_dir,
        doc_file,
    ]
    logger.debug(" ".join(cli_args))
    p = Popen(
        cli_args,
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return False, _union_java_output(out, err)
    else:
        logger.info("Wrote {}".format(os.path.basename(doc_file_no_extension + ".xml")))
    p.terminate()

    #
    # TRANSFORMATIONS XSL Métopes v3
    #
    cli_args = [
        JAVA_PATH,
        "-jar",
        SAXON_PATH,
        doc_file_no_extension + ".xml",
        RESOURCES_PATH + "ue.xsl",
    ]
    logger.debug(" ".join(cli_args))
    p = Popen(
        cli_args,
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return False, _union_java_output(out, err)
    else:
        with open(doc_file_no_extension + ".xml", "wb") as f:
            f.write(out)
            logger.info(
                "Wrote {}".format(os.path.basename(doc_file_no_extension + ".xml"))
            )
    p.terminate()
    return True, _union_java_output(out, err)


def metopes2tei(working_dir: str, logger: logging.Logger, options: dict = None):
    success_counter = 0
    failure_counter = 0
    doc_files = _find_files("*.docx", working_dir) + _find_files("*.odt", working_dir)
    logger.info("{} file(s) to convert.".format(len(doc_files)))
    for doc_file in doc_files:
        logger.info("converting {}".format(os.path.basename(doc_file)))
        success, output = _process_doc(doc_file, working_dir, logger)
        if not success:
            logger.error(
                "could not convert {}. Process output: {}".format(
                    os.path.basename(doc_file), output
                )
            )
            failure_counter = failure_counter + 1
        else:
            success_counter = success_counter + 1
            logger.info("{}: success".format(os.path.basename(doc_file)))
    logger.info("Job done, {} files converted".format(success_counter))


metopes2tei.description = {
    "label": "Fichiers stylés vers TEI Métopes v3",
    "help": "Convertir les fichiers *.docx et *.odt en fichiers *.xml (vocabulaire TEI Métopes (v3))",
    "options": [],
}
