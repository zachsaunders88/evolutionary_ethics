# utils/pl_parser.py

import re
from pathlib import Path
from typing import List, Tuple


def parse_scenarios(pl_path: Path) -> List[Tuple[str, int, int, str, str, int]]:
    """
    Extract all 'scenario' clauses from a Prolog file and return a list of 6-tuples:
      (code, owner_nearby, valuable, environment, legal_context, OwnerTraceability)

    Example Return Value:
      [
        ('dropped_wallet_1', 1, 1, 'many_people_around', 'none', 1),
        ('dropped_wallet_2', 1, 1, 'many_people_around', 'none', 0),
        ...
      ]
    """

    # 1. Read the file using utf-8-sig to automatically skip a BOM if present
    text = pl_path.read_text(encoding='utf-8-sig')

    pattern = re.compile(
        r"scenario\s*\(\s*"                       # 'scenario(' with optional whitespace
        r"([a-zA-Z0-9_]+)\s*,\s*"                 # 1: code
        r"scenario\s*\(\s*"                       # nested 'scenario('
        r"[a-zA-Z0-9_]+\s*,\s*"                   # inner type (ignored)
        r"(true|false)\s*,\s*"                    # 2: owner_nearby
        r"(true|false)\s*,\s*"                    # 3: valuable
        r"([a-zA-Z0-9_]+)\s*,\s*"                 # 4: environment
        r"([a-zA-Z0-9_]+)\s*,\s*"                 # 5: legal_context
        r"(true|false)\s*"                         # 6: OwnerTraceability
        r"\)\s*\)\s*\.\s*",                    # ')).'
        re.IGNORECASE
    )

    scenarios = []
    # 2. Find all single-line scenario clauses with regex
    for m in pattern.finditer(text):
        # m.groups() corresponds exactly to (code, owner_nearby, valuable, environment, legal_context, OwnerTraceability)
        code, onearby, val, env, legal, ownertrace = m.groups()
        scenarios.append((
            code,
            1 if onearby.lower() == 'true' else 0,
            1 if val.lower() == 'true' else 0,
            env,
            legal,
            1 if ownertrace.lower() == 'true' else 0
        ))

    return scenarios
