import mimetypes
import shutil
import os


class BaseResponse():
    def __init__(self, content_type, content_encoding=None, status_code=200):
        self.content_type = content_type
        self.content_encoding = content_encoding
        self.status_code = status_code

    @property
    def headers(self):
        yield ("Content-Type", self.content_type)

        if self.content_encoding:
            yield ("Content-Encoding", self.content_encoding)

    def write(self, stream):
        raise NotImplementedError


class Response(BaseResponse):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = content

    @property
    def headers(self):
        yield from super().headers

        yield ("Content-Length", len(self.content))

    def write(self, stream):
        stream.write(self.content.encode())


class JsonResponse(Response):
    def __init__(self, content, status_code=200):
        super().__init__(content, "application/json", status_code)


class StreamResponse(BaseResponse):
    def __init__(self, stream, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stream = stream

    def write(self, stream):
        shutil.copyfileobj(self.stream, stream)


class FileResponse(BaseResponse):
    def __init__(self, file_path, *args, **kwargs):
        content_type, _ = mimetypes.guess_type(file_path)

        super().__init__(content_type, *args, **kwargs)

        self.file_path = file_path

    @property
    def headers(self):
        yield from super().headers

        yield ("Content-Length", os.path.getsize(self.file_path))

    def write(self, stream):
        with open(self.file_path, "rb") as file:
            shutil.copyfileobj(file, stream)
