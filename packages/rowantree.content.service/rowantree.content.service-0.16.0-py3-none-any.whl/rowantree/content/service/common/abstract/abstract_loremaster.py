""" Abstract Lore Master Definition """
from abc import abstractmethod

from pydantic import BaseModel


class AbstractLoremaster(BaseModel):
    """Abstract Lore Master"""

    @abstractmethod
    def generate_event(self):
        """Generate Event"""
