from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Union, Any, Dict
from copy import copy
from zpy.utils.funcs import Maybe, if_get
from zpy.utils.values import if_null_get

T = TypeVar("T")
S = TypeVar("S")


class UCMeta:
    def __init__(self, identifier: str, key_identifier: str = None) -> None:
        self.id = identifier
        if key_identifier:
            setattr(self, key_identifier, identifier)


class Selectable:
    def __init__(self, identifier: str, key_identifier: str = None, weight: float = 1.0) -> None:
        """

        @param identifier: value of selector based. E.g. UserCreator
        @param key_identifier: key of selector based. E.g. action
        """
        if not key_identifier:
            key_identifier = 'id'
        self.weight = weight
        self.identifiers: Dict[str, Dict[str, str]] = {
            key_identifier: {"value": identifier, "weight": weight}
        }

    def configure_for_all(self, weight: float = 2.0):
        self.identifiers['*'] = {"value": '*', "weight": weight}

    def configure(self, uc_identifier: Any, weight: float, key_identifier: Any = 'id'):
        self.identifiers[key_identifier] = {
            "value": uc_identifier,
            "weight": weight
        }


class UseCase(ABC, Generic[T, S]):
    def __init__(self, name: Any = None):
        self.name = name

    @abstractmethod
    def execute(self, input_data: T, *args, **kwargs) -> S:
        """Execute use case"""
        pass


class UseCaseSelector(UseCase, UCMeta):

    def __init__(self, use_cases: List[Union[UseCase, UCMeta, Any]], action_keys: List[str] = None,
                 key_uc_identifier: str = 'id', selector_id='default', payload_keys: List[str] = None):
        UCMeta.__init__(self, identifier=selector_id)
        self.cases = {getattr(x, key_uc_identifier): x for x in use_cases}
        self.action_keys = if_null_get(action_keys, ['action'])
        self.key_identifier = key_uc_identifier
        self.payload_keys = if_null_get(payload_keys, ['payload'])

    def execute(self, data: dict, context: Any = None, *args, **kwargs) -> dict:
        action = None
        for key_action in self.action_keys:
            if key_action in data:
                action = key_action
                break
        if action is None:
            raise ValueError(f'Request provided is malformed. Missing {action} key!')

        operation: Union[UseCase, UCMeta] = self.cases.get(data[action], None)

        if not operation:
            raise ValueError(f"Use case for action: {data['action']} not registered in selector.")

        payload_key = None
        for pk in self.payload_keys:
            if pk in data:
                payload_key = pk
                break

        payload = data.get(payload_key, data)
        return operation.execute(payload, context=context)


class CaseSelector(UseCase, Selectable):

    def __init__(self, use_cases: List[Union[UseCase, Selectable, Any]], action_keys: List[str] = None,
                 key_uc_identifier: str = 'id', selector_id='default', payload_keys: List[str] = None,
                 payload_mutation: bool = False):
        Selectable.__init__(self, identifier=selector_id, key_identifier=key_uc_identifier)
        self.action_keys = if_null_get(action_keys, ['action'])
        self.payload_keys = if_null_get(payload_keys, ['payload'])
        self.allow_payload_mutation = payload_mutation
        self.cases = Maybe(use_cases) \
            .bind(self.__group_cases) \
            .bind(self.__sort_cases) \
            .value

    @staticmethod
    def __group_cases(cases: List[Union[UseCase, Selectable, Any]]):
        group_to_sort = {}
        for case in cases:
            for k, v in case.identifiers.items():
                if v['value'] not in group_to_sort:
                    group_to_sort[v['value']] = {
                        v['weight']: case
                    }
                    continue
                group_to_sort[v['value']][v['weight']] = case

        return group_to_sort

    @staticmethod
    def __sort_cases(cases: Dict[str, Dict[Any, Union[UseCase, Selectable, Any]]]):
        return {c: [x[1] for x in sorted(cases[c].items())] for c in cases}

    def execute(self, data: dict, context: Any = None, *args, **kwargs) -> List[Any]:
        action = None
        for key_action in self.action_keys:
            if key_action in data:
                action = key_action
                break

        if action is None:
            raise ValueError(f'Request provided is malformed. Missing {action} key!')

        cases_to_execute: List[Union[UseCase, Selectable]] = self.cases.get(data[action], [])
        cases_to_execute = sorted(cases_to_execute + self.cases.get('*', []), key=lambda x: x.weight)

        if not cases_to_execute:
            raise ValueError(f"Use case for action: {data['action']} not registered in selector.")

        payload_key = None
        for pk in self.payload_keys:
            if pk in data:
                payload_key = pk
                break

        payload = data.get(payload_key, data)
        return [case.execute(input_data=if_get(self.allow_payload_mutation, payload, copy(payload)), context=context)
                for case in cases_to_execute]
