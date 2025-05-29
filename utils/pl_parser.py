# utils/pl_parser.py

import re
from pathlib import Path
from typing import List, Tuple

def parse_scenarios(pl_path: Path) -> List[Tuple[str,int,int,str,str]]:
    """
    Extract all scenarios from a Prolog file:
      scenario(Code, scenario(Template, OwnerNearby, Valuable, Env, Legal)).

    Returns a list:
      [(Code, owner_nearby, valuable, environment, legal_context), ...]
    where owner_nearby and valuable are represented as 0/1.
    """
    text = pl_path.read_text(encoding='utf-8')
    # Explanation:
    #  group1 = code
    #  group2 = template (ignored)
    #  group3 = true|false -> owner_nearby
    #  group4 = true|false -> valuable
    #  group5 = environment
    #  group6 = legal_context
    pattern = re.compile(
        r"scenario\(\s*"
        r"([a-zA-Z0-9_]+)\s*,\s*"                # 1: dropped_wallet_1
        r"scenario\(\s*"
        r"[a-zA-Z0-9_]+\s*,\s*"                  # template name (ignored)
        r"(true|false)\s*,\s*"                   # 3: owner_nearby
        r"(true|false)\s*,\s*"                   # 4: valuable
        r"([a-zA-Z0-9_]+)\s*,\s*"                # 5: environment
        r"([a-zA-Z0-9_]+)\s*"                    # 6: legal_context
        r"\)\s*\)\."                             # end of statement
    )
    scenarios = []
    for m in pattern.finditer(text):
        code, onearby, val, env, legal = m.groups()
        scenarios.append((
            code,
            1 if onearby == 'true' else 0,
            1 if val     == 'true' else 0,
            env,
            legal
        ))
    return scenarios
