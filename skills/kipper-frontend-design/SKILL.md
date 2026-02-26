---
name: kipper-frontend-design
description: 创建独特、生产级别的前端界面，具有高设计质量。当用户要求构建 Web 组件、页面、artifacts、海报或应用程序时使用此技能（例如网站、落地页、仪表盘、React 组件、HTML/CSS 布局，或美化任何 Web UI）。生成富有创意、精致的代码和 UI 设计，避免千篇一律的 AI 美学风格。
license: 完整条款见 LICENSE.txt
---

此技能指导创建独特、生产级别的前端界面，避免千篇一律的"AI 流水线"美学风格。实现真正可运行的代码，对美学细节和创意选择给予极高关注。

用户提供前端需求：需要构建的组件、页面、应用程序或界面。他们可能会包含关于用途、目标受众或技术约束的背景信息。

## 设计思维

在编码之前，理解背景并确定一个**大胆**的美学方向：
- **目的**：这个界面解决什么问题？谁在使用它？
- **基调**：选择一个极端风格：极简主义、极繁主义混沌、复古未来主义、有机/自然、奢华/精致、趣味/玩具感、编辑/杂志风、粗野主义/原始、装饰艺术/几何、柔和/粉彩、工业/实用主义等。有太多风格可供选择。以这些为灵感，但设计出真正符合美学方向的作品。
- **约束**：技术要求（框架、性能、无障碍性）。
- **差异化**：是什么让这个设计**令人难忘**？用户会记住的那一点是什么？

**关键**：选择一个清晰的概念方向并精准执行。大胆的极繁主义和精致的极简主义都可以——关键在于设计的意图性，而非强度。

然后实现可运行的代码（HTML/CSS/JS、React、Vue 等），需要：
- 生产级别且功能完善
- 视觉上引人注目且令人难忘
- 具有清晰美学观点的整体协调性
- 每个细节都经过精心打磨

## 前端美学指南

重点关注：
- **字体排印**：选择美观、独特、有趣的字体。避免使用 Arial 和 Inter 等通用字体；选择能提升前端美感的独特字体；出人意料的、有个性的字体选择。将独特的展示字体与精致的正文字体搭配使用。
- **色彩与主题**：坚持一致的美学风格。使用 CSS 变量保持一致性。主色调配合鲜明的强调色，比畏首畏尾、均匀分布的调色板效果更好。
- **动效**：使用动画实现效果和微交互。HTML 优先使用纯 CSS 解决方案。React 可用时使用 Motion 库。专注于高影响力的时刻：一个精心编排的页面加载配合错落的显示效果（animation-delay）比零散的微交互更令人愉悦。使用能带来惊喜的滚动触发和悬停状态。
- **空间构图**：出人意料的布局。不对称。重叠。对角线流动。打破网格的元素。大量留白或有控制的密集布局。
- **背景与视觉细节**：营造氛围和深度，而不是默认使用纯色。添加与整体美学相匹配的情境效果和纹理。应用创意形式，如渐变网格、噪点纹理、几何图案、分层透明度、戏剧性阴影、装饰性边框、自定义光标和颗粒叠加。

**绝不**使用千篇一律的 AI 生成美学风格，如过度使用的字体系列（Inter、Roboto、Arial、系统字体）、老套的配色方案（特别是白色背景上的紫色渐变）、可预测的布局和组件模式，以及缺乏情境特色的模板化设计。

创造性地解读需求，做出出人意料的选择，让设计感觉是为特定情境量身定制的。没有任何设计应该是相同的。在浅色和深色主题、不同字体、不同美学风格之间变换。**绝不**在多次生成中趋同于常见选择（例如 Space Grotesk）。

**重要**：使实现复杂度与美学愿景相匹配。极繁主义设计需要精心编写的代码，包含大量动画和效果。极简主义或精致的设计需要克制、精确，以及对间距、字体排印和微妙细节的仔细关注。优雅来自于对愿景的出色执行。

记住：Claude 有能力完成非凡的创意工作。不要有所保留，展示跳出框架思考并全身心投入独特愿景时能真正创造出的作品。

## 图片生成能力

当设计需要自定义图片素材时（如背景图、插图、图标、概念图等），可以使用 Gemini 图片生成工具。

### 调用方式

使用 `tools/generate_image.py` 脚本生成图片：

```bash
# 生成图片并保存到文件
python ~/.agents/skills/frontend-design/tools/generate_image.py \
  -p "A futuristic city skyline at sunset, cyberpunk style" \
  -o hero.png

# 生成正方形图片（适合图标）
python ~/.agents/skills/frontend-design/tools/generate_image.py \
  -p "Minimalist rocket icon, flat design" \
  -r 1:1 \
  -o icon.png

# 生成 4K 高清背景
python ~/.agents/skills/frontend-design/tools/generate_image.py \
  -p "Abstract gradient background in soft purple and blue" \
  --resolution 4K \
  -o background.png

# 输出 base64（用于内嵌 HTML）
python ~/.agents/skills/frontend-design/tools/generate_image.py \
  -p "Small decorative pattern" \
  -r 1:1
```

### 参数说明

- **-p, --prompt**: 图片描述（必需），建议用英文以获得更好效果
- **-r, --ratio**: 宽高比，支持 1:1、2:3、3:2、3:4、4:3、4:5、5:4、9:16、16:9、21:9（默认 16:9）
- **--resolution**: 分辨率，支持 1K、2K、4K（默认 2K）
- **-o, --output**: 输出文件路径，如不指定则输出 base64

### 环境要求

需要设置 `QINIU_API_KEY` 环境变量。

### 输出处理

- 指定 `-o` 参数时，图片直接保存为 PNG 文件
- 不指定 `-o` 时，输出 base64 字符串，可在 HTML 中使用：`<img src="data:image/png;base64,{output}">`

### 使用场景

- **Hero 背景**: 生成大气的首屏背景图
- **插图**: 为内容区域生成配套插图
- **图标**: 生成独特的图标素材
- **纹理**: 生成背景纹理或装饰元素
- **概念图**: 为产品展示生成概念图

### Prompt 编写技巧

为获得高质量的 UI 素材，prompt 应包含：
1. **主题描述**: 核心内容是什么
2. **风格定义**: 极简、扁平、3D、写实、抽象等
3. **色彩要求**: 主色调、是否需要透明背景
4. **用途说明**: 用于网页背景、图标、插图等
5. **技术规格**: 如"无文字"、"纯色背景便于抠图"

示例 prompt：
- `A minimal abstract gradient background in soft purple and blue tones, suitable for a tech startup landing page, no text, 4K resolution`
- `Flat design icon of a rocket launching, vibrant orange and white colors, clean vector style, transparent background`
