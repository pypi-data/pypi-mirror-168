import argparse
from typing import List, Dict, Any, MethodType

from dataclasses import dataclass, field
from carlyleconfig.plugins import BasePlugin
from carlyleconfig import ConfigKey


@dataclass
class ArgParseProvider:
    name: str
    args: Dict[str, Any]

    def provide(self, name: str) -> Any:
        return getattr(args, name)


def factory(name: str):
    provider = ArgParseProvider(name, {})
    return provider


@dataclass
class ArgParsePlugin(BasePlugin):
    factory_name: str = 'argparse'
    parser: argparse.ArgumentParser

    def inject_factory_method(self, key: ConfigKey) -> ConfigKey:
        setattr(key, self.factory_name, MethodType(factory, key, ConfigKey))
        return key
