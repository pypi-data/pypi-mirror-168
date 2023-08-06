import logging
import mimetypes

from heaserver.service.representor import cj

from heaserver.fileawss3.service import MIME_TYPES
from .fileawss3testcase import AWSS3FileTestCase
from .filemimetypetestcase import AWSS3FileContentTypeTestCase, db_values
from heaserver.service.testcase.mixin import DeleteMixin, GetAllMixin, GetOneMixin, PutMixin
from aiohttp import hdrs


class TestDeleteFile(AWSS3FileTestCase, DeleteMixin):
    pass


class TestGetFiles(AWSS3FileTestCase, GetAllMixin):
    pass


class TestGetFile(AWSS3FileTestCase, GetOneMixin):
    # Currently backs 200 because it uses the same request handler as the normal get
    # async def test_get_status_opener_choices(self) -> None:
    #     """Checks if a GET request for the opener for a file succeeds with status 300."""
    #     obj = await self.client.request('GET',
    #                                     (self._href / self._id() / 'opener').path,
    #                                     headers=self._headers)
    #     self.assertEqual(300, obj.status)

    async def test_get_status_opener_hea_default_exists(self) -> None:
        """
        Checks if a GET request for the opener for a file succeeds and returns JSON that contains a
        Collection+JSON object with a rel property in its links that contains 'hea-default'.
        """
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'opener').path,
                                        headers={**self._headers, hdrs.ACCEPT: cj.MIME_TYPE})
        if not obj.ok:
            self.fail(f'GET request failed: {await obj.text()}')
        received_json = await obj.json()
        rel = received_json[0]['collection']['items'][0]['links'][0]['rel']
        self.assertIn('hea-default', rel)


class TestPutFile(AWSS3FileTestCase, PutMixin):
    pass


class TestGetFileCheckContentType(AWSS3FileContentTypeTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids = {'.' + x['display_name'].split('.', maxsplit=1)[-1]: x['id'] for x in db_values[self._coll]}

    def setUp(self):
        super().setUp()

        for type_, extensions in MIME_TYPES.items():
            for ext in extensions:
                logging.info('%s -> %s', type_, ext)
                mimetypes.add_type(type_, ext, strict=False)

    async def test_get_content_type_fastq(self) -> None:
        """
        Checks if the response to a GET request for the content of an AWS S3 File object with the file extension
        ".fastq" has the Content-Type header equal "application/x.fastq".
        """
        async with self.client.request('GET',
                                       (self._href / self.ids['.fastq'] / 'content').path,
                                       headers=self._headers) as resp:
            self.assertEqual('application/x.fastq', resp.headers.get(hdrs.CONTENT_TYPE))

    async def test_get_content_type_fasta(self) -> None:
        """
        Checks if the response to a GET request for the content of an AWS S3 File object with the file extension
        ".ffn" has the Content-Type header equal "application/x.fasta".
        """
        async with self.client.request('GET',
                                       (self._href / self.ids['.ffn'] / 'content').path,
                                       headers=self._headers) as resp:
            self.assertEqual('application/x.fasta', resp.headers.get(hdrs.CONTENT_TYPE))

    # mimetypes does not support double file extensions
    # async def test_get_content_type_bambai(self) -> None:
    #     """
    #     Checks if the response to a GET request for the content of an AWS S3 File object with the file extension
    #     ".bam.bai" has the Content-Type header equal "application/x.bambai".
    #     """
    #     async with self.client.request('GET',
    #                                    (self._href / self.ids['.bam.bai'] / 'content').path,
    #                                    headers=self._headers) as resp:
    #         self.assertEqual('application/x.bambai', resp.headers.get(hdrs.CONTENT_TYPE))

    async def test_get_content_type_no_file_extension(self) -> None:
        """
        Checks if the response to a GET request for the content of an AWS S3 File object with no file extension has
        the Content-Type header equal "application/octet-stream".
        """
        async with self.client.request('GET',
                                       (self._href / self.ids['.nofileextension'] / 'content').path,
                                       headers=self._headers) as resp:
            self.assertEqual('application/octet-stream', resp.headers.get(hdrs.CONTENT_TYPE))
