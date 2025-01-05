import logging
from types import TracebackType
from typing import Optional

from httpx import Client

from src.office_to_pdf_client._convert.libre_office import LibreOfficeApi


class OfficeToPdfClient:
    def __init__(
        self,
        host: str,
        *,
        timeout: float = 30.0,
        log_level: int = logging.ERROR,
        http2: bool = True,
    ):
        """_summary_
        Initialize a new office-to-pdf instance.

        Args:
            host (str): _description_
            timeout (float, optional): _description_. Defaults to 30.0.
            log_level (int, optional): _description_. Defaults to logging.ERROR.
            http2 (bool, optional): _description_. Defaults to True.
        """
        # Configure the client
        self._client = Client(base_url=host, timeout=timeout, http2=http2)

        # Set the log level
        logging.getLogger("httpx").setLevel(log_level)
        logging.getLogger("httpcore").setLevel(log_level)

        # Add the resources
        self.libre_office = LibreOfficeApi(self._client)

    def add_headers(self, header: dict[str, str]) -> None:
        """
        Update the httpx Client headers with the given values.

        Args:
            header (Dict[str, str]): A dictionary of header names and values to add.
        """
        self._client.headers.update(header)

    def close(self) -> None:
        """
        Close the underlying HTTP client connection.
        """
        self._client.close()

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """
        Exit the runtime context related to this object.

        This method ensures that the client connection is closed when exiting a context manager.

        Args:
            exc_type: The type of the exception that caused the context to be exited, if any.
            exc_val: The instance of the exception that caused the context to be exited, if any.
            exc_tb: A traceback object encoding the stack trace, if an exception occurred.
        """
        self.close()
