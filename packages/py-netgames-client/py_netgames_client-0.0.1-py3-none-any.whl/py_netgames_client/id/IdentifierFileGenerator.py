import logging
import uuid
from pathlib import Path
from typing import Optional
from uuid import UUID


class IdentifierFileGenerator:
    _logger: logging.Logger

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger("py_netgames_client")

    def get_or_create_identifier(self) -> UUID:
        path = Path("gameid.txt")
        if game_id := self._get_id(path):
            self._logger.info(f"Found game_id at {path.absolute()} with value {game_id}")
            return game_id
        else:
            game_id = uuid.uuid4()
            path.write_text(str(game_id))
            self._logger.info(f"Creating game_id at {path.absolute()} with value {game_id}")
            return game_id

    def _get_id(self, path: Path) -> Optional[UUID]:
        try:
            if path.is_file():
                return UUID(path.read_text())
            else:
                return None
        except Exception:
            return None
