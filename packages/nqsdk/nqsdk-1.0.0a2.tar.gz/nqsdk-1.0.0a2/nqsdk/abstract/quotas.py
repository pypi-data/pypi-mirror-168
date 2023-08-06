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
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:  # pragma: no cover
    from nqsdk.enums import QuotaIdentityType, QuotaType


class Quota(ABC):
    @property
    @abstractmethod
    def quota_type(self) -> QuotaType:
        pass


class ProviderQuota(Quota, ABC):
    @property
    def quota_type(self) -> QuotaType:
        return QuotaType.PROVIDER

    @property
    @abstractmethod
    def identity_type(self) -> QuotaIdentityType:
        pass


class ProviderStaticQuota(ProviderQuota, ABC):
    @property
    @abstractmethod
    def limit(self) -> int:
        pass

    @property
    @abstractmethod
    def frame(self) -> int:
        pass


class ProviderDynamicQuota(ProviderQuota, ABC):
    @property
    @abstractmethod
    def delay(self) -> Optional[int]:
        pass

    @property
    @abstractmethod
    def until(self) -> Optional[datetime]:
        pass
