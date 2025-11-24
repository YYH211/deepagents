---
name: travel-planning
description: 完成旅游规划助手 - 提供全面的旅游规划服务，包括目的地推荐、行程安排、预算规划等 | Complete travel planning assistant providing comprehensive travel services including destination recommendations, itinerary planning, and budget management
---

# 旅游规划助手 (Travel Planning Assistant Skill)

这个技能提供全面的旅游规划服务，帮助用户规划完美的旅行体验。

This skill provides comprehensive travel planning services to help users plan perfect travel experiences.

## 何时使用此技能 (When to Use This Skill)

使用此技能当您需要：
- 规划旅游行程和目的地推荐
- 制定详细的旅游行程安排
- 预算规划和费用估算
- 景点和活动推荐
- 交通和住宿建议
- 获取旅游攻略和实用信息

Use this skill when you need to:
- Plan travel itineraries and get destination recommendations
- Create detailed travel schedules
- Budget planning and cost estimation
- Attraction and activity recommendations
- Transportation and accommodation suggestions
- Get travel guides and practical information

## 旅游规划流程 (Travel Planning Process)

### 第一步：收集旅行需求 (Step 1: Gather Travel Requirements)

在开始规划前，收集以下信息：

1. **目的地偏好** (Destination Preferences)
   - 国内还是国外旅行
   - 气候偏好（热带、温带、寒带）
   - 地形偏好（海滨、山区、城市、乡村）

2. **旅行时间** (Travel Time)
   - 出发日期和返回日期
   - 旅行总天数
   - 季节考虑

3. **预算范围** (Budget Range)
   - 总预算
   - 每日预算
   - 预算分配偏好（住宿、餐饮、交通、活动）

4. **旅行同伴** (Travel Companions)
   - 人数
   - 年龄段
   - 特殊需求（儿童、老人、残障人士）

5. **兴趣偏好** (Interests)
   - 文化历史、自然风光、美食体验
   - 冒险活动、休闲度假、购物娱乐
   - 摄影、徒步、潜水等特殊爱好

### 第二步：创建旅行计划 (Step 2: Create Travel Plan)

使用 `write_file` 工具创建旅行规划文件：

1. **创建旅行文件夹** - 组织所有旅行文件：
   ```
   mkdir travel_[destination]_[date]
   ```

2. **编写旅行需求文档** - 使用 `write_file` 创建 `travel_[destination]_[date]/requirements.md`：
   - 旅行目的地和日期
   - 预算和人员信息
   - 兴趣和特殊需求
   - 必去景点清单

3. **制定行程计划** - 使用 `write_file` 创建 `travel_[destination]_[date]/itinerary.md`：
   - 每日详细行程
   - 交通安排
   - 住宿预订
   - 餐饮推荐
   - 备选方案

### 第三步：使用旅游规划工具 (Step 3: Use Travel Planning Tools)

使用Python脚本进行旅游规划：

**注意：** 始终使用技能目录的绝对路径（显示在上面的系统提示中）。

如果从虚拟环境运行 deepagents：
```bash
.venv/bin/python [YOUR_SKILLS_DIR]/travel-planning/travel_planner.py [command] [options]
```

或者使用系统 Python：
```bash
python3 [YOUR_SKILLS_DIR]/travel-planning/travel_planner.py [command] [options]
```

将 `[YOUR_SKILLS_DIR]` 替换为系统提示中的绝对技能目录路径。

#### 可用命令 (Available Commands)

1. **目的地推荐** (Destination Recommendation)
```bash
python3 travel_planner.py recommend --interests "文化,美食,海滨" --budget 10000 --days 7
```

2. **行程生成** (Itinerary Generation)
```bash
python3 travel_planner.py itinerary --destination "巴黎" --days 5 --interests "文化,艺术"
```

3. **预算规划** (Budget Planning)
```bash
python3 travel_planner.py budget --destination "东京" --days 7 --travelers 2 --level "中档"
```

4. **景点推荐** (Attraction Recommendations)
```bash
python3 travel_planner.py attractions --destination "北京" --days 3 --type "historical"
```

**参数说明 (Arguments):**
- `command`: 命令类型（recommend/itinerary/budget/attractions）
- `--destination`: 目的地名称
- `--interests`: 兴趣标签，逗号分隔
- `--budget`: 总预算（人民币）
- `--days`: 旅行天数
- `--travelers`: 旅行人数（默认：1）
- `--level`: 档次（经济/中档/高档）
- `--type`: 类型（historical/natural/cultural/entertainment）

### 第四步：委托给研究子代理 (Step 4: Delegate to Research Subagents)

