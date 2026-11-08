# 游戏层：额外要点

游戏的"最后 10%"几乎全是手感和乐趣，最难用语言描述，也最贵返工。所以游戏项目在通用流程上再加这些约束。用 `init.py --game` 会带上对应模板（GDD 版设计文档、`contracts/game_rules.md`、素材台账）。

## 1. 引擎选择影响 AI 能做多少

AI 擅长读写文本。引擎的场景、资源如果是人类可读的文本，AI 能完整改动；如果是二进制资源或只能在编辑器里点出来，AI 就够不着，验收时也难以让它自己复现。

- 顺手：Godot（`.gd` / `.tscn` 是文本）、Three.js、Phaser、PixiJS、Pygame、LÖVE、Bevy。
- 吃力：Unity、Unreal 的场景、预制体、蓝图这类二进制或编辑器内操作。能用但要把逻辑尽量留在 C# / C++ 代码里。

立项时在 DESIGN 第 0 节问 2 回答的就是这个。

## 2. 灰盒先行

第一个里程碑只做方块 + 文字，通过"手感"和"想继续"两个维度的验收，才上美术、音效、特效。这三样一旦做了，推翻玩法的代价翻几倍。

## 3. 手感参数

把会被人说"太飘 / 太快 / 太慢 / 太软"的数值全部放进配置，带单位和范围：

移动速度、加速度、摩擦、重力、跳跃初速度、土狼时间、跳跃缓冲、冲刺距离、攻击前摇与后摇、命中停顿、镜头震动、受击无敌时间、动画时长、缓动曲线。

F9 调参面板做成滑块，"复制当前参数"输出配置片段。人调好贴回，AI 写入配置。

## 4. 确定性与可复现

- 所有随机用带种子的随机数，同种子同结果。
- 逻辑用固定时间步长或 delta，不依赖帧率。
- 界面角落显示版本和种子。
- 这三条合在一起，人说"第三关那个怪卡住了"，AI 凭种子和调试信息就能复现。

## 5. 最小实现

### Web（Three.js / Phaser / Canvas）

```js
// F8：复制调试信息
const events = [];                       // 在关键事件处 events.push(`${t} ${msg}`)，保留最近 20 条
window.addEventListener('error', e => events.push('ERR ' + e.message));
window.addEventListener('keydown', e => {
  if (e.key !== 'F8') return;
  e.preventDefault();
  const report = JSON.stringify({
    version: VERSION, milestone: 'M1', seed: game.seed,
    scene: game.scene, state: game.debugState(), events: events.slice(-20),
  }, null, 2);
  navigator.clipboard.writeText(report);
});
// F9：切换调参面板；URL 参数 ?scene=boss&seed=123 直达场景
const q = new URLSearchParams(location.search);
```

### Godot 4

```gdscript
func _unhandled_input(event):
    if event is InputEventKey and event.pressed and event.keycode == KEY_F8:
        DisplayServer.clipboard_set(JSON.stringify(debug_report()))
```

`debug_report()` 返回版本、种子、场景、关键状态和最近事件的字典。调参面板可用一个读写 `config` 资源的简单 `Control` 场景。

## 6. 试玩方法

- 让人真玩，不是"看一眼"。路线里写明要完成的目标。
- 新鲜的眼睛比熟悉的眼睛更有价值：首次接触时的困惑最能暴露"清晰"问题。可以请第二个人只打"清晰"和"想继续"两项。
- 第一次打开到第一次"哦有意思"之间的时间，是核心循环最诚实的指标，DESIGN 里的"一分钟测试"就是在检验它。
- 里程碑进入打磨阶段前，至少有 3 次不同人 / 不同时间的试玩记录。

## 7. 存档与版本

存档带版本号；改结构要写迁移，或明确废弃旧存档并记入 DECISIONS。否则人的测试进度会悄悄丢失，之后的反馈也会因此失真。

## 8. 素材与合规

每个素材（含 AI 生成）登记来源和授权到 `ledgers/assets_ledger.md`。上架平台审核（如 Steam）会问 AI 生成内容的披露，台账让这件事不再临时翻找。
