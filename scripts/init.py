#!/usr/bin/env python3
"""把 vibecodingflow 的文档骨架铺到项目里（不覆盖已有文件）。

用法：
    python init.py <项目目录> [--lang en|zh] [--name 项目名] [--genre 类型] [--game] [--full]
                              [--agents] [--hooks] [--force]
    python init.py --genre list          列出可用的类型预设

    --lang    文档语言 en（默认）或 zh；写入 docs/dev/.lang，所有脚本两种语言都能解析
    --genre   带入类型验收基准预设（平台跳跃、肉鸽、解谜……）。除 web_app_tool 外会自动加 --game
    --game    叠加游戏层：GDD 版设计文档、游戏规则、素材台账
    --full    带上完整版的可选模板（审查、性能、路线图、调研、更新日志、参考资料）
    --agents  安装 4 个 Claude Code 子代理（实现 / 验证 / 文书 / 审查）到 .claude/agents/
    --hooks   安装 Claude Code hook（Stop 拦截 ERROR、SessionStart 注入摘要）和 git pre-commit
    --force   覆盖已存在的同名文件（默认跳过）
"""
import argparse
import datetime
import json
import os
import re
import shutil
import stat
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dk_common as dk  # noqa: E402

ROOT = HERE.parent
TEMPLATES_BASE = ROOT / "assets" / "templates"
GENRES_BASE = ROOT / "assets" / "genres"
AGENTS_BASE = ROOT / "assets" / "agents"
REFS_BASE = ROOT / "references"
LANGS = ("en", "zh")
# 类型预设里要提取的小节标题（与 assets/genres/<lang>/*.md 一致）
GENRE_HEADS = {
    "zh": {"baseline": "验收基准", "params": "手感参数起点",
           "notes": ["常见返工点", "体验路线示例", "一分钟测试", "灰盒阶段验什么"]},
    "en": {"baseline": "Acceptance baseline", "params": "Starting feel parameters",
           "notes": ["Common rework points", "Sample test route", "One-minute test",
                     "What to check at the greybox stage"]},
}
# 占位符替换：同时列出中英文写法
SUB_KEYS = {
    "name": ["{{项目名}}", "{{游戏名}}", "{{Project name}}", "{{Game name}}", "{{project name}}", "{{game name}}"],
    "date": ["{{日期}}", "{{Date}}", "{{date}}"],
}
PANEL_HTML = ROOT / "assets" / "review_panel.html"
TOOLS = ["dk_common.py", "check_docs.py", "new_review.py", "build_panel.py", "dk_hook.py", "adopt.py"]
TEXT_EXT = {".md", ".txt", ".gitkeep", ""}
NON_GAME_GENRES = {"web_app_tool"}
PRE_COMMIT_MARK = "# ai-dev-kit pre-commit"


# ---------- 复制 ----------

def _w(path, text):
    """统一用 LF 写文件：Windows 上 write_text 会写成 CRLF，pre-commit 这类 shell 脚本会因此无法执行。"""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _sub(text, subs):
    for k, v in subs.items():
        if v:
            text = text.replace(k, v)
    return text


def copy_tree(src, dst, subs, force, report):
    for p in sorted(src.rglob("*")):
        if p.is_dir():
            continue
        target = dst / p.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target in report["placed"]:
            continue  # 本次运行里已由更靠前的层（如游戏层）放好，不算"跳过用户文件"
        if target.exists() and not force:
            report["skipped"].append(target)
            continue
        report["placed"].add(target)
        if p.suffix in TEXT_EXT:
            _w(target, _sub(p.read_text(encoding="utf-8"), subs))
        else:
            shutil.copy2(p, target)
        report["created"].append(target)


def copy_file(src, target, force, report):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        report["skipped"].append(target)
        return
    shutil.copy2(src, target)
    report["created"].append(target)


def append_agents_line(dst, marker, line):
    p = dst / "AGENTS.md"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    if marker in t:
        return
    _w(p, t.rstrip("\n") + "\n" + line + "\n")


# ---------- 类型预设 ----------

def list_genres(lang="en"):
    return sorted(p.stem for p in (GENRES_BASE / lang).glob("*.md"))


def _find_h2(lines, prefix):
    start = None
    for i, ln in enumerate(lines):
        m = re.match(r"^##\s+(.*)$", ln)
        if m and m.group(1).strip().startswith(prefix):
            start = i
            break
    if start is None:
        return None, None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^##\s", lines[j]):
            end = j
            break
    return start, end


