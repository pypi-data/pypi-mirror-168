from pathlib import Path


class Auth:
    @staticmethod
    def _get_auth_file() -> Path:
        return Path.home() / ".config" / "arvan-cli" / "auth"

    @staticmethod
    def create(api_key: str) -> None:
        auth_file = Auth._get_auth_file()
        auth_file.parent.mkdir(parents=True, exist_ok=True)
        with open(auth_file, "w") as f:
            f.write(api_key)

    @staticmethod
    def exists() -> bool:
        return Auth._get_auth_file().exists()

    @staticmethod
    def get() -> str:
        with open(Auth._get_auth_file(), "r") as f:
            return f.read()
