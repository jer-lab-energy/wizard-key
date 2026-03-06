from dataclasses import dataclass, field


@dataclass
class CommandMatch:
    """Represents a matched command from NLP processing."""
    command: str
    score: float
    example: str
    args: dict = field(default_factory=dict)


@dataclass
class ExecutionResult:
    """Represents the result of command execution."""
    ok: bool
    message: str
    data: dict = field(default_factory=dict)
