from io import BytesIO

from unittest import TestCase
from unittest.mock import patch, mock_open, Mock

from qozyd.http.response import BaseResponse, Response, JsonResponse, StreamResponse, FileResponse


class BaseResponseTest(TestCase):
    def test_headers(self):
        response = BaseResponse("text/html", content_encoding="utf-8", status_code=200)

        self.assertEqual(dict(response.headers), {"Content-Type": "text/html", "Content-Encoding": "utf-8"})

    def test_write(self):
        response = BaseResponse("text/html", content_encoding="utf-8", status_code=200)

        with self.assertRaises(NotImplementedError):
            response.write(None)


class ResponseTest(TestCase):
    def test_headers(self):
        response = Response("test-content", "text/html", content_encoding="utf-8", status_code=200)

        self.assertEqual(dict(response.headers), {"Content-Type": "text/html", "Content-Encoding": "utf-8", "Content-Length": 12})

    def test_write(self):
        response = Response("test-content", "text/html", content_encoding="utf-8", status_code=200)

        response_stream = BytesIO()
        response.write(response_stream)

        self.assertEqual(response_stream.getvalue().decode("utf-8"), "test-content")


class JsonResponseTest(TestCase):
    def test(self):
        response = JsonResponse("string")

        self.assertEqual(response.content_type, "application/json")


class StreamResponseTest(TestCase):
    def test(self):
        input_stream = BytesIO(b"test")
        output_stream = BytesIO()

        response = StreamResponse(input_stream, "text/plain")
        response.write(output_stream)

        self.assertEqual(output_stream.getvalue().decode("utf-8"), "test")


class FileResponseTest(TestCase):
    def test(self):
        output_stream = BytesIO()

        response = FileResponse("/test-file.html")

        with patch("builtins.open", mock_open(read_data=b"file-content")) as open_mock:
            response.write(output_stream)

        with patch("os.path.getsize", Mock(return_value=12)):
            self.assertEqual(dict(response.headers), {"Content-Length": 12, "Content-Type": "text/html"})

        open_mock.assert_called_with("/test-file.html", "rb")
        self.assertEqual(output_stream.getvalue().decode("utf-8"), "file-content")
