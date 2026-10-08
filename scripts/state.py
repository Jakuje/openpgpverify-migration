"""Shared helpers for data/state/packages.jsonl, the per-package state file.

The file holds one JSON object per line, sorted by package name. It is
rewritten atomically so an interrupted run never leaves it half-written.
"""
import datetime
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, 'data', 'state', 'packages.jsonl')


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def load(path=STATE):
    if not os.path.exists(path):
        return {}
    with open(path) as fh:
        return {r['package']: r for r in map(json.loads, fh) if r}


def save(state, path=STATE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh:
        for name in sorted(state):
            fh.write(json.dumps(state[name], sort_keys=True) + '\n')
    os.replace(tmp, path)


def load_inventory(path):
    with open(path) as fh:
        return {r['package']: r for r in map(json.loads, fh) if r}
