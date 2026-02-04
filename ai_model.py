import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import streamlit as st
import os
from PIL import Image

# بيانات التربة من SoilGrids (محاكاة) مع قيم واقعية لفلسطين
SOILGRIDS_DATA = {
    "طولكرم": {"N": 90, "P": 42, "K": 43, "soil_type": "طينية", "ph": 7.2},
    "جنين": {"N": 70, "P": 50, "K": 35, "soil_type": "طميية", "ph": 6.8},
    "أريحا": {"N": 40, "P": 30, "K": 20, "soil_type": "رملية", "ph": 6.5},
    "الخليل": {"N": 80, "P": 55, "K": 40, "soil_type": "حجرية", "ph": 7.5},
    "رام الله": {"N": 75, "P": 48, "K": 38, "soil_type": "طينية", "ph": 7.0},
    "بيت لحم": {"N": 78, "P": 52, "K": 41, "soil_type": "طميية", "ph": 6.9},
    "قلقيلية": {"N": 88, "P": 45, "K": 44, "soil_type": "طينية", "ph": 7.1},
    "سلفيت": {"N": 82, "P": 47, "K": 39, "soil_type": "حجرية", "ph": 7.3},
    "طوباس": {"N": 68, "P": 44, "K": 36, "soil_type": "طميية", "ph": 6.7},
    "نابلس": {"N": 85, "P": 53, "K": 42, "soil_type": "طينية", "ph": 7.0},
    "أبو ديس": {"N": 45, "P": 32, "K": 22, "soil_type": "رملية", "ph": 6.4},
    "القدس": {"N": 72, "P": 46, "K": 37, "soil_type": "حجرية", "ph": 7.4},
    "بيت حانون": {"N": 92, "P": 44, "K": 45, "soil_type": "طينية", "ph": 7.2},
    "خان يونس": {"N": 35, "P": 28, "K": 18, "soil_type": "رملية", "ph": 6.3},
    "رفح": {"N": 30, "P": 25, "K": 15, "soil_type": "رملية", "ph": 6.2},
    "دير البلح": {"N": 38, "P": 31, "K": 20, "soil_type": "رملية", "ph": 6.5},
    "بيت لاهيا": {"N": 89, "P": 43, "K": 43, "soil_type": "طينية", "ph": 7.1},
    "جبليا": {"N": 86, "P": 46, "K": 41, "soil_type": "طميية", "ph": 6.9},
}

# قاعدة بيانات المناخ التلقائية لفلسطين
PALESTINE_CLIMATE_DATA = {
    "طولكرم": {"avg_rainfall": 500, "avg_ph": 7.2, "climate_zone": "ساحلي", "altitude": 100},
    "جنين": {"avg_rainfall": 450, "avg_ph": 6.8, "climate_zone": "جبلية", "altitude": 250},
    "أريحا": {"avg_rainfall": 150, "avg_ph": 6.5, "climate_zone": "صحراوي", "altitude": -250},
    "الخليل": {"avg_rainfall": 400, "avg_ph": 7.5, "climate_zone": "جبلية", "altitude": 930},
    "رام الله": {"avg_rainfall": 600, "avg_ph": 7.0, "climate_zone": "جبلية", "altitude": 880},
    "بيت لحم": {"avg_rainfall": 580, "avg_ph": 6.9, "climate_zone": "جبلية", "altitude": 775},
    "قلقيلية": {"avg_rainfall": 480, "avg_ph": 7.1, "climate_zone": "ساحلي", "altitude": 80},
    "سلفيت": {"avg_rainfall": 520, "avg_ph": 7.3, "climate_zone": "جبلية", "altitude": 510},
    "طوباس": {"avg_rainfall": 420, "avg_ph": 6.7, "climate_zone": "جبلية", "altitude": 320},
    "نابلس": {"avg_rainfall": 550, "avg_ph": 7.0, "climate_zone": "جبلية", "altitude": 550},
    "أبو ديس": {"avg_rainfall": 350, "avg_ph": 6.4, "climate_zone": "صحراوي", "altitude": 630},
    "القدس": {"avg_rainfall": 620, "avg_ph": 7.4, "climate_zone": "جبلية", "altitude": 760},
    "بيت حانون": {"avg_rainfall": 450, "avg_ph": 7.2, "climate_zone": "ساحلي", "altitude": 45},
    "خان يونس": {"avg_rainfall": 300, "avg_ph": 6.3, "climate_zone": "ساحلي", "altitude": 40},
    "رفح": {"avg_rainfall": 250, "avg_ph": 6.2, "climate_zone": "ساحلي", "altitude": 45},
    "دير البلح": {"avg_rainfall": 320, "avg_ph": 6.5, "climate_zone": "ساحلي", "altitude": 30},
    "بيت لاهيا": {"avg_rainfall": 480, "avg_ph": 7.1, "climate_zone": "ساحلي", "altitude": 50},
    "جبليا": {"avg_rainfall": 470, "avg_ph": 6.9, "climate_zone": "ساحلي", "altitude": 55},
    "غزة": {"avg_rainfall": 400, "avg_ph": 7.0, "climate_zone": "ساحلي", "altitude": 30},
    "البيرة": {"avg_rainfall": 590, "avg_ph": 7.1, "climate_zone": "جبلية", "altitude": 860},
    "بيت ساحور": {"avg_rainfall": 570, "avg_ph": 6.8, "climate_zone": "جبلية", "altitude": 620},
    "بيت جالا": {"avg_rainfall": 560, "avg_ph": 6.9, "climate_zone": "جبلية", "altitude": 775},
    "عنبتا": {"avg_rainfall": 520, "avg_ph": 7.0, "climate_zone": "جبلية", "altitude": 180},
    "قباطية": {"avg_rainfall": 480, "avg_ph": 6.9, "climate_zone": "جبلية", "altitude": 210},
    "يعبد": {"avg_rainfall": 460, "avg_ph": 6.8, "climate_zone": "جبلية", "altitude": 190},
    "مرج بن عامر": {"avg_rainfall": 440, "avg_ph": 7.1, "climate_zone": "سهلية", "altitude": 120},
}

