# office-to-pdf-client

## クライアント使用方法

### 1. 事前準備
docker compose等でoffice-to-pdf-serveのサーバーを立ち上げる
（docker composeの場合、"http://127.0.0.1:8000"でサーバーが立ち上がる）

### 2. クライアント使用例
以下のコード例のように、クライアントを使用できる (examples/client_example.py参照)

```python
from pathlib import Path

from office_to_pdf_client import OfficeToPdfClient

office_to_pdf_url = "http://127.0.0.1:8000"
office_file_path = Path("./examples/test.xlsx")
output_file_path = Path("./examples/test.pdf")
# office-to-pdf-serveのホスト(office_to_pdf_url)を引数に与えて、クライアントのインスタンスを作成
client = OfficeToPdfClient(office_to_pdf_url)
# convert_to_pdfの引数に、入力ファイルパス(office_file_path), 出力ファイルパス(output_file_path)を与えて、対象のファイルをPDFに変換
client.convert_to_pdf(office_file_path, output_file_path)
```

※エンドポイント("/convert_to_pdf")は内部でURLに結合され、"http://127.0.0.1:8000/convert_to_pdf"のような形でバックエンドへリクエストが送信される