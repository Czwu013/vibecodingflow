"""vibecodingflow 测试套件（纯标准库）。运行：python -m unittest discover -s tests -v"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import dk_common as dk  # noqa: E402


def run(script, *args, cwd=None, stdin=None, env=None):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run(
        [sys.executable, "-I", str(script), *map(str, args)],
        cwd=cwd, input=stdin, capture_output=True, text=True, encoding="utf-8", env=e,
    )


def init(tmp, *flags):
    if "--lang" not in flags:
        flags = ("--lang", "zh") + flags  # 旧测试都针对中文项目；英文见 TestEnglish
    r = run(SCRIPTS / "init.py", tmp, *flags)
    assert r.returncode == 0, r.stderr + r.stdout
    return Path(tmp)


def tool(proj, name):
    return proj / "docs" / "dev" / "tools" / name


def check(proj, *flags):
    return run(tool(proj, "check_docs.py"), proj, *flags)


def set_plan(proj, rows):
    body = "# 里程碑计划\n\n| 里程碑 | 内容 | 状态 | 验收（轮次 · 结论） | 计划文档 |\n| --- | --- | --- | --- | --- |\n"
    body += "".join(f"| {r} |\n" for r in rows)
    (proj / "docs/dev/plans/README.md").write_text(body, encoding="utf-8")


def new_card(proj, ms="M1"):
    r = run(tool(proj, "new_review.py"), ms, "--root", proj)
    assert r.returncode == 0, r.stderr
    n = max(int(m.group(1)) for p in (proj / "docs/dev/reviews").glob(f"{ms}_r*.md")
            for m in [re.search(r"_r(\d+)\.md", p.name)])
    p = proj / f"docs/dev/reviews/{ms}_r{n}.md"
    # 填满 AI 部分的占位符
    t = re.sub(r"\{\{[^}]*\}\}", "ok", p.read_text(encoding="utf-8"))
    p.write_text(t, encoding="utf-8")
    return p


def fill(path, scores, concl, signer="", date="", override="", issues=""):
    t = Path(path).read_text(encoding="utf-8")
    for d, s in zip(["能用", "看着", "手感", "清晰", "想继续"], scores):
        why = "理由" if s <= 2 or s == 5 else ""
        t = re.sub(rf"^\| {d} \|.*$", f"| {d} | {s} | {why} |", t, flags=re.M)
    if issues:
        t = t.replace("### 问题\n", "### 问题\n" + issues + "\n", 1)
    t = re.sub(r"^结论：.*$", f"结论：{concl}", t, flags=re.M)
    t = re.sub(r"^验收人：.*$", f"验收人：{signer}", t, flags=re.M)
    t = re.sub(r"^日期：.*$", f"日期：{date}", t, flags=re.M)
    t = re.sub(r"^(覆盖原因[^\n]*：).*$", lambda m: m.group(1) + override, t, flags=re.M)
    Path(path).write_text(t, encoding="utf-8")


class Base(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.tmp = Path(self._td.name)
        self.addCleanup(self._td.cleanup)

    def project(self, *flags):
        return init(self.tmp / "proj", "--name", "测试", *flags)


class TestVerdictRules(unittest.TestCase):
    def test_table(self):
        s = dk.suggest_verdict
        D = ["能用", "看着", "手感", "清晰", "想继续"]
        cases = [
            ([4, 4, 4, 4, 4], [], "通过"),
            ([5, 5, 4, 4, 4], [], "通过"),
            ([4, 4, 4, 4, 4], [("看着", "低", "x", "")], "通过"),
            ([4, 3, 4, 4, 4], [], "小改后过"),
            ([4, 4, 4, 4, 4], [("手感", "中", "x", "")], "小改后过"),
            ([4, 3, 2, 4, 4], [], "返工"),
            ([4, 4, 4, 4, 4], [("手感", "高", "x", "")], "返工"),
            ([1, 4, 4, 4, 4], [], "返工"),
        ]
        for scores, issues, want in cases:
            self.assertEqual(s(dict(zip(D, scores)), issues)[0], want, (scores, issues))
        self.assertEqual(s({}, [])[0], None)


class TestInit(Base):
    def test_core_files_and_claude_md(self):
        p = self.project()
        for rel in ["AGENTS.md", "CLAUDE.md", "README.md", "docs/design/DESIGN.md", "docs/dev/README.md",
                    "docs/dev/contracts/taste.md", "docs/dev/contracts/feedback_friendly.md",
                    "docs/dev/reviews/_TEMPLATE_review.md", "docs/dev/references/human-loop.md"]:
            self.assertTrue((p / rel).exists(), rel)
        self.assertEqual((p / "CLAUDE.md").read_text(encoding="utf-8").strip(), "@AGENTS.md")
        for t in ["dk_common.py", "check_docs.py", "new_review.py", "build_panel.py", "dk_hook.py", "adopt.py", "review_panel.html"]:
            self.assertTrue(tool(p, t).exists(), t)

    def test_grill_reference_copied_into_project(self):
        p = self.project()
        self.assertTrue((p / "docs/dev/references/grill.md").exists())
        self.assertIn("追问", (p / "docs/dev/references/grill.md").read_text(encoding="utf-8"))
        en = init(self.tmp / "en", "--lang", "en", "--name", "Demo")
        self.assertIn("interview", (en / "docs/dev/references/grill.md").read_text(encoding="utf-8").lower())

    def test_idempotent_and_no_overwrite(self):
        p = self.project()
        (p / "AGENTS.md").write_text("我的内容\n", encoding="utf-8")
        init(p, "--name", "x")
        self.assertEqual((p / "AGENTS.md").read_text(encoding="utf-8"), "我的内容\n")

    def test_genre_injects_baseline(self):
        p = self.project("--genre", "platformer")
        design = (p / "docs/design/DESIGN.md").read_text(encoding="utf-8")
        sec6 = dk.strip_comments(dk.section(design, "6."))
        self.assertIn("土狼时间", sec6)
        self.assertNotIn("{{", sec6)
        self.assertIn("类型预设", sec6)
        self.assertIn("土狼时间", dk.section(design, "5."))
        notes = (p / "docs/design/genre_notes.md").read_text(encoding="utf-8")
        self.assertIn("常见返工点", notes)
        self.assertIn("genre_notes.md", (p / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertTrue((p / "docs/dev/contracts/game_rules.md").exists())  # 自动带上游戏层

    def test_all_genres_have_required_sections(self):
        for g in sorted((ROOT / "assets/genres/zh").glob("*.md")):
            t = g.read_text(encoding="utf-8")
            for h in ["验收基准", "手感参数起点", "常见返工点", "体验路线示例", "一分钟测试", "灰盒阶段验什么"]:
                self.assertTrue(dk.section(t, h).strip(), f"{g.name} 缺 {h}")
            rows = [l for l in dk.section(t, "验收基准").splitlines() if l.startswith("|")]
            self.assertEqual(len(rows), 7, g.name)  # 表头 + 分隔 + 5 个维度
            for d in ["能用", "看着", "手感", "清晰", "想继续"]:
                self.assertTrue(any(r.startswith(f"| {d} ") for r in rows), f"{g.name} 缺维度 {d}")

    def test_every_genre_inits(self):
        for g in sorted((ROOT / "assets/genres/zh").glob("*.md")):
            p = init(self.tmp / g.stem, "--genre", g.stem)
            sec6 = dk.strip_comments(dk.section((p / "docs/design/DESIGN.md").read_text(encoding="utf-8"), "6."))
            self.assertNotIn("{{", sec6, g.stem)

    def test_unknown_genre_fails(self):
        r = run(SCRIPTS / "init.py", self.tmp / "x", "--genre", "nope")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("platformer", r.stderr + r.stdout)

    def test_agents_installed(self):
        p = self.project("--agents")
        want = {"dk-implementer": "sonnet", "dk-verifier": "sonnet", "dk-scribe": "haiku", "dk-reviewer": "opus"}
        for name, model in want.items():
            f = p / ".claude/agents" / f"{name}.md"
            self.assertTrue(f.exists(), name)
            t = f.read_text(encoding="utf-8")
            fm = re.match(r"---\n(.*?)\n---\n", t, flags=re.S).group(1)
            self.assertIn(f"name: {name}", fm)
            self.assertRegex(fm, rf"(?m)^model: {model}$")
            self.assertRegex(fm, r"(?m)^description: .{40,}")
            tools = re.search(r"(?m)^tools: (.*)$", fm).group(1)
            self.assertNotIn("Agent", tools)  # 不再往下派
        # 验证者和审查者不能改源码
        for n in ("dk-verifier", "dk-reviewer"):
            tools = re.search(r"(?m)^tools: (.*)$", (p / ".claude/agents" / f"{n}.md").read_text(encoding="utf-8")).group(1)
            self.assertNotIn("Edit", tools)
            self.assertNotIn("Write", tools)
        self.assertTrue((p / "docs/dev/references/delegation.md").exists())
        self.assertIn("delegation.md", (p / "AGENTS.md").read_text(encoding="utf-8"))

    def test_hooks_merge_and_idempotent(self):
        proj = self.tmp / "proj"
        (proj / ".claude").mkdir(parents=True)
        (proj / ".claude/settings.json").write_text(json.dumps({"permissions": {"allow": ["Bash(ls)"]}}), encoding="utf-8")
        subprocess.run(["git", "init", "-q", str(proj)], check=True)
        init(proj, "--hooks")
        init(proj, "--hooks")  # 第二次不重复
        data = json.loads((proj / ".claude/settings.json").read_text(encoding="utf-8"))
        self.assertEqual(data["permissions"]["allow"], ["Bash(ls)"])  # 保留原有设置
        for ev, arg in (("Stop", "stop"), ("SessionStart", "start")):
            groups = data["hooks"][ev]
            self.assertEqual(len(groups), 1, ev)
            h = groups[0]["hooks"][0]
            self.assertEqual(h["type"], "command")
            self.assertIn("${CLAUDE_PROJECT_DIR}/docs/dev/tools/dk_hook.py", h["command"])
            self.assertTrue(h["command"].endswith(" " + arg))
        pc = proj / ".git/hooks/pre-commit"
        self.assertTrue(pc.exists())
        self.assertTrue(os.access(pc, os.X_OK))

    def test_hooks_keep_foreign_precommit(self):
        proj = self.tmp / "proj"
        subprocess.run(["git", "init", "-q", str(proj)], check=True)
        pc = proj / ".git/hooks/pre-commit"
        pc.parent.mkdir(parents=True, exist_ok=True)
        pc.write_text("#!/bin/sh\necho mine\n", encoding="utf-8")
        init(proj, "--hooks")
        self.assertIn("echo mine", pc.read_text(encoding="utf-8"))

    def test_hooks_invalid_json_untouched(self):
        proj = self.tmp / "proj"
        (proj / ".claude").mkdir(parents=True)
        (proj / ".claude/settings.json").write_text("{坏的", encoding="utf-8")
        init(proj, "--hooks")
        self.assertEqual((proj / ".claude/settings.json").read_text(encoding="utf-8"), "{坏的")


class TestChecker(Base):
    def ready(self, *flags):
        """带类型预设的项目（验收基准已填），方便测其他规则。"""
        return self.project("--genre", "platformer", *flags)

    def test_fresh_project_passes(self):
        p = self.project()
        r = check(p)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0 个错误", r.stdout)

    def test_done_without_card_is_error(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 完成 | — | —"])
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("完成", r.stdout)

    def test_done_requires_signature(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 完成 | — | —"])
        card = new_card(p)
        fill(card, [4, 4, 4, 4, 4], "通过")  # 没签字
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("缺验收人", r.stdout)
        fill(card, [4, 4, 4, 4, 4], "通过", "小陈", "2026-11-02")
        r = check(p)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_verdict_mismatch_needs_override(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 待验收 | — | —"])
        card = new_card(p)
        issues = "1.[手感][高] 飘 | 利落"
        fill(card, [4, 3, 2, 4, 3], "通过", "小陈", "2026-11-02", "", issues)
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("不一致", r.stdout)
        fill(card, [4, 3, 2, 4, 3], "通过", "小陈", "2026-11-02", "故意的", issues)
        self.assertNotIn("不一致", check(p).stdout)

    def test_rework_but_status_pending_warns(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 待验收 | — | —"])
        card = new_card(p)
        fill(card, [4, 3, 2, 4, 3], "返工", "小陈", "2026-11-02", "", "1.[手感][高] 飘 | 利落")
        out = check(p).stdout
        self.assertIn("应退回「进行中」", out)

    def test_circuit_breaker(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 进行中 | — | —"])
        for _ in range(2):
            card = new_card(p)
            fill(card, [4, 4, 2, 4, 4], "返工", "小陈", "2026-11-02", "", "1.[手感][高] 飘 | 利落")
        self.assertIn("连续 2 轮返工", check(p).stdout)

    def test_design_gate(self):
        p = self.project()  # 通用版，验收基准未填
        set_plan(p, ["M1 灰盒 | x | 待验收 | — | —"])
        new_card(p)
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("验收基准", r.stdout)
        set_plan(p, ["M1 灰盒 | x | 进行中 | — | —"])
        r = check(p)
        self.assertEqual(r.returncode, 0)  # 进行中只是警告
        self.assertIn("验收基准", r.stdout)

    def test_debt_requires_payoff(self):
        p = self.project()
        f = p / "docs/dev/DEVELOP_DEBT.md"
        t = f.read_text(encoding="utf-8")
        line = [l for l in t.splitlines() if l.startswith("| DEBT-001")][0]
        f.write_text(t.replace(line, "| DEBT-001 | 2026-10-31 | 没建 git | 无法退回 |  | 高 |"), encoding="utf-8")
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("还清", r.stdout)

    def test_strict_fails_on_placeholders(self):
        p = self.project()
        self.assertEqual(check(p, "--strict").returncode, 1)

    def test_delegation_lint_and_stats(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 进行中 | — | —"])
        plan = p / "docs/dev/plans/M1_greybox.md"
        plan.write_text(
            "# M1\n\n## 任务拆分\n"
            "| # | 任务 | 文件范围 | 机器验证 | 路由 | 结果 |\n| --- | --- | --- | --- | --- | --- |\n"
            "| T1 | 缺验证 | src/a.js | | sonnet | |\n"
            "| T2 | 主会话做 | | | 主 | 一次通过 |\n"
            "| T3 | 并行A | src/ | npm test | sonnet | |\n"
            "| T4 | 并行B | src/b.js | npm test | haiku | |\n"
            "| T5 | 做完了 | src/c.js | npm test | sonnet | 一次通过 |\n"
            "| T6 | 返修了 | src/d.js | npm test | sonnet | 返修1次 |\n"
            "| T7 | 路由写错 | src/e.js | x | gpt | |\n",
            encoding="utf-8")
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("T1", r.stdout)
        self.assertIn("缺机器验证", r.stdout)
        self.assertIn("文件范围重叠", r.stdout)  # T3(src/) 与 T4(src/b.js)
        self.assertIn("路由「gpt」", r.stdout)
        self.assertNotIn("T2：", r.stdout)  # 路由为"主"不需要范围和验证
        s = check(p, "--stats").stdout
        self.assertIn("分派统计", s)
        self.assertRegex(s, r"sonnet\s+4\s+2\s+50%")

    def test_brief(self):
        p = self.ready()
        set_plan(p, ["M0 基线 | x | 完成 | — | —", "M1 灰盒 | x | 进行中 | — | —"])
        out = check(p, "--brief").stdout
        self.assertTrue(out.startswith("[vibecodingflow 状态]"))
        self.assertIn("当前：M1", out)
        self.assertLessEqual(len(out.strip().splitlines()), 15)

    def _plan_with_tasks(self, p, status, rows):
        set_plan(p, [f"M1 灰盒 | x | {status} | — | —"])
        (p / "docs/dev/plans/M1_greybox.md").write_text(
            "# M1\n\n## 任务拆分\n"
            "| # | 任务 | 文件范围 | 机器验证 | 路由 | 结果 |\n| --- | --- | --- | --- | --- | --- |\n" + rows,
            encoding="utf-8")

    def test_progress_command_and_brief_line(self):
        p = self.ready()
        self._plan_with_tasks(p, "进行中",
                              "| T1 | 表单 | src/a.js | npm test | 主 | 一次通过 |\n"
                              "| T2 | 保存 | src/b.js | npm test | 主 | 返修1次 |\n"
                              "| T3 | 刷新保留 | src/c.js | npm test | 主 | |\n"
                              "| T4 | 统计 | src/d.js | npm test | 主 | |\n")
        out = check(p, "--progress").stdout
        self.assertIn("2/4", out)
        self.assertIn("[##########----------]", out)
        brief = check(p, "--brief").stdout
        self.assertIn("任务进度：M1 [#####-----] 2/4", brief)
        self.assertLessEqual(len(brief.strip().splitlines()), 15)

    def test_progress_without_tasks_does_not_crash(self):
        p = self.project()
        r = check(p, "--progress")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("任务进度", check(p, "--brief").stdout)

    def test_consistency_in_progress_needs_plan_file(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 进行中 | — | —"])
        self.assertIn("没有 M1_*.md 计划文件", check(p).stdout)
        set_plan(p, ["M0 接手基线 | x | 进行中 | — | —"])
        self.assertNotIn("计划文件", check(p).stdout)  # M0 是接手基线，不需要计划文件

    def test_consistency_review_with_unfinished_tasks_warns(self):
        p = self.ready()
        self._plan_with_tasks(p, "待验收", "| T1 | 表单 | src/a.js | npm test | 主 | 一次通过 |\n"
                                           "| T2 | 保存 | src/b.js | npm test | 主 | |\n")
        out = check(p).stdout
        self.assertIn("还有 1 个任务没有结果（T2）", out)

    def test_consistency_main_task_needs_check(self):
        p = self.ready()
        self._plan_with_tasks(p, "进行中", "| T1 | 没写验证 | src/a.js | | 主 | |\n"
                                           "| T2 | 做完了没写验证 | src/b.js | | 主 | 一次通过 |\n")
        out = check(p).stdout
        self.assertIn("T1：没写验证方式", out)
        self.assertNotIn("T2：没写验证方式", out)

    def test_new_review_prefills_recheck(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 进行中 | — | —"])
        new_card(p)
        log = p / "docs/dev/feedback_log.md"
        t = log.read_text(encoding="utf-8")
        line = [l for l in t.splitlines() if l.startswith("| FB-001")][0]
        log.write_text(t.replace(line, "| FB-001 | M1·r1 | 手感 | 高 | 太飘 | 利落 | 种子1 | 已修改，待复验 | 重力 2.4→3.1 |"), encoding="utf-8")
        r2 = new_card(p)
        self.assertIn("FB-001", r2.read_text(encoding="utf-8"))
        data = json.loads(self._panel_data(p, r2))
        self.assertEqual(data["recheck"][0]["id"], "FB-001")
        self.assertEqual(data["round"], 2)

    def _panel_data(self, p, card):
        out = card.with_suffix(".html")
        r = run(tool(p, "build_panel.py"), card, "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        m = re.search(r"var D = (\{.*?\});\nif\(!D\)", out.read_text(encoding="utf-8"), flags=re.S)
        return m.group(1).replace("<\\/", "</")

    def test_panel_data_strips_step_numbers(self):
        p = self.ready()
        set_plan(p, ["M1 灰盒 | x | 进行中 | — | —"])
        card = new_card(p)
        t = card.read_text(encoding="utf-8").replace("- ok\n\n### AI 已验证", "- 1. 起跳三次 → 高度可控\n- 2. 急停 → 不滑步\n\n### AI 已验证", 1)
        card.write_text(t, encoding="utf-8")
        d = json.loads(self._panel_data(p, card))
        self.assertEqual(d["steps"][:2], ["起跳三次 → 高度可控", "急停 → 不滑步"])
        self.assertEqual(d["dims"], ["能用", "看着", "手感", "清晰", "想继续"])


class TestHook(Base):
    def setUp(self):
        super().setUp()
        # 防死循环的计数器按会话 ID 存在系统临时目录里，每个测试用独立的会话 ID，避免互相污染
        self.session = "test-" + uuid.uuid4().hex
        self.addCleanup(lambda: [f.unlink() for f in Path(tempfile.gettempdir()).glob(f"dk_hook_{self.session}*.json")])

    def stop(self, proj, session=None):
        return run(tool(proj, "dk_hook.py"), "stop", cwd=proj,
                   stdin=json.dumps({"session_id": session or self.session, "cwd": str(proj)}),
                   env={"CLAUDE_PROJECT_DIR": str(proj)})

    def broken(self):
        p = self.project("--genre", "platformer")
        set_plan(p, ["M1 灰盒 | x | 完成 | — | —"])  # 完成但没有验收卡 → ERROR
        return p

    def test_stop_blocks_then_releases(self):
        p = self.broken()
        r1 = self.stop(p)
        out = json.loads(r1.stdout)
        self.assertEqual(out["decision"], "block")
        self.assertIn("M1", out["reason"])
        self.assertIn("不要自行绕过或代签", out["reason"])
        self.assertEqual(json.loads(self.stop(p).stdout)["decision"], "block")
        r3 = self.stop(p)  # 同一错误第 3 次：放行
        self.assertEqual(r3.stdout.strip(), "")
        self.assertEqual(r3.returncode, 0)
        self.assertIn("不再拦截", r3.stderr)

    def test_stop_silent_when_clean(self):
        p = self.project()
        r = self.stop(p)
        self.assertEqual(r.stdout.strip(), "")
        self.assertEqual(r.returncode, 0)

    def test_stop_state_resets_after_fix(self):
        p = self.broken()
        self.stop(p)
        set_plan(p, ["M1 灰盒 | x | 进行中 | — | —"])  # 修好
        self.assertEqual(self.stop(p).stdout.strip(), "")
        set_plan(p, ["M1 灰盒 | x | 完成 | — | —"])  # 再次出错应重新计数，被拦
        self.assertEqual(json.loads(self.stop(p).stdout)["decision"], "block")

    def test_start_injects_brief(self):
        p = self.broken()
        r = run(tool(p, "dk_hook.py"), "start", cwd=p, stdin=json.dumps({"cwd": str(p)}), env={"CLAUDE_PROJECT_DIR": str(p)})
        self.assertEqual(r.returncode, 0)
        self.assertTrue(r.stdout.startswith("[vibecodingflow 状态]"))
        self.assertIn("M1 完成", r.stdout)

    def test_silent_outside_project(self):
        d = self.tmp / "other"
        d.mkdir()
        p = self.project()
        r = run(tool(p, "dk_hook.py"), "stop", cwd=d, stdin="{}", env={"CLAUDE_PROJECT_DIR": str(d)})
        self.assertEqual((r.stdout.strip(), r.returncode), ("", 0))

    def test_garbage_stdin_does_not_crash(self):
        p = self.project()
        r = run(tool(p, "dk_hook.py"), "stop", cwd=p, stdin="不是json", env={"CLAUDE_PROJECT_DIR": str(p)})
        self.assertEqual(r.returncode, 0)


@unittest.skipUnless(shutil.which("git") and shutil.which("sh"), "需要 git 和 sh")
class TestEndToEndHooks(Base):
    def git(self, proj, *args):
        return subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "-C", str(proj), *args],
                              capture_output=True, text=True, encoding="utf-8")

    def test_hook_script_is_lf_only(self):
        # Windows 上用 write_text 会写出 CRLF，"#!/bin/sh\r" 无法执行
        proj = self.tmp / "proj"
        subprocess.run(["git", "init", "-q", str(proj)], check=True)
        init(proj, "--hooks")
        self.assertNotIn(b"\r", (proj / ".git/hooks/pre-commit").read_bytes())
        self.assertNotIn(b"\r", (proj / "AGENTS.md").read_bytes())

    def test_precommit_blocks_bad_commit_then_allows_good(self):
        proj = self.tmp / "proj"
        subprocess.run(["git", "init", "-q", str(proj)], check=True)
        init(proj, "--genre", "platformer", "--hooks")
        set_plan(proj, ["M1 灰盒 | x | 完成 | — | —"])  # 完成但没有验收卡
        self.git(proj, "add", "-A")
        bad = self.git(proj, "commit", "-qm", "bad")
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("提交已拦截", bad.stderr)
        set_plan(proj, ["M1 灰盒 | x | 进行中 | — | —"])
        self.git(proj, "add", "-A")
        good = self.git(proj, "commit", "-qm", "good")
        self.assertEqual(good.returncode, 0, good.stderr)

    def test_settings_command_runs_through_shell(self):
        proj = self.tmp / "proj"
        init(proj, "--genre", "platformer", "--hooks")
        data = json.loads((proj / ".claude/settings.json").read_text(encoding="utf-8"))
        stdin = json.dumps({"session_id": "sh-" + uuid.uuid4().hex, "cwd": str(proj)})
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(proj))
        # Claude Code 在 Windows 上也是用 Git Bash 执行 hook；cmd.exe 不认 ${VAR}，所以这里显式用 sh
        start = subprocess.run(["sh", "-c", data["hooks"]["SessionStart"][0]["hooks"][0]["command"]], input=stdin,
                               capture_output=True, text=True, encoding="utf-8", env=env, cwd=self.tmp)
        self.assertEqual(start.returncode, 0, start.stderr)
        self.assertTrue(start.stdout.startswith("[vibecodingflow 状态]"), start.stdout)


class TestAdopt(Base):
    def test_godot(self):
        d = self.tmp / "g"
        d.mkdir()
        (d / "project.godot").write_text('config/features=PackedStringArray("4.3", "Forward Plus")\nrun/main_scene="res://main.tscn"\n', encoding="utf-8")
        (d / "player.gd").write_text("func _ready():\n\tvar x = randf()\n" * 5, encoding="utf-8")
        out = run(SCRIPTS / "adopt.py", d, "--lang", "zh").stdout
        self.assertIn("Godot 4.3", out)
        self.assertIn("res://main.tscn", out)
        self.assertIn("不是 git 仓库", out)
        self.assertIn("没有一键复制调试信息", out)
        self.assertIn("随机没有走带种子的随机数", out)

    def test_web_phaser(self):
        d = self.tmp / "w"
        (d / "src").mkdir(parents=True)
        (d / "package.json").write_text(json.dumps({"dependencies": {"phaser": "^3.80.1"}, "scripts": {"dev": "vite"}}), encoding="utf-8")
        (d / "index.html").write_text("<canvas></canvas>", encoding="utf-8")
        (d / "src/main.js").write_text("const rng = mulberry32(seed);\nconst f = document.addEventListener('keydown', e => e.key==='F8' && navigator.clipboard.writeText('x'));\n", encoding="utf-8")
        (d / "test_game.py").write_text("", encoding="utf-8")
        out = run(SCRIPTS / "adopt.py", d, "--lang", "zh").stdout
        self.assertIn("Web: phaser ^3.80.1", out)
        self.assertIn("npm run dev", out)
        self.assertNotIn("没有一键复制调试信息", out)  # 找到了 F8 / clipboard
        self.assertNotIn("没有自动化测试", out)

    def test_ignores_node_modules(self):
        d = self.tmp / "n"
        (d / "node_modules/x").mkdir(parents=True)
        (d / "node_modules/x/big.js").write_text("a\n" * 9999, encoding="utf-8")
        (d / "app.js").write_text("a\n", encoding="utf-8")
        out = run(SCRIPTS / "adopt.py", d, "--lang", "zh").stdout
        self.assertNotIn("big.js", out)

    def test_output_file(self):
        d = self.tmp / "o"
        d.mkdir()
        (d / "a.py").write_text("x=1\n", encoding="utf-8")
        run(SCRIPTS / "adopt.py", d, "--lang", "zh", "-o", self.tmp / "scan.md")
        self.assertTrue((self.tmp / "scan.md").read_text(encoding="utf-8").startswith("# 接手扫描"))


def new_card_en(proj, ms="M1"):
    r = run(tool(proj, "new_review.py"), ms, "--root", proj)
    assert r.returncode == 0, r.stderr
    n = max(int(re.search(r"_r(\d+)\.md", p.name).group(1)) for p in (proj / "docs/dev/reviews").glob(f"{ms}_r*.md"))
    p = proj / f"docs/dev/reviews/{ms}_r{n}.md"
    t = re.sub(r"\{\{[^}]*\}\}", "ok", p.read_text(encoding="utf-8"))
    p.write_text(t, encoding="utf-8")
    return p


def fill_en(path, scores, concl, signer="", date="", override="", issues=""):
    t = Path(path).read_text(encoding="utf-8")
    for d, s in zip(["Usable", "Looks", "Feel", "Clarity", "Engaging"], scores):
        why = "reason" if s <= 2 or s == 5 else ""
        t = re.sub(rf"^\| {d} \|.*$", f"| {d} | {s} | {why} |", t, flags=re.M)
    t = re.sub(r"(### Issues\n(?:(?s:<!--.*?-->)\n)?)(?:\d+\. [^\n]*\n)*", lambda m: m.group(1) + (issues + "\n" if issues else ""), t, count=1)
    t = re.sub(r"^Verdict:.*$", f"Verdict: {concl}", t, flags=re.M)
    t = re.sub(r"^Reviewer:.*$", f"Reviewer: {signer}", t, flags=re.M)
    t = re.sub(r"^Date:.*$", f"Date: {date}", t, flags=re.M)
    t = re.sub(r"^(Override reason[^\n]*:).*$", lambda m: m.group(1) + " " + override, t, flags=re.M)
    Path(path).write_text(t, encoding="utf-8")


def set_plan_en(proj, rows):
    body = "# Plan\n\n| Milestone | Content | Status | Review (rounds · verdict) | Plan doc |\n| --- | --- | --- | --- | --- |\n"
    body += "".join(f"| {r} |\n" for r in rows)
    (proj / "docs/dev/plans/README.md").write_text(body, encoding="utf-8")


CJK = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")


class TestEnglish(unittest.TestCase):
    """英文项目：模板、解析、检查输出、面板数据、hook、接手扫描全链路。"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def project(self, *flags):
        return init(self.tmp / "p", "--lang", "en", "--name", "Demo", *flags)

    def test_no_cjk_in_english_trees(self):
        for base in ["assets/templates/en", "assets/genres/en", "assets/agents/en", "references/en"]:
            for f in (ROOT / base).rglob("*"):
                if f.is_file():
                    self.assertFalse(CJK.search(f.read_text(encoding="utf-8")), f"CJK left in {f}")

    def test_zh_en_trees_have_same_files(self):
        for base in ["assets/templates", "assets/genres", "assets/agents", "references"]:
            zh = {p.relative_to(ROOT / base / "zh") for p in (ROOT / base / "zh").rglob("*") if p.is_file()}
            en = {p.relative_to(ROOT / base / "en") for p in (ROOT / base / "en").rglob("*") if p.is_file()}
            if base == "references":
                zh.discard(Path("SKILL.zh.md"))
            self.assertEqual(zh, en, base)

    def test_english_project_has_no_chinese_and_passes_check(self):
        p = self.project("--genre", "platformer", "--agents", "--hooks", "--full")
        for f in p.rglob("*"):
            if f.is_file() and ".git" not in f.parts and "tools" not in f.parts and f.suffix in (".md", ".json", ""):
                self.assertFalse(CJK.search(f.read_text(encoding="utf-8")), f"CJK in generated {f.relative_to(p)}")
        self.assertEqual((p / "docs/dev/.lang").read_text().strip(), "en")
        r = check(p)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("All checks passed", r.stdout)
        self.assertRegex((p / "docs/design/DESIGN.md").read_text(encoding="utf-8"), r"Acceptance baseline")

    def test_genre_baseline_injected_in_english(self):
        for g in sorted(p.stem for p in (ROOT / "assets/genres/en").glob("*.md")):
            proj = init(self.tmp / g, "--lang", "en", "--genre", g)
            sec6 = dk.strip_comments(dk.section((proj / "docs/design/DESIGN.md").read_text(encoding="utf-8"), "6."))
            self.assertNotIn("{{", sec6, g)
            self.assertIn("Usable", sec6, g)
            notes = (proj / "docs/design/genre_notes.md").read_text(encoding="utf-8")
            self.assertIn("Common rework points", notes, g)

    def test_full_review_cycle_english(self):
        p = self.project("--genre", "platformer")  # 预设填好 DESIGN §6，否则验收基准闸门会报错
        # 在英文模板上走完：In review 没卡 → ERROR；Done 没签字 → ERROR；签字 Pass → 通过
        (p / "docs/dev/plans/README.md").write_text(
            "# Plan\n\n| Milestone | Content | Status | Review (rounds · verdict) | Plan doc |\n| --- | --- | --- | --- | --- |\n"
            "| M1 Jump | jump | In review | — | — |\n", encoding="utf-8")
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("M1 is marked \"In review\" but has no review card", r.stdout)
        card = new_card_en(p)
        # 第 1 轮：Feel 2 + High issue → Rework
        fill_en(card, [4, 3, 2, 4, 3], "Rework", signer="Sam", date="2026-10-31",
                issues="1. [Feel][High] floaty landing | wants it crisp")
        parsed = dk.parse_review(card.read_text(encoding="utf-8"))
        self.assertEqual(parsed["conclusion"], "返工")
        self.assertEqual(parsed["issues"][0][:2], ("Feel", "高"))
        self.assertEqual(parsed["scores"]["Feel"], 2)
        sug = run(tool(p, "check_docs.py"), "--suggest", card).stdout
        self.assertIn("Suggested verdict: Rework", sug)
        # 结论与分数不符且没覆盖原因 → ERROR（英文消息）
        fill_en(card, [4, 3, 2, 4, 3], "Pass", signer="Sam", date="2026-10-31")
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("differs from the score-based", r.stdout)
        # 状态 Done 但最新卡是 Rework
        fill_en(card, [4, 3, 2, 4, 3], "Rework", signer="Sam", date="2026-10-31", issues="")
        set_plan_en(p, ["M1 Jump | jump | Done | — | —"])
        r = check(p)
        self.assertIn("has not passed human review", r.stdout)
        # 第 2 轮签字通过 → 干净
        card2 = new_card_en(p)
        fill_en(card2, [4, 4, 4, 4, 4], "Pass", signer="Sam", date="2026-10-31")
        r = check(p)
        self.assertEqual(r.returncode, 0, r.stdout)
        stats = check(p, "--stats").stdout
        self.assertIn("First-round pass rate: 0/1", stats)
        self.assertIn("Rework → Pass", stats)

    def test_signoff_cannot_be_forged_by_status_alone_english(self):
        p = self.project()
        set_plan_en(p, ["M1 Jump | jump | Done | — | —"])
        r = check(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("Only a human review can confirm Done", r.stdout)

    def test_english_status_tokens_in_feedback_and_debt(self):
        p = self.project()
        debt = p / "docs/dev/DEVELOP_DEBT.md"
        t = debt.read_text(encoding="utf-8")
        t = re.sub(r"^\| DEBT-001 .*$", "| DEBT-001 | 2026-10-31 | no git | cannot roll back |  | High |", t, flags=re.M)
        debt.write_text(t, encoding="utf-8")
        r = check(p)
        self.assertIn("has no \"Payoff criteria\"", r.stdout)

    def test_hook_stop_message_is_english(self):
        p = self.project("--hooks")
        set_plan_en(p, ["M1 Jump | jump | Done | — | —"])
        sid = "t-" + uuid.uuid4().hex
        r = run(tool(p, "dk_hook.py"), "stop", stdin=json.dumps({"session_id": sid, "cwd": str(p)}), env={"CLAUDE_PROJECT_DIR": str(p)})
        self.addCleanup(lambda: (Path(tempfile.gettempdir()) / f"dk_hook_{sid}.json").unlink(missing_ok=True))
        out = json.loads(r.stdout)
        self.assertEqual(out["decision"], "block")
        self.assertIn("handle them before finishing", out["reason"])
        self.assertFalse(CJK.search(out["reason"]))

    def test_progress_and_consistency_english(self):
        p = self.project("--genre", "web_app_tool")
        set_plan_en(p, ["M1 Core | x | In review | — | —"])
        (p / "docs/dev/plans/M1_core.md").write_text(
            "# M1\n\n## Tasks\n"
            "| # | Task | File scope | Machine check | Route | Result |\n| --- | --- | --- | --- | --- | --- |\n"
            "| T1 | Form | src/a.js | npm test | main | First pass |\n"
            "| T2 | Save | src/b.js | npm test | main | Retry 1x |\n"
            "| T3 | Reload | src/c.js | npm test | main | |\n",
            encoding="utf-8")
        prog = check(p, "--progress").stdout
        self.assertIn("2/3", prog)
        self.assertFalse(CJK.search(prog), prog)
        brief = check(p, "--brief").stdout
        self.assertIn("Task progress: M1 [#######---] 2/3", brief)
        self.assertFalse(CJK.search(brief), brief)
        out = check(p).stdout
        self.assertIn("1 task(s) in the table have no result (T3)", out)
        self.assertFalse(CJK.search(out), out)

    def test_hook_start_brief_english(self):
        p = self.project("--hooks")
        r = run(tool(p, "dk_hook.py"), "start", stdin=json.dumps({"cwd": str(p)}), env={"CLAUDE_PROJECT_DIR": str(p)})
        self.assertIn("[vibecodingflow status]", r.stdout)
        self.assertFalse(CJK.search(r.stdout), r.stdout)

    def test_panel_data_english(self):
        p = self.project()
        set_plan_en(p, ["M1 Jump | jump | In review | — | —"])
        card = new_card_en(p)
        t = card.read_text(encoding="utf-8")
        t = t.replace("- ok\n\n### Key questions", "- ok\n\n### Key questions", 1)
        card.write_text(t, encoding="utf-8")
        out = self.tmp / "panel.html"
        r = run(tool(p, "build_panel.py"), card, "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        html = out.read_text(encoding="utf-8")
        data = json.loads(re.search(r"var D = (\{.*?\});\nif\(!D\)", html, flags=re.S).group(1))
        self.assertEqual(data["lang"], "en")
        self.assertEqual(data["dims"], ["Usable", "Looks", "Feel", "Clarity", "Engaging"])
        self.assertTrue(data["steps"])

    def test_adopt_english_default(self):
        d = self.tmp / "g"
        d.mkdir()
        (d / "project.godot").write_text("config_version=5\nconfig/features=PackedStringArray(\"4.3\")\n", encoding="utf-8")
        (d / "a.gd").write_text("extends Node\n", encoding="utf-8")
        out = run(SCRIPTS / "adopt.py", d).stdout
        self.assertIn("Adoption scan", out)
        self.assertIn("Godot 4.3", out)
        self.assertFalse(CJK.search(out.replace("（", "").replace("）", "")), out)

    def test_default_lang_is_english(self):
        r = run(SCRIPTS / "init.py", self.tmp / "d")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((self.tmp / "d/docs/dev/.lang").read_text().strip(), "en")
        self.assertIn("Initialized", r.stdout)


class TestSkillFiles(unittest.TestCase):
    def test_panel_no_native_append_of_null(self):
        # 原生 DOM append(null) 会渲染出文字 "null"；曾在面板里出现过
        html = (ROOT / "assets" / "review_panel.html").read_text(encoding="utf-8")
        for m in re.finditer(r"\b(?:vb|sb|qb|rb|box|app)\.append\([^;]*\?[^;]*:null", html):
            line = html[:m.start()].count("\n") + 1
            seg = m.group(0)
            # el(...) 助手会忽略 null，但直接放在原生 append 的参数里不行
            depth_ok = seg.count("el(") > 0 and seg.rfind(":null") < seg.rfind("el(") + len(seg)
            self.assertTrue(depth_ok, f"review_panel.html 第 {line} 行：原生 append 可能收到 null")

    def test_licence_and_readmes(self):
        self.assertTrue((ROOT / "LICENSE").exists())
        self.assertTrue((ROOT / "README.md").exists())
        self.assertTrue((ROOT / "README.zh-CN.md").exists())
        for f in ROOT.rglob("*.md"):
            self.assertNotIn("高铁调度员", f.read_text(encoding="utf-8"), str(f))

    def test_frontmatter(self):
        t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        fm = re.match(r"---\n(.*?)\n---\n", t, flags=re.S).group(1)
        self.assertRegex(fm, r"(?m)^name: vibecodingflow$")
        desc = re.search(r"(?m)^description: (.+)$", fm).group(1)
        self.assertLessEqual(len(desc), 1024)
        self.assertLess(len(t.splitlines()), 500)

    def test_referenced_files_exist(self):
        t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for rel in set(re.findall(r"`((?:references|assets|scripts)/[\w./-]+)`", t)):
            if "*" in rel or rel.endswith("/"):
                continue
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_panel_template_has_placeholder(self):
        self.assertIn("/*__DATA__*/null", (ROOT / "assets/review_panel.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
