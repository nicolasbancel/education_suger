import json
import zipfile
from pathlib import Path
from typing import Iterator, Dict, Any, List, Tuple


def iter_messages_from_export_zip(zip_path: Path) -> Iterator[Tuple[str, str]]:
    """
    Itère sur (conversation_id, text) à partir d'un export ChatGPT zip.
    Essaie de trouver conversations.json dans le zip.
    """
    with zipfile.ZipFile(zip_path, "r") as z:
        # Cherche un fichier qui finit par conversations.json
        candidates = [n for n in z.namelist() if n.endswith("conversations.json")]
        if not candidates:
            raise FileNotFoundError(
                "conversations.json introuvable dans le zip d'export."
            )
        name = candidates[0]

        with z.open(name) as f:
            data = json.load(f)

    # La structure peut varier, on fait défensif :
    for conv in data:
        conv_id = conv.get("id") or conv.get("conversation_id") or "unknown"
        mapping = conv.get("mapping", {})
        for node in mapping.values():
            msg = (node or {}).get("message") or {}
            content = msg.get("content") or {}
            parts = content.get("parts") or []
            if parts:
                # parts peut être une liste de strings
                text = "\n".join([p for p in parts if isinstance(p, str)]).strip()
                if text:
                    yield conv_id, text