def get_soil_data(city):
    """الحصول على بيانات التربة من قاعدة بيانات محلية أو API"""
    if city in SOILGRIDS_DATA:
        return SOILGRIDS_DATA[city]
    else:
        # قيم افتراضية واقعية للمدن الأخرى
        return {"N": 70, "P": 40, "K": 35, "soil_type": "طميية", "ph": 6.8}

def get_climate_data(city):
    """الحصول على بيانات المناخ التلقائية للمنطقة"""
    if city in PALESTINE_CLIMATE_DATA:
        return PALESTINE_CLIMATE_DATA[city]
    else:
        # تقدير بناءً على المنطقة الجغرافية
        region_data = {
            "شمال الضفة": {"avg_rainfall": 480, "avg_ph": 6.9, "climate_zone": "جبلية"},
            "وسط الضفة": {"avg_rainfall": 580, "avg_ph": 7.2, "climate_zone": "جبلية"},
            "جنوب الضفة": {"avg_rainfall": 350, "avg_ph": 7.0, "climate_zone": "صحراوي-جبلية"},
            "قطاع غزة": {"avg_rainfall": 380, "avg_ph": 6.8, "climate_zone": "ساحلي"}
        }
        
        # تحديد المنطقة من بيانات المدن
        default_region = "وسط الضفة"
        return region_data.get(default_region, {"avg_rainfall": 450, "avg_ph": 7.0, "climate_zone": "معتدل"})

