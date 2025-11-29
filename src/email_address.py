class EmailAddress:
    def __init__(self, address: str):
        self._address = self.normalize_address(address)
        if not self._check_correct_email():
            raise ValueError(f"Invalid email address: {self._address}")

    @property
    def address(self) -> str:
        return self._address

    @property
    def masked(self) -> str:
        login, domain = self._address.split('@', 1)
        return f"{login[:2]}***@{domain}"

    def normalize_address(self, addr: str) -> str:
        return addr.strip().lower()

    def _check_correct_email(self) -> bool:
        if '@' not in self._address:
            return False
        domain = self._address.split('@')[-1]
        return domain.endswith(('.com', '.ru', '.net'))

    def __str__(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return self.masked
