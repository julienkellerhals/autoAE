class User():
    is_authenticated: bool = None
    is_active: bool = None
    is_anonymous: bool = None
    id: bytes = None
    username: str = None

    def __init__(
        self,
        is_authenticated: bool,
        is_active: bool,
        is_anonymous: bool,
        id: bytes,
        username: str,
    ) -> None:
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous
        self.id = id
        self.username = username

    def get_id(self) -> bytes:
        return self.id