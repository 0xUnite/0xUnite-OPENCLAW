# Skills 清单

## 非内置技能同步清单

- 数据来源：本机 `openclaw skills list --json`
- 同步时间：2026-03-11 11:31:49 KST
- 同步范围：排除 `openclaw-bundled` 后共 **51** 个技能

## 按来源分组

### 个人仓技能 (`agents-skills-personal`) - 1

| Skill | 可用 | 简述 |
|---|---|---|
| `agent-reach` | ✅ | Give your AI agent eyes to see the entire internet. Install and configure upstream tools for Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, ... |

### 项目仓技能 (`agents-skills-project`) - 18

| Skill | 可用 | 简述 |
|---|---|---|
| `bnbchain-mcp` | ✅ | BNB Chain MCP server connection and tool usage. Covers npx @bnb-chain/mcp@latest, PRIVATE_KEY and RPC, and every MCP tool — blocks, transactions, contracts, ERC... |
| `crypto-market-rank` | ✅ | Crypto market rankings and leaderboards. Query trending tokens, top searched tokens, Binance Alpha tokens, tokenized stocks, social hype sentiment ranks, smart ... |
| `meme-rush` | ✅ | Meme token fast-trading assistant with two core capabilities: 1. Meme Rush - Real-time meme token lists from launchpads (Pump.fun, Four.meme, etc.) across new, ... |
| `okx-cex-bot` | ✅ | This skill should be used when the user asks to 'start a grid bot', 'create a grid bot', 'stop the grid bot', 'show my grid bots', 'grid bot status', 'grid bot ... |
| `okx-cex-market` | ✅ | This skill should be used when the user asks for 'price of BTC', 'ETH ticker', 'show me the orderbook', 'market depth', 'BTC candles', 'OHLCV chart data', 'fund... |
| `okx-cex-portfolio` | ✅ | This skill should be used when the user asks about 'account balance', 'how much USDT do I have', 'my funding account', 'show my positions', 'open positions', 'p... |
| `okx-cex-trade` | ✅ | This skill should be used when the user asks to 'buy BTC', 'sell ETH', 'place a limit order', 'place a market order', 'cancel my order', 'amend my order', 'long... |
| `okx-dex-market` | ✅ | Use this skill when users want live on-chain market data: token prices, price charts (K-line, OHLC), trade history, swap activity. Also, it covers on-chain sign... |
| `okx-dex-swap` | ✅ | This skill should be used when the user asks to 'swap tokens', 'trade OKB for USDC', 'buy tokens', 'sell tokens', 'exchange crypto', 'convert tokens', 'swap SOL... |
| `okx-dex-token` | ✅ | This skill should be used when the user asks to 'find a token', 'search for a token', 'look up PEPE', 'what\'s trending', 'top tokens', 'trending tokens on Sola... |
| `okx-onchain-gateway` | ✅ | This skill should be used when the user asks to 'broadcast transaction', 'send tx', 'estimate gas', 'simulate transaction', 'check tx status', 'track my transac... |
| `okx-wallet-portfolio` | ✅ | This skill should be used when the user asks to 'check my wallet balance', 'show my token holdings', 'how much OKB do I have', 'what tokens do I have', 'check m... |
| `query-address-info` | ✅ | Query any on-chain wallet address token balances and positions. Retrieves all token holdings for a specified wallet address on a given chain, including token na... |
| `query-token-audit` | ✅ | Query token security audit to detect scams, honeypots, and malicious contracts before trading. Returns comprehensive security analysis including contract risks,... |
| `query-token-info` | ✅ | Query token details by keyword, contract address, or chain. Search tokens, get metadata and social links, retrieve real-time market data (price, price trend, vo... |
| `spot` | ✅ | Binance Spot request using the Binance API. Authentication requires API key and secret key. Supports testnet and mainnet. |
| `square-post` | ✅ | Post content to Binance Square (Binance social platform for sharing trading insights). Auto-run on messages like 'post to square', 'square post'. Supports pure ... |
| `trading-signal` | ✅ | Subscribe and retrieve on-chain Smart Money signals. Monitor trading activities of smart money addresses, including buy/sell signals, trigger price, current pri... |

### 托管技能 (`openclaw-managed`) - 11

| Skill | 可用 | 简述 |
|---|---|---|
| `Agent Browser` | ✅ | A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured comma... |
| `actionbook` | ✅ | Activate when the user needs to interact with any website — browser automation, web scraping, screenshots, form filling, UI testing, monitoring, or building AI ... |
| `browser-use` | ✅ | Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web ... |
| `fortytwo` | ✅ | Fortytwo AI Swarm Network - Decentralized AI inference where multiple agents collaborate on queries. Earn Energy by answering, spend it by asking. Auto-particip... |
| `google-calendar` | ✅ | Manage Google Calendar events, create meetings, check availability, and sync schedules. Use when agents need to create calendar events, check free/busy times, m... |
| `moltbook` | ✅ | The social network for AI agents. Post, comment, upvote, and create communities. |
| `x-collect` | ✅ | Collect and research materials for X (Twitter) content creation using multi-round web search strategy. Use when user wants to gather trending topics, research s... |
| `x-create` | ✅ | Create viral X (Twitter) posts including short tweets, threads, and replies. Use when user wants to write X content, create posts, or mentions "create tweet", "... |
| `x-filter` | ✅ | Score and filter topics for X content creation using weighted criteria. Use when user wants to evaluate collected materials, filter topics by score, or mentions... |
| `x-publish` | ✅ | Publish tweets and threads to X (Twitter) draft using browser automation. Use when user wants to publish content to X, save to drafts, or mentions "publish to X... |
| `x-tweet-fetcher` | ✅ | Fetch tweets, replies, and user timelines from X/Twitter without login or API keys. Also supports Chinese platforms (Weibo, Bilibili, CSDN, WeChat). Includes ca... |

### 工作区技能 (`openclaw-workspace`) - 21

| Skill | 可用 | 简述 |
|---|---|---|
| `bird` | ✅ | X/Twitter CLI for reading, searching, and posting via cookies or Sweetistics. |
| `find-skills` | ✅ | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express int... |
| `github-trending-cn` | ✅ | GitHub 趋势监控 \\| GitHub Trending Monitor. 获取 GitHub 热门项目、编程语言趋势、开源动态 \\| Get GitHub trending repos, language trends, open source updates. 触发词：GitHub、trending、开源、热门项目... |
| `jina-cli` | ✅ | Reads web content and searches the web using Jina AI Reader API. Use when extracting content from URLs, reading social media posts (X/Twitter), or web searching... |
| `keyword-model-router` | ✅ | Hard keyword routing for model/tool selection. Trigger when message includes whole-word WIN or GO. WIN routes to GPT-5.4 subagent; GO routes to Gemini CLI. |
| `mm-music-maker` | ✅ | Create music with MiniMax music models (e.g., music-2.5). Use when generating songs or instrumental tracks from lyrics and style prompts, or when integrating Mi... |
| `mm-voice-maker` | ✅ | Enables voice synthesis, voice cloning, voice design, and audio post-processing using MiniMax Voice API and FFmpeg. Use when converting text to speech, creating... |
| `okx-mcp-skill` | ✅ | Use OKX OnchainOS MCP through UXC for token discovery, market data, wallet balance, and swap execution planning. Use when tasks need OKX MCP tools such as token... |
| `opennews` | ❌ | Crypto news search, AI ratings, trading signals, and real-time updates via the OpenNews 6551 API. Supports keyword search, coin filtering, source filtering, AI ... |
| `proactive-agent` | ✅ | Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. Includes memory architecture with pre-compaction... |
| `simmer` | ✅ | The best prediction market interface for AI agents. Trade on Polymarket with self-custody wallets, safety rails, and smart context. |
| `skill-auto-iteration` | ✅ | Automatically learn from errors and improve OpenClaw Skills through iteration. |
| `tavily` | ✅ | AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents. |
| `total-recall` | ✅ | The only memory skill that watches on its own. No database. No vectors. No manual saves. Just an LLM observer that compresses your conversations into prioritise... |
| `xhs-auth` | ✅ | 小红书认证管理技能。检查登录状态、登录（二维码或手机号）、多账号管理。 当用户要求登录小红书、检查登录状态、切换账号时触发。  |
| `xhs-content-ops` | ✅ | 小红书复合内容运营技能。组合搜索、详情、发布、互动等能力完成运营工作流。 当用户要求竞品分析、热点追踪、内容创作、互动管理等复合任务时触发。  |
| `xhs-explore` | ✅ | 小红书内容发现与分析技能。搜索笔记、浏览首页、查看详情、获取用户资料。 当用户要求搜索小红书、查看笔记详情、浏览首页、查看用户主页时触发。  |
| `xhs-interact` | ✅ | 小红书社交互动技能。发表评论、回复评论、点赞、收藏。 当用户要求评论、回复、点赞或收藏小红书帖子时触发。  |
| `xhs-publish` | ✅ | 小红书内容发布技能。支持图文发布、视频发布、长文发布、定时发布、标签、可见性设置。 当用户要求发布内容到小红书、上传图文、上传视频、发长文时触发。  |
| `xiaohongshu-skills` | ✅ | 小红书自动化技能集合。支持认证登录、内容发布、搜索发现、社交互动、复合运营。 当用户要求操作小红书（发布、搜索、评论、登录、分析、点赞、收藏）时触发。  |
| `youtube-full` | ❌ | Complete YouTube toolkit — transcripts, search, channels, playlists, and metadata all in one skill. Use when you need comprehensive YouTube access, want to sear... |

## 备注

- `onchainos-skills` 是记忆库里的聚合称呼；本机实际已拆分为多个 `okx-*` 技能。
- 如需再次同步，请重新执行导出并覆盖本文件。
