from dataclasses import dataclass, field


@dataclass
class BasePlugin:
    factory_name: str = field(init=False)
