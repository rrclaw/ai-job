# ATS 与 AI 简历筛选机制（2025-2026 现状）

调研日期 2026-07-04。

## 1. 关键认知

- **ATS 不自动拒人，人才拒人。**「石沉大海」多数是没被招聘官关键词搜索命中或解析失败，不是被机器打低分
- Greenhouse 不给简历打分，只解析+索引供搜索；Lever 招聘官先看解析后的 profile 而非原文件
- 国内北森/Moka 已转向 NLP+语义理解（厂商自称 92% 匹配准确率，当方向参考别当事实）
- 2025 年起企业在 ATS 之上叠 LLM 评估层（Eightfold/HireVue/自建 API），**LLM 像人一样通读简历对照 JD**，
  不再是关键词计数器。隐形白字、重复灌词会被主动检测标记为操纵行为
- 83% 公司计划 2025 年用 AI 筛简历（Resume Builder 对 948 名企业负责人调查）

## 2. 格式铁律（解析失败三大杀手：图片文字、表格双栏、页眉页脚）

- 单栏排版；标准节标题（工作经历/教育背景/Work Experience/Education/Skills）
- 关键信息（联系方式）放正文区，**不放页眉页脚**（多数 ATS 直接跳过）
- 无表格、无文本框、无图片承载文字；原生文字 PDF（非扫描/图片型）
- 日期格式统一；职位名用行业标准称谓
- 缩写与全称成对出现一次（如「ATS (Applicant Tracking System)」），兼顾搜索与阅读
- 超 40% 简历被拒源于格式而非内容（Jobscan 2025）

## 3. 面向 LLM 初筛的写法

- 每段经历自带完整语境：公司一句话+角色+成果，假设读者是通读全文的模型
- 从 JD 提取术语原文自然回填（写进真实成就句里），禁堆砌
- 技能写在有上下文的句子里，不只堆技能表（语义解析吃这套）

## 4. 中国 AI 公司投递渠道

- 多轨并存：官网 careers / Boss直聘 / 官方公众号 / 邮件直投
- 邮件直投标题格式（DeepSeek 官方要求）：**姓名-岗位-联系方式**
- Boss直聘开场白本身就是被 AI 读的第一份材料，按 mini 简历写（一句定位+两条硬证据+一个链接）
- 附件命名规范：姓名-岗位-简历.pdf

## 5. 落进流程的闸（checks.py 已实现的部分标注）

- [x] 单栏无表格 → 模板层保证
- [x] 链接可达 → checks.py --links
- [x] JD 关键词覆盖率 ≥70% → checks.py --jd
- [x] AI 味词表零命中 → checks.py
- [ ] 解析回测：PDF 产出后重新抽文本核对信息零丢失（人工/agent 步骤）
- [ ] 多版本简历相似度对比防模板感（agent 审阅步骤）

出处：jobscan.co Greenhouse/格式分析 · resumeoptimizerpro.com Greenhouse/Lever 指南 · support.greenhouse.io · beisen.com/mokahr.com · blog.theinterviewguys.com 83% 调查 · atsverification.com LLM 筛选 2026 · cnn.com/npr.org 专题 · lawandtheworkplace.com Workday 集体诉讼
