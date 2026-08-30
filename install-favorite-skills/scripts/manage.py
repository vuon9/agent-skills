#!/usr/bin/env python3
"""Manage the favorites.json manifest.

Commands:
  list                          Show current favorites (name + source).
  add <name> --source <repo>    Add a favorite, or change its source if it exists.
  remove <name>                 Remove a favorite from the manifest.
  set-source <name> <repo>      Change only the source of an existing favorite.

After any change, run scripts/install.py to apply it to the local machine.
"""
import argparse
import json
import os
import sys

MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "favorites.json")


def load():
    with open(MANIFEST) as fh:
        data = json.load(fh)
    if "skills" not in data:
        data["skills"] = []
    return data


def save(data):
    data["skills"].sort(key=lambda s: s["name"])
    with open(MANIFEST, "w") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


def find(entries, name):
    for entry in entries:
        if entry["name"] == name:
            return entry
    return None


def cmd_list(data):
    for entry in sorted(data["skills"], key=lambda s: s["name"]):
        source = entry.get("source", "?")
        suffix = f"  ({entry['note']})" if source == "local" and entry.get("note") else ""
        print(f"{entry['name']}\t{source}{suffix}")


def cmd_add(data, name, source):
    entry = find(data["skills"], name)
    if entry:
        entry["source"] = source
        entry.pop("note", None)
        print(f"updated {name} -> {source}")
    else:
        data["skills"].append({"name": name, "source": source})
        print(f"added {name} <- {source}")


def cmd_remove(data, name):
    before = len(data["skills"])
    data["skills"] = [e for e in data["skills"] if e["name"] != name]
    print(f"removed {name}" if len(data["skills"]) < before else f"not found: {name}")


def cmd_set_source(data, name, source):
    entry = find(data["skills"], name)
    if not entry:
        print(f"not found: {name}", file=sys.stderr)
        sys.exit(1)
    entry["source"] = source
    entry.pop("note", None)
    print(f"{name} -> {source}")


def main():
    parser = argparse.ArgumentParser(description="Manage favorites.json.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list")

    p_add = sub.add_parser("add")
    p_add.add_argument("name")
    p_add.add_argument("--source", required=True)

    p_rm = sub.add_parser("remove")
    p_rm.add_argument("name")

    p_set = sub.add_parser("set-source")
    p_set.add_argument("name")
    p_set.add_argument("source")

    args = parser.parse_args()
    data = load()

    if args.command == "list":
        cmd_list(data)
        return
    if args.command == "add":
        cmd_add(data, args.name, args.source)
    elif args.command == "remove":
        cmd_remove(data, args.name)
    elif args.command == "set-source":
        cmd_set_source(data, args.name, args.source)

    save(data)


if __name__ == "__main__":
    main()
