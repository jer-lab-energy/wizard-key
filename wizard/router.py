import numpy as np
from sentence_transformers import SentenceTransformer

from .schema import CommandMatch
from .memory import lookup_alias


class Router:
    """Routes user input to matching commands using semantic similarity."""

    def __init__(self, command_defs: dict):
        """
        Initialize router with command definitions.

        Args:
            command_defs: Dict mapping command names to command configs with "examples" key.
        """
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.command_defs = command_defs

        # Build flat examples list and example-to-command mapping
        self.examples = []
        self.example_to_command = {}

        for cmd_name, cmd_config in command_defs.items():
            for example in cmd_config.get("examples", []):
                idx = len(self.examples)
                self.examples.append(example)
                self.example_to_command[idx] = cmd_name

        # Pre-encode all examples once
        self.encoded_examples = self.model.encode(self.examples, convert_to_tensor=False)

    def route(self, text: str, threshold: float = 0.42) -> CommandMatch:
        """
        Route input text to best matching command.

        First checks alias memory, then uses semantic similarity.

        Args:
            text: User input text.
            threshold: Similarity threshold (0-1).

        Returns:
            CommandMatch with matched command or "unknown".
        """
        # Check alias memory first
        alias_result = lookup_alias(text)
        if alias_result:
            cmd_name, args = alias_result
            cmd_config = self.command_defs.get(cmd_name, {})
            example = (cmd_config.get("examples") or [""])[0]
            return CommandMatch(command=cmd_name, score=1.0, example=example, args=args)

        # Semantic similarity lookup
        text_embedding = self.model.encode(text, convert_to_tensor=False)

        # Find most similar example
        best_idx = 0
        best_score = -2.0

        for i, enc_example in enumerate(self.encoded_examples):
            sim = self._cosine_similarity(text_embedding, enc_example)
            if sim > best_score:
                best_score = sim
                best_idx = i

        best_cmd = self.example_to_command[best_idx]
        best_example = self.examples[best_idx]

        if best_score < threshold:
            return CommandMatch(command="unknown", score=best_score, example=best_example)

        return CommandMatch(command=best_cmd, score=best_score, example=best_example)

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
