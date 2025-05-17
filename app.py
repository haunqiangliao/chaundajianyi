import streamlit as st
import pandas as pd
import random
import datetime

# 页面配置
st.set_page_config(
    page_title="智能穿搭助手",
    page_icon="👗",
    layout="wide"
)

# 预设服装数据库（增加了一些基础款，确保所有条件下都有可选衣物）
clothes_db = {
    "上衣": [
        {"name": "白色T恤", "color": "#FFFFFF", "season": ["春季", "夏季", "秋季"]},
        {"name": "黑色T恤", "color": "#000000", "season": ["春季", "夏季", "秋季"]},
        {"name": "灰色卫衣", "color": "#808080", "season": ["春季", "秋季", "冬季"]},
        {"name": "牛仔衬衫", "color": "#3B7A9D", "season": ["春季", "秋季"]},
        {"name": "白色衬衫", "color": "#FFFFFF", "season": ["春季", "夏季", "秋季"]},
        {"name": "黑色西装", "color": "#000000", "season": ["春季", "秋季", "冬季"]},
        {"name": "红色连衣裙", "color": "#FF0000", "season": ["春季", "夏季"]},
        {"name": "蓝色连衣裙", "color": "#0000FF", "season": ["春季", "夏季"]},
        {"name": "针织开衫", "color": "#D2B48C", "season": ["春季", "秋季"]},
        {"name": "羽绒服", "color": "#F0F8FF", "season": ["冬季"]},
        {"name": "毛衣", "color": "#A0522D", "season": ["秋季", "冬季"]},
        {"name": "基础款长袖", "color": "#8B4513", "season": ["全年"]},  # 新增全年可用选项
        {"name": "休闲外套", "color": "#696969", "season": ["全年"]}     # 新增全年可用选项
    ],
    "下装": [
        {"name": "蓝色牛仔裤", "color": "#3B7A9D", "season": ["春季", "秋季", "冬季"]},
        {"name": "黑色西装裤", "color": "#000000", "season": ["春季", "秋季", "冬季"]},
        {"name": "卡其色休闲裤", "color": "#F0E68C", "season": ["春季", "秋季"]},
        {"name": "黑色短裙", "color": "#000000", "season": ["春季", "夏季", "秋季"]},
        {"name": "碎花长裙", "color": "#FFB6C1", "season": ["春季", "夏季"]},
        {"name": "运动裤", "color": "#8FBC8F", "season": ["全年"]},       # 新增全年可用选项
        {"name": "加绒裤", "color": "#8B4513", "season": ["冬季"]},
        {"name": "基础款短裤", "color": "#D3D3D3", "season": ["夏季"]}     # 新增夏季选项
    ],
    "鞋履": [
        {"name": "白色运动鞋", "color": "#FFFFFF", "season": ["全年"]},    # 新增全年可用选项
        {"name": "黑色皮鞋", "color": "#000000", "season": ["全年"]},
        {"name": "凉鞋", "color": "#FFA500", "season": ["夏季"]},
        {"name": "切尔西靴", "color": "#8B4513", "season": ["秋季", "冬季"]},
        {"name": "雪地靴", "color": "#F5F5DC", "season": ["冬季"]},
        {"name": "低跟鞋", "color": "#800080", "season": ["全年"]},
        {"name": "高跟鞋", "color": "#FF0000", "season": ["全年"]},
        {"name": "帆布鞋", "color": "#CD5C5C", "season": ["全年"]}         # 新增全年可用选项
    ],
    "配饰": [
        {"name": "黑色围巾", "color": "#000000", "season": ["冬季"]},
        {"name": "白色帽子", "color": "#FFFFFF", "season": ["全年"]},
        {"name": "太阳镜", "color": "#808080", "season": ["夏季"]},
        {"name": "项链", "color": "#FFD700", "season": ["全年"]},
        {"name": "手提包", "color": "#A52A2A", "season": ["全年"]},
        {"name": "手表", "color": "#C0C0C0", "season": ["全年"]}           # 新增全年可用选项
    ]
}

