"""
Copyright (c) 2022 Inqana Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import json
import random
import uuid
from datetime import datetime
from decimal import Decimal
from importlib import resources
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Type

import pytz
import requests
from requests import Response

from nqsdk.abstract.channel import Channel
from nqsdk.abstract.provider import Provider
from .message import DummySentMeta
from .quotas import PerHourQuota, PerSecondQuota

if TYPE_CHECKING:  # pragma: no cover
    from nqsdk.abstract.message import Message, SentMessage, SentMeta
    from nqsdk.abstract.quotas import ProviderQuota
    from nqsdk.callback import CallbackResponse


class DummyProvider(Provider):

    label = "Dummy provider"
    is_health_check_supported = True
    is_balance_check_supported = True

    @classmethod
    def get_channels(cls) -> List[Type[Channel]]:
        channels = []
        for label in [
            "email",
            "dummy",
            "push",
            "sms",
            "phone",
            "telegram",
            "viber",
            "whatsapp",
            "icq",
        ]:
            channels.append(Channel.create(label=label))

        return channels

    @classmethod
    def get_config_schema(cls) -> Dict:
        return json.loads(
            resources.files("nqsdk.dummy").joinpath("resources/config_schema.json").read_text()
        )

    @classmethod
    def get_quotas(cls) -> List[ProviderQuota]:
        return [PerSecondQuota(), PerHourQuota()]

    def check_health(self) -> bool:
        self._request(key="health_check")

        return True

    def get_balance(self) -> Optional[Decimal]:
        self._request(key="balance_get")

        return Decimal(f"{random.uniform(1.0, 1000.0 * 10):.2f}")

    def send(self, *, message: Message, channel: str) -> SentMeta:
        data = {
            "recipient_id": message.get_recipient_id(),
            "signature": message.get_signature(channel=channel),
            "content": message.get_content(channel=channel),
        }

        # If 'callback_url_param' is set then we need to send it in each request
        if self.config.get("callback_url_param", False):
            data[self.config["callback_url_param"]] = self.get_callback_url(
                attempt_uid=message.delivery_attempt
            )

        self._request(key="send", data=data)

        return DummySentMeta(
            message=message, ext_id=uuid.uuid4().hex, dt_sent=datetime.now(tz=pytz.timezone("UTC"))
        )

    def check_delivery(self, *, message: SentMessage) -> Optional[SentMeta]:
        self._request(key="delivery_check", data={"message_id": message.ext_id})
        if random.choice([True, False]):
            return DummySentMeta(
                message=message, dt_delivered=datetime.now(tz=pytz.timezone("UTC"))
            )

    def check_ack(self, *, message: SentMessage) -> Optional[SentMeta]:
        self._request(key="ack_check", data={"message_id": message.ext_id})
        if random.choice([True, False]):
            return DummySentMeta(message=message, dt_ack=datetime.now(tz=pytz.timezone("UTC")))

    def handle_delivered(self, *, request) -> Tuple[CallbackResponse, SentMeta]:
        pass

    def handle_ack(self, *, request) -> Tuple[CallbackResponse, SentMeta]:
        pass

    def handle_callback(self, *, request) -> Tuple[CallbackResponse, SentMeta]:
        pass

    def _request(self, key: str, data: Dict = None) -> Optional[Response]:
        options = self._get_request_options(key)
        if options:
            if options["method"] == "get":
                options["params"] = data
            else:
                options["json"] = data

            resp = requests.request(**options)
            if resp.status_code == 200:
                return resp
            else:
                resp.raise_for_status()

    def _get_request_options(
        self, key: str, default_method: str = "get"
    ) -> Optional[Dict[str, Any]]:
        url = self.config.get(f"{key}_url")
        if url:
            options = {"url": url, "method": self.config.get(f"{key}_url_method", default_method)}

            auth_header = self.config.get("auth_header")
            auth_token = self.config.get("auth_token")
            if auth_header and auth_token:
                options["headers"] = {auth_header: auth_token}

            return options
