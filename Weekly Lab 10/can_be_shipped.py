from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """
    Interface-style contract: any class that can be shipped must be able
    to calculate its shipping cost.
    """

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the cost of shipping this object."""
        pass