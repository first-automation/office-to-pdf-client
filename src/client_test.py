from pathlib import Path

from office_to_pdf_client._client import OfficeToPdfClient


def client_test():
    office_to_pdf_url = "http://127.0.0.1:8000"
    office_file_path = "../samples/test.xlsx"
    output_file_path = "../samples/test.pdf"
    headers = {}
    if isinstance(office_file_path, str):
        office_file_path = Path(office_file_path)
    if isinstance(output_file_path, str):
        output_file_path = Path(output_file_path)
    client = OfficeToPdfClient(office_to_pdf_url)
    if headers:
        client.add_headers(headers)
    route = client.libre_office.to_pdf()
    response = route.convert(office_file_path).run()
    output_file_path.write_bytes(response.content)


if __name__ == "__main__":
    client_test()