# 天气对应穿搭规则（调整为更宽松的筛选条件）
weather_rules = {
    "晴天": {"上衣": ["T恤", "衬衫", "薄外套", "连衣裙"], "下装": ["短裤", "短裙", "薄款长裤"], "鞋履": ["凉鞋", "运动鞋", "帆布鞋"]},
    "多云": {"上衣": ["衬衫", "卫衣", "薄外套", "针织开衫"], "下装": ["牛仔裤", "休闲裤"], "鞋履": ["休闲鞋", "运动鞋", "帆布鞋"]},
    "雨天": {"上衣": ["防水外套", "风衣", "休闲外套"], "下装": ["长裤"], "鞋履": ["雨鞋", "防水鞋", "切尔西靴"]},
    "寒冷": {"上衣": ["毛衣", "羽绒服", "厚外套", "卫衣"], "下装": ["加绒裤", "毛裤", "牛仔裤"], "鞋履": ["雪地靴", "切尔西靴"]}
}

# 场合对应穿搭规则（调整为更宽松的筛选条件）
occasion_rules = {
    "日常": {"上衣": ["T恤", "卫衣", "衬衫", "针织开衫"], "下装": ["牛仔裤", "休闲裤", "短裤", "短裙"], "鞋履": ["运动鞋", "休闲鞋", "帆布鞋"]},
    "上班": {"上衣": ["衬衫", "西装", "职业装", "连衣裙"], "下装": ["西装裤", "长裙", "牛仔裤"], "鞋履": ["皮鞋", "低跟鞋"]},
    "运动": {"上衣": ["运动背心", "运动卫衣", "T恤"], "下装": ["运动裤", "瑜伽裤"], "鞋履": ["运动鞋"]},
    "约会": {"上衣": ["连衣裙", "雪纺衫", "针织衫", "衬衫"], "下装": ["牛仔裤", "短裙", "长裙"], "鞋履": ["高跟鞋", "凉鞋", "低跟鞋"]},
    "派对": {"上衣": ["晚礼服", "闪亮上衣", "露肩装", "连衣裙"], "下装": ["长裙", "紧身裤", "短裙"], "鞋履": ["高跟鞋", "凉鞋"]}
}

