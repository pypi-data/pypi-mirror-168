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

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .abstract.message import SentMeta
    from .abstract.quotas import Quota
    from .callback import CallbackResponse


class BaseSentException(Exception):
    def __init__(self, *args, meta: SentMeta):
        super().__init__(*args)
        self._meta = meta

    @property
    def meta(self) -> SentMeta:
        return self._meta


class SentException(BaseSentException):
    pass


class DeliveryException(BaseSentException):
    pass


class AckException(BaseSentException):
    pass


class CallbackHandlingException(Exception):
    def __init__(self, *args, response: CallbackResponse):
        super().__init__(*args)
        self._response = response

    @property
    def response(self) -> CallbackResponse:
        return self._response


class ImproperlyConfigured(Exception):
    pass


class QuotaExceededException(Exception):
    def __init__(self, *args, quota: Quota):
        super().__init__(*args)
        self._quota = quota

    @property
    def quota(self) -> Quota:
        return self._quota
