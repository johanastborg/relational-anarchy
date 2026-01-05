from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class Agent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def log(self, message: str):
        logger.info(f"[{self.name}] {message}")
