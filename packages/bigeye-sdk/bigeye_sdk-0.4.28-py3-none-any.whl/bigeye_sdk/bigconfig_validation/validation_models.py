from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any

from pydantic_yaml import YamlModel

from bigeye_sdk.log import get_logger

log = get_logger(__file__)


@dataclass()
class FileMatchResult:
    file_name: str
    lines: Dict[int, str]  # TODO could remove and just have a top line?  Think about reporting.
    error_message: str


class ValidationError(YamlModel):
    error_lines: List[str]
    erroneous_configuration_cls_name: str
    error_message: str
    error_context_lines: List[str] = None
    matched_in_file: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.warning(self.error_message)
