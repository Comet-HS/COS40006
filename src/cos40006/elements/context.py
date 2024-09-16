from typing import Any

class ContextManager:
    def __init__(self, aiko: Any = None, message: Any = None) -> None:
        self.aiko = aiko
        self.message = message
        self.protocol = None
        self.activate()

    def activate(self) -> "ContextManager":
        global _CONTEXT
        _CONTEXT = self
        return self

    def __enter__(self) -> "ContextManager":
        return self.activate()

    def __exit__(self, *args: Any) -> None:
        pass

    def set_protocol(self, protocol: str) -> None:
        """Set the protocol attribute."""
        self.protocol = protocol  # Store the protocol as an instance variable
        print(f"Protocol set to: {protocol}")

    def get_implementation(self, name: str):
        """Return the implementation class based on the provided name."""
        if name == "PipelineElement":
            from pipelines.elements import PE_SpeechtoText  
            return PE_SpeechtoText
        return None

    def get_context(self) -> Any:
        global _CONTEXT
        return _CONTEXT
