#!/usr/bin/env python3
"""Count my commits on GitHub for the activity chart, and keep only weekly totals.

    python3 assets/collect_activity.py OWNER [OWNER ...]   # then: python3 assets/build.py

It asks GitHub (through the signed-in `gh` CLI) for every non-fork repo the owners have
pushed to in the last year, reads each default branch, and keeps commits GitHub credits to
the signed-in account. A commit is counted once even when its history was copied into another repo.
Private repos are counted but never named: activity.json holds only weekly totals, the
total, the number of days with a commit, and how many commits name an AI agent as
co-author. Merges and bookkeeping that tools commit by themselves are left out. That is the same information GitHub's own graph shows for private work.
"""
import collections
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys

AGENTS = ('claude', 'codex', 'gemini', 'grok', 'muse', 'copilot', 'cursor')
# Bookkeeping that tools commit on their own: merges, saved agent notes, sync snapshots.
# Left out so the chart counts changes someone actually made.
AUTOMATIC = re.compile(r'^(Merge |Batch \d+: merge |Save agent closing note|Archive older agent closing notes|[\w.-]+/[\w.-]+: \d{4}-\d\d-\d\dT)')


def gh(*args):
    out = subprocess.run(['gh', 'api', *args], capture_output=True, text=True, check=True).stdout
    return [json.loads(line) for line in out.splitlines() if line.strip()]


def main(owners):
    me = gh('user', '--jq', '{login: .login}')[0]['login']
    since = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    commits = {}
    for owner in owners:
        kind = 'users' if owner.lower() == me.lower() else 'orgs'
        path = f'user/repos?affiliation=owner&per_page=100' if kind == 'users' else f'orgs/{owner}/repos?per_page=100'
        repos = gh('--paginate', path, '--jq', '.[] | select(.fork | not) | {full_name, pushed_at, owner: .owner.login}')
        for repo in repos:
            if repo['owner'].lower() != owner.lower() or (repo['pushed_at'] or '') < since:
                continue
            try:
                rows = gh('--paginate', f"repos/{repo['full_name']}/commits?author={me}&since={since}T00:00:00Z&per_page=100",
                          '--jq', '.[] | {sha, date: .commit.author.date, message: .commit.message}')
            except subprocess.CalledProcessError:
                continue  # an empty repo answers 409
            for row in rows:
                # Copied or rewritten history gets new SHAs but keeps the author date and
                # subject, so key on those: a commit carried into a second repo counts once.
                commits.setdefault((row['date'], row['message'].split('\n', 1)[0]), row)
    automatic = [k for k in commits if AUTOMATIC.match(k[1])]
    for key in automatic:
        del commits[key]
    if os.environ.get('ACTIVITY_DEBUG'):
        shape = collections.Counter(re.sub(r'[0-9a-f]{7,}|\d+', '#', k[1])[:70] for k in commits)
        print('left out as automatic:', len(automatic), file=sys.stderr)
        for s, n in shape.most_common(25):
            print(f'{n:6} {s}', file=sys.stderr)
    weeks = collections.Counter()
    days = set()
    with_agent = 0
    for row in commits.values():
        day = datetime.date.fromisoformat(row['date'][:10])
        days.add(day)
        weeks[(day - datetime.timedelta(days=day.weekday())).isoformat()] += 1
        trailers = [l.lower() for l in row['message'].splitlines() if l.lower().startswith('co-authored-by:')]
        if any(a in t for t in trailers for a in AGENTS):
            with_agent += 1
    data = dict(counted=datetime.date.today().isoformat(), since=since, commits=len(commits),
                days_with_commits=len(days), commits_naming_an_agent=with_agent, weeks=dict(sorted(weeks.items())))
    path = pathlib.Path(__file__).with_name('activity.json')
    path.write_text(json.dumps(data, indent=1) + '\n')
    print({k: v for k, v in data.items() if k != 'weeks'})


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
