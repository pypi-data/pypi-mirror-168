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
from decimal import Decimal
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Type

from jsonschema import ValidationError, validate

from nqsdk.exceptions import ImproperlyConfigured

if TYPE_CHECKING:  # pragma: no cover
    from nqsdk.callback import CallbackResponse
    from .channel import Channel
    from .message import Message, SentMessage, SentMeta
    from .quotas import ProviderQuota


class Provider(ABC):
    """
    Base provider class.

    Attributes:
        label:
            Provider name (slug).
        is_health_check_supported:
            Provider supports health checks.
        is_balance_check_supported:
            Provider is able to return current account balance.
    """

    label: str = ""
    is_health_check_supported: bool = False
    is_balance_check_supported: bool = False

    def __init__(self, *, config: Dict, callback_url: str):
        """
        Args:
            config:
                Provider config.
            callback_url:
                URL template for callbacks.

        Raises:
            nqsdk.exceptions.ImproperlyConfigured:
                Config validation failed.
        """

        self._callback_url = callback_url
        self._config = self.check_config(config=config)

    @property
    def config(self) -> Dict:
        """Provider config."""
        return self._config

    def get_callback_url(self, *, attempt_uid: str) -> str:
        return self._callback_url.format(attempt_uid=attempt_uid)

    def get_quotas(self) -> List[ProviderQuota]:
        return []

    @abstractmethod
    def check_health(self) -> bool:
        pass

    def get_balance(self) -> Optional[Decimal]:
        pass

    @abstractmethod
    def send(self, *, message: Message, channel: str) -> SentMeta:
        """
        Sends message.

        Args:
            message:
            channel:
                Channel label.

        Returns:
            Sent message metadata.

        Raises:
            nqsdk.exception.SentException:
                Message sending failed by some reason reported by provider.
                This type of exception should only be raised if the failure is
                reported by provider. It's not for network errors, etc.
            nqsdk.exception.QuotaExceededException:
                Provider reported that quota was exceeded.
        """

    @abstractmethod
    def check_delivery(self, *, message: SentMessage) -> Optional[SentMeta]:
        pass

    @abstractmethod
    def check_ack(self, *, message: SentMessage) -> Optional[SentMeta]:
        pass

    @abstractmethod
    def handle_delivered(self, *, request) -> Tuple[CallbackResponse, SentMeta]:
        """
        Handles 'message delivered' callback from provider.

        Args:
            request:
                Raw HTTP request from provider's callback.

        Returns:
            Callback response & sent message metadata.

        Raises:
            nqsdk.exceptions.CallbackHandlingException:
                Must be raised in case of handling error.
        """

    @abstractmethod
    def handle_ack(self, *, request) -> Tuple[CallbackResponse, SentMeta]:
        """
        Handles 'message read' callback from provider.

        Args:
            request:
                Raw HTTP request from provider's callback.

        Returns:
            Callback response & sent message metadata.

        Raises:
            nqsdk.exceptions.CallbackHandlingException:
                Must be raised in case of handling error.
        """

    @abstractmethod
    def handle_callback(self, *, request) -> Tuple[CallbackResponse, SentMeta]:
        pass

    @classmethod
    @abstractmethod
    def get_config_schema(cls) -> Dict:
        """JSON schema for config validation."""

    @classmethod
    @abstractmethod
    def get_channels(cls) -> List[Type[Channel]]:
        """List of channels supported by provider."""

    @classmethod
    def check_config(cls, config: Dict) -> Dict:
        """
        Validates provider config against its schema.

        Args:
            config:
                Provider config.

        Returns:
            Provider config.

        Raises:
            nqsdk.exceptions.ImproperlyConfigured:
                Config validation failed.
        """
        try:
            validate(config, cls.get_config_schema())
        except ValidationError as e:
            raise ImproperlyConfigured(e)

        return config
