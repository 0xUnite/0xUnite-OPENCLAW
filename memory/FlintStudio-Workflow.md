# FlintStudio AI短剧自动化工作流

## 概述
- **目标**: 小说 → 剧本 → 分镜 → 图片 → 配音 → 视频
- **当前状态**: 除视频生成外全部配置完成
- **最后一步**: 视频生成由用户在即梦/Jimeng手动完成

---

## 已完成配置

### 1. MiniMax API（文字+图片）
- **API Key**: `sk-cp-I6J-KeKQnl-M_pzNQaEgKqSJptVFg4CQ45k5QQpqRZ-MQQodsiHI61m6HkFlRhc8K2R9HnClErdMaIYIufB6Fz1JjgilxPieRGOsMaUOiHLSHRllzt0BaFE`
- **Endpoint**: `https://api.minimaxi.com`
- **用途**: LLM分析 + 图片生成(Image-01)

### 2. FlintStudio 已运行
- **地址**: http://localhost:3000
- **测试账号**: test-user

### 3. 一致性增强（已完成代码优化）
- **文件**: `~/FlintStudio/src/lib/workflow/consistency.ts`
- **功能**: 自动注入角色外貌、场景信息到prompt
- **原理**: 读取CharacterAppearance.referenceImage + LocationImage.imageUrl

---

## 完整工作流

### Step 1: 小说输入
1. 打开 http://localhost:3000
2. 新建项目 → 导入小说文本
3. FlintStudio自动分析提取：角色、场景、章节

### Step 2: 角色管理（关键！）
1. 进入项目 → 角色管理
2. **为每个角色上传参考图**
   - 上传位置: CharacterAppearance (appearanceIndex=0作为主图)
   - 参考图URL字段: `character.appearances[0].imageUrl`
3. 填写角色外貌描述 (profileData)

### Step 3: 场景管理
1. 进入项目 → 场景管理
2. **为每个场景上传参考图**
   - 上传位置: LocationImage (isSelected=true作为主图)
   - 参考图URL字段: `location.images[0].imageUrl`
3. 填写场景描述 (summary)

### Step 4: 剧本生成
1. 运行「小说→剧本」工作流
2. LLM自动分析小说生成结构化剧本
3. 自动分章节

### Step 5: 分镜生成
1. 运行「剧本→分镜」工作流
2. 自动拆分为多个镜头(panels)
3. 每个panel包含: description, imagePrompt, shotType, cameraMove等

### Step 6: 图片生成（自动）
1. Worker读取panels
2. **自动注入一致性信息到prompt**:
   - 角色外貌描述
   - 场景灯光氛围
   - "consistent appearance"标记
3. 调用MiniMax Image-01生成
4. 保存到NovelPromotionPanel.imageUrl

### Step 7: 配音生成（自动）
- 使用EdgeTTS（免费）
- 自动提取对白生成配音

### Step 8: 视频生成（手动）
**由用户在即梦/Jimeng操作:**

#### 流程:
1. **先在即梦生成角色参考图**
   - Prompt示例（李逍遥）:
     ```
     武侠风格，年轻人，18岁，黑色长发束发髻，穿蓝色汉服，腰佩长剑，表情坚毅，电影感画质
     ```
   - Prompt示例（赵灵儿）:
     ```
     古风美女，16岁，长黑发，白色飘逸长裙，神态恬静脱俗，电影感画质
     ```

2. **用角色图在即梦生成视频**
   - 模式: 「图生视频」
   - 上传角色参考图
   - 输入动作prompt:
     ```
     侠客风范的年轻人持剑站立，缓缓拔出长剑，剑光闪烁
     ```

3. **用场景图生成环境视频**
   - 酒楼场景:
     ```
     传统中国酒楼内部，暖色灯笼光，木质桌椅，古风装饰，氛围温馨
     ```

---

## 一致性增强代码（已部署）

### 文件: ~/FlintStudio/src/lib/workflow/consistency.ts

```typescript
// 核心函数
export async function getConsistencyContext(projectId: string): Promise<ConsistencyContext>

export function enhanceFullPrompt(
  basePrompt: string,
  characterNames: string[],
  locationName: string | undefined,
  context: ConsistencyContext,
  options?: { includeReferenceImage?: boolean; styleSuffix?: string }
): string
```

### Worker调用: ~/FlintStudio/src/lib/workers/index.ts
- 加载一致性上下文
- 获取clip的角色名和场景名
- 注入到每个panel的prompt

---

## 测试项目信息

- **项目ID**: aed5ddf0-b3dd-4c14-89f3-673ffee33e09
- **NovelPromotionID**: 5d0d09ca-1d3e-420f-bbf8-1ebfa20fad1a
- **测试账号**: test-user
- **角色**: 李逍遥, 赵灵儿
- **场景**: 酒楼, 苏州城外

---

## MiniMax API 端点

| 功能 | 端点 | 模型 |
|-----|------|------|
| 文字 | /v1/chat/completions | MiniMax-M2.7 |
| 图片 | /v1/image_generation | image-01 |
| 视频 | ❌ 需单独开通 | Hailuo-2.3 |

---

## 成本估算（批量生产1集）

| 环节 | 单价 | 预估用量 | 成本 |
|-----|------|---------|------|
| LLM分析 | ¥2.1/百万token | ~10万token | ¥0.21 |
| 图片生成 | ~¥0.01/张 | ~50张 | ¥0.5 |
| 配音 | 免费(EdgeTTS) | - | ¥0 |
| **合计** | | | **¥0.71/集** |

视频生成（未来）:
- 即梦: ¥0.6-1/秒
- Seedance: ¥1/秒

---

## 待解决问题

1. **MiniMax视频API**: 已有端点但模型参数不正确，需确认权限
2. **即梦视频**: 需手动在网页操作
3. **可灵AI**: 可作为免费视频生成备选（需注册）

---

## 参考资料

- Jellyfish开源项目: https://github.com/Forget-C/Jellyfish
- Toonflow开源项目: https://github.com/HBAI-Ltd/Toonflow-app
- FlintStudio: ~/FlintStudio/
- MiniMax文档: platform.minimaxi.com
