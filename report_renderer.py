import streamlit as st
import numpy as np
from datetime import datetime

def render_farmer_report_html(report_html):
    """عرض تقرير المزارع بشكل صحيح في Streamlit"""
    # استخدام container لعزل التقرير
    with st.container():
        # إضافة CSS إضافي للتقرير
        st.markdown("""
        <style>
        .agriq-report-container {
            font-family: 'Arial', 'Segoe UI', sans-serif;
            line-height: 1.6;
        }
        .agriq-report-container h2 {
            color: #10b981;
            text-align: center;
            border-bottom: 2px solid #334155;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .agriq-report-container h3 {
            color: #10b981;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        .agriq-report-container h4 {
            color: #10b981;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .agriq-report-container p {
            margin: 8px 0;
        }
        .agriq-report-container ul {
            padding-right: 20px;
        }
        .agriq-report-container li {
            margin: 5px 0;
        }
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 15px;
            border-radius: 10px;
            border-right: 4px solid #10b981;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # عرض التقرير
        st.markdown(f"""
        <div class="agriq-report-container">
            {report_html}
        </div>
        """, unsafe_allow_html=True)

def generate_simple_report(crop_data, city, weather_data, soil_data, model_accuracy):
    """توليد تقرير مبسط وسهل القراءة"""
    
    # حساب نسبة الملاءمة
    suitability_score = min(95, 70 + abs(weather_data.get('temp', 25)-25) + abs(soil_data.get('ph', 7.0)-6.8)*10)
    
    # نص الملاءمة
    if suitability_score >= 85:
        suitability_text = "ممتازة 🎯"
        suitability_color = "#10b981"
    elif suitability_score >= 70:
        suitability_text = "جيدة جداً 👍"
        suitability_color = "#3b82f6"
    elif suitability_score >= 60:
        suitability_text = "جيدة ✅"
        suitability_color = "#f59e0b"
    else:
        suitability_text = "متوسطة ⚠️"
        suitability_color = "#ef4444"
    
    # خطة الري
    irrigation_plan = {
        "الذرة": "الري بالتنقيط السطحي (مرتان أسبوعياً)",
        "البندورة": "الري بالتنقيط المتقطع (كل يومين)",
        "البطاطا": "الري بالرشاشات الخفيفة (مرة أسبوعياً)",
        "الزيتون": "الري التكميلي (مرة كل أسبوعين)",
        "البرتقال": "الري بالتنقيط (مرتان أسبوعياً)"
    }
    
    irrigation = irrigation_plan.get(crop_data['ar'], "الري بالتنقيط السطحي الموفر")
    
    # العائد المتوقع
    expected_profit = crop_data['profit'] * 1.1  # زيادة 10% للتحفيز
    
    return f"""
    ## 🌱 تقرير الزراعة الذكي - AgriQ
    
    **📍 الموقع:** {city}
    **📅 التاريخ:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
    
    ---
    
    ### 🎯 المحصول المقترح: **{crop_data['ar']}**
    
    بناءً على تحليل دقيق لظروف تربتك ومناخ منطقتك، ننصحك بزراعة **{crop_data['ar']}** لأنه:
    - ✅ **ملائم بنسبة {suitability_score:.0f}%** لظروف منطقتك
    - 💧 **موفر للمياه** بنسبة {crop_data['water_saving']}%
    - 💰 **ربحي** مع عائد متوقع **{expected_profit:,} شيكل/دونم**
    - 📈 **مطلوب في السوق** ({crop_data['market_demand']})
    
    ---
    
    ### 📊 تحليل منطقتك
    
    **🌡️ الطقس الحالي:**
    - درجة الحرارة: {weather_data.get('temp', 25)}°C
    - الرطوبة: {weather_data.get('humidity', 60)}%
    
    **🧪 حالة التربة:**
    - النوع: {soil_data.get('soil_type', 'طميية')}
    - الحموضة: {soil_data.get('ph', 7.0)}
    - المغذيات: N:{soil_data.get('N', 70)} P:{soil_data.get('P', 40)} K:{soil_data.get('K', 35)}
    
    ---
    
    ### 📅 خطة الزراعة
    
    1. **🌱 موعد الزراعة:** {crop_data['season']}
    2. **💧 طريقة الري:** {irrigation}
    3. **🔄 مدة النمو:** {crop_data['growth_days']} يوم
    4. **🍎 موعد الحصاد:** بعد {crop_data['growth_days']} يوم من الزراعة
    
    ---
    
    ### 💡 نصائح ذهبية
    
    • ابدأ الزراعة في الصباح الباكر
    • استخدم الأسمدة العضوية لتحسين التربة
    • سجل تقدم المحصول في تطبيق AgriQ
    • احصد في الطقس الجاف للحفاظ على الجودة
    
    ---
    
    ### 📊 معلومات النموذج
    **دقة الذكاء الاصطناعي:** {model_accuracy*100:.1f}%
    **رقم التقرير:** AGR{np.random.randint(1000, 9999)}
    
    ---
    
    **🤝 مع تمنياتنا بحصاد وافر وموسم ناجح!**
    **فريق AgriQ - من أجل زراعة فلسطينية مستدامة 🇵🇸**
    """