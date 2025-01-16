import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir + "/src")

from pathlib import Path

from office_to_pdf_client._client import OfficeToPdfClient


def client_example():
    office_to_pdf_url = "http://127.0.0.1:8000"
    office_file_path = "./examples/test.xlsx"
    output_file_path = "./examples/test.pdf"
    headers = {}
    if isinstance(office_file_path, str):
        office_file_path = Path(office_file_path)
    if isinstance(output_file_path, str):
        output_file_path = Path(output_file_path)
    client = OfficeToPdfClient(office_to_pdf_url)
    if headers:
        client.add_headers(headers)
    client.convert_to_pdf(office_file_path, output_file_path)


if __name__ == "__main__":
    client_example()
