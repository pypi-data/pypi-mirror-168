from aiohttp import hdrs
from heaserver.service.representor import cj

from .fileawss3testcase import AWSS3FileTestCase
from heaserver.service.testcase.mixin import DeleteMixin, GetAllMixin, GetOneMixin, PutMixin


class TestDeleteFile(AWSS3FileTestCase, DeleteMixin):
    pass


class TestGetFiles(AWSS3FileTestCase, GetAllMixin):
    async def test_options_status_files(self):
        """Checks if an OPTIONS request for all the files succeeds with status 200."""
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_options_files(self):
        """
        Checks if the "Allow" header in a response to an OPTIONS request for all the files contains GET, DELETE, HEAD,
        and OPTIONS and contains neither POST nor PUT.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        allow = {method.strip() for method in obj.headers.get(hdrs.ALLOW).split(',')}
        self.assertEqual({'GET', 'DELETE', 'HEAD', 'OPTIONS'}, allow)

    async def test_methods_not_allowed(self) -> None:
        """
        Checks if all the methods (except POST) not in the "Allow" header in a response to an OPTIONS request for all
        the files fail with status 405.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        allowed_methods = {method.strip() for method in obj.headers[hdrs.ALLOW].split(',')}
        all_methods = {'HEAD', 'OPTIONS', 'PUT', 'GET', 'DELETE'}
        prohibited_methods = all_methods - allowed_methods
        resps = {}
        for prohibited in prohibited_methods:
            obj = await self.client.request(prohibited,
                                            (self._href / '').path,
                                            headers=self._headers)
            resps |= {prohibited: obj.status}
        self.assertEqual(dict(zip(prohibited_methods, [405] * len(prohibited_methods))), resps)


class TestGetFile(AWSS3FileTestCase, GetOneMixin):
    async def test_options_status_file(self):
        """Checks if an OPTIONS request for a single file succeeds with status 200."""
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_options_file(self):
        """
        Checks if the "Allow" header in a response to an OPTIONS request for a single file contains GET, POST, DELETE,
        HEAD, and OPTIONS and does not contain PUT.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        allow = {method.strip() for method in obj.headers.get(hdrs.ALLOW).split(',')}
        self.assertEqual({'GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'}, allow)

    async def test_methods_not_allowed(self) -> None:
        """
        Checks if all the methods not in the "Allow" header in a response to an OPTIONS request for a single file
        fail with status 405.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        allowed_methods = {method.strip() for method in obj.headers.get(hdrs.ALLOW).split(',')}
        all_methods = {'HEAD', 'OPTIONS', 'POST', 'PUT', 'GET', 'DELETE'}
        prohibited_methods = all_methods - allowed_methods
        resps = {}
        for prohibited in prohibited_methods:
            obj = await self.client.request(prohibited,
                                            (self._href / self._id()).path,
                                            headers=self._headers)
            resps |= {prohibited: obj.status}
        self.assertEqual(dict(zip(prohibited_methods, [405] * len(prohibited_methods))), resps)

    # Currently backs 200 because it uses the same request handler as the normal get
    # async def test_get_status_opener_choices(self) -> None:
    #     """Checks if a GET request for the opener for a file succeeds with status 300."""
    #     obj = await self.client.request('GET',
    #                                     (self._href / self._id() / 'opener').path,
    #                                     headers=self._headers)
    #     self.assertEqual(300, obj.status)

    async def test_get_opener_hea_default_exists(self) -> None:
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
