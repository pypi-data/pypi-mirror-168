import typing
import aiohttp

from . import base
from tippisell_api import methods, models


class Client(base.BaseClient):
    async def get_user(self, user_id=None, telegram_id=None) -> models.User:
        result = await self._request(methods.GetUser(user_id=user_id, telegram_id=telegram_id))
        return models.User(**result)

    async def upload_goods(self, product_id: int, data: typing.List[str]) -> int:
        result = await self._request(methods.UploadGoods(product_id=product_id, data=data))
        return result["count"]

    async def _request(self, method: methods.BaseMethod):
        method.prepare_shop_id(self.shop_id)
        method.prepare_api_key(self.api_key)
        method.validate()

        async with aiohttp.ClientSession() as session:
            response = await session.request(**self._http_request_kwargs(method))
            await response.read()

        result = await response.json()
        self._check_response(models.HttpResponse(status_code=response.status, result=result))

        return result["result"]
