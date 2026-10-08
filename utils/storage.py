import json
from datetime import datetime
from pathlib import Path

from models.session import Session


CONVERSATION_DIR = Path("data/conversations")


def create_session(MODEL: str) -> Session:
    CONVERSATION_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()

    session_id = f"{MODEL}_{now.strftime('%Y%m%d_%H%M%S')}"

    return Session(
        session_id=session_id,
        created_at=now,
        updated_at=now,
        messages=[],
    )


def save_session(session: Session):
    CONVERSATION_DIR.mkdir(parents=True, exist_ok=True)

    session.updated_at = datetime.now()

    file_path = CONVERSATION_DIR / f"{session.session_id}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            session.model_dump(mode="json"),
            file,
            indent=4,
        )


def load_session(session_id: str) -> Session:
    file_path = CONVERSATION_DIR / f"{session_id}.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return Session.model_validate(data)


def delete_session(session_id: str):
    file_path = CONVERSATION_DIR / f"{session_id}.json"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Session '{session_id}' does not exist."
        )

    file_path.unlink()


def list_sessions() -> list[str]:
    CONVERSATION_DIR.mkdir(parents=True, exist_ok=True)

    return sorted(
        file.stem
        for file in CONVERSATION_DIR.glob("*.json")
    )