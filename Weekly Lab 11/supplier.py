class Supplier:
    """Represents a product supplier (Association with Product)."""

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = str(supplier_id)
        self.name: str = str(name)
        self.contact_email: str = str(contact_email)

    def display_information(self) -> None:
        """Displays supplier details."""
        print(f"Supplier ID: {self.supplier_id} | Name: {self.name} | Contact: {self.contact_email}")

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
        return cls(
            supplier_id=data["supplier_id"],
            name=data["name"],
            contact_email=data["contact_email"]
        )