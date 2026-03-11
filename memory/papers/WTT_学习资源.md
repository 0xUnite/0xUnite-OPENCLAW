# WTT 自然交易理论 - 完整学习资源与笔记

## 官网
- 微信读书: https://weread.qq.com/web/appreader/45432fd071f38607454aef6kecc32f3013eccbc87e4b62e
- Tradingview: https://www.tradingview.com/u/W-TT/

---

## 核心理论摘要（已整理）

### 核心三要素
| 要素 | 说明 |
|------|------|
| **空间** | 斐波那契回撤决定空间，即开平仓点位 |
| **时间** | 斐波那契时间决定时间，即交易时间点 |
| **能量** | 交易量的波动决定趋势，即多空方向 |

### 心术（70%权重）
> 天下交易，三分技术，七分心态

- 冷静分析 + 正确开单 = 盈利
- 平仓获利离场才是终点
- 心态决定能否守住利润

### 学习阶段
| 阶段 | 正确率 | 目标 |
|------|--------|------|
| S1 | 60%+ | 仓位管理、心态基础、三要素 |
| S2 | 70%+ | 指标组合、综合判断 |
| S3 | 80%+ | 基本面分析、高阶心态 |

### 摒弃传统指标
- ❌ MA（均线）
- ❌ MACD
- ❌ KDJ
- ❌ BOLL
- ❌ RSI

### 正确率
- 普通人：约17%
- 学完S1：60%+

---

## 教学视频列表

### 1. 基础常识
- 什么是比特币期货合约: https://youtu.be/A6BM39I62VU
- 比特币价格波动和涨跌幅的关系: https://youtu.be/txuyFV4VBgo
- 季度合约和永续合约的差别: https://youtu.be/ewAW7Qb0V_E
- NFT是什么: https://youtu.be/ipdgqsAV4ak
- 什么是"市值": https://youtu.be/lKoGyBkvUFc
- 美元加息影响: https://youtu.be/9BvJ3MgqJ1w
- 去中心化与Uniswap: https://youtu.be/EJ-9hZAyMPs

### 2. 庄家与散户
- 操盘手如何操盘: https://youtu.be/4IBsSxVp-LY
- 大宗期货操盘手分享: https://youtu.be/7N7TQNtbjKI | https://youtu.be/C_slOXFBgYc
- 庄家思维vs散户思维: https://youtu.be/I_U4xJLGmZo

### 3. 山寨币
- 山寨币如何兴风作浪: https://youtu.be/nikTvQn14Go
- 如何挑选山寨币现货: https://youtu.be/7pLLpsWxrKc

### 4. Fib通道绘制
- 上升通道: https://youtu.be/X77JoMVcUOU | https://youtu.be/3nyEZFZtyS4
- 下降通道: https://youtu.be/4i7BXZjFeRc | https://youtu.be/_ZMuaVAjQMI

### 5. 网格量化/套利
- 派网网格量化: https://youtu.be/40_hN3gwN_A
- 套期保现: https://youtu.be/-KYxKrtvMa0k
- 套利: https://youtu.be/UQRQg89x0D0

### 6. Bybit交易所
- 合约教学: https://youtu.be/M3czZDyLFFA
- 仓位杠杆止盈止损: https://youtu.be/mEMd7gNLVK4
- 防守止盈止损: https://youtu.be/13IIfTmLzkw

---

## 学习计划

- [ ] 看完基础常识系列
- [ ] 学习庄家思维
- [ ] 掌握Fib通道绘制
- [ ] 实践网格量化
- [ ] 结合模拟盘测试WTT策略

---

## 自然交易理论课程-基础篇

> 来源: 用户分享的WTT系列课程视频
> ⚠️ 状态: 视频在韩国地区受限无法直接播放

### K线与量能
1. 《关于自然交易理论课程-基础篇》炒二级必学(K线) ● 炒合约必学(量能) 心术与仓位管理: https://youtu.be/XvyEcySBCXO

### 斐波那契回撤与趋势
2. 自然交易基础 (斐波那契回撤)以及通道的区别: https://youtu.be/qzvWBmTWO4U
3. 斐波那契趋势时间: https://youtu.be/Os4RnuG1fso

### 斐波那契数列
4. 自然交易理论基础!斐波那契数列黄金分割线: https://youtu.be/UVfiuTzrkyg
5. 斐波那契回撤实战: https://youtu.be/3eiOcQKStYk
6. 斐波那契时间周期: https://youtu.be/X-HMDPdJW4g
7. 斐波那契实战应用: https://youtu.be/konAlrmOak8

### Fib通道绘制
8. Fib通道绘制教程!自然交易理论!: https://youtu.be/WWTsl-dblcE

---

## 技术工具学习

### X.com 内容获取 (2026-02-16)
**问题**: X.com 检测严格，普通 playwright/browser 无法访问
**解决方案**: 使用 `rebrowser-playwright` - 有真 GPU 指纹，可绕过检测

**安装**:
```bash
npm install rebrowser-playwright
```

**脚本**: `~/.openclaw/workspace/scripts/x-fetch.js`
```bash
node x-fetch.js <tweet-url>
```

**替代方案**:
- transcriptapi.com - 获取 YouTube 字幕（需要账号注册）
- nitter.net / vxtwitter.com - X.com 备用前端（不稳定）

### YouTube 字幕获取
- **transcriptapi.com**: 100 免费积分，可获取 YouTube 字幕
- 注册: `node ./scripts/tapi-auth.js register --email <邮箱>`
- 验证: `node ./scripts/tapi-auth.js verify --token <token> --otp <验证码>`
- API Key 保存到 `~/.openclaw/openclaw.json`
