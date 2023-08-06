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

from abc import ABC, abstractmethod
from datetime import datetime
from typing import IO, List, Optional, Union


class Attachment(ABC):
    @abstractmethod
    def get_content_type(self) -> str:
        pass

    @abstractmethod
    def get_content(self) -> Union[str, bytes, IO]:
        pass


class Message(ABC):
    @property
    @abstractmethod
    def delivery_attempt(self) -> str:
        """Returns unique delivery attempt ID."""

    @property
    @abstractmethod
    def ext_id(self) -> Optional[str]:
        """Sent message ID assigned by provider."""

    @abstractmethod
    def get_recipient_id(self) -> str:
        """
        Returns external ID like phone number or username where provider needs to send the message.

        Returns:
            Recipient ID
        """

    def get_signature(self, *, channel: str = None) -> Optional[str]:
        """
        Returns sender signature.

        Args:
            channel:
                Channel label.

        Returns:
            Sender signature.
        """

    @abstractmethod
    def get_content(self, *, channel: str = None) -> str:
        pass

    def get_attachments(self, *, channel: str = None) -> Optional[List[Attachment]]:
        pass


class SentMessage(Message, ABC):
    @property
    @abstractmethod
    def ext_id(self) -> str:
        """Sent message ID assigned by provider."""


class SentMeta(ABC):
    @property
    @abstractmethod
    def delivery_attempt(self) -> str:
        """Unique delivery attempt ID."""

    @property
    @abstractmethod
    def ext_id(self) -> Optional[str]:
        """Sent message ID assigned by provider."""

    @property
    @abstractmethod
    def dt_sent(self) -> Optional[datetime]:
        """Timezone aware date & time the message was sent."""

    @property
    def dt_delivered(self) -> Optional[datetime]:
        """Timezone aware date & time the message was delivered."""
        return None

    @property
    def dt_ack(self) -> Optional[datetime]:
        """Timezone aware date & time the message was read."""
        return None
