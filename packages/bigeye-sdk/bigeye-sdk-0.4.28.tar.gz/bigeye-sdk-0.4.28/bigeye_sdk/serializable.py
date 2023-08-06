from __future__ import annotations

import abc
import json
from dataclasses import asdict
from typing import TypeVar

import yaml
from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder
from pydantic_yaml import YamlModelMixin

from bigeye_sdk.bigconfig_validation.validation_context import put_bigeye_yaml_file_to_ix, process_validation_errors, \
    get_validation_error_cnt
from bigeye_sdk.bigconfig_validation.yaml_model_base import YamlModelWithValidatorContext
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import INVALID_OBJECT_TYPE_ERRMSG, \
    POSSIBLE_MATCH_ERRMSG, NO_POSSIBLE_MATCH_ERRMSG
from bigeye_sdk.exceptions.exceptions import FileLoadException
from bigeye_sdk.functions.search_and_match_functions import fuzzy_match
from bigeye_sdk.log import get_logger

log = get_logger(__file__)


class PydanticSubtypeSerializable(YamlModelWithValidatorContext):
    _subtypes_ = dict()

    def __init_subclass__(cls, type=None):
        cls._subtypes_[type or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_real_type_

    @classmethod
    def _convert_to_real_type_(cls, data):
        data_type = None
        if isinstance(data, dict):
            data_type = data.get("type")
        elif data.type in cls._subtypes_:
            return data
        else:
            error_message = INVALID_OBJECT_TYPE_ERRMSG.format(data_type=data_type,
                                                              match_message=NO_POSSIBLE_MATCH_ERRMSG)
            raise FileLoadException(error_message)

        if not data_type:
            error_message = INVALID_OBJECT_TYPE_ERRMSG.format(data_type='None',
                                                              match_message=NO_POSSIBLE_MATCH_ERRMSG)
            raise FileLoadException(error_message)

        sub = cls._subtypes_.get(data_type)

        if sub is None:
            errln = yaml.safe_dump({'type': data_type}, indent=True, sort_keys=False)
            possible_matches = fuzzy_match(data_type, list(cls._subtypes_.keys()), 50)

            if possible_matches:
                pms = [i[1] for i in possible_matches]
                possible_match_message = POSSIBLE_MATCH_ERRMSG.format(possible_matches=", ".join(pms))
            else:
                possible_match_message = NO_POSSIBLE_MATCH_ERRMSG
            PydanticSubtypeSerializable.register_validation_error(
                error_lines=[errln],
                error_message=INVALID_OBJECT_TYPE_ERRMSG.format(data_type=data_type,
                                                                match_message=possible_match_message)
            )
            if possible_matches:
                data['type'] = possible_matches[0]
            return data

        return sub(**data)

    @classmethod
    def parse_obj(cls, obj) -> FILE:
        return cls._convert_to_real_type_(obj)


FILE = TypeVar('FILE', bound='File')

class File(PydanticSubtypeSerializable, YamlModelMixin):
    type: str
    _exclude_defaults: bool = True

    @classmethod
    def load(cls, file_name: str) -> FILE:
        error = None

        log.info(f"Loading file: {file_name}")

        for clazz in File.__subclasses__():
            try:
                with open(file_name, 'r') as fin:
                    file = yaml.safe_load(fin)

                instance = clazz.parse_obj(file)

                put_bigeye_yaml_file_to_ix(file_name=file_name)
                return instance
            except TypeError as e:
                error = e

        if error:
            if get_validation_error_cnt():
                """Processing validation errors if any exist and throw exception."""
                fixme_file_list = process_validation_errors()
                errmsg = f'File is invalid.  File: {file_name}; Error: {error};' \
                         f'\nFIXME Files: {yaml.safe_dump(fixme_file_list)}'
                raise FileLoadException(errmsg)
        else:
            fixme_file_list = process_validation_errors()
            errmsg = f'File is invalid.  File: {file_name}; Error: {error};' \
                     f'\nFIXME Files: {yaml.safe_dump(fixme_file_list)}'
            raise FileLoadException(errmsg)

    def save(self, file: str):
        with open(file, 'w') as fout:
            lines = self.yaml(exclude_unset=True, exclude_none=True, exclude_defaults=self._exclude_defaults,
                              indent=True)
            fout.writelines(lines)


BIGCONFIG_FILE = TypeVar('BIGCONFIG_FILE', bound='BigConfigFile')


class BigConfigFile(File):
    pass


@dataclass
class YamlSerializable(abc.ABC):
    @classmethod
    def load_from_file(cls, file: str):
        print(f'load_from_file class name: {cls.__name__}')
        with open(file, 'r') as fin:
            d = yaml.safe_load(fin)
            bsc = cls(**d)
            if bsc is None:
                raise Exception('Could not load from disk.')
            log.info(f'Loaded instance of {bsc.__class__.__name__} from disk: {file}')
            return bsc

    def to_dict(self, exclude_empty: bool = True):
        return asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v and exclude_empty})

    def save_to_file(self, file: str):
        j = json.dumps(self.to_dict(), indent=True, default=pydantic_encoder, sort_keys=False)
        d = json.loads(j)
        with open(file, 'w') as file:
            yaml.dump(d, file, sort_keys=False)
