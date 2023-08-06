from ..base import RequestBehaviour


class VoidTransaction(RequestBehaviour):
    def __init__(self):
        super().__init__()

        self.payment_uuid: str = None
        """Payment UUID"""

        self.void_reason: str = None
        """Reason for void the order"""