对于需要详细研究的部分，使用 `task` 工具委托给子代理：

1. **目的地调研** - 了解目的地详情
```
研究[目的地]的旅游信息。使用 web_search 工具收集信息。
完成后使用 write_file 保存调研结果到 travel_[destination]/research_destination.md。
包括：气候、签证、交通、住宿、景点、美食、文化习俗。
最多使用 3-5 次网络搜索。
```

2. **景点详情** - 深入了解特定景点
```
研究[目的地]的热门景点。使用 web_search 工具收集信息。
完成后保存到 travel_[destination]/attractions_detail.md。
包括：开放时间、门票价格、游览时长、交通指南、游客评价。
```

3. **美食推荐** - 搜索当地美食
```
研究[目的地]的特色美食和餐厅。
保存到 travel_[destination]/food_guide.md。
包括：特色菜品、推荐餐厅、价格范围、用餐礼仪。
```

### 第五步：综合和输出 (Step 5: Synthesize and Output)

所有子代理完成后：

1. **审查调研文件** - 查看已保存的文件：
   ```bash
   list_files travel_[destination]
   read_file travel_[destination]/research_destination.md
   read_file travel_[destination]/attractions_detail.md
   read_file travel_[destination]/food_guide.md
   ```

2. **综合信息** - 创建完整的旅行计划：
   - 整合所有调研结果
   - 优化行程安排
   - 提供实用建议和注意事项
   - 添加紧急联系方式和求助信息

3. **生成最终报告** - 使用 `write_file` 创建完整旅游计划：
   ```
   travel_[destination]_[date]/travel_plan_final.md
   ```

   报告应包括：
   - **行程概览**：日期、目的地、主题
   - **每日行程**：详细的时间安排和活动
   - **交通指南**：机票、火车、当地交通
   - **住宿建议**：酒店推荐和预订链接
   - **美食地图**：餐厅推荐和特色美食
   - **预算分解**：详细费用清单
   - **实用信息**：签证、货币、通讯、紧急联系
   - **打包清单**：必备物品清单
   - **旅行贴士**：当地文化、礼仪、安全提示

## 可用工具 (Available Tools)

您可以访问：
- **write_file**: 保存旅行计划和调研结果到本地文件
- **read_file**: 读取本地文件（例如，子代理保存的调研结果）
- **list_files**: 查看目录中存在的文件
- **task**: 委托给有 web_search 访问权限的研究子代理
- **web_search**: 搜索旅游信息、景点、酒店、餐厅评价

## 输出格式 (Output Format)

旅游规划脚本返回格式化的结果：
- **Markdown 格式**：结构化的旅游信息
- **清晰的章节**：行程、预算、景点、美食等
- **实用链接**：官方网站、预订平台、地图
- **可视化提示**：emoji 图标增强可读性

## 功能特点 (Features)

- **智能推荐**：基于兴趣和预算的个性化推荐
- **详细行程**：每日时间表和活动安排
- **预算管理**：透明的费用分解和预算控制
- **本地化支持**：中英文双语支持
- **实时信息**：最新的旅游信息和评价
- **灵活调整**：支持行程修改和备选方案

## 依赖项 (Dependencies)

此技能不需要额外的 Python 包，使用标准库即可运行。

## 最佳实践 (Best Practices)

- **提前规划** - 始终先创建 requirements.md
- **分步调研** - 使用子代理分别调研不同方面
- **文件组织** - 将所有文件保存在专门的旅行文件夹中
- **综合分析** - 完成所有调研后再制定最终计划
- **灵活备选** - 为每个景点和活动准备备选方案
- **安全第一** - 包括紧急联系信息和安全提示
- **文化尊重** - 了解并尊重当地文化和习俗

## 示例场景 (Example Scenarios)

### 场景 1：家庭度假规划
```
目标：规划一次5天的三亚家庭度假
人数：2大1小（5岁）
预算：15000元
兴趣：海滩、水上活动、亲子乐园
```

### 场景 2：文化探索之旅
```
目标：深度游览西安历史文化
天数：4天3夜
兴趣：历史遗迹、博物馆、传统美食
预算：8000元/人
```

### 场景 3：海外自由行
```
目标：日本东京-大阪7日游
人数：2人
预算：20000元/人
兴趣：动漫文化、美食、购物、温泉
```

## 注意事项 (Notes)

- 提供的信息基于一般旅游建议，实际情况可能变化
- 预算估算仅供参考，实际费用取决于具体选择
- 建议提前预订机票和热门景点门票
- 注意查看目的地的签证要求和入境政策
- 购买适当的旅游保险
- 尊重当地文化和环境保护规定
