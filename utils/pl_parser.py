# utils/pl_parser.py

import re
from pathlib import Path
from typing import List, Tuple

def parse_scenarios(pl_path: Path) -> List[Tuple[str,int,int,str,str,int]]:
    """
    从 Prolog 文件中提取所有 scenario 语句，返回一个列表，每个元素是一个 6 元组：
      (code, owner_nearby, valuable, environment, legal_context, OwnerTraceability)

    例如：
      [
        ('dropped_wallet_1', 1, 1, 'many_people_around', 'none', 1),
        ('dropped_wallet_2', 1, 1, 'many_people_around', 'none', 0),
         ...
      ]
    """

    # ─── ① 用 utf-8-sig 自动跳过文件开头可能带的 BOM（如果 .pl 行首有 BOM，用 utf-8 会导致第一个字符不是 ":-"） ───
    text = pl_path.read_text(encoding='utf-8-sig')

    pattern = re.compile(
        r"scenario\s*\(\s*"                      # “scenario(” 之间允许空白
        r"([a-zA-Z0-9_]+)\s*,\s*"                # 1: code
        r"scenario\s*\(\s*"                      # 嵌套 “scenario(”
        r"[a-zA-Z0-9_]+\s*,\s*"                  # (inner) type (ignored)
        r"(true|false)\s*,\s*"                   # 2: owner_nearby
        r"(true|false)\s*,\s*"                   # 3: valuable
        r"([a-zA-Z0-9_]+)\s*,\s*"                # 4: environment
        r"([a-zA-Z0-9_]+)\s*,\s*"                # 5: legal_context
        r"(true|false)\s*"                       # 6: OwnerTraceability
        r"\)\s*\)\s*\.\s*",                      # ")) ."
        re.IGNORECASE
    )

    scenarios = []
    # ─── ④ 用正则去抓所有“单行” scenario 语句 ───
    for m in pattern.finditer(text):
        # m.groups() 顺序正好对应 (code, owner_nearby, valuable, environment, legal_context, OwnerTraceability)
        code, onearby, val, env, legal, ownertrace = m.groups()
        scenarios.append((
            code,
            1 if onearby    .lower() == 'true' else 0,
            1 if val        .lower() == 'true' else 0,
            env,
            legal,
            1 if ownertrace .lower() == 'true' else 0
        ))

    return scenarios
