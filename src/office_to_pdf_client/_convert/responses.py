import dataclasses

from pathlib import Path
from typing import Union

from httpx import Headers


@dataclasses.dataclass
class _BaseApiResponse:
    """
    The basic response from the API, containing the status code and the
    response content.  This is compatible with the Response used before from
    httpx
    """

    status_code: int
    headers: Headers
    content: Union[bytes, bytearray]

    def to_file(self, file_path: Path) -> None:
        """
        Writes the response content to a given file.
        """
        file_path.write_bytes(self.content)


@dataclasses.dataclass
class SingleFileResponse(_BaseApiResponse):
    pass
