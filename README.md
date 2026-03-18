# Quantum-hive

OpenClaw 工作区数据仓库 - 备份与恢复指南

## 包含内容

### 工作区文件 (workspace/)
AI Agent 生成的 Python 交易机器人相关文件：
- OKX 交易所交易脚本
- Binance 交易所交易脚本
- 套利策略实现
- 账户状态监控
- 连接调试工具

### 记忆数据 (memory/)
- `main.sqlite` - OpenClaw 长期记忆数据库

### 聊天记录 (agents/)
- `agents/main/sessions/` - 对话会话记录 (.jsonl 文件)
- `agents/main/agent/` - Agent 配置 (models.json, auth-profiles.json)

### 扩展 (extensions/)
- qqbot - QQ 机器人扩展
- xiaoyi - 小艺助手扩展

### 技能 (workspace/skills/)
- agent-browser
- find-skills
- self-improving-agent
- skill-vetter
- summarize
- tavily-search
- weather

---

## 服务器重装后恢复步骤

### 1. 安装 OpenClaw
```bash
# 安装 OpenClaw (请参考官方文档)
npm install -g openclaw
# 或
pnpm add -g openclaw
```

### 2. 克隆仓库
```bash
git clone https://github.com/noahmartinsage/Quantum-hive.git ~/.openclaw
```

### 3. 配置 API 密钥
编辑 `~/.openclaw/openclaw.json`，填入你的 API 密钥：
- MINIMAX_API_KEY
- OPENCODE_API_KEY
- NVIDIA_API_KEY
- 其他 API 密钥

### 4. 恢复完成
启动 OpenClaw 后，之前的记忆和对话历史都会保留。

---

## 注意事项

⚠️ `credentials/` 目录包含敏感 API 密钥，已排除推送。请在首次安装后手动配置或从安全的地方恢复。