# 穿搭推荐页面
def outfit_recommendation():
    st.title("✨ 智能穿搭助手")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # 用户输入
        st.subheader("请选择您的穿搭条件")
        
        col_a, col_b = st.columns(2)
        with col_a:
            weather = st.selectbox("天气", ["晴天", "多云", "雨天", "寒冷"])
        with col_b:
            occasion = st.selectbox("场合", ["日常", "上班", "运动", "约会", "派对"])
        
        season = st.selectbox("季节", ["春季", "夏季", "秋季", "冬季"])
        
        if st.button("生成穿搭建议", use_container_width=True):
            with st.spinner("正在为您搭配..."):
                # 获取符合条件的衣物
                valid_clothes = {}
                
                for category, items in clothes_db.items():
                    # 应用季节筛选（最基本的筛选）
                    season_filtered = [item for item in items 
                                      if not item['season'] or season in item['season']]
                    
                    # 应用天气筛选（如果有对应规则）
                    weather_filtered = []
                    if weather in weather_rules and category in weather_rules[weather]:
                        weather_keywords = weather_rules[weather][category]
                        weather_filtered = [item for item in season_filtered 
                                           if any(keyword in item['name'] for keyword in weather_keywords)]
                        
                        # 如果天气筛选后没有结果，放宽条件使用季节筛选结果
                        if not weather_filtered:
                            weather_filtered = season_filtered
                    else:
                        weather_filtered = season_filtered
                    
                    # 应用场合筛选（如果有对应规则）
                    if occasion in occasion_rules and category in occasion_rules[occasion]:
                        occasion_keywords = occasion_rules[occasion][category]
                        occasion_filtered = [item for item in weather_filtered 
                                            if any(keyword in item['name'] for keyword in occasion_keywords)]
                        
                        # 如果场合筛选后没有结果，放宽条件使用天气筛选结果
                        if not occasion_filtered:
                            occasion_filtered = weather_filtered
                        valid_clothes[category] = occasion_filtered
                    else:
                        valid_clothes[category] = weather_filtered
                
                # 确保每个分类至少有一个选项（防止空列表错误）
                for category in valid_clothes:
                    if not valid_clothes[category]:
                        # 如果所有筛选都失败，使用原始数据库中第一个符合季节的衣物
                        fallback_items = [item for item in clothes_db[category] 
                                         if not item['season'] or season in item['season']]
                        if fallback_items:
                            valid_clothes[category] = fallback_items
                        else:
                            # 如果季节筛选也失败，使用该分类的所有衣物
                            valid_clothes[category] = clothes_db[category]
                
                # 生成至少一套穿搭建议
                outfits = []
                
                # 生成第一套穿搭（强制生成）
                outfit = {}
                for category in valid_clothes:
                    outfit[category] = random.choice(valid_clothes[category])
                outfits.append(outfit)
                
                # 尝试生成额外的穿搭建议（最多2套）
                max_attempts = 20
                attempts = 0
                
                while len(outfits) < 3 and attempts < max_attempts:
                    new_outfit = {}
                    for category in valid_clothes:
                        new_outfit[category] = random.choice(valid_clothes[category])
                    
                    # 检查是否与已生成的穿搭重复
                    is_duplicate = False
                    for existing_outfit in outfits:
                        if all(new_outfit[category] == existing_outfit[category] for category in new_outfit):
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        outfits.append(new_outfit)
                    
                    attempts += 1
                
                # 显示穿搭建议
                st.subheader(f"为您生成的 {occasion} {weather} 穿搭建议：")
                
                for i, outfit in enumerate(outfits, 1):
                    st.markdown(f"""
                    <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; margin-bottom: 15px; transition: all 0.3s ease; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h3 style="color: #1E88E5; margin: 0; display: flex; align-items: center;">
                            <span style="background-color: #1E88E5; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">{i}</span>
                            穿搭方案 {i}
                        </h3>
                        <div style="margin-top: 15px;">
                    """, unsafe_allow_html=True)
                    
                    for category, item in outfit.items():
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <div style="width: 24px; height: 24px; background-color: {item['color']}; border-radius: 50%; margin-right: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);"></div>
                            <span style="font-weight: 500; width: 80px; display: inline-block;">{category}:</span>
                            <span style="margin-left: 5px; color: #333;">{item['name']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 添加提示信息
                    if i == 1 and len(outfits) == 1:
                        st.markdown(f"""
                        <div style="margin-top: 10px; padding: 8px; background-color: #fff3cd; border-radius: 5px; color: #856404; font-size: 0.9em;">
                            <i class="fa fa-lightbulb-o"></i> 由于筛选条件较严格，仅生成了一套穿搭建议。您可以尝试调整条件以获取更多选择。
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        st.subheader("穿搭小贴士")
        
        tips = {
            "晴天": "阳光明媚，适合亮色和轻薄面料",
            "多云": "温度适中，可叠穿增加层次感",
            "雨天": "别忘了携带雨具，选择防水材质",
            "寒冷": "保暖第一，注意围巾和手套的搭配",
            "日常": "舒适为主，可适当添加配饰提升整体感",
            "上班": "简约大方，避免过于花哨的设计",
            "运动": "选择透气吸汗的运动装备",
            "约会": "根据场合选择优雅或休闲的风格",
            "派对": "可以大胆尝试闪亮元素和独特设计"
        }
        
        st.info(f"**{weather} {occasion} 小贴士**:\n\n{tips[weather]} | {tips[occasion]}")
        
        # 今日日期和天气信息
        today = datetime.datetime.now().strftime("%Y年%m月%d日 %A")
        st.markdown(f"📅 **今日日期**: {today}")
        
        # 随机搭配技巧
        style_tips = [
            "同色系搭配会显得更加协调统一",
            "小面积亮色可以提升整体造型的亮点",
            "材质对比（如针织与皮革）能增加穿搭层次感",
            "配饰是穿搭的灵魂，合适的配饰能让造型更完整",
            "遵循上松下紧或上紧下松的原则会更显身材",
            "深色显瘦，浅色显温柔，可以根据需求选择",
            "尝试不同风格的混搭，可能会有意想不到的效果"
        ]
        
        st.markdown(f"💡 **搭配技巧**: {random.choice(style_tips)}")

# 主页面
def main():
    outfit_recommendation()

if __name__ == "__main__":
    main()
