# 简历写作方法论（STAR / PAR / XYZ + 中英差异）

调研日期 2026-07-04，出处见文末。

## 1. 三个公式，用途各异

- **Google XYZ**（写简历 bullet 用）：出自 Google 前人力 SVP Laszlo Bock《Work Rules!》：
  "Accomplished **X** as measured by **Y**, by doing **Z**"。X=成果，Y=可度量影响（%/金额/规模/排名），Z=方法。
  一条 bullet 只讲一个成就，把「职责描述」改写成「有证据的成就陈述」。
- **PAR**（MIT CAPD 的 bullet 构造法）：Project → Action → Result，动作动词开头+任务+结果，能量化就量化。
- **STAR**（面试回答用，不是写简历用）：Situation/Task/Action/Result，时间分配 S 20% / T 10% / **A 60%** / R 10%。
  写简历时压缩为 A+R；面试深挖卡按完整 STAR 准备。

## 2. Harvard / MIT 硬规则

- 动作动词开头，拒绝被动语态；禁第一人称（I/we）；不写完整句
- **过去职位用过去时，当前职位用现在时**（时态闸）
- 事实为基础，能量化就量化；「没量化的 bullet = 无凭据的主张」
- 倒序时间；格式一致；转 PDF 后检查排版
- 页数：一页或两页，**禁 1.25 页**（要么填满要么砍）
- 英文版禁照片/年龄/婚育状况（反歧视文化）；不附推荐人列表

## 3. 中英文简历差异（不是互译关系）

| 维度 | 中文简历（投内资） | 英文简历 |
|------|------------------|---------|
| 照片 | 传统上常带（本 skill 默认不带，AI 公司无此要求） | 绝对不带 |
| 个人信息 | 手机号必写（招聘方电话联系习惯） | 姓名+邮箱即可 |
| 篇幅 | 可到两页，经历写更细 | 一页为主，资深两页 |
| 风格 | 常有「自我评价」段 | Summary 两三行，成就导向点到为止 |
| 撰写 | 各自独立撰写 | **禁机器直译**，逐条重写 |

## 4. bullet 改写自查（每条过一遍）

1. 动词开头了吗？「参与/协助/负责支持」→ 换成「我发现/我搭建/我提出」级别的主动词
2. 有 Y 吗（数字+口径）？没有就找替代量化（规模/频率/对比/排名）
3. 有 Z 吗（具体方法/工具名）？纯抽象动宾结构打回
4. 这条为主线叙事服务吗？不服务就砍，再漂亮也砍
5. 面试官追问三层还立得住吗？立不住的数字降级或删除

## 5. 可借鉴的高星项目机制（2026-07-04 GitHub 实查星数）

- **Resume-Matcher（27.6k⭐）**：简历↔JD 匹配打分+关键词 gap 分析，投前必跑 → 本 skill checks.py 的 jd-coverage 闸
- **open-resume（8.7k⭐）**：构建器+解析器二合一，把产出 PDF 重新 parse 核对零丢失 → 解析回测思路
- **Reactive-Resume（39.3k⭐）**：数据与呈现分离，结构化内容+多模板渲染 → 本 skill 的 md 源文件+render 分离
- **AIHawk（30k⭐）**：每个 JD 一份定制简历的流水线 → 取其定制，弃其自动海投（封号+AI 味风险）
- **tech-interview-handbook（140k⭐）**：resume 章节可作英文简历 rubric
- **coding-interview-university（355k⭐）**：checklist 式求职作战计划 → tracker.md 的设计

出处：inc.com Laszlo Bock XYZ · capd.mit.edu PAR/动词表/时态 · careerservices.fas.harvard.edu · wondercv/知乎 中英差异 · GitHub API 星数实查
