"""Plan of the package workflow (.github/workflows/packages.yml).

User's rule: a new release is published only when the packages of ALL systems are in it – nobody gets the update
notice before the file for their computer exists.
- a pushed v* tag: a DRAFT release is created (text .github/RELEASE_BODY.md), all systems are built and add their
  packages to it;
- every hour (schedule): the newest draft release – the systems whose packages are still missing are built again
  (GitHub sometimes has no free runner for a system, e.g. macOS arm64, and cancels the waiting job – the next hour
  tries again, for as long as it takes); without a draft – the latest published release, if a package is missing;
- by hand: with a tag – that release (the systems given, else the missing ones, else all); without a tag – a test
  build of the branch (no release);
- `release_plan.py finalize TAG`: the draft with all the packages is published (and becomes the latest).
Outputs of the plan (GITHUB_OUTPUT): tag, matrix (JSON list for the build job), any (true / false)."""
import json
import os
import subprocess
import sys

SYSTEMS = [  # name, runner, the files that system adds to a release (endings of the names)
    ("Windows", "windows-latest", ["-windows-x64-setup.exe", "-windows-x64.zip"]),
    ("macOS", "macos-15", ["-macos-arm64.dmg"]),
    ("macOS-Intel", "macos-15-intel", ["-macos-x64.dmg"]),
    ("Linux", "ubuntu-22.04", ["_amd64.deb", "-linux-x86_64.tar.gz"]),
]
REPO = os.environ.get("GITHUB_REPOSITORY", "damiankozuszek/kayenn")


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def releases():
    """All releases, drafts too (newest first): [{tag, draft, assets}]."""
    code, out, err = gh("api", f"repos/{REPO}/releases?per_page=30")
    if code != 0:
        raise SystemExit(f"cannot list the releases: {err}")
    return [dict(tag=r["tag_name"], draft=r["draft"], assets=[a["name"] for a in r.get("assets", [])],
                 created=r.get("created_at") or "") for r in json.loads(out)]


def retry_now(created):
    """Scheduled retries of the missing systems: every hour for the first 3 hours after the release was created,
    then every 6 hours. A job that gets no runner makes the whole run „failed” (and GitHub e-mails it) – fewer
    attempts while GitHub has no machines means fewer such e-mails; an hour with nothing to build is a success."""
    import datetime
    try:
        t = datetime.datetime.fromisoformat(created.replace("Z", "+00:00"))
    except ValueError:
        return True
    age = int((datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() // 3600)
    return age <= 3 or age % 6 == 0


def find(tag):
    return next((r for r in releases() if r["tag"] == tag), None)


def missing(names):
    return [s for s in SYSTEMS if not all(any(n.endswith(e) for n in names) for e in s[2])]


def ensure_draft(tag):
    if find(tag) is None:
        code, out, err = gh("release", "create", tag, "--draft", "--verify-tag", "--title", tag,
                            "--notes-file", ".github/RELEASE_BODY.md")
        print(f"draft release {tag} created" if code == 0 else f"release {tag} NOT created: {err}")
        if code != 0:
            raise SystemExit(1)


def finalize(tag):
    r = find(tag)
    if r is None:
        print(f"no release {tag}")
        return
    lack = [s[0] for s in missing(r["assets"])]
    if not r["draft"]:
        print(f"{tag} already published" + (f"; packages still missing: {lack}" if lack else ""))
    elif lack:
        print(f"{tag} stays a draft – packages missing: {lack} (built again by the scheduled run)")
    else:
        code, out, err = gh("release", "edit", tag, "--draft=false", "--latest")
        print(f"{tag} PUBLISHED – all packages ready" if code == 0 else f"publishing {tag} failed: {err}")
        if code != 0:
            raise SystemExit(1)


def plan():
    event = os.environ.get("EVENT", "")
    wanted = [s.strip().lower() for s in os.environ.get("IN_SYSTEMS", "").split(",") if s.strip()]
    tag = ""
    if event == "push" and os.environ.get("REF_NAME", "").startswith("v"):
        tag = os.environ["REF_NAME"]
        ensure_draft(tag)
        todo = list(SYSTEMS)
    elif event == "schedule":
        rel = releases()
        draft = next((r for r in rel if r["draft"] and r["tag"].startswith("v")), None)
        pub = next((r for r in rel if not r["draft"] and r["tag"].startswith("v")), None)
        target = draft or pub
        tag = target["tag"] if target else ""
        todo = missing(target["assets"]) if target else []
        if todo and not retry_now(target["created"]):
            print(f"{tag}: missing {[s[0] for s in todo]} – not this hour (retries: hourly for 3 h, then every 6 h)")
            todo = []
    else:                                                                              # by hand
        tag = os.environ.get("IN_TAG", "").strip()
        if tag:
            ensure_draft(tag)
            todo = missing(find(tag)["assets"]) or list(SYSTEMS)
        else:
            todo = list(SYSTEMS)
        if wanted:
            todo = [s for s in SYSTEMS if s[0].lower() in wanted]
    matrix = [{"name": n, "os": o} for n, o, _ in todo]
    print(f"release: {tag or '(none – test build)'}; systems to build: {[m['name'] for m in matrix] or 'none'}")
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
        f.write(f"tag={tag}\nmatrix={json.dumps(matrix)}\nany={'true' if matrix else 'false'}\n")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "finalize":
        finalize(sys.argv[2])
    else:
        plan()
