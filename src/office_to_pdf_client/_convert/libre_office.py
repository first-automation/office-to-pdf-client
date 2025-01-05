import logging
from contextlib import ExitStack
from pathlib import Path
from typing import Optional, Self

from httpx import Client
from httpx._types import RequestFiles

from src.office_to_pdf_client._convert.responses import SingleFileResponse
from src.office_to_pdf_client._utils import guess_mime_type


logger = logging.getLogger(__name__)


class LibreOfficeConvertRoute:
    """
    Represents the office-to-pdf route for converting documents to PDF using LibreOffice.

    This class allows adding single or multiple files for conversion, optionally
    merging them into a single PDF.
    """

    def __init__(self, client: Client, api_route: str) -> None:
        self._client = client
        self._route = api_route
        self._stack = ExitStack()
        # These are the options that will be set to office-to-pdf.  Things like PDF/A
        self._form_data: dict[str, str] = {}
        # These are the names of files, mapping to their Path
        self._file_map: dict[str, Path] = {}
        self._result_is_zip = False
        self._convert_calls = 0

    def _add_file_map(self, filepath: Path, *, name: Optional[str] = None) -> None:
        """
        Small helper to handle bookkeeping of files for later opening.  The name is
        optional to support those things which are required to have a certain name
        generally for ordering or just to be found at all
        """
        if name is None:
            name = filepath.name

        if name in self._file_map:  # pragma: no cover
            logger.warning(f"{name} has already been provided, overwriting anyway")

        self._file_map[name] = filepath

    def _get_all_resources(self) -> RequestFiles:
        """
        Deals with opening all provided files for multi-part uploads, including
        pushing their new contexts onto the stack to ensure resources like file
        handles are cleaned up
        """
        resources = {}
        for filename in self._file_map:
            file_path = self._file_map[filename]

            # Helpful but not necessary to provide the mime type when possible
            mime_type = guess_mime_type(file_path)
            if mime_type is not None:
                resources.update(
                    {"file": (filename, self._stack.enter_context(file_path.open("rb")), mime_type)},
                )
            else:  # pragma: no cover
                resources.update({"file": (filename, self._stack.enter_context(file_path.open("rb")))})  # type: ignore [dict-item]
        return resources

    def convert(self, input_file_path: Path) -> Self:
        """
        Adds a single file to be converted to PDF.

        Calling this method multiple times will result in a ZIP containing
        individual PDFs for each converted file.

        Args:
            input_file_path (Path): The path to the file to be converted.

        Returns:
            LibreOfficeConvertRoute: This object itself for method chaining.
        """

        self._add_file_map(input_file_path)
        self._convert_calls += 1
        if self._convert_calls > 1:
            self._result_is_zip = True
        return self

    def run(self) -> SingleFileResponse:  # type: ignore[override]
        """
        Executes the configured route against the server and returns the resulting
        Response.
        """
        resp = self._client.post(
            url=self._route,
            files=self._get_all_resources(),
        )
        resp.raise_for_status()
        return resp


class BaseApi:
    """
    Simple base class for an API, which wraps one or more routes, providing
    each with the client to use
    """

    def __init__(self, client: Client) -> None:
        self._client = client


class LibreOfficeApi(BaseApi):
    """
    Represents the office-to-pdf API for LibreOffice-based conversions.

    Provides a method to create a LibreOfficeConvertRoute object for converting
    documents to PDF using LibreOffice.
    """

    _CONVERT_ENDPOINT = "/convert_to_pdf"

    def to_pdf(self) -> LibreOfficeConvertRoute:
        """
        Creates a LibreOfficeConvertRoute object for converting documents to PDF.

        Returns:
            LibreOfficeConvertRoute: A new LibreOfficeConvertRoute object.
        """

        return LibreOfficeConvertRoute(self._client, self._CONVERT_ENDPOINT)
