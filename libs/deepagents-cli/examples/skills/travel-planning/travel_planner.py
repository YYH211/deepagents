#!/usr/bin/env python3
"""旅游规划助手 (Travel Planning Assistant).

提供全面的旅游规划服务，包括目的地推荐、行程安排、预算规划等。
Provides comprehensive travel planning services including destination recommendations,
itinerary planning, and budget management.
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional


# 目的地数据库 (Destination Database)
DESTINATIONS = {
    "国内": {
        "三亚": {
            "类型": ["海滨", "度假"],
            "特色": "热带海滨风光、水上活动、海鲜美食",
            "最佳季节": "10月-次年3月",
            "日均预算": {"经济": 300, "中档": 600, "高档": 1200},
        },
        "北京": {
            "类型": ["历史", "文化", "城市"],
            "特色": "故宫、长城、历史古迹、京味美食",
            "最佳季节": "春秋两季（4-5月，9-10月）",
            "日均预算": {"经济": 250, "中档": 500, "高档": 1000},
        },
        "成都": {
            "类型": ["美食", "文化", "自然"],
            "特色": "川菜、大熊猫、古镇、休闲生活",
            "最佳季节": "春秋两季（3-5月，9-11月）",
            "日均预算": {"经济": 200, "中档": 400, "高档": 800},
        },
        "西安": {
            "类型": ["历史", "文化"],
            "特色": "兵马俑、古城墙、历史遗迹、陕西美食",
            "最佳季节": "春秋两季（4-5月，9-10月）",
            "日均预算": {"经济": 220, "中档": 450, "高档": 900},
        },
        "杭州": {
            "类型": ["自然", "文化", "城市"],
            "特色": "西湖、古镇、江南美食、茶文化",
            "最佳季节": "春秋两季（3-5月，9-11月）",
            "日均预算": {"经济": 280, "中档": 550, "高档": 1100},
        },
        "桂林": {
            "类型": ["自然", "山水"],
            "特色": "漓江山水、溶洞、少数民族文化",
            "最佳季节": "4-10月",
            "日均预算": {"经济": 200, "中档": 400, "高档": 800},
        },
    },
    "国际": {
        "东京": {
            "类型": ["城市", "文化", "购物"],
            "特色": "现代都市、传统文化、动漫、美食",
            "最佳季节": "春季（3-5月）、秋季（9-11月）",
            "日均预算": {"经济": 600, "中档": 1200, "高档": 2500},
        },
        "巴黎": {
            "类型": ["文化", "艺术", "城市"],
            "特色": "艺术博物馆、埃菲尔铁塔、浪漫氛围",
            "最佳季节": "春季（4-6月）、秋季（9-10月）",
            "日均预算": {"经济": 700, "中档": 1400, "高档": 3000},
        },
        "曼谷": {
            "类型": ["文化", "美食", "城市"],
            "特色": "佛教寺庙、泰式按摩、街头美食",
            "最佳季节": "11月-次年2月",
            "日均预算": {"经济": 300, "中档": 600, "高档": 1200},
        },
        "巴厘岛": {
            "类型": ["海滨", "度假", "自然"],
            "特色": "海滩、冲浪、瑜伽、热带风情",
            "最佳季节": "4-10月",
            "日均预算": {"经济": 400, "中档": 800, "高档": 1600},
        },
    },
}

# 景点类型数据 (Attraction Types)
ATTRACTION_TYPES = {
    "historical": {"名称": "历史古迹", "emoji": "🏛️"},
    "natural": {"名称": "自然风光", "emoji": "🏞️"},
    "cultural": {"名称": "文化体验", "emoji": "🎭"},
    "entertainment": {"名称": "娱乐休闲", "emoji": "🎢"},
    "shopping": {"名称": "购物商业", "emoji": "🛍️"},
    "food": {"名称": "美食探索", "emoji": "🍜"},
}


def recommend_destinations(
    interests: Optional[List[str]] = None,
    budget: Optional[int] = None,
    days: int = 7,
) -> str:
    """推荐旅游目的地 (Recommend travel destinations).

    Parameters
    ----------
    interests : List[str], optional
        兴趣标签列表 (List of interest tags)
    budget : int, optional
        总预算（人民币）(Total budget in RMB)
    days : int, default=7
        旅行天数 (Number of travel days)

    Returns
    -------
    str
        格式化的目的地推荐 (Formatted destination recommendations)
    """
    recommendations = []
    interests = interests or []
    daily_budget = budget / days if budget else None

    # 遍历所有目的地
    for region, destinations in DESTINATIONS.items():
        for dest_name, dest_info in destinations.items():
            score = 0

            # 兴趣匹配
            if interests:
                matching_interests = set(interests) & set(dest_info["类型"])
                score += len(matching_interests) * 2

            # 预算匹配
            if daily_budget:
                for level, daily_cost in dest_info["日均预算"].items():
                    if abs(daily_cost - daily_budget) < 200:
                        score += 3
                        budget_level = level
                        break
                else:
                    # 选择最接近的预算级别
                    closest = min(
                        dest_info["日均预算"].items(),
                        key=lambda x: abs(x[1] - daily_budget),
                    )
                    budget_level = closest[0]
                    score += 1
            else:
                budget_level = "中档"

            if score > 0 or not interests:
                recommendations.append(
                    {
                        "name": dest_name,
                        "region": region,
                        "score": score,
                        "info": dest_info,
                        "budget_level": budget_level,
                    }
                )

    # 排序推荐
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    # 格式化输出
    output = ["# 🌍 旅游目的地推荐 (Destination Recommendations)\n"]
    output.append(f"**旅行天数**: {days}天")
    if budget:
        output.append(f"**总预算**: ¥{budget:,} ({budget_level}档)")
    if interests:
        output.append(f"**兴趣偏好**: {', '.join(interests)}")
    output.append("\n---\n")

    for i, rec in enumerate(recommendations[:5], 1):
        dest = rec["info"]
        emoji = "🏙️" if "城市" in dest["类型"] else "🏝️"
        output.append(f"## {i}. {emoji} {rec['name']} ({rec['region']})")
        output.append(f"\n**特色**: {dest['特色']}")
        output.append(f"**类型**: {', '.join(dest['类型'])}")
        output.append(f"**最佳季节**: {dest['最佳季节']}")

        if budget:
            daily_cost = dest["日均预算"][rec["budget_level"]]
            total_cost = daily_cost * days
            output.append(
                f"**预算估算**: ¥{daily_cost}/天 × {days}天 = ¥{total_cost:,} ({rec['budget_level']}档)"
            )

        output.append("\n")

    return "\n".join(output)


def generate_itinerary(
    destination: str, days: int, interests: Optional[List[str]] = None
) -> str:
    """生成旅游行程 (Generate travel itinerary).

    Parameters
    ----------
    destination : str
        目的地名称 (Destination name)
    days : int
        旅行天数 (Number of days)
    interests : List[str], optional
        兴趣标签 (Interest tags)

    Returns
    -------
    str
        格式化的行程安排 (Formatted itinerary)
    """
    interests = interests or ["文化", "美食", "景点"]

    # 查找目的地信息
    dest_info = None
    for region, destinations in DESTINATIONS.items():
        if destination in destinations:
            dest_info = destinations[destination]
            break

    if not dest_info:
        return f"❌ 未找到目的地 '{destination}' 的信息。请检查目的地名称。"

    output = [f"# 📅 {destination} {days}日游行程 (Itinerary)\n"]
    output.append(f"**目的地**: {destination}")
    output.append(f"**天数**: {days}天{days-1}夜")
    output.append(f"**主题**: {', '.join(interests)}")
    output.append(f"\n**目的地特色**: {dest_info['特色']}")
    output.append(f"**最佳旅游季节**: {dest_info['最佳季节']}\n")
    output.append("---\n")

    # 行程模板
    morning_activities = {
        "历史": ["参观历史遗迹", "游览古建筑群", "探索博物馆"],
        "文化": ["体验传统文化", "参观艺术展览", "访问文化街区"],
        "自然": ["游览自然景区", "徒步登山", "欣赏自然风光"],
        "美食": ["品尝当地早点", "探访美食街", "学习烹饪课程"],
        "海滨": ["海滩漫步", "水上运动", "海岛游览"],
    }

    afternoon_activities = {
        "历史": ["深度游览景点", "听导游讲解", "拍照留念"],
        "文化": ["参加文化活动", "手工艺体验", "传统表演"],
        "自然": ["风景区深度游", "生态观察", "自然摄影"],
        "美食": ["特色餐厅午餐", "美食市场探索", "茶馆品茗"],
        "海滨": ["潜水浮潜", "沙滩活动", "海鲜大餐"],
    }

    evening_activities = {
        "历史": ["夜游古城", "灯光秀", "传统餐饮"],
        "文化": ["观看演出", "夜市闲逛", "品尝夜宵"],
        "自然": ["观赏日落", "夜间生态游", "星空观测"],
        "美食": ["夜市小吃", "特色餐厅", "酒吧休闲"],
        "海滨": ["海滩日落", "海鲜晚餐", "海边酒吧"],
    }

    # 生成每日行程
    for day in range(1, days + 1):
        output.append(f"## 第{day}天 (Day {day})")

        if day == 1:
            output.append(f"\n### 🛫 上午 (Morning)")
            output.append("- 抵达目的地")
            output.append("- 酒店入住")
            output.append("- 附近区域熟悉")
        else:
            # 根据目的地类型选择活动
            dest_types = dest_info["类型"]
            primary_type = dest_types[0] if dest_types else "文化"

            output.append(f"\n### 🌅 上午 (Morning)")
            activities = morning_activities.get(primary_type, morning_activities["文化"])
            output.append(f"- {activities[day % len(activities)]}")
            if "美食" in interests:
                output.append("- 品尝当地特色早餐")

        output.append(f"\n### 🌞 下午 (Afternoon)")
        dest_types = dest_info["类型"]
        primary_type = dest_types[0] if dest_types else "文化"
        activities = afternoon_activities.get(
            primary_type, afternoon_activities["文化"]
        )
        output.append(f"- {activities[(day + 1) % len(activities)]}")
        output.append("- 特色午餐")

        output.append(f"\n### 🌃 傍晚/夜晚 (Evening/Night)")
        activities = evening_activities.get(primary_type, evening_activities["文化"])
        output.append(f"- {activities[(day + 2) % len(activities)]}")

        if day == days:
            output.append("- 整理行李，准备离开")

        output.append("\n")

    # 添加旅游贴士
    output.append("---\n")
    output.append("## 💡 旅游贴士 (Travel Tips)\n")
    output.append("- 📱 提前下载离线地图和翻译应用")
    output.append("- 🎫 热门景点建议提前预订门票")
    output.append("- 🚇 了解当地交通方式和交通卡")
    output.append("- 💰 准备适量现金和银行卡")
    output.append("- 📸 充电宝、相机等设备充满电")
    output.append("- 🏥 记录紧急联系电话和医院地址")

    return "\n".join(output)


def plan_budget(
    destination: str, days: int, travelers: int = 1, level: str = "中档"
) -> str:
    """规划旅游预算 (Plan travel budget).

    Parameters
    ----------
    destination : str
        目的地名称 (Destination name)
    days : int
        旅行天数 (Number of days)
    travelers : int, default=1
        旅行人数 (Number of travelers)
    level : str, default="中档"
        档次级别：经济/中档/高档 (Budget level: 经济/中档/高档)

    Returns
    -------
    str
        格式化的预算规划 (Formatted budget plan)
    """
    # 查找目的地信息
    dest_info = None
    region = None
    for reg, destinations in DESTINATIONS.items():
        if destination in destinations:
            dest_info = destinations[destination]
            region = reg
            break

    if not dest_info:
        return f"❌ 未找到目的地 '{destination}' 的信息。"

    if level not in dest_info["日均预算"]:
        level = "中档"

    daily_budget = dest_info["日均预算"][level]

    output = [f"# 💰 {destination} 旅游预算规划 (Budget Plan)\n"]
    output.append(f"**目的地**: {destination} ({region})")
    output.append(f"**天数**: {days}天{days-1}夜")
    output.append(f"**人数**: {travelers}人")
    output.append(f"**档次**: {level}\n")
    output.append("---\n")

    # 预算分解
    output.append("## 📊 预算分解 (Budget Breakdown)\n")

    # 交通费用
    transport_cost = 0
    if region == "国内":
        if destination in ["三亚", "桂林"]:
            transport_cost = 1500 * travelers  # 机票
        else:
            transport_cost = 800 * travelers  # 高铁
    else:
        transport_cost = 4000 * travelers  # 国际机票

    output.append(f"### 🛫 交通费用 (Transportation)")
    output.append(f"- 往返交通: ¥{transport_cost:,}")
    if days > 3:
        local_transport = 50 * days * travelers
        output.append(f"- 当地交通: ¥{local_transport:,} (¥50/天/人)")
        transport_cost += local_transport
    output.append(f"- **小计**: ¥{transport_cost:,}\n")

    # 住宿费用
    accommodation_rates = {"经济": 200, "中档": 400, "高档": 800}
    if region == "国际":
        accommodation_rates = {k: v * 2 for k, v in accommodation_rates.items()}

    room_rate = accommodation_rates[level]
    nights = days - 1
    # 假设双人间，奇数人数需要加房间
    rooms_needed = (travelers + 1) // 2
    accommodation_cost = room_rate * nights * rooms_needed

    output.append(f"### 🏨 住宿费用 (Accommodation)")
    output.append(f"- 房型: {level}酒店")
    output.append(f"- 房间数: {rooms_needed}间")
    output.append(f"- 房价: ¥{room_rate}/晚/间")
    output.append(f"- 住宿天数: {nights}晚")
    output.append(f"- **小计**: ¥{accommodation_cost:,}\n")

    # 餐饮费用
    meal_rates = {"经济": 100, "中档": 200, "高档": 400}
    if region == "国际":
        meal_rates = {k: v * 1.5 for k, v in meal_rates.items()}

    meal_daily = meal_rates[level]
    food_cost = meal_daily * days * travelers

    output.append(f"### 🍽️ 餐饮费用 (Food)")
    output.append(f"- 餐饮标准: ¥{meal_daily}/天/人")
    output.append(f"- **小计**: ¥{food_cost:,}\n")

    # 景点门票
    attraction_rates = {"经济": 150, "中档": 300, "高档": 500}
    if region == "国际":
        attraction_rates = {k: v * 1.5 for k, v in attraction_rates.items()}

    attraction_daily = attraction_rates[level]
    attraction_cost = attraction_daily * days * travelers

    output.append(f"### 🎫 景点门票 (Attractions)")
    output.append(f"- 门票预算: ¥{attraction_daily}/天/人")
    output.append(f"- **小计**: ¥{attraction_cost:,}\n")

    # 购物和其他
    shopping_rates = {"经济": 300, "中档": 1000, "高档": 3000}
    shopping_cost = shopping_rates[level] * travelers

    output.append(f"### 🛍️ 购物及其他 (Shopping & Others)")
    output.append(f"- 购物预算: ¥{shopping_rates[level]}/人")
    output.append(f"- **小计**: ¥{shopping_cost:,}\n")

    # 总计
    total_cost = (
        transport_cost + accommodation_cost + food_cost + attraction_cost + shopping_cost
    )
    per_person = total_cost / travelers

    output.append("---\n")
    output.append("## 💵 费用总计 (Total Cost)\n")
    output.append(f"- **总费用**: ¥{total_cost:,}")
    output.append(f"- **人均费用**: ¥{per_person:,.0f}/人")
    output.append(f"- **日均费用**: ¥{total_cost/days:,.0f}/天\n")

    # 建议预留金额
    reserve = total_cost * 0.15
    output.append("## 📝 建议 (Recommendations)\n")
    output.append(f"- 建议预留 15% 应急资金: ¥{reserve:,.0f}")
    output.append(f"- **建议总预算**: ¥{total_cost + reserve:,.0f}")

    return "\n".join(output)


def recommend_attractions(
    destination: str, days: int = 3, attraction_type: str = "cultural"
) -> str:
    """推荐旅游景点 (Recommend attractions).

    Parameters
    ----------
    destination : str
        目的地名称 (Destination name)
    days : int, default=3
        旅行天数 (Number of days)
    attraction_type : str, default="cultural"
        景点类型 (Attraction type)

    Returns
    -------
    str
        格式化的景点推荐 (Formatted attraction recommendations)
    """
    # 查找目的地信息
    dest_info = None
    for region, destinations in DESTINATIONS.items():
        if destination in destinations:
            dest_info = destinations[destination]
            break

    if not dest_info:
        return f"❌ 未找到目的地 '{destination}' 的信息。"

    type_info = ATTRACTION_TYPES.get(
        attraction_type, {"名称": "综合景点", "emoji": "📍"}
    )

    output = [f"# {type_info['emoji']} {destination} 景点推荐 ({type_info['名称']})\n"]
    output.append(f"**目的地**: {destination}")
    output.append(f"**景点类型**: {type_info['名称']}")
    output.append(f"**游览天数**: {days}天\n")
    output.append("---\n")

    # 根据目的地提供推荐景点（示例数据）
    attractions_db = {
        "北京": [
            {
                "name": "故宫博物院",
                "type": "historical",
                "time": "4-5小时",
                "ticket": "60元",
                "highlight": "明清皇宫，世界文化遗产",
            },
            {
                "name": "长城（八达岭）",
                "type": "historical",
                "time": "半天",
                "ticket": "40元",
                "highlight": "世界七大奇迹之一",
            },
            {
                "name": "颐和园",
                "type": "cultural",
                "time": "3-4小时",
                "ticket": "30元",
                "highlight": "皇家园林，山水景观",
            },
            {
                "name": "天坛公园",
                "type": "cultural",
                "time": "2-3小时",
                "ticket": "15元",
                "highlight": "明清祭天场所",
            },
            {
                "name": "南锣鼓巷",
                "type": "cultural",
                "time": "2-3小时",
                "ticket": "免费",
                "highlight": "胡同文化，特色小吃",
            },
        ],
        "三亚": [
            {
                "name": "亚龙湾",
                "type": "natural",
                "time": "全天",
                "ticket": "免费",
                "highlight": "天下第一湾，水质清澈",
            },
            {
                "name": "蜈支洲岛",
                "type": "natural",
                "time": "全天",
                "ticket": "144元",
                "highlight": "海岛风光，潜水圣地",
            },
            {
                "name": "南山文化旅游区",
                "type": "cultural",
                "time": "半天",
                "ticket": "129元",
                "highlight": "南山海上观音",
            },
            {
                "name": "天涯海角",
                "type": "natural",
                "time": "2-3小时",
                "ticket": "81元",
                "highlight": "浪漫地标",
            },
        ],
        "西安": [
            {
                "name": "兵马俑博物馆",
                "type": "historical",
                "time": "半天",
                "ticket": "120元",
                "highlight": "世界第八大奇迹",
            },
            {
                "name": "西安城墙",
                "type": "historical",
                "time": "2-3小时",
                "ticket": "54元",
                "highlight": "中国现存最完整的古城墙",
            },
            {
                "name": "大雁塔",
                "type": "cultural",
                "time": "2小时",
                "ticket": "40元",
                "highlight": "唐代佛教圣地",
            },
            {
                "name": "回民街",
                "type": "food",
                "time": "2-3小时",
                "ticket": "免费",
                "highlight": "陕西美食聚集地",
            },
        ],
    }

    # 获取该目的地的景点
    attractions = attractions_db.get(
        destination,
        [
            {
                "name": f"{destination}标志性景点",
                "type": attraction_type,
                "time": "半天",
                "ticket": "待查询",
                "highlight": dest_info["特色"],
            }
        ],
    )

    # 筛选符合类型的景点
    if attraction_type != "cultural":
        filtered = [a for a in attractions if a["type"] == attraction_type]
        if filtered:
            attractions = filtered

    # 输出推荐景点
    for i, attr in enumerate(attractions[:days * 2], 1):  # 每天最多2个景点
        output.append(f"## {i}. {attr['name']}")
        output.append(f"- **类型**: {ATTRACTION_TYPES.get(attr['type'], {}).get('名称', '综合')}")
        output.append(f"- **游览时长**: {attr['time']}")
        output.append(f"- **门票价格**: {attr['ticket']}")
        output.append(f"- **亮点**: {attr['highlight']}\n")

    output.append("---\n")
    output.append("## 🗓️ 游览建议 (Visit Suggestions)\n")
    output.append(f"- 根据 {days} 天的行程，建议选择 {min(days * 2, len(attractions))} 个景点深度游览")
    output.append("- 热门景点建议提前网上预订门票")
    output.append("- 合理安排时间，避开旅游高峰期")
    output.append("- 注意景点开放时间和特殊要求")

    return "\n".join(output)


def main() -> None:
    """主函数 (Main function)."""
    parser = argparse.ArgumentParser(
        description="旅游规划助手 (Travel Planning Assistant)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令 (Available commands)")

    # 目的地推荐命令
    recommend_parser = subparsers.add_parser("recommend", help="推荐旅游目的地")
    recommend_parser.add_argument(
        "--interests", type=str, help="兴趣标签，逗号分隔 (例如: 文化,美食,海滨)"
    )
    recommend_parser.add_argument("--budget", type=int, help="总预算（人民币）")
    recommend_parser.add_argument("--days", type=int, default=7, help="旅行天数")

    # 行程生成命令
    itinerary_parser = subparsers.add_parser("itinerary", help="生成旅游行程")
    itinerary_parser.add_argument("--destination", type=str, required=True, help="目的地名称")
    itinerary_parser.add_argument("--days", type=int, required=True, help="旅行天数")
    itinerary_parser.add_argument("--interests", type=str, help="兴趣标签，逗号分隔")

    # 预算规划命令
    budget_parser = subparsers.add_parser("budget", help="规划旅游预算")
    budget_parser.add_argument("--destination", type=str, required=True, help="目的地名称")
    budget_parser.add_argument("--days", type=int, required=True, help="旅行天数")
    budget_parser.add_argument("--travelers", type=int, default=1, help="旅行人数")
    budget_parser.add_argument(
        "--level",
        type=str,
        default="中档",
        choices=["经济", "中档", "高档"],
        help="档次级别",
    )

    # 景点推荐命令
    attractions_parser = subparsers.add_parser("attractions", help="推荐旅游景点")
    attractions_parser.add_argument(
        "--destination", type=str, required=True, help="目的地名称"
    )
    attractions_parser.add_argument("--days", type=int, default=3, help="旅行天数")
    attractions_parser.add_argument(
        "--type",
        type=str,
        default="cultural",
        choices=list(ATTRACTION_TYPES.keys()),
        help="景点类型",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 执行相应命令
    if args.command == "recommend":
        interests = args.interests.split(",") if args.interests else None
        result = recommend_destinations(
            interests=interests, budget=args.budget, days=args.days
        )
    elif args.command == "itinerary":
        interests = args.interests.split(",") if args.interests else None
        result = generate_itinerary(
            destination=args.destination, days=args.days, interests=interests
        )
    elif args.command == "budget":
        result = plan_budget(
            destination=args.destination,
            days=args.days,
            travelers=args.travelers,
            level=args.level,
        )
    elif args.command == "attractions":
        result = recommend_attractions(
            destination=args.destination, days=args.days, attraction_type=args.type
        )
    else:
        parser.print_help()
        return

    print(result)


if __name__ == "__main__":
    main()
