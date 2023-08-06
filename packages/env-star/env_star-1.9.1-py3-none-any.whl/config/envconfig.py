import pathlib
import typing
from dataclasses import dataclass

from config import _helpers
from config.exceptions import MissingName

from .config import MISSING, AnyCallable, Config, T
from .enums import Env

StrOrPath = typing.Union[str, pathlib.Path]
# Validator receives an EnvConfig instance and the env_name currently checking
Validator = typing.Callable[['Config'], typing.Callable[[str], bool]]

# Using tuples with integers to prevent bugs with sorting


class OptionalConfig(Config):
    def __init__(
        self,
        required_if: Validator,
        env_file: typing.Optional[StrOrPath],
        mapping: typing.Optional[typing.Mapping[str, str]] = None,
        ignore_default: bool = True,
    ) -> None:
        super().__init__(env_file)
        self._mapping = mapping or self._mapping
        self._ignore_default = ignore_default
        self._required_if = required_if(Config(mapping=self._mapping))

    @_helpers.memoize
    def validate(self, name: str):
        return self._required_if(name)

    def _get_value(
        self,
        name: str,
        default: typing.Any,
        ignore_default: typing.Optional[bool] = None,
    ) -> str:
        ignore_default = (
            self._ignore_default if ignore_default is None else ignore_default
        )
        value: typing.Union[str, object] = self._mapping.get(name, MISSING)
        if self.validate(name) and value is MISSING:
            value = self._file_vals.get(name, MISSING)
        if not ignore_default and value is MISSING:
            value = default
        if value is MISSING:
            raise MissingName(name)
        return typing.cast(str, value)

    def get(
        self,
        name: str,
        cast: typing.Optional[AnyCallable] = None,
        default: typing.Any = MISSING,
        ignore_default: typing.Optional[bool] = None,
    ) -> typing.Any:
        value = self._get_value(name, default, ignore_default)
        return value if cast is None else self._cast(name, value, cast)

    @typing.overload
    def __call__(
        self,
        name: str,
        cast: typing.Callable[[str], T],
        default: typing.Any = MISSING,
        ignore_default: typing.Optional[bool] = None,
    ) -> T:
        ...

    @typing.overload
    def __call__(
        self,
        name: str,
        cast: None = None,
        default: typing.Any = MISSING,
        ignore_default: typing.Optional[bool] = None,
    ) -> str:
        ...

    def __call__(
        self,
        name: str,
        cast: typing.Optional[AnyCallable] = None,
        default: typing.Any = MISSING,
        ignore_default: typing.Optional[bool] = None,
    ) -> typing.Any:
        return self.get(name, cast, default, ignore_default)


ENV_RELEVANCY = {Env.TEST: 0, Env.LOCAL: 1, Env.DEV: 2, Env.PRD: 3}


@dataclass(frozen=True)
class ByRelevancy:

    max_relevancy: Env = Env.LOCAL
    env_name: str = 'ENV'

    if typing.TYPE_CHECKING:

        @property
        def env(self) -> Env:
            ...

    def required_if(self, config: Config):
        env = config(self.env_name, Env)
        object.__setattr__(self, 'env', env)
        expected = ENV_RELEVANCY[self.max_relevancy]

        def validator(_: str):
            return ENV_RELEVANCY[env] <= expected

        return validator


class EnvConfig(OptionalConfig):
    def __init__(
        self,
        by_relevancy: ByRelevancy = ByRelevancy(),
        env_file: StrOrPath = '.env',
        mapping: typing.Optional[typing.Mapping[str, str]] = None,
        ignore_default: bool = True,
    ) -> None:
        self._by_relevancy = by_relevancy
        super().__init__(
            by_relevancy.required_if, env_file, mapping, ignore_default
        )

    @property
    def env(self) -> Env:
        return self._by_relevancy.env
