#!/usr/bin/env python3
"""Distill (chatconv.py): convert chat transcripts between plain text and JSONL.

Text format: lines starting with "User:" or "Assistant:" (case-insensitive).
Lines without a prefix continue the previous message.
JSONL format: one conversation per line: {"messages":[{"role":..,"content":..}]}
"""
import argparse, json, re, sys

PREFIX = re.compile(r"^\s*(user|assistant|system)\s*:\s?(.*)$", re.I)

def parse_text(text):
    msgs = []
    for line in text.splitlines():
        m = PREFIX.match(line)
        if m:
            msgs.append({"role": m.group(1).lower(), "content": m.group(2)})
        elif msgs:
            msgs[-1]["content"] += "\n" + line
    for m in msgs:
        m["content"] = m["content"].strip()
    return msgs

def to_text(msgs):
    return "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in msgs) + "\n"

def txt2jsonl(text):
    """Conversations in the text are separated by a line containing only ---"""
    convs = [c for c in re.split(r"^\s*---\s*$", text, flags=re.M) if c.strip()]
    msgs = [parse_text(c) for c in convs]
    return "".join(json.dumps({"messages": m}, ensure_ascii=False) + "\n" for m in msgs if m)

def jsonl2txt(data):
    out = []
    for n, line in enumerate(data.splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            raise SystemExit(f"line {n}: invalid JSON ({e})")
        if not isinstance(obj, dict) or not isinstance(obj.get("messages"), list):
            raise SystemExit(f"line {n}: expected {{\"messages\": [...]}}")
        if obj["messages"]:
            out.append(to_text(obj["messages"]))
    return "---\n".join(out)

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["txt2jsonl", "jsonl2txt"])
    ap.add_argument("src"); ap.add_argument("dst")
    a = ap.parse_args(argv)
    try:
        with open(a.src, encoding="utf-8") as f: data = f.read()
    except FileNotFoundError:
        raise SystemExit(f"file not found: {a.src}")
    except UnicodeDecodeError:
        raise SystemExit(f"{a.src} isn't a UTF-8 text file")
    out = txt2jsonl(data) if a.mode == "txt2jsonl" else jsonl2txt(data)
    with open(a.dst, "w", encoding="utf-8") as f: f.write(out)
    print(f"wrote {a.dst}")

if __name__ == "__main__":
    main()