def _inject_table(text, prefix, table_lines, note):
    """替换第 prefix 节里的第一张表；没有表就追加到该节末尾。节不存在则追加到文末。"""
    lines = text.split("\n")
    start, end = _find_h2(lines, prefix)
    if start is None:
        return text.rstrip("\n") + "\n\n" + "\n".join(table_lines) + "\n\n" + note + "\n"
    ts = te = None
    for i in range(start + 1, end):
        if lines[i].lstrip().startswith("|"):
            if ts is None:
                ts = i
            te = i + 1
        elif ts is not None:
            break
    block = table_lines + ["", note]
    if ts is not None:
        # 已有注释行就不重复加
        after = lines[te:te + 3]
        if any(note[:10] in a for a in after):
            block = table_lines
        lines[ts:te] = block
    else:
        k = end
        while k > start + 1 and not lines[k - 1].strip():
            k -= 1
        lines[k:k] = [""] + block
    return "\n".join(lines)


def apply_genre(dst, genre, report, lang):
    H = GENRE_HEADS[lang]
    src = GENRES_BASE / lang / f"{genre}.md"
    text = src.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    design = dst / "docs" / "design" / "DESIGN.md"
    if design.exists():
        d = design.read_text(encoding="utf-8")
        base_tbl = [l for l in dk.section(text, H["baseline"]).splitlines() if l.strip().startswith("|")]
        param_tbl = [l for l in dk.section(text, H["params"]).splitlines() if l.strip().startswith("|")]
        if lang == "en":
            note6 = (f'> From genre preset "{title}" — a starting point, not a verdict: calibrate to your taste after the '
                     "first review and log it in DECISIONS.md.")
            note5 = f'> Starting values from genre preset "{title}". Feel wins: drag them in the tuning panel.'
        else:
            note6 = f"> 以上来自类型预设「{title}」，是起点不是定论：首轮验收后按你的口味校准，并在 DECISIONS.md 记一笔。"
            note5 = f"> 参数起点来自类型预设「{title}」，以手感为准，在调参面板里拖。"
        if base_tbl:
            d = _inject_table(d, "6.", base_tbl, note6)
        if param_tbl:
            d = _inject_table(d, "5.", param_tbl, note5)
        _w(design, d)
    notes = dst / "docs" / "design" / "genre_notes.md"
    if lang == "en":
        parts = [f"# Genre notes: {title}", "",
                 f"<!-- From vibecodingflow genre preset {genre}. A starting point, not a verdict. When writing a review card, "
                 "take the most likely rework points and the sample test route from here. -->", ""]
    else:
        parts = [f"# 类型说明：{title}", "",
                 f"<!-- 来自 vibecodingflow 类型预设 {genre}。是起点不是定论。AI 写验收卡时，从这里取「最可能返工的点」和体验路线示例。 -->", ""]
    for h in H["notes"]:
        body = dk.section(text, h).strip()
        if body:
            parts += [f"## {h}", "", body, ""]
    notes.parent.mkdir(parents=True, exist_ok=True)
    _w(notes, "\n".join(parts))
    report["created"].append(notes)
    append_agents_line(dst, "genre_notes", dk.L(
        "10. 类型说明与常见返工点：`docs/design/genre_notes.md`（写验收卡、设计体验路线时参考）。",
        "10. Genre notes and common rework points: `docs/design/genre_notes.md` (use when writing review cards and test routes)."))


# ---------- 子代理与 hook ----------

def install_agents(dst, force, report, lang):
    for p in sorted((AGENTS_BASE / lang).glob("*.md")):
        copy_file(p, dst / ".claude" / "agents" / p.name, force, report)
    copy_file(REFS_BASE / lang / "delegation.md", dst / "docs" / "dev" / "references" / "delegation.md", force, report)
    append_agents_line(
        dst, "delegation.md",
        dk.L("11. 可委派的任务按计划任务表的「路由」交给 `.claude/agents/` 里的子代理；规则见 `docs/dev/references/delegation.md`。"
             "只有边界清楚、能机器验证的任务才委派；状态和签字永远由主会话和人处理。",
             "11. Delegable tasks go to the subagents in `.claude/agents/` according to the plan's \"Route\" column; rules in "
             "`docs/dev/references/delegation.md`. Delegate only bounded, machine-verifiable tasks; status and sign-off always stay "
             "with the main session and the human."),
    )