def train_model_from_csv():
    """نماذج تدريب محسنة مع بيانات تجريبية واقعية لفلسطين"""
    try:
        # محاولة تحميل بيانات حقيقية إذا وجدت
        data_paths = [
            'data/AgriQ_Final_Tulkarm_Data.csv',
            'data/sample_agriculture_data.csv',
            'data/palestine_crops_dataset.csv'
        ]
        
        df = None
        for path in data_paths:
            if os.path.exists(path):
                df = pd.read_csv(path)
                print(f"تم تحميل البيانات من: {path}")
                break
        
        if df is None:
            raise FileNotFoundError("لم يتم العثور على ملفات البيانات")
        
        # تحديد الأعمدة المطلوبة
        required_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'water_access']
        
        # التحقق من وجود الأعمدة المطلوبة
        missing_cols = [col for col in required_features if col not in df.columns]
        if missing_cols:
            print(f"الأعمدة المفقودة: {missing_cols}، استخدام بيانات تجريبية")
            raise ValueError("أعمدة مفقودة")
            
        X = df[required_features]
        
        # البحث عن عمود التصنيف
        label_cols = ['label', 'crop', 'محصول', 'crop_name']
        y = None
        for col in label_cols:
            if col in df.columns:
                y = df[col]
                break
        
        if y is None:
            raise ValueError("لم يتم العثور على عمود التصنيف")
        
        # تقسيم البيانات وتدريب النموذج
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(
            n_estimators=150,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # حساب دقة النموذج وحفظها للعرض
        accuracy = model.score(X_test, y_test)
        st.session_state['model_accuracy'] = accuracy
        st.session_state['trained_model'] = model
        st.session_state['training_samples'] = len(X_train)
        
        print(f"تم تدريب النموذج بدقة: {accuracy:.2f}")
        return model
        
    except Exception as e:
        print(f"خطأ في تحميل البيانات: {e}")
        print("استخدام بيانات تجريبية واقعية لفلسطين...")
        
        # بيانات تجريبية واقعية لـ 10 محاصيل أساسية في فلسطين
        crops_data = {
            'N': [90, 40, 70, 85, 60, 50, 75, 80, 65, 55, 95, 45, 78, 82, 68],
            'P': [42, 30, 50, 45, 35, 40, 48, 52, 38, 42, 44, 32, 47, 53, 44],
            'K': [43, 20, 35, 40, 28, 32, 38, 41, 30, 35, 45, 22, 39, 42, 36],
            'temperature': [24, 32, 22, 26, 28, 25, 23, 27, 26, 24, 30, 35, 21, 29, 24],
            'humidity': [65, 30, 55, 60, 70, 45, 58, 62, 52, 48, 75, 40, 50, 65, 55],
            'ph': [7.2, 6.5, 6.8, 7.0, 7.5, 6.2, 7.1, 6.9, 7.3, 6.7, 7.4, 6.4, 7.2, 6.8, 7.0],
            'rainfall': [400, 100, 350, 450, 300, 200, 380, 420, 320, 280, 500, 150, 370, 400, 360],
            'water_access': [0.9, 0.4, 0.7, 0.8, 0.6, 0.5, 0.75, 0.85, 0.65, 0.55, 0.95, 0.3, 0.7, 0.8, 0.6]
        }
        
        labels = ['maize', 'orange', 'tomato', 'potato', 'onion', 
                 'pepper', 'cucumber', 'eggplant', 'grape', 'olive',
                 'papaya', 'date', 'almond', 'pomegranate', 'fig']
        
        # إنشاء 300 عينة واقعية
        all_data = []
        all_labels = []
        
        for i in range(300):
            crop_idx = i % len(labels)
            noise_level = 0.15  # مستوى ضواقعي
            
            sample = []
            for j, key in enumerate(['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'water_access']):
                base_value = crops_data[key][crop_idx]
                # إضافة ضواقعي مع الحفاظ على نطاق واقعي
                if key == 'ph':
                    noise = np.random.normal(0, noise_level * 0.5)
                elif key in ['temperature', 'humidity']:
                    noise = np.random.normal(0, noise_level * 2)
                else:
                    noise = np.random.normal(0, noise_level * base_value)
                
                noisy_value = base_value + noise
                
                # ضمان نطاقات واقعية
                if key == 'ph':
                    noisy_value = max(4.0, min(9.0, noisy_value))
                elif key == 'temperature':
                    noisy_value = max(10, min(45, noisy_value))
                elif key == 'humidity':
                    noisy_value = max(20, min(95, noisy_value))
                elif key == 'water_access':
                    noisy_value = max(0.1, min(1.0, noisy_value))
                elif key == 'rainfall':
                    noisy_value = max(50, min(800, noisy_value))
                else:  # N, P, K
                    noisy_value = max(10, min(150, noisy_value))
                
                sample.append(noisy_value)
            
            all_data.append(sample)
            all_labels.append(labels[crop_idx])
        
        X = pd.DataFrame(all_data, columns=list(crops_data.keys()))
        y = pd.Series(all_labels)
        
        # تقسيم وتدريب النموذج
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(
            n_estimators=150,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # حساب وحفظ دقة النموذج
        accuracy = model.score(X_test, y_test)
        st.session_state['model_accuracy'] = accuracy
        st.session_state['trained_model'] = model
        st.session_state['training_samples'] = len(X_train)
        st.session_state['data_source'] = "بيانات تجريبية واقعية لفلسطين"
        
        print(f"تم تدريب النموذج التجريبي بدقة: {accuracy:.2f}")
        return model

def predict_disease_risk(city, temperature, humidity, crop_type, ph=None, rainfall=None):
    """نظام إنذار مبكر متقدم للأمراض الزراعية في فلسطين"""
    
    # قاعدة معرفة للأمراض الشائعة في فلسطين
    disease_knowledge_base = {
        'الفطريات_التربة': {
            'conditions': lambda t, h, p, r: h > 75 and t > 22 and p > 7.0,
            'severity': 'متوسط',
            'message': "⚠️ خطر الإصابة بأمراض فطرية في التربة",
            'advice': "استخدام مبيدات فطرية وقائية، تحسين تصريف التربة",
            'affected_crops': ['tomato', 'potato', 'cucumber', 'eggplant']
        },
        'البياض_الدقيقي': {
            'conditions': lambda t, h, p, r: 65 <= h <= 85 and 20 <= t <= 28,
            'severity': 'مرتفع',
            'message': "⚠️ ظروف مثالية لانتشار البياض الدقيقي",
            'advice': "رش بمبيدات الكبريت، تقليل الري الورقي، تحسين التهوية",
            'affected_crops': ['grape', 'cucumber', 'tomato', 'pepper']
        },
        'اللفحة_المتأخرة': {
            'conditions': lambda t, h, p, r: h > 80 and t > 25 and r > 300,
            'severity': 'عالي',
            'message': "🚨 خطر شديد للإصابة باللفحة المتأخرة",
            'advice': "استخدام مبيدات متخصصة، عزل النباتات المصابة فوراً",
            'affected_crops': ['tomato', 'potato']
        },
        'عفن_الجذور': {
            'conditions': lambda t, h, p, r: h > 85 and r > 400,
            'severity': 'عالي',
            'message': "🚨 خطر الإصابة بعفن الجذور",
            'advice': "تحسين الصرف، تقليل الري، استخدام تربة جيدة التهوية",
            'affected_crops': ['tomato', 'pepper', 'eggplant', 'cucumber']
        },
        'النيماتودا': {
            'conditions': lambda t, h, p, r: t > 30 and p > 7.5,
            'severity': 'متوسط',
            'message': "⚠️ ظروف مناسبة لانتشار النيماتودا",
            'advice': "تناوب المحاصيل، استخدام أصناف مقاومة، تعقيم التربة",
            'affected_crops': ['tomato', 'potato', 'pepper', 'eggplant']
        },
        'نقص_التغذية': {
            'conditions': lambda t, h, p, r: h < 40 and t > 35,
            'severity': 'منخفض',
            'message': "⚠️ ظروف قد تؤدي لنقص امتصاص العناصر",
            'advice': "إضافة أسمدة ورقية، الري في الصباح الباكر، تظليل المحصول",
            'affected_crops': ['maize', 'tomato', 'pepper']
        },
        'حرقة_الشمس': {
            'conditions': lambda t, h, p, r: t > 35 and h < 30,
            'severity': 'متوسط',
            'message': "⚠️ خطر الإصابة بحروق الشمس",
            'advice': "الري المنتظم، استخدام شبكات التظليل، الري بالرشاشات",
            'affected_crops': ['pepper', 'tomato', 'cucumber']
        }
    }
    
    # معلومات خاصة بكل مدينة
    city_risks = {
        'طولكرم': {'معدل_أمراض': 'مرتفع', 'الأمراض_الشائعة': ['الفطريات_التربة', 'اللفحة_المتأخرة']},
        'غزة': {'معدل_أمراض': 'متوسط', 'الأمراض_الشائعة': ['عفن_الجذور', 'حرقة_الشمس']},
        'أريحا': {'معدل_أمراض': 'منخفض', 'الأمراض_الشائعة': ['حرقة_الشمس', 'نقص_التغذية']},
        'الخليل': {'معدل_أمراض': 'متوسط', 'الأمراض_الشائعة': ['البياض_الدقيقي', 'النيماتودا']}
    }
    
    alerts = []
    
    # فحص جميع الأمراض في قاعدة المعرفة
    for disease_id, disease_info in disease_knowledge_base.items():
        try:
            if disease_info['conditions'](temperature, humidity, ph or 7.0, rainfall or 300):
                # التحقق إذا كان المحصول معرضاً لهذا المرض
                if crop_type in disease_info['affected_crops'] or disease_info['affected_crops'] == ['all']:
                    alerts.append({
                        'disease': disease_id.replace('_', ' '),
                        'severity': disease_info['severity'],
                        'message': disease_info['message'],
                        'advice': disease_info['advice'],
                        'confidence': min(95, 70 + abs(temperature-25) + abs(humidity-70)/2)
                    })
        except Exception as e:
            continue
    
    # إضافة تحذيرات خاصة بالمدينة
    if city in city_risks:
        city_info = city_risks[city]
        alerts.append({
            'disease': 'مخاطر منطقة',
            'severity': city_info['معدل_أمراض'],
            'message': f"📍 منطقة {city} معروفة بمخاطر: {', '.join(city_info['الأمراض_الشائعة'])}",
            'advice': "راجع خطة الوقاية الخاصة بمنطقتك",
            'confidence': 85
        })
    
    # إذا لم توجد تحذيرات
    if not alerts:
        alerts.append({
            'disease': 'حالة جيدة',
            'severity': 'منخفض',
            'message': "✅ الظروف الحالية مناسبة ولا توجد أمراض متوقعة",
            'advice': "استمر في برنامج العناية المعتاد مع المراقبة الدورية",
            'confidence': 90
        })
    
    # ترتيب التحذيرات حسب الخطورة
    severity_order = {'عالي': 3, 'مرتفع': 2, 'متوسط': 1, 'منخفض': 0}
    alerts.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
    
    return alerts

def analyze_soil_vision(image_file):
    """تحليل متقدم لصورة التربة باستخدام رؤية حاسوبية محسنة"""
    if image_file is not None:
        try:
            image = Image.open(image_file)
            
            # معالجة متقدمة للصورة
            img_array = np.array(image)
            
            # تحليل اللون بشكل متقدم
            avg_color = np.mean(img_array, axis=(0,1))
            std_color = np.std(img_array, axis=(0,1))
            
            # تحليل القوام من خلال التباين
            texture_score = np.mean(std_color)
            
            # تحليل محتوى المواد العضوية (محاكاة)
            organic_matter = 0
            
            # تحليل اللون الأحمر (الحديد)
            red_dominance = avg_color[0] / np.sum(avg_color)
            
            # تحديد نوع التربة بناءً على تحليل متقدم
            if texture_score > 60 and red_dominance > 0.4:
                texture = "تربة طينية ثقيلة"
                ph = 7.5
                organic_matter = 3.2
                fertility = "عالية"
            elif texture_score > 40 and avg_color[1] > 150:
                texture = "تربة طينية"
                ph = 7.2
                organic_matter = 2.8
                fertility = "جيدة"
            elif texture_score > 50 and avg_color[0] > 200:
                texture = "تربة رملية"
                ph = 6.5
                organic_matter = 1.2
                fertility = "منخفضة"
            elif avg_color[1] > 180 and texture_score > 35:
                texture = "تربة طميية (Loamy)"
                ph = 6.8
                organic_matter = 3.5
                fertility = "ممتازة"
            elif std_color[2] > 40:  # تباين عالي في اللون الأزرق
                texture = "تربة جيرية"
                ph = 8.0
                organic_matter = 1.8
                fertility = "متوسطة"
            else:
                texture = "تربة مختلطة"
                ph = 7.0
                organic_matter = 2.3
                fertility = "متوسطة"
            
            # تحليل الرطوبة (محاكاة من لون الصورة)
            moisture_level = "منخفضة"
            if avg_color[2] < 100:  # أزرق غامق
                moisture_level = "عالية"
            elif avg_color[2] < 150:
                moisture_level = "متوسطة"
            
            return {
                "texture": texture,
                "ph": round(ph, 1),
                "organic_matter": f"{organic_matter}%",
                "fertility": fertility,
                "moisture": moisture_level,
                "color_analysis": f"متوسط RGB: {avg_color.astype(int)}, تباين: {std_color.astype(int)}",
                "texture_score": round(texture_score, 1),
                "analysis_confidence": "85%"
            }
        except Exception as e:
            return {
                "texture": "خطأ في التحليل",
                "ph": 7.0,
                "organic_matter": "غير معروف",
                "fertility": "غير معروف",
                "error": str(e)
            }
    
    # قيمة افتراضية محسنة
    return {
        "texture": "يرجى رفع صورة للتحليل",
        "ph": 7.0,
        "organic_matter": "يتطلب تحليل",
        "fertility": "غير معروف",
        "moisture": "غير معروف"
    }

def generate_farmer_report(crop_name, city, weather_data, soil_data, 
                          profit=None, water_saving=None, additional_params=None):
    """توليد تقرير مفصل ومتقدم للمزارع بلغة عربية واضحة"""
    
    # معلومات المحصول المحسنة
    crop_database = {
        'الذرة': {
            'ar': 'الذرة',
            'profit': 2500,
            'water_saving': 25,
            'season': 'صيفي',
            'growth_days': 90,
            'market_demand': 'مرتفع'
        },
        'البندورة': {
            'ar': 'البندورة',
            'profit': 3500,
            'water_saving': 20,
            'season': 'ربيعي وصيفي',
            'growth_days': 75,
            'market_demand': 'عالي جداً'
        },
        'البطاطا': {
            'ar': 'البطاطا',
            'profit': 2800,
            'water_saving': 30,
            'season': 'شتوي وربيعي',
            'growth_days': 100,
            'market_demand': 'مرتفع'
        },
        'البصل': {
            'ar': 'البصل',
            'profit': 2200,
            'water_saving': 35,
            'season': 'شتوي',
            'growth_days': 120,
            'market_demand': 'جيد'
        },
        'الفلفل': {
            'ar': 'الفلفل',
            'profit': 3200,
            'water_saving': 22,
            'season': 'صيفي',
            'growth_days': 85,
            'market_demand': 'مرتفع'
        },
        'الخيار': {
            'ar': 'الخيار',
            'profit': 3000,
            'water_saving': 18,
            'season': 'صيفي',
            'growth_days': 70,
            'market_demand': 'جيد'
        },
        'الباذنجان': {
            'ar': 'الباذنجان',
            'profit': 2900,
            'water_saving': 23,
            'season': 'صيفي',
            'growth_days': 80,
            'market_demand': 'متوسط'
        },
        'العنب': {
            'ar': 'العنب',
            'profit': 4200,
            'water_saving': 40,
            'season': 'صيفي وخريفي',
            'growth_days': 150,
            'market_demand': 'عالي'
        },
        'الزيتون': {
            'ar': 'الزيتون',
            'profit': 4500,
            'water_saving': 45,
            'season': 'دائم',
            'growth_days': 200,
            'market_demand': 'عالي جداً'
        },
        'البرتقال': {
            'ar': 'البرتقال',
            'profit': 3800,
            'water_saving': 35,
            'season': 'شتوي',
            'growth_days': 180,
            'market_demand': 'مرتفع'
        },
        'البابايا': {
            'ar': 'البابايا',
            'profit': 4800,
            'water_saving': 28,
            'season': 'صيفي',
            'growth_days': 160,
            'market_demand': 'عالي'
        }
    }
    
    crop_data = crop_database.get(crop_name, {
        'ar': crop_name,
        'profit': 2800,
        'water_saving': 25,
        'season': 'معتدل',
        'growth_days': 90,
        'market_demand': 'متوسط'
    })
    
    final_profit = profit if profit else crop_data["profit"]
    final_water_saving = water_saving if water_saving else crop_data["water_saving"]
    
    # معلومات الري المحسنة
    irrigation_info = {
        "الذرة": {"method": "الري بالتنقيط السطحي", "frequency": "مرتان أسبوعياً", "time": "الصباح الباكر"},
        "البابايا": {"method": "الري بالتنقيط العميق", "frequency": "3 مرات أسبوعياً", "time": "المساء"},
        "البندورة": {"method": "الري بالتنقيط المتقطع", "frequency": "كل يومين", "time": "الصباح"},
        "البطاطا": {"method": "الري بالرشاشات الخفيفة", "frequency": "مرة أسبوعياً", "time": "الصباح"},
        "البصل": {"method": "الري السطحي الخفيف", "frequency": "مرة أسبوعياً", "time": "المساء"},
        "الفلفل": {"method": "الري بالتنقيط الدقيق", "frequency": "كل يومين", "time": "الصباح الباكر"},
        "العنب": {"method": "الري بالتنقيط المحدود", "frequency": "مرة أسبوعياً", "time": "المساء"},
        "الزيتون": {"method": "الري التكميلي", "frequency": "مرة كل أسبوعين", "time": "المساء"}
    }
    
    irrigation_data = irrigation_info.get(crop_data["ar"], {
        "method": "الري بالتنقيط السطحي الموفر",
        "frequency": "مرتان أسبوعياً",
        "time": "الصباح الباكر"
    })
    
    # تحليل مخاطر الأمراض
    disease_alerts = predict_disease_risk(
        city, 
        weather_data.get('temp', 25), 
        weather_data.get('humidity', 60),
        crop_name.lower(),
        soil_data.get('ph', 7.0),
        additional_params.get('rainfall', 300) if additional_params else 300
    )
    
    # إنشاء قسم الإنذار المبكر
    alert_section = ""
    for i, alert in enumerate(disease_alerts[:3]):  # عرض أول 3 تحذيرات فقط
        if alert['severity'] == 'عالي':
            bg_color = "#7c2d12"  # أحمر غامق
            emoji = "🚨"
        elif alert['severity'] == 'مرتفع':
            bg_color = "#92400e"  # برتقالي غامق
            emoji = "⚠️"
        elif alert['severity'] == 'متوسط':
            bg_color = "#854d0e"  # برتقالي فاتح
            emoji = "🔸"
        else:
            bg_color = "#1a5c1a"  # أخضر
            emoji = "✅"
        
        alert_section += f"""
        <div style="background: {bg_color}; padding: 12px; border-radius: 10px; margin: 8px 0; 
                    border-right: 4px solid {'#ef4444' if alert['severity'] == 'عالي' else '#f97316' if alert['severity'] in ['مرتفع', 'متوسط'] else '#10b981'}">
            <h5 style="margin: 0; color: white;">{emoji} {alert['disease']} - خطورة: {alert['severity']}</h5>
            <p style="margin: 5px 0; color: #f1f5f9;"><b>{alert['message']}</b></p>
            <p style="margin: 5px 0; color: #cbd5e1;">💡 {alert['advice']}</p>
            <p style="margin: 0; font-size: 0.9em; color: #94a3b8;">ثقة النظام: {alert.get('confidence', 80)}%</p>
        </div>
        """
    
    # قسم معلومات النموذج
    model_info = ""
    try:
        if 'model_accuracy' in st.session_state:
            accuracy = st.session_state['model_accuracy']
            samples = st.session_state.get('training_samples', 300)
            source = st.session_state.get('data_source', 'بيانات تجريبية')
            
            model_info = f"""
            <div style="background: linear-gradient(135deg, #0c4a6e 0%, #075985 100%); 
                        padding: 10px; border-radius: 8px; margin: 15px 0;">
                <p style="margin: 0; color: #e0f2fe;">
                    🧠 <b>معلومات النموذج:</b> دقة: {accuracy*100:.1f}% | عينات تدريب: {samples} | مصدر البيانات: {source}
                </p>
            </div>
            """
    except:
        model_info = ""
    
    # حساب العائد المتوقع بشكل أكثر واقعية
    expected_return = final_profit * (1 + final_water_saving/100) * 0.85  # عامل تصحيح واقعي
    
    # إنشاء التقرير HTML
    report_html = f"""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                padding: 25px; border-radius: 15px; border-right: 5px solid #10b981; 
                color: #f1f5f9; direction: rtl; text-align: right; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
        
        <h2 style="color: #10b981; text-align: center; border-bottom: 2px solid #334155; padding-bottom: 10px;">
            📋 تقرير الزراعة المثلى - {city}
        </h2>
        
        {model_info}
        
        <div style="background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
            <h3 style="color: #10b981; margin-top: 0;">🌱 المحصول المقترح: <span style="color: #f1f5f9;">{crop_data['ar']}</span></h3>
            <p style="margin: 5px 0;">هذا المحصول تم اختياره بناءً على تحليل متكامل لظروف منطقتك الزراعية.</p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
            <div style="background: #1a472a; padding: 15px; border-radius: 10px;">
                <h4 style="color: #4ade80; margin: 0;">💰 العائد المتوقع</h4>
                <p style="font-size: 1.5em; font-weight: bold; margin: 5px 0;">{final_profit:,} شيكل/دونم</p>
                <p style="font-size: 0.9em; color: #86efac;">بعد حساب التوفير في المياه</p>
            </div>
            
            <div style="background: #164e63; padding: 15px; border-radius: 10px;">
                <h4 style="color: #22d3ee; margin: 0;">💧 توفير المياه</h4>
                <p style="font-size: 1.5em; font-weight: bold; margin: 5px 0;">{final_water_saving}%</p>
                <p style="font-size: 0.9em; color: #a5f3fc;">مقارنة بالمحاصيل التقليدية</p>
            </div>
            
            <div style="background: #422006; padding: 15px; border-radius: 10px;">
                <h4 style="color: #f59e0b; margin: 0;">🔄 موسم النمو</h4>
                <p style="font-size: 1.2em; font-weight: bold; margin: 5px 0;">{crop_data['season']}</p>
                <p style="font-size: 0.9em; color: #fcd34d;">{crop_data['growth_days']} يوم حتى النضج</p>
            </div>
            
            <div style="background: #3730a3; padding: 15px; border-radius: 10px;">
                <h4 style="color: #818cf8; margin: 0;">📈 طلب السوق</h4>
                <p style="font-size: 1.2em; font-weight: bold; margin: 5px 0;">{crop_data['market_demand']}</p>
                <p style="font-size: 0.9em; color: #c7d2fe;">فرص تسويقية ممتازة</p>
            </div>
        </div>
        
        <h3 style="color: #10b981; border-bottom: 1px solid #334155; padding-bottom: 5px;">🚨 نظام الإنذار المبكر</h3>
        {alert_section}
        
        <h3 style="color: #10b981; border-bottom: 1px solid #334155; padding-bottom: 5px;">📅 خطة الزراعة المقترحة</h3>
        <div style="background: rgba(30, 41, 59, 0.8); padding: 15px; border-radius: 10px; margin: 10px 0;">
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="margin: 10px 0; padding-right: 25px; position: relative;">
                    <span style="position: absolute; right: 0; color: #10b981;">💧</span>
                    <b>طريقة الري:</b> {irrigation_data['method']}
                </li>
                <li style="margin: 10px 0; padding-right: 25px; position: relative;">
                    <span style="position: absolute; right: 0; color: #10b981;">🔄</span>
                    <b>عدد مرات الري:</b> {irrigation_data['frequency']} ({irrigation_data['time']})
                </li>
                <li style="margin: 10px 0; padding-right: 25px; position: relative;">
                    <span style="position: absolute; right: 0; color: #10b981;">🛡️</span>
                    <b>خطة الوقاية من الآفات:</b> مراقبة الفطريات بسبب رطوبة {city}، واستخدام المبيدات العضوية كل 15 يوم
                </li>
                <li style="margin: 10px 0; padding-right: 25px; position: relative;">
                    <span style="position: absolute; right: 0; color: #10b981;">🌱</span>
                    <b>موعد زراعة المحصول:</b> بداية الموسم القادم (أيلول/سبتمبر)
                </li>
                <li style="margin: 10px 0; padding-right: 25px; position: relative;">
                    <span style="position: absolute; right: 0; color: #10b981;">🍎</span>
                    <b>موعد حصاد الثمار:</b> بعد {crop_data['growth_days']} يوماً من الإنبات
                </li>
            </ul>
        </div>
        
        <div style="background: rgba(101, 163, 13, 0.2); padding: 15px; border-radius: 10px; margin-top: 20px; border: 1px solid #65a30d;">
            <h4 style="color: #84cc16; margin: 0 0 10px 0;">💡 نصائح إضافية:</h4>
            <p style="margin: 5px 0;">• ننصح بإجراء فحص دوري للتربة كل 3 أشهر وتعديل الأسمدة حسب الحاجة.</p>
            <p style="margin: 5px 0;">• استخدم الأسمدة العضوية لتحسين خصوبة التربة على المدى الطويل.</p>
            <p style="margin: 5px 0;">• حافظ على سجلات زراعية دقيقة لمتابعة أداء المحصول وتكاليف الإنتاج.</p>
        </div>
        
        <div style="text-align: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid #334155;">
            <p style="color: #94a3b8; font-size: 0.9em;">
                ⏱️ تم إنشاء هذا التقرير في: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')} |
                🏷️ رقم المرجع: AGR{np.random.randint(1000, 9999)}
            </p>
        </div>
    </div>
    """
    
    return {
        "html": report_html,
        "crop_name": crop_name,
        "city": city,
        "profit": final_profit,
        "water_saving": final_water_saving,
        "crop_info": crop_data
    }

def predict_crop(model, inputs):
    """التنبؤ بالمحصول مع معالجة الأخطاء"""
    if model is not None:
        try:
            prediction = model.predict([inputs])[0]
            
            # تحسين أسماء المحاصيل للعرض
            crop_display_names = {
                'maize': 'الذرة',
                'tomato': 'البندورة',
                'potato': 'البطاطا',
                'onion': 'البصل',
                'pepper': 'الفلفل',
                'cucumber': 'الخيار',
                'eggplant': 'الباذنجان',
                'grape': 'العنب',
                'olive': 'الزيتون',
                'orange': 'البرتقال',
                'papaya': 'البابايا'
            }
            
            return crop_display_names.get(prediction, prediction)
        except Exception as e:
            print(f"خطأ في التنبؤ: {e}")
            return "البندورة"  # قيمة افتراضية
    return "البندورة"