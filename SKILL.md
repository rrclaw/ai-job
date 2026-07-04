---
name: ai-job
description: >
  AI 时代求职闭环 skill：从头部 AI 公司人才观出发，走「JD 解析 → 素材挖掘 → 定位叙事 →
  简历生成（中英）→ 批判审阅（多 agent 对抗 + 代码闸）→ 面试准备 → 投递复盘」七阶段闭环。
  当用户说"改简历 / 写简历 / 投递 XX 公司 / 求职 / 面试准备 / ai-job"时使用。
---

# ai-job：AI 时代求职闭环

## 顶层思想

传统简历逻辑是「证明你合格」；AI 公司筛选逻辑是「证明你有 agency」。
详见 `references/talent-philosophy.md`（头部 AI 公司人才观调研）。三条公理贯穿全流程：

1. **可验证 > 可描述。** 一个能点开的链接胜过十行形容词。作品集（公开 repo、公网站点、
   可追溯数据）是简历的一等公民，不是附录。
2. **口径即诚信。** 每个数字必须带口径（时间窗、样本、统计方式），能被面试官当场验证。
   写不出口径的数字不许上简历。
3. **人味 > 完美。** AI 初筛之后是人终审。过度打磨的通用话术（中文「赋能/深耕/助力」，
   英文 spearheaded/passionate 滥用）是减分项。规则见 `references/anti-ai-flavor.md`。

## 七阶段闭环

每个候选人一个目录：`candidates/<name>/`（**默认 gitignore，个人数据永不入公开库**）。

### ① JD 解析与岗位画像
- 收集目标岗位 JD 原文（截图 OCR / 网页 / 招聘 app 转述），存 `candidates/<name>/jd/<公司>-<岗位>.md`
- 每份 JD 提炼：硬性门槛 / 核心职责 / 隐含偏好（从「为什么加入我们」段落反推）/ 关键词表（供 checks.py 覆盖率检查）
- 多家投递时做岗位聚类：一版主简历 + 每类岗位一个微调版，不做 N 份全定制

### ② 素材挖掘（evidence）
- 产出 `candidates/<name>/evidence.md`：分类罗列全部可用素材，**每条带来源和口径**
- 素材优先级：可公开验证的作品（链接）> 有第三方口径的成绩（平台数据）> 内部可追溯的工作成果（周报/报告）> 自述
- 红线：写简历时数字只能从 evidence.md 抄，禁止凭记忆写数

### ③ 定位与叙事
- 人岗匹配矩阵：JD 要求 × 素材证据，逐条对齐，找出「唯一性交集」（别人没有、岗位需要、你有证据的东西）
- 定一条主线叙事（一句话），全简历所有 bullet 都为主线服务；与主线无关的素材砍掉，再好也砍
- 产出 `candidates/<name>/positioning.md`

### ④ 简历生成
- 用 `templates/resume_cn.md` / `resume_en.md` 骨架，写法规则见 `references/methodology.md`（STAR/XYZ、量化 bullet、中英差异）
- 格式铁律：无照片、单栏、无表格排版、≤2 页、衬线中文/无衬线英文正文、联系方式+作品集链接置顶
- 渲染：`python3 scripts/render_resume.py <resume.md> --pdf --docx`

### ⑤ 批判审阅（闭环的核心）
先跑代码闸，再跑对抗审阅，都过才算定稿：
- 代码闸：`python3 scripts/checks.py <resume.md> --jd <jd.md> --evidence <evidence.md> --links`
  （页数 / 量化密度 / AI 味词表 / JD 关键词覆盖率 / 链接可达）
- 对抗审阅：派 3 个独立 agent 分别扮演
  a. **目标公司招聘官**（按 talent-philosophy 的该公司画像挑刺）
  b. **ATS/AI 初筛器**（按 ats-and-ai-screening 规则模拟打分）
  c. **事实核查员**（逐数字对 evidence.md，任何对不上的数字直接打回）
- 审阅结论分 BLOCK / FLAG / PASS，BLOCK 必须改，FLAG 给用户拍板

### ⑥ 面试准备
- 每个头部项目一张深挖卡：背景 / 关键决策 / 取舍 / 失败与证伪 / 如果重来
- 岗位题库（从 JD 职责反推面试问题）+ 认知题（该公司创始人/高管公开观点的应对）
- 反问清单（体现 agency 的问题，不问福利）+ 90 秒自我介绍稿（中英）

### ⑦ 投递跟踪与复盘
- `candidates/<name>/tracker.md`：投递日期 / 渠道 / 版本 / 状态 / 反馈
- 每次拒信或面试反馈回填 evidence 和 positioning，迭代下一版。闭环在这里闭上。

## 目录结构

```
ai-job/
  SKILL.md
  references/
    talent-philosophy.md      # 头部 AI 公司人才观（定期刷新）
    methodology.md            # STAR/PAR/XYZ、量化 bullet、中英差异
    ats-and-ai-screening.md   # ATS/AI 筛选机制与格式规范
    anti-ai-flavor.md         # 反 AI 味文风清单
  templates/
    resume_cn.md  resume_en.md  resume.css
  scripts/
    render_resume.py          # md → PDF(headless chrome) + docx(python-docx)
    checks.py                 # 五项代码闸
  candidates/
    example/                  # 脱敏示例（虚构人物，演示七阶段产物）
    <name>/                   # 真实候选人，gitignore，永不入库
```

## 脱敏红线（公开库纪律）

- `candidates/*` 除 `example/` 外全部 gitignore；commit 前 `git status` 确认无个人文件
- references/templates/scripts 里不出现任何真实姓名、电话、邮箱、雇主、内部数据
- example 用虚构人物「林深 / Lin Shen」，数据一律标注「示例数据」
