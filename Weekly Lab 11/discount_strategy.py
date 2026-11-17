from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy interface: every discount turns an order total into a new total."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the discounted total."""
        pass


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float):
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total that reaches the threshold."""

    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.threshold: float = float(threshold)
        self.amount: float = float(amount)

    def apply(self, total: float) -> float:
        return total - self.amount if total >= self.threshold else total


class StudentDiscount(DiscountStrategy):
    """Fourth strategy (Section 2.4): a flat 5% student discount.
    Added without touching Order or any existing strategy."""

    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)
