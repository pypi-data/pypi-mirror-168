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

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from nqsdk.abstract.message import SentMeta

if TYPE_CHECKING:  # pragma: no cover
    from nqsdk.abstract.message import Message


class DummySentMeta(SentMeta):
    def __init__(
        self,
        *,
        message: Message,
        ext_id: str = None,
        dt_sent: datetime = None,
        dt_delivered: datetime = None,
        dt_ack: datetime = None,
    ):
        self._message = message
        self._ext_id = ext_id
        self._dt_sent = dt_sent
        self._dt_delivered = dt_delivered
        self._dt_ack = dt_ack

    @property
    def delivery_attempt(self) -> str:
        return self._message.delivery_attempt

    @property
    def ext_id(self) -> Optional[str]:
        return self._ext_id

    @property
    def dt_sent(self) -> Optional[datetime]:
        return self._dt_sent

    @property
    def dt_delivered(self) -> Optional[datetime]:
        return self._dt_delivered

    @property
    def dt_ack(self) -> Optional[datetime]:
        return self._dt_ack
