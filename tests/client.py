import contextlib
from enum import IntEnum
from functools import wraps
from json import JSONDecodeError
from urllib.parse import urljoin

import httpx
from tests import settings

def async_client(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with httpx.AsyncClient() as client:
            return await func(self, client, *args, **kwargs)

    return wrapper


class BaseClient:
    """Базовый класс для реализации API клиентов."""
    @staticmethod
    def _build_url(endpoint):
        """Принимает название endpoint'а и возвращает URL, готовый к отправке запроса."""
        return urljoin(settings.BACKEND_API_URL, endpoint)


class FAQClient(BaseClient):
    @async_client
    async def fetch_sections(self, client):
        try:
            response = await client.get(self._build_url('/faq/sections/'))
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = []

        return response

    @async_client
    async def fetch_subsection(self, client, telegram_id, section_id):
        try:
            response = await client.get(
                self._build_url('/faq/sections/subsection/'),
                params={'parent': section_id, 'telegram_id': telegram_id}
            )
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = {'description': '', 'sections': []}

        return response

    @async_client
    async def fetch_parent_sections(
        self,
        client,
        telegram_id,
        parent_section_id,
        last_clicked_type,
    ):
        try:
            response = await client.get(
                self._build_url('/faq/sections/parent/'),
                params={
                    'parent': parent_section_id,
                    'type': last_clicked_type,
                    'telegram_id': telegram_id,
                }
            )
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = {'description': '', 'sections': []}

        return response

    @async_client
    async def fetch_answer(self, client, telegram_id, section_id, answer_id=None):
        try:
            response = await client.get(
                self._build_url(f'/faq/sections/{section_id}/'),
                params={'telegram_id': telegram_id, 'answer_id': answer_id},
            )
            response.raise_for_status()
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = {}

        return response

    @async_client
    async def search_sections(self, client, telegram_id, query):
        try:
            response = await client.get(
                self._build_url('/faq/sections/search/'),
                params={
                    'query': query,
                    'telegram_id': telegram_id,
                },
            )
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = {}

        return response


class GlossaryClient(BaseClient):
    """Реализует методы для работы со словарем."""

    @async_client
    async def search_terms(self, client, query):
        try:
            response = await client.get(
                self._build_url(f'/glossary/terms/search/'),
                params={
                    'query': query,
                },
            )
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = {}

        return response

    @async_client
    async def search_term_id(self, client, query):
        """Найти термин по ID."""
        try:
            response = await client.get(
                self._build_url(f'/glossary/terms/search_id/'),
                params={
                    'query': query,
                },
            )
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = {}

        return response
    
    @async_client
    async def search_term_an_column(self, client, query, column):
        """Найти термин по указанной колонке."""
        try:
            response = await client.get(
                self._build_url(f'/glossary/terms/search_column/'),
                params={
                    'query': query,
                    'column': column,
                },
            )
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = {}

        return response
    
class UserClient(BaseClient):
    async def _request_registered_users(self, client, notification_id, page):
        response = await client.get(
            self._build_url(f'/users/product-user/registered/'),
            params={'page': page, 'notification_id': notification_id},
        )
        response.raise_for_status()

        return response.json()

    @async_client
    async def fetch_user(self, client, telegram_id):
        try:
            response = await client.get(
                self._build_url(f'/users/product-user/{telegram_id}/'),
            )
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError, ):
            response = {}

        return response

    @async_client
    async def check_email(self, client, telegram_id, email):
        response = await client.get(
            self._build_url(f'/users/product-user/{telegram_id}/check-email/'),
            params={'email': email},
        )

        if response.status_code > 200:
            if response.status_code == _HTTP_404_NOT_FOUND_STATUS:
                raise exceptions.UserDoesNotExist
            if response.status_code == _HTTP_403_FORBIDDEN:
                raise exceptions.UserNotAllowed

            raise exceptions.RequestFailed

        return response.json().get('email')

    @async_client
    async def check_phone(self, client, telegram_id, phone):
        response = await client.get(
            self._build_url(f'/users/product-user/{telegram_id}/check-phone/'),
            params={'phone': phone},
        )

        if response.status_code > 200:
            if response.status_code == _HTTP_404_NOT_FOUND_STATUS:
                raise exceptions.UserDoesNotExist

            raise exceptions.RequestFailed

        return response.json().get('email')

    @async_client
    async def check_code(self, client, telegram_id, code):
        response = await client.get(
            self._build_url(f'/users/product-user/{telegram_id}/check-code/'),
            params={'code': code},
        )

        if response.status_code > 200:
            if response.status_code == _HTTP_401_UNAUTHORIZED:
                raise exceptions.InvalidCode

            if response.status_code == _HTTP_403_FORBIDDEN:
                raise exceptions.UserIsBanned

            raise exceptions.RequestFailed

    @async_client
    async def fetch_legal_entities(self, client, telegram_id):
        try:
            response = await client.get(
                self._build_url(f'/users/product-user/{telegram_id}/legal-entities/'),
            )
            response.raise_for_status()
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError,):
            response = []

        return response

    @async_client
    async def create_log(self, client, telegram_id, action_flag, message,
            user_input='', context=None, config=None):
        """Создаст лог-запись"""
        
        previous_flag=0
        bot_answer=''
        bot_kb=''
        if context:
            if 'previous_flag' in context.user_data:
                previous_flag=context.user_data['previous_flag']
            context.user_data['previous_flag']=action_flag

        if config:
            if config.keyboard:
                bot_kb=str([[btn.caption for btn in row] for row in config.keyboard])
            bot_answer=(f'{str(config.description)}\n{bot_kb}')

        with contextlib.suppress(JSONDecodeError, httpx.HTTPError, ):
            await client.post(
                self._build_url(f'/users/log/'),
                json={
                    'user': telegram_id,
                    'action_flag': action_flag,
                    'previous_flag': previous_flag,
                    'change_message': message,
                    'user_input': user_input,
                    'bot_answer': bot_answer,
                },
            )

    @async_client
    async def fetch_registered(self, client, notification_id, page=1):
        """Запрашивает постранично пользователей и возвращает их."""

        users = []
        try:
            response = await self._request_registered_users(client, notification_id, page)
        except (JSONDecodeError, httpx.HTTPError,):
            return users

        users += response['results']
        if response['count'] > len(users):
            users += await self.fetch_registered(notification_id, page=page + 1)

        return users


