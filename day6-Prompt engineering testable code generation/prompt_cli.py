#!/usr/bin/env python3
"""
Prompt Template CLI

Automate using the five AI coding templates in this folder.

Features:
- List available templates
- Build a prompt from one or more templates
- Replace placeholder `[your task description here]`
- Output to stdout or save/append to a file

Usage examples:
  - List templates:
      python prompt_cli.py --list

  - Build from template 3 with a task description and print:
      python prompt_cli.py --templates 3 --desc "convert CSV to JSON with type conversion"

  - Combine templates 2 and 4, write to prompt.md:
      python prompt_cli.py -t 2 -t 4 -d "parse log files and summarize errors" -o prompt.md

  - Interactive mode (select templates and enter description):
      python prompt_cli.py --interactive

Notes:
- Templates are auto-discovered by pattern `template*.md` in the current folder.
- The CLI extracts the English instruction block inside the first triple-backtick code fence.
- If a template has no placeholder, nothing is replaced (still useful as-is).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


TEMPLATE_GLOB = "template*.md"


@dataclass
class TemplateInfo:
    index: int
    path: Path
    title: str
    english_block: str


def find_templates(base: Path) -> List[TemplateInfo]:
    files = sorted(base.glob(TEMPLATE_GLOB), key=_template_sort_key)
    templates: List[TemplateInfo] = []
    for i, p in enumerate(files, start=1):
        text = p.read_text(encoding="utf-8", errors="ignore")
        title = _extract_title(text) or p.stem
        english = _extract_first_code_block(text) or text.strip()
        templates.append(TemplateInfo(index=i, path=p, title=title, english_block=english.strip()))
    return templates


def _template_sort_key(p: Path) -> Tuple[int, str]:
    m = re.search(r"template(\d+)", p.stem)
    if m:
        return (int(m.group(1)), p.name)
    return (9999, p.name)


def _extract_title(text: str) -> Optional[str]:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _extract_first_code_block(text: str) -> Optional[str]:
    # Extract text between the first pair of triple backticks
    fence = "```"
    start = text.find(fence)
    if start == -1:
        return None
    start += len(fence)
    # Skip optional language identifier on the same line
    # Move to next newline
    newline_pos = text.find("\n", start)
    if newline_pos == -1:
        return None
    content_start = newline_pos + 1
    end = text.find(fence, content_start)
    if end == -1:
        return None
    return text[content_start:end].strip()


def replace_placeholder(english: str, description: Optional[str]) -> str:
    if not description:
        return english
    return english.replace("[your task description here]", description).replace(
        "[此处描述你的任务]", description
    )


def combine_blocks(blocks: Iterable[str]) -> str:
    parts = [b.strip() for b in blocks if b.strip()]
    return "\n\n".join(parts)


def build_prompt(templates: List[TemplateInfo], indices: List[int], desc: Optional[str]) -> str:
    selected = []
    max_index = len(templates)
    for idx in indices:
        if idx < 1 or idx > max_index:
            raise ValueError(f"Template index {idx} is out of range 1..{max_index}")
        selected.append(templates[idx - 1])
    replaced = [replace_placeholder(t.english_block, desc) for t in selected]
    return combine_blocks(replaced)


def interactive_select(templates: List[TemplateInfo]) -> Tuple[List[int], Optional[str]]:
    print("Available templates:")
    for t in templates:
        print(f"  {t.index}. {t.title} ({t.path.name})")
    raw = input("Enter template numbers (e.g., 1 or 1,3,5): ").strip()
    indices = [int(x) for x in re.split(r"\s*,\s*", raw) if x]
    desc = input("Task description to fill in (optional): ")
    return indices, (desc or None)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AI Prompt Template CLI")
    p.add_argument("--list", action="store_true", help="List available templates and exit")
    p.add_argument("-t", "--templates", action="append", help="Template index or filename; can repeat")
    p.add_argument("-d", "--desc", help="Task description to replace placeholder")
    p.add_argument("-o", "--out", help="Write output to file instead of stdout")
    p.add_argument("--append", action="store_true", help="Append to output file if it exists")
    p.add_argument("--interactive", action="store_true", help="Interactive selection mode")
    return p.parse_args(argv)


def resolve_template_indices(arg_values: Optional[List[str]], templates: List[TemplateInfo]) -> List[int]:
    if not arg_values:
        return []
    indices: List[int] = []
    name_to_index = {t.path.name.lower(): t.index for t in templates}
    for v in arg_values:
        v = v.strip()
        if v.isdigit():
            indices.append(int(v))
        else:
            key = v.lower()
            if key in name_to_index:
                indices.append(name_to_index[key])
            else:
                raise ValueError(f"Unknown template reference: {v}")
    return indices


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    base = Path.cwd()
    templates = find_templates(base)
    if not templates:
        print("No templates found (expected files like template1_*.md)", file=sys.stderr)
        return 2

    if args.list:
        for t in templates:
            print(f"{t.index}. {t.title}\n   -> {t.path.name}")
        return 0

    indices: List[int]
    desc: Optional[str] = args.desc

    if args.interactive:
        indices, desc = interactive_select(templates)
    else:
        indices = resolve_template_indices(args.templates, templates)

    if not indices:
        print("No templates selected. Use --interactive or -t to choose.", file=sys.stderr)
        return 2

    try:
        prompt = build_prompt(templates, indices, desc)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2

    if args.out:
        out_path = Path(args.out)
        mode = "a" if args.append else "w"
        with out_path.open(mode, encoding="utf-8") as f:
            if args.append and out_path.exists() and out_path.stat().st_size > 0:
                f.write("\n\n")
            f.write(prompt)
            f.write("\n")
        print(f"Written prompt to {out_path}")
    else:
        print(prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

