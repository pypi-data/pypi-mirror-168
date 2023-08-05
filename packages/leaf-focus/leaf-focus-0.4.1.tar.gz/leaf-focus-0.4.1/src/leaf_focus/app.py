"""Main application."""

import dataclasses
import datetime
import logging
import pathlib
import platform
import typing

from leaf_focus import utils
from leaf_focus.ocr import keras_ocr
from leaf_focus.pdf import model, xpdf


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class AppArgs:
    """Arguments for running the application."""

    input_pdf: pathlib.Path
    """path to the pdf file"""

    output_dir: pathlib.Path
    """path to the output directory to save text files"""

    first_page: typing.Optional[int] = None
    """the first pdf page to process"""

    last_page: typing.Optional[int] = None
    """the last pdf page to process"""

    save_page_images: bool = False
    """save each page of the pdf to a separate image"""

    run_ocr: bool = False
    """run OCR over each page of the pdf"""

    log_level: typing.Optional[str] = None
    """the log level"""


class App:
    """The main application."""

    def __init__(self, exe_dir: pathlib.Path):
        """
        Create a new instance of the application.

        :param exe_dir: path to the directory containing the executable files
        """
        if not exe_dir or not exe_dir.exists() or not exe_dir.is_dir():
            raise NotADirectoryError(f"The path '{exe_dir or ''}' is not a directory.")
        self._exe_dir = exe_dir

    def run(self, app_args: AppArgs) -> bool:
        """
        Run the application.

        :param app_args: the application arguments
        :return: return true if the text extraction succeeded, otherwise false
        :rtype: bool
        """
        timestamp_start = datetime.datetime.utcnow()
        logger.info("Starting leaf-focus")

        input_pdf = utils.validate_path(
            "input pdf", app_args.input_pdf, must_exist=True
        )
        output_dir = utils.validate_path(
            "output directory", app_args.output_dir, must_exist=False
        )

        # create the output directory
        if not output_dir.is_dir():
            logger.warning("Creating output directory '%s'.", output_dir)
            output_dir.mkdir(exist_ok=True, parents=True)
        else:
            logger.info("Using output directory '%s'.", output_dir)

        # run the pdf text extraction
        xpdf_prog = xpdf.XpdfProgram(self._exe_dir)

        # pdf file info
        xpdf_info_args = model.XpdfInfoArgs(
            include_metadata=True,
            first_page=app_args.first_page,
            last_page=app_args.last_page,
        )
        xpdf_prog.info(input_pdf, output_dir, xpdf_info_args)

        # pdf embedded text
        xpdf_text_args = model.XpdfTextArgs(
            line_end_type=self.get_line_ending(),
            use_original_layout=True,
            first_page=app_args.first_page,
            last_page=app_args.last_page,
        )
        xpdf_prog.text(input_pdf, output_dir, xpdf_text_args)

        # pdf page image
        xpdf_image = None
        if app_args.save_page_images or app_args.run_ocr:
            xpdf_image_args = model.XpdfImageArgs(use_grayscale=True)
            xpdf_image = xpdf_prog.image(input_pdf, output_dir, xpdf_image_args)

        # pdf page image ocr
        if app_args.run_ocr and xpdf_image:
            keras_ocr_prog = keras_ocr.OpticalCharacterRecognition()
            for xpdf_image_file in xpdf_image.output_files:
                keras_ocr_prog.recognise_text(xpdf_image_file, output_dir)

        timestamp_finish = datetime.datetime.utcnow()
        program_duration = timestamp_finish - timestamp_start
        logger.info("Finished (duration %s)", program_duration)
        return True

    def get_line_ending(self) -> str:
        """
        Get the line endings based on the current platform.

        :return: the line ending style
        """
        opts = {
            "Linux": "unix",
            "Darwin": "mac",
            "Windows": "dos",
        }
        plat = platform.system()

        return opts[plat]
