#!/usr/bin/env python3
"""Drill-down map and mechanical checkup for a master OS folder.

    python3 tools/os_map.py            # writes os-map.html in the OS root
    python3 tools/os_map.py --check    # prints checkup findings, exit 1 on errors

Reads:
  decisions/file-map.md     why each folder lives where it does
  automations/registry.csv  the log sheet of live automations
  automations/flows/*.md    one mermaid flowchart per automation

Standard library only. Brand data/ folders are counted, never listed.
"""
import argparse
import csv
import datetime as dt
import html
import json
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
SKIP_FILES = {"os-map.html", ".DS_Store"}
REGISTRY_COLUMNS = {"id", "name", "brand", "status", "trigger", "skills_used",
                    "reads_from", "writes_to", "credential", "flow_doc", "last_reviewed"}
STATUSES = {"live", "pilot", "paused", "retired"}
STALE_DAYS = 90


def rel(path, root):
    return path.relative_to(root).as_posix()


def is_data_dir(path, root):
    parts = Path(rel(path, root)).parts
    return len(parts) == 3 and parts[0] == "brands" and parts[2] == "data"


def md(text):
    """Escape text and render `backticks` as <code>."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text))


def brand_of(relpath):
    parts = relpath.split("/")
    if parts[0] == "brands" and len(parts) > 1:
        return parts[1]
    if parts[0] == "clients":
        return "client"
    return "shared"


def load_file_map(root):
    notes = {}
    path = root / "decisions" / "file-map.md"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|\s*$", line)
            if m:
                notes[m.group(1).rstrip("/")] = m.group(2)
    return notes


def load_registry(root):
    path = root / "automations" / "registry.csv"
    if not path.exists():
        return [], set()
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), set(reader.fieldnames or [])


def mermaid_block(path):
    m = re.search(r"```mermaid\n(.*?)```", path.read_text(encoding="utf-8"), re.S)
    return m.group(1).strip() if m else ""


def find_skills(root):
    """Return {name: [(scope, relpath)]} plus findings for misplaced skills."""
    skills, findings = {}, []
    for skill_md in sorted(root.rglob("SKILL.md")):
        if SKIP_DIRS & set(skill_md.parts):
            continue
        r = rel(skill_md, root)
        parts = r.split("/")
        if len(parts) < 4 or parts[-3] != "skills" or parts[-4] != ".claude":
            findings.append(("error", f"Misplaced skill: {r} is not in a .claude/skills/<name>/ folder"))
            continue
        text = skill_md.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(\S+)", text, re.M) if text.startswith("---") else None
        name = m.group(1) if m else parts[-2]
        if not re.search(r"^description:\s*\S", text, re.M):
            findings.append(("warn", f"Skill {name} ({r}) has no description, so Claude can't tell when to use it"))
        scope = "shared" if len(parts) == 4 else brand_of(r)
        skills.setdefault(name, []).append((scope, r))
    for skills_dir in root.rglob(".claude/skills"):
        for d in skills_dir.iterdir():
            if d.is_dir() and not (d / "SKILL.md").exists():
                findings.append(("error", f"Skill folder with no SKILL.md: {rel(d, root)}"))
    for name, places in skills.items():
        scopes = {s for s, _ in places}
        if "shared" in scopes and len(places) > 1:
            findings.append(("warn", f"Skill name '{name}' exists at the root and inside a brand. "
                                     "Rename one so it's clear which runs"))
    return skills, findings


def check_routing(root, findings):
    brands = sorted(d.name for d in (root / "brands").iterdir() if d.is_dir()) if (root / "brands").exists() else []
    for claude_md in sorted(root.rglob("CLAUDE.md")):
        if SKIP_DIRS & set(claude_md.parts):
            continue
        for line in claude_md.read_text(encoding="utf-8").splitlines():
            in_table = line.lstrip().startswith("|")
            for token in re.findall(r"`([^`\n]+)`", line):
                if any(c in token for c in "<>*~ ") or token.startswith(("http", "-", "/")):
                    continue
                multi_segment = "/" in token.rstrip("/")
                is_file = token.endswith((".md", ".csv", ".json", ".py"))
                # A bare folder name like `data/` is a route only inside a routing table.
                if not (multi_segment or is_file or (in_table and token.endswith("/"))):
                    continue
                if not ((claude_md.parent / token).exists() or (root / token).exists()):
                    findings.append(("error", f"Routing in {rel(claude_md, root)} points to a missing path: {token}"))
    root_md = root / "CLAUDE.md"
    root_text = root_md.read_text(encoding="utf-8") if root_md.exists() else ""
    for b in brands:
        if f"brands/{b}" not in root_text:
            findings.append(("warn", f"Brand '{b}' has no row in the root CLAUDE.md routing table"))
        if not (root / "brands" / b / "CLAUDE.md").exists():
            findings.append(("warn", f"Brand '{b}' has no CLAUDE.md of its own"))
    return brands


def check_registry(root, rows, columns, skills, brands, findings):
    missing = REGISTRY_COLUMNS - columns
    if rows and missing:
        findings.append(("error", f"registry.csv is missing columns: {', '.join(sorted(missing))}"))
    today = dt.date.today()
    referenced = set()
    for row in rows:
        rid = row.get("id", "?")
        if row.get("status") not in STATUSES:
            findings.append(("warn", f"{rid}: status '{row.get('status')}' is not one of {sorted(STATUSES)}"))
        if row.get("brand") not in brands:
            findings.append(("error", f"{rid}: brand '{row.get('brand')}' has no folder in brands/"))
        for skill in re.split(r"[;,]", row.get("skills_used", "")):
            skill = skill.strip()
            if not skill or skill.lower() == "n/a":
                continue
            if skill not in skills:
                findings.append(("error", f"{rid}: uses skill '{skill}', which doesn't exist"))
            elif all(s not in ("shared", row.get("brand")) for s, _ in skills[skill]):
                findings.append(("error", f"{rid}: brand '{row.get('brand')}' uses '{skill}', "
                                          "a skill that belongs to another brand"))
        flow = row.get("flow_doc", "").strip()
        referenced.add(flow)
        if not flow or not (root / flow).exists():
            findings.append(("error", f"{rid}: flowchart '{flow}' is missing"))
        try:
            age = (today - dt.date.fromisoformat(row.get("last_reviewed", ""))).days
            if age > STALE_DAYS:
                findings.append(("warn", f"{rid}: last reviewed {age} days ago (over {STALE_DAYS})"))
        except ValueError:
            findings.append(("warn", f"{rid}: last_reviewed '{row.get('last_reviewed')}' is not a YYYY-MM-DD date"))
    flows_dir = root / "automations" / "flows"
    if flows_dir.exists():
        for flow in sorted(flows_dir.glob("*.md")):
            if rel(flow, root) not in referenced:
                findings.append(("warn", f"Flowchart {rel(flow, root)} has no row in registry.csv"))


def check_clients_and_data(root, findings):
    clients = root / "clients"
    if clients.exists():
        for item in sorted(clients.iterdir()):
            if item.is_dir() or item.suffix != ".md":
                findings.append(("error", f"Client work inside the OS: {rel(item, root)}. "
                                          "Move it out and keep a pointer .md file"))
    try:
        tracked = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True,
                                 text=True, check=True).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        tracked = []
    for t in tracked:
        parts = t.split("/")
        if len(parts) > 3 and parts[0] == "brands" and parts[2] == "data" and parts[-1] != "README.md":
            findings.append(("error", f"Brand data is committed to git: {t}"))


def check_file_map(root, notes, findings):
    for d in sorted(p for p in root.rglob("*") if p.is_dir()):
        r = rel(d, root)
        parts = Path(r).parts
        inside_data = len(parts) > 3 and parts[0] == "brands" and parts[2] == "data"
        inside_client = len(parts) > 1 and parts[0] == "clients"  # already flagged as client work
        if SKIP_DIRS & set(parts) or inside_data or inside_client:
            continue
        if r not in notes:
            findings.append(("warn", f"No reason recorded for folder {r}/ in decisions/file-map.md"))
    for path in notes:
        if not (root / path).exists():
            findings.append(("warn", f"file-map.md lists {path}, which no longer exists"))


def run_checks(root):
    findings = []
    notes = load_file_map(root)
    rows, columns = load_registry(root)
    skills, skill_findings = find_skills(root)
    findings += skill_findings
    brands = check_routing(root, findings)
    check_registry(root, rows, columns, skills, brands, findings)
    check_clients_and_data(root, findings)
    check_file_map(root, notes, findings)
    order = {"error": 0, "warn": 1}
    findings = sorted(dict.fromkeys(findings), key=lambda f: order[f[0]])
    return findings, notes, rows, skills, brands


# ---------- HTML ----------

def tree_html(path, root, notes):
    r = rel(path, root) if path != root else ""
    if path != root and is_data_dir(path, root):
        count = sum(1 for p in path.rglob("*") if p.is_file() and p.name != "README.md")
        return (f'<li class="dir"><span class="name">data/</span> <span class="tag">{brand_of(r)}</span>'
                f' <span class="note">{md(notes.get(r, ""))} ({count} local files, not listed)</span></li>')
    children = sorted((p for p in path.iterdir() if p.name not in SKIP_DIRS | SKIP_FILES),
                      key=lambda p: (p.is_file(), p.name.lower()))
    items = []
    for child in children:
        if child.is_dir():
            items.append(tree_html(child, root, notes))
        else:
            cr = rel(child, root)
            note = md(notes.get(cr, ""))
            items.append(f'<li class="file"><span class="name">{html.escape(child.name)}</span>'
                         f' <span class="note">{note}</span></li>')
    inner = "<ul>" + "".join(items) + "</ul>"
    if path == root:
        return inner
    note = notes.get(r)
    note_html = (f'<span class="note">{md(note)}</span>' if note
                 else '<span class="missing">no reason recorded</span>')
    return (f'<li class="dir"><details><summary><span class="name">{html.escape(path.name)}/</span>'
            f' <span class="tag">{brand_of(r)}</span> {note_html}</summary>{inner}</details></li>')


def automations_html(root, rows):
    head = ("<tr><th>ID</th><th>Name</th><th>Brand</th><th>Status</th><th>Trigger</th>"
            "<th>Skills</th><th>Reads</th><th>Writes</th><th>Credential</th></tr>")
    body, flows = [], []
    for row in rows:
        e = {k: html.escape(v or "") for k, v in row.items()}
        body.append(f"<tr><td>{e['id']}</td><td>{e['name']}</td><td>{e['brand']}</td>"
                    f"<td><span class='status {e['status']}'>{e['status']}</span></td>"
                    f"<td>{e['trigger']}: {e.get('schedule_or_endpoint', '')}</td><td>{e['skills_used']}</td>"
                    f"<td>{e['reads_from']}</td><td>{e['writes_to']}</td><td>{e['credential']}</td></tr>")
        flow_path = root / row.get("flow_doc", "")
        src = mermaid_block(flow_path) if flow_path.is_file() else ""
        flows.append(f"<details class='flow'><summary>{e['id']} {e['name']}</summary>"
                     f"<div class='diagram' data-src='{html.escape(json.dumps(src))}'></div>"
                     f"<pre class='src'>{html.escape(src) or 'No flowchart found'}</pre></details>")
    return f"<div class='scroll'><table>{head}{''.join(body)}</table></div>{''.join(flows)}"


def write_html(root, out, findings, notes, rows, skills, brands):
    projects = sum(1 for b in brands for p in (root / "brands" / b / "projects").glob("*") if p.is_dir())
    shared = sum(1 for places in skills.values() for s, _ in places if s == "shared")
    total_skills = sum(len(p) for p in skills.values())
    active = sum(1 for r in rows if r.get("status") in ("live", "pilot"))
    errors = sum(1 for f in findings if f[0] == "error")
    tiles = [("Brands", len(brands)), ("Projects", projects),
             ("Skills", f"{total_skills} <small>({shared} shared)</small>"),
             ("Automations", f"{active} <small>live or pilot</small>"),
             ("Checkup", f"{len(findings)} <small>({errors} errors)</small>")]
    tiles_html = "".join(f"<div class='tile'><div class='label'>{k}</div><div class='value'>{v}</div></div>"
                         for k, v in tiles)
    findings_html = "".join(f"<li class='{lvl}'><b>{lvl}</b> {html.escape(msg)}</li>" for lvl, msg in findings) \
        or "<li>No findings.</li>"
    page = TEMPLATE.format(date=dt.date.today().isoformat(), tiles=tiles_html,
                           tree=tree_html(root, root, notes), automations=automations_html(root, rows),
                           findings=findings_html)
    out.write_text(page, encoding="utf-8")


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Master OS Map</title>
<style>
:root {{ --bg:#fafaf9; --fg:#1c1917; --muted:#78716c; --line:#e7e5e4; --card:#fff; --accent:#2563eb;
        --warn:#b45309; --error:#b91c1c; --ok:#15803d; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#1c1917; --fg:#f5f5f4; --muted:#a8a29e; --line:#44403c;
        --card:#292524; --accent:#60a5fa; --warn:#fbbf24; --error:#f87171; --ok:#4ade80; }} }}
body {{ margin:0; padding:24px 16px; background:var(--bg); color:var(--fg);
        font:15px/1.5 system-ui, -apple-system, Segoe UI, sans-serif; }}
main {{ max-width:1100px; margin:0 auto; }}
h1 {{ margin:0 0 4px; font-size:24px; }} h2 {{ margin:32px 0 8px; font-size:18px; }}
.sub {{ color:var(--muted); margin:0 0 16px; }}
.tiles {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:12px; }}
.tile {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px; }}
.label {{ color:var(--muted); font-size:13px; }} .value {{ font-size:22px; font-weight:600; }}
.value small {{ font-size:13px; font-weight:400; color:var(--muted); }}
input {{ width:100%; box-sizing:border-box; padding:10px; border:1px solid var(--line); border-radius:8px;
        background:var(--card); color:var(--fg); font:inherit; margin:8px 0; }}
.tree {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:8px 12px; overflow-x:auto; }}
.tree ul {{ list-style:none; padding-left:18px; margin:2px 0; }} .tree > ul {{ padding-left:0; }}
summary {{ cursor:pointer; }} .name {{ font-weight:600; }} .file .name {{ font-weight:400; }}
.note {{ color:var(--muted); }} .missing {{ color:var(--warn); font-size:13px; }}
code {{ font-size:13px; }}
.tag {{ font-size:11px; border:1px solid var(--line); border-radius:4px; padding:0 4px; color:var(--muted); }}
.hide {{ display:none; }}
.scroll {{ overflow-x:auto; }}
table {{ border-collapse:collapse; width:100%; font-size:13px; background:var(--card); }}
th, td {{ border:1px solid var(--line); padding:6px 8px; text-align:left; vertical-align:top; }}
.status.live {{ color:var(--ok); }} .status.pilot {{ color:var(--accent); }}
.flow {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:8px 12px; margin-top:8px; }}
.diagram svg {{ max-width:100%; height:auto; }} .src {{ font-size:12px; color:var(--muted); white-space:pre-wrap; }}
.findings li.error b {{ color:var(--error); }} .findings li.warn b {{ color:var(--warn); }}
</style></head><body><main>
<h1>Master OS map</h1><p class="sub">Generated {date} by tools/os_map.py</p>
<div class="tiles">{tiles}</div>
<h2>Folders</h2>
<input id="q" placeholder="Search files and reasons, for example: cost, ticket, clients">
<div class="tree" id="tree">{tree}</div>
<h2>Automations</h2>{automations}
<h2>Checkup</h2><ul class="findings">{findings}</ul>
</main>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
<script>
const dark = matchMedia('(prefers-color-scheme: dark)').matches;
if (window.mermaid) mermaid.initialize({{ startOnLoad: false, theme: dark ? 'dark' : 'default' }});
let n = 0;
document.querySelectorAll('details.flow').forEach(d => d.addEventListener('toggle', async () => {{
  const box = d.querySelector('.diagram');
  if (!d.open || box.dataset.done || !window.mermaid) return;
  const src = JSON.parse(box.dataset.src);
  if (!src) return;
  try {{ box.innerHTML = (await mermaid.render('m' + (n++), src)).svg; box.dataset.done = 1;
         d.querySelector('.src').classList.add('hide'); }} catch (e) {{ }}
}}));
document.getElementById('q').addEventListener('input', e => {{
  const q = e.target.value.trim().toLowerCase();
  document.querySelectorAll('#tree li').forEach(li => {{
    const hit = !q || li.textContent.toLowerCase().includes(q);
    li.classList.toggle('hide', !hit);
    const d = li.querySelector(':scope > details');
    if (d && q) d.open = hit;
  }});
}});
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--out", type=Path, help="HTML output path (default: <root>/os-map.html)")
    ap.add_argument("--check", action="store_true", help="print checkup findings only")
    args = ap.parse_args()
    root = args.root.resolve()
    findings, notes, rows, skills, brands = run_checks(root)
    if args.check:
        for lvl, msg in findings:
            print(f"[{lvl.upper():5}] {msg}")
        errors = sum(1 for f in findings if f[0] == "error")
        print(f"\n{len(findings)} findings, {errors} errors")
        return 1 if errors else 0
    out = args.out or root / "os-map.html"
    write_html(root, out, findings, notes, rows, skills, brands)
    print(f"Wrote {out} ({len(findings)} checkup findings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
