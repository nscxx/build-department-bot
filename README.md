# Build Department Bot

把已批准的 FAQ、Word、Excel、PDF、制度或流程材料，转成一个安全、可测试、可回滚的企业内部机器人配置包。

## 一键安装

在 Codex 中发送：

```text
请安装这个 Skill：https://github.com/nscxx/build-department-bot/tree/main/skills/build-department-bot
```

或在终端运行：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo nscxx/build-department-bot \
  --path skills/build-department-bot
```

安装完成后，在下一轮对话中使用：

```text
请使用 $build-department-bot，为财务部创建内部机器人。机器人叫“小财”，唯一知识来源是我上传的材料，安全优先，找不到答案就转人工。生成完整配置包并校验，暂不发布。
```

## 它会生成什么

- 项目立项与责任确认
- 规范化知识库
- 可直接复制的系统提示词
- 最小工作流蓝图
- 12 类测试矩阵
- 发布检查表
- 内测运营手册
- 验收与回滚方案

## 默认原则

1. 只使用已批准知识，不用模型常识补充业务结论。
2. 知识库、提示词和工作流三层分离。
3. 默认使用精确 FAQ；不明确时只列真实问题。
4. 找不到就转人工，不展示关键词、匹配过程或推理。
5. 从稳定版本做最小修改，每次变更都可测试、可回滚。

## 项目结构

```text
skills/build-department-bot/   可安装的 Codex Skill
docs/                          GitHub Pages 安装与介绍页面
.github/workflows/             页面自动发布工作流
```

访问项目页面：<https://nscxx.github.io/build-department-bot/>

> 本仓库只包含通用方法、模板与脚本，不包含任何部门原始知识库或个人信息。使用者仍需由本部门内容负责人批准知识和最终发布。
