"""Plan of the package workflow (.github/workflows/packages.yml): which release and which systems to build.

- a pushed v* tag: the release is created at once (published, text .github/RELEASE_BODY.md), all systems are built;
- schedule: the latest release is checked – only the systems whose packages are missing in it are built;
- by hand: with a tag – that release (the systems given, else the missing ones, else all); without a tag – a test
  build of the branch (no release).
Outputs (GITHUB_OUTPUT): tag, matrix (JSON list for the build job), any (true / false)."""
import json
import os
import subprocess

SYSTEMS = [  # name, runner, the files that system adds to a release (endings of the names)
    ("Windows", "windows-latest", ["-windows-x64-setup.exe", "-windows-x64.zip"]),
    ("macOS", "macos-15", ["-macos-arm64.dmg"]),
    ("macOS-Intel", "macos-15-intel", ["-macos-x64.dmg"]),
    ("Linux", "ubuntu-22.04", ["_amd64.deb", "-linux-x86_64.tar.gz"]),
]


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def assets(tag):
    """Names of the files of the release, or None when there is no such release."""
    code, out, _ = gh("release", "view", tag, "--json", "assets", "--jq", "[.assets[].name]")
    return json.loads(out) if code == 0 and out else None


def missing(names):
    return [s for s in SYSTEMS if not all(any(n.endswith(e) for n in names) for e in s[2])]


def ensure_release(tag):
    if assets(tag) is None:
        code, out, err = gh("release", "create", tag, "--verify-tag", "--title", tag,
                            "--notes-file", ".github/RELEASE_BODY.md")
        print(f"release {tag} created" if code == 0 else f"release {tag} NOT created: {err}")
        if code != 0:
            raise SystemExit(1)


event = os.environ.get("EVENT", "")
tag = ""
wanted = [s.strip().lower() for s in os.environ.get("IN_SYSTEMS", "").split(",") if s.strip()]
if event == "push" and os.environ.get("REF_NAME", "").startswith("v"):
    tag = os.environ["REF_NAME"]
    ensure_release(tag)
    todo = list(SYSTEMS)
elif event == "schedule":
    code, out, _ = gh("release", "view", "--json", "tagName", "--jq", ".tagName")     # the latest release
    tag = out if code == 0 else ""
    todo = missing(assets(tag) or []) if tag else []
else:                                                                                 # by hand
    tag = os.environ.get("IN_TAG", "").strip()
    if tag:
        ensure_release(tag)
        todo = missing(assets(tag) or []) or list(SYSTEMS)
    else:
        todo = list(SYSTEMS)
    if wanted:
        todo = [s for s in SYSTEMS if s[0].lower() in wanted]

matrix = [{"name": n, "os": o} for n, o, _ in todo]
print(f"tag: {tag or '(none – test build)'}; systems: {[m['name'] for m in matrix] or 'none – nothing missing'}")
with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
    f.write(f"tag={tag}\nmatrix={json.dumps(matrix)}\nany={'true' if matrix else 'false'}\n")