class MailClient(BaseClient):
    @async_client
    async def send_mail(self, client, data):
        try:
            response = await client.post(
                self._build_url(f'/mail/send-mail/'),
                json=data,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise exceptions.RequestFailed from exc


class NotificationClient(BaseClient):
    """Реализует методы для работы с уведомлениями."""

    @async_client
    async def next_notification(self, client):
        """Отправляет запрос на получение уведомления, которого нужно отправить."""

        try:
            response = await client.get(
                self._build_url(f'/notifications/notifications/next/'),
            )
            response.raise_for_status()
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError,):
            response = []

        return response

    @async_client
    async def mark_notification_as_received(self, client, notification_id, count_recipients):
        """Отправляет запрос на пометку указанного уведомления как доставленного (received)."""

        with contextlib.suppress(JSONDecodeError, httpx.HTTPError,):
            await client.patch(
                self._build_url(f'/notifications/notifications/{notification_id}/'),
                data={
                    'status': _NOTIFICATION_RECEIVED_STATUS,
                    'count_recipients': count_recipients,
                },
            )


class MainClient(BaseClient):
    """Реализует методы для работы с основным содержимым."""

    @cache(60 * 20)
    @async_client
    async def fetch_caption(self, client, caption_name):
        """Отправляет запрос на получение текстовки."""

        try:
            response = await client.get(
                self._build_url(f'/main/captions/{caption_name}/'),
            )
            response.raise_for_status()
            response = response.json()
        except (JSONDecodeError, httpx.HTTPError,):
            response = None

        return response
