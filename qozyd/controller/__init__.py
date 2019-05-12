import mimetypes
import pkg_resources

from aiohttp import web


class Controller():
    def routes(self):
        return []


def static_file_handler(package=None, base_path=None, directory_index=None):
    async def handler(request):
        path = request.match_info.get("path")

        file_path = "/".join([base_path or "", path])

        if pkg_resources.resource_isdir(package, file_path) and directory_index is not None:
            if isinstance(directory_index, str):
                file_path = "/".join([file_path, directory_index])
            else:
                # try all directory_index files
                for directory_index_file in directory_index:
                    test_file_path = "/".join([file_path, directory_index_file])

                    if pkg_resources.resource_exists(package, test_file_path) and not pkg_resources.resource_isdir(package, test_file_path):
                        file_path = test_file_path
                        break
                else:
                    raise web.HTTPNotFound()

        if not pkg_resources.resource_exists(package, file_path):
            raise web.HTTPNotFound()

        content_type, _ = mimetypes.guess_type(pkg_resources.resource_filename(package, file_path))

        response = web.StreamResponse()
        response.content_type = content_type

        await response.prepare(request)

        input_stream = pkg_resources.resource_stream(package, file_path)

        # stream package resource to response
        while 1:
            buf = input_stream.read(16*1024)

            if not buf:
                break
            await response.write(buf)

        return response

    return handler

