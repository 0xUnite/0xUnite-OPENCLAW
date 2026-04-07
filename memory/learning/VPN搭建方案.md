# VPN搭建方案学习记录

## 方案：Cloudflare Workers 免费搭建VPN

**来源：** Twitter @ferdie_jhovie (2026-04-07)
**链接：** https://x.com/i/status/2041173024289018132

---

## 核心信息

- **原理：** 用Cloudflare Workers/Pages免费服务搭建
- **成本：** ~$5（买域名）可用3-5年
- **优势：** 不需要服务器，纯免费

---

## 所需材料

1. 一个自己的域名
2. Cloudflare账号（免费）
3. 项目压缩包（原推文有下载链接）
4. CMLiussss脚本支持

---

## 步骤概要

1. Cloudflare → Workers和Pages → 创建应用
2. 选择Pages，拖拽上传压缩包
3. 设置ADMIN变量（WebUI管理员密码）
4. 创建KV命名空间，绑定到项目（变量名必须大写KV）
5. 重新部署使变量生效

---

## 注意事项

- 项目名称必须全新，避免1101错误
- ADMIN密码建议复杂，防止暴力破解
- KV命名空间名称建议EDT2便于区分

---

## 适用场景

- 轻度翻墙使用
- 成本敏感的用户
- 不想买服务器的情况

---

## 标签

#VPN #翻墙 #Cloudflare #免费 #教程