def install_claude_hooks(dst, force):
    """合并写入 .claude/settings.json 的 hooks。已有同类 hook 就不重复添加。返回提示列表。"""
    notes = []
    py = "python" if os.name == "nt" else "python3"
    path = dst / ".claude" / "settings.json"
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8") or "{}")
        except Exception:
            notes.append(dk.L(f"{path} 不是合法 JSON，未修改。请手动加入 hooks（见 README）",
                              f"{path} is not valid JSON; left unchanged. Add the hooks manually (see README)"))
            return notes
    hooks = data.setdefault("hooks", {})
    for event, arg in (("Stop", "stop"), ("SessionStart", "start")):
        groups = hooks.setdefault(event, [])
        if any("dk_hook.py" in h.get("command", "") for g in groups for h in g.get("hooks", [])):
            continue
        groups.append({"hooks": [{
            "type": "command",
            "command": f'{py} "${{CLAUDE_PROJECT_DIR}}/docs/dev/tools/dk_hook.py" {arg}',
            "timeout": 30,
        }]})
    path.parent.mkdir(parents=True, exist_ok=True)
    _w(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    notes.append(dk.L(f"已写入 {path.relative_to(dst)}（Stop 拦截 + SessionStart 摘要）",
                      f"Wrote {path.relative_to(dst)} (Stop blocker + SessionStart brief)"))
    return notes


def install_git_hook(dst):
    git = dst / ".git"
    if not git.is_dir():
        return dk.L("不是 git 仓库，跳过 pre-commit（git init 后再运行 --hooks 即可）",
                    "Not a git repo; skipped pre-commit (run git init, then re-run with --hooks)")
    hook = git / "hooks" / "pre-commit"
    if hook.exists() and PRE_COMMIT_MARK not in hook.read_text(encoding="utf-8", errors="ignore"):
        return dk.L("已有别的 pre-commit，未覆盖；可手动加一行：python3 docs/dev/tools/check_docs.py || exit 1",
                    "An existing pre-commit was left untouched; add manually: python3 docs/dev/tools/check_docs.py || exit 1")
    hook.parent.mkdir(parents=True, exist_ok=True)
    block_msg = dk.L("vibecodingflow：docs 检查有 ERROR，提交已拦截（git commit --no-verify 可跳过）",
                     "vibecodingflow: docs check found ERRORs, commit blocked (skip with git commit --no-verify)")
    head = dk.L(f"{PRE_COMMIT_MARK}：docs 规则有 ERROR 时拦截提交。跳过：git commit --no-verify",
                f"{PRE_COMMIT_MARK}: blocks the commit when the docs rules report ERRORs. Skip: git commit --no-verify")
    _w(
        hook,
        "#!/bin/sh\n"
        f"{head}\n"
        'PY=$(command -v python3 || command -v python)\n'
        '[ -z "$PY" ] && exit 0\n'
        f'"$PY" docs/dev/tools/check_docs.py >&2 || {{ echo "{block_msg}" >&2; exit 1; }}\n',
    )
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return dk.L("已安装 .git/hooks/pre-commit", "Installed .git/hooks/pre-commit")


# ---------- 主流程 ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="项目根目录（不存在会创建）")
    ap.add_argument("--lang", default="en", choices=LANGS, help="文档语言 en / zh")
    ap.add_argument("--name", default="", help="项目名，替换模板里的 {{项目名}}")
    ap.add_argument("--genre", default="", help="类型预设；list 列出可用项")
    ap.add_argument("--game", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--agents", action="store_true")
    ap.add_argument("--hooks", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    lang = dk.set_lang(a.lang)
    TEMPLATES = TEMPLATES_BASE / lang
    if a.genre == "list":
        print(dk.L("可用类型预设：", "Available genre presets: ") + dk.L("、", ", ").join(list_genres(lang)))
        return
    if not a.target:
        ap.error("需要项目目录 / project directory required")
    if a.genre and a.genre not in list_genres(lang):
        sys.exit(dk.L(f"没有这个类型预设：{a.genre}。可用：{'、'.join(list_genres(lang))}",
                      f"No such genre preset: {a.genre}. Available: {', '.join(list_genres(lang))}"))
    if not TEMPLATES.exists():
        sys.exit(dk.L(f"找不到模板目录：{TEMPLATES}（请从 skill 目录运行本脚本）",
                      f"Template directory not found: {TEMPLATES} (run this script from the skill folder)"))
    if a.genre and a.genre not in NON_GAME_GENRES:
        a.game = True

    dst = Path(a.target).resolve()
    dst.mkdir(parents=True, exist_ok=True)
    subs = {k: a.name for k in SUB_KEYS["name"]}
    subs.update({k: datetime.date.today().isoformat() for k in SUB_KEYS["date"]})
    report = {"created": [], "skipped": [], "placed": set()}

    # 先复制游戏层，这样它的 DESIGN.md 会先占位，核心层同名文件被跳过
    if a.game:
        copy_tree(TEMPLATES / "game", dst, subs, a.force, report)
    copy_tree(TEMPLATES / "core", dst, subs, a.force, report)
    if a.full:
        copy_tree(TEMPLATES / "full", dst, subs, a.force, report)

    claude_md = dst / "CLAUDE.md"
    if not claude_md.exists() or a.force:
        _w(claude_md, "@AGENTS.md\n")
        report["created"].append(claude_md)
    else:
        report["skipped"].append(claude_md)

    # 细则文档放进项目（默认不读），没装 skill 的工具也能查
    refs = dst / "docs" / "dev" / "references"
    copy_file(REFS_BASE / lang / "human-loop.md", refs / "human-loop.md", a.force, report)
    copy_file(REFS_BASE / lang / "grill.md", refs / "grill.md", a.force, report)
    if a.game:
        copy_file(REFS_BASE / lang / "game-layer.md", refs / "game-layer.md", a.force, report)
    (dst / "docs" / "dev").mkdir(parents=True, exist_ok=True)
    _w((dst / "docs" / "dev" / ".lang"), lang + "\n")

    # 工具每次都刷新为最新版（它们不是用户内容）
    tools = dst / "docs" / "dev" / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    for name in TOOLS:
        shutil.copy2(HERE / name, tools / name)
    shutil.copy2(PANEL_HTML, tools / "review_panel.html")

    notes = []
    if a.genre:
        apply_genre(dst, a.genre, report, lang)
        notes.append(dk.L(f"已带入类型预设「{a.genre}」：验收基准和手感参数起点已写进 DESIGN，常见返工点在 docs/design/genre_notes.md",
                          f'Applied genre preset "{a.genre}": baseline and starting parameters are in DESIGN; common rework points in docs/design/genre_notes.md'))
    if a.agents:
        install_agents(dst, a.force, report, lang)
        notes.append(dk.L("已安装子代理到 .claude/agents/（dk-implementer / dk-verifier / dk-scribe / dk-reviewer）",
                          "Installed subagents to .claude/agents/ (dk-implementer / dk-verifier / dk-scribe / dk-reviewer)"))
    if a.hooks:
        notes += install_claude_hooks(dst, a.force)
        notes.append(install_git_hook(dst))

    gi = dst / ".gitignore"
    line = "docs/dev/reviews/*.html"
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if line not in existing:
        _w(gi, existing + ("" if existing.endswith("\n") or not existing else "\n") + line + "\n")

    L = dk.L
    print(L(f"已初始化：{dst}", f"Initialized: {dst}"))
    print(L(f"  新建 {len(report['created'])} 个文件，跳过已存在 {len(report['skipped'])} 个；工具已放入 docs/dev/tools/",
            f"  Created {len(report['created'])} files, skipped {len(report['skipped'])} existing; tools placed in docs/dev/tools/"))
    for p in report["skipped"]:
        print(L(f"  - 跳过 {p.relative_to(dst)}", f"  - skipped {p.relative_to(dst)}"))
    for n in notes:
        print(f"  · {n}")
    print(L("\n下一步：", "\nNext steps:"))
    print(L("  1. 让 AI 按 docs/dev/references/grill.md 追问你，把答案落进 docs/design/DESIGN.md（尤其第 0 节批判性问题、第 4 节范围和第 6 节验收基准）" + ("；基准已有预设，按口味校准" if a.genre else ""),
            "  1. Have the AI interview you (docs/dev/references/grill.md) and land the answers in docs/design/DESIGN.md (especially §0 critical questions, §4 scope and §6 acceptance baseline)"
            + ("; the baseline already has a preset — calibrate it to your taste" if a.genre else "")))
    print(L("  2. 全局搜索 {{ 替换占位符；只想要精简版就不要加 --full",
            "  2. Search for {{ and replace the placeholders; skip --full if you only want the lean set"))
    print(L("  3. 对 AI 说：先读 AGENTS.md", "  3. Tell the AI: read AGENTS.md first"))
    print(L("  4. 随时检查：python docs/dev/tools/check_docs.py（--brief 看摘要，--progress 看任务进度，--stats 看统计）",
            "  4. Check anytime: python docs/dev/tools/check_docs.py (--brief for a summary, --progress for task progress, --stats for statistics)"))


if __name__ == "__main__":
    main()
