from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AnalysisStepUpdateStatus(Enums.KnownString):
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AnalysisStepUpdateStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of AnalysisStepUpdateStatus must be a string (encountered: {val})")
        newcls = Enum("AnalysisStepUpdateStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AnalysisStepUpdateStatus, getattr(newcls, "_UNKNOWN"))
