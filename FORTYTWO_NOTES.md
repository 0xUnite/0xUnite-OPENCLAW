# Fortytwo Network 学习笔记

> 记录日期：2026-02-09
> 官方文档：https://docs.fortytwo.network/

---

## 1. 节点类型

### 三种运行方式

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **Fortytwo App** | 桌面应用程序，界面友好 | Mac 用户首选 |
| **Fortytwo CLI** | 命令行工具 | 服务器/无头环境 |
| **Fortytwo Container** | Docker 容器 | 多GPU/专业部署 |

---

## 2. 硬件要求

### PC (Windows / Linux)
- **系统**: Windows 10+ (64-bit) / Ubuntu 20.04+ / Debian 10+
- **CPU**: 8核处理器 (i7/Ryzen 7 或更高)
- **内存**: 16GB 最低
- **GPU**: Nvidia RTX 3060 或更高（必须NVIDIA GPU）
- **存储**: 20GB+ 可用空间（NVMe SSD 推荐）
- **网络**: 稳定网络，最低 10 Mbps 上传/下载

### macOS
- **系统**: macOS 13 (Ventura) 或更新
- **芯片**: Apple Silicon (M1 或更新)
- **内存**: 16GB 最低（32GB 推荐）
- **存储**: 20GB+ 可用空间

### Linux GPU 驱动安装
```bash
sudo apt update
sudo apt install nvidia-driver-535  # 替换为适合你GPU的版本
reboot
```

---

## 3. 快速启动 (Fortytwo CLI)

### macOS
```bash
cd ~/FortytwoCLI/fortytwo-console-app-main
bash macos.sh
```

### 启动后
- 节点会保持运行直到用户停止或系统重启
- 可以最小化终端窗口
- 自动检查更新

### 停止节点
```bash
# 按 Ctrl+C 终止
```

---

## 4. 常见问题与解决方案

### 网络连接问题

**症状**:
- 无法连接到 Fortytwo 网络
- 因响应超时导致推理轮次失败
- 大型复杂问题时胜率下降
- 模型下载/更新错误

**解决方案**:
1. **VPN 测试**: 某些地区可能需要VPN
2. **关闭VPN**: 如果已用VPN但有问题，尝试关闭
3. **报告问题**: Discord #tech-support 频道

### 节点无收益

**可能原因**:
1. 连接问题
2. 网络请求量低
3. 模型太大导致响应慢
4. 模型回答质量不高

**排查步骤**:
1. 重启节点
2. 尝试切换不同模型
3. 等待24小时以上无收益 → 联系 Discord support

### 模型加载失败

**可能原因**:
- 系统资源不足
- 模型超出内存

**解决方案**:
1. 关闭其他资源密集型应用（3D编辑、视频编辑、游戏）
2. 选择比可用内存小约 2GB 的模型

### 余额问题

**MON 余额为零**:
- 有激活码：24小时内自动充值
- 超过24小时：Discord 消息支持

**获取 MON**:
- 官方水龙头: https://faucet.monad.xyz/
- 条件：主网钱包至少 10 MON
- 每6小时可Claim一次

---

## 5. 关键概念

### 推理轮次工作流程
1. 安装应用并启动 → 加入网络
2. 网络出现请求时参与响应生成
3. 每轮消耗 1 FOR 参与
4. 获胜获得 +X FOR 奖励

### 注意事项
- ❌ 同一钱包只能运行一个节点
- ❌ CLI 和 App 不能同时运行（算两个节点）
- ✅ Container 可多节点（需多GPU）
- ✅ 推理节点需要 GPU，CPU 不支持

---

## 6. 重要文件位置

| 类型 | macOS 位置 |
|------|-----------|
| **CLI** | `~/FortytwoCLI/fortytwo-console-app-main/` |
| **启动脚本** | `macos.sh` |
| **监控脚本** | `monitor.sh` (需要创建) |

---

## 7. 启动命令速查

```bash
# 启动节点 (macOS)
cd ~/FortytwoCLI/fortytwo-console-app-main
bash macos.sh

# 检查状态
docker ps (如果用 Container)
```

---

## 8. 常见错误代码

（待补充 - 官方文档可能包含详细错误代码）

---

## 9. 故障排查清单

当节点出现问题时，按顺序检查：

- [ ] 网络连接是否稳定？
- [ ] GPU 驱动是否最新？
- [ ] nvidia-smi 命令是否正常？
- [ ] 内存是否充足？
- [ ] MON 和 FOR 余额是否足够？
- [ ] 日志中是否有具体错误信息？

---

## 10. 参考链接

- **官网**: https://fortytwo.network/
- **文档**: https://docs.fortytwo.network/
- **Discord**: https://discord.gg/fortytwo
- **水龙头**: https://faucet.monad.xyz/
- **Monad Testnet**: https://testnet.monad.xyz/

---

*最后更新: 2026-02-09*
