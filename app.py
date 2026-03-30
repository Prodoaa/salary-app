import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os

# ==========================================
# 1. إعدادات الصفحة الأساسية
# ==========================================
st.set_page_config(
    page_title="بوابة الرواتب | جامعة ابن سينا", 
    page_icon="🏛️", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# ==========================================
# 2. التصميم الاحترافي (CSS) - متضمن حلول الطباعة العمودية
# ==========================================
st.markdown("""
<style>
    /* إخفاء القائمة السفلية والعلوية مع الحفاظ على زر الشريط الجانبي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* ألوان وإعدادات الأزرار والحقول */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        background: linear-gradient(90deg, #0369a1 0%, #075985 100%);
    }

    /* بطاقات المعلومات العلوية */
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    .card-label { color: #64748b; font-size: 15px; font-weight: 600; margin-bottom: 5px; }
    .card-value { color: #1e293b; font-size: 20px; font-weight: bold; }
    .salary-value { color: #059669; font-size: 32px; font-weight: 900; }

    /* =========================================
       إعدادات الطباعة الاحترافية (ورقة واحدة بالطول + إظهار الألوان)
       ========================================= */
    @media print {
        * {
            -webkit-print-color-adjust: exact !important;
            color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        /* جعل الورقة بالطول (Portrait) لتناسب الشكل العمودي */
        @page {
            size: A4 portrait;
            margin: 15mm;
        }
        
        /* إخفاء القوائم والأزرار لتبدو كوثيقة رسمية */
        [data-testid="stSidebar"], header, [data-testid="stForm"], iframe, button { 
            display: none !important; 
        }
        
        .stApp { background: white !important; }
        
        /* منع انقسام البطاقات والجدول بين صفحتين */
        .info-card, .receipt-container, table, tr { 
            page-break-inside: avoid !important; 
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. شريط الإدارة الجانبي
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; direction: rtl;'>⚙️ لوحة التحكم</h2>", unsafe_allow_html=True)
    password = st.text_input("رمز مرور الإدارة:", type="password", key="admin_pass")
    
    if password == "1234":
        st.success("✅ تم الدخول بنجاح")
        uploaded_file = st.file_uploader("📂 رفع ملف الرواتب (Excel):", type=["xlsx", "xls"])
        if uploaded_file is not None:
            with open("salaries.xlsx", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("✨ تم تحديث قاعدة البيانات!")

# ==========================================
# 4. ترويسة النظام
# ==========================================
st.markdown("""
<div style='background: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;'>
    <div style='font-size: 45px; margin-bottom: 10px;'>🏛️</div>
    <h1 style='color: #0f172a; margin: 0; font-size: 34px;'>بوابة الرواتب الإلكترونية</h1>
    <h3 style='color: #475569; margin-top: 5px; font-weight: normal; font-size: 18px;'>جامعة ابن سينا للعلوم الطبية والصيدلانية</h3>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. منطقة البحث الآمنة
# ==========================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<h4 style='text-align: center; color: #334155; direction: rtl; font-weight: bold;'>يرجى إدخال الرقم الوظيفي الخاص بك للاستعلام:</h4>", unsafe_allow_html=True)
    
    with st.form(key='search_form'):
        emp_id = st.text_input("الرقم الوظيفي", placeholder="اكتب الرقم الوظيفي هنا...", label_visibility="collapsed")
        search_button = st.form_submit_button("🔐 عرض كشف الراتب", use_container_width=True)

st.write("---")

# ==========================================
# 6. معالجة البيانات وعرض النتائج
# ==========================================
if search_button:
    if not emp_id.strip():
        st.warning("⚠️ يرجى كتابة الرقم الوظيفي أولاً قبل الضغط على الزر.")
    elif not os.path.exists("salaries.xlsx"):
        st.error("❌ ملف قاعدة البيانات (salaries.xlsx) غير موجود. يرجى رفعه من لوحة التحكم الجانبية.")
    else:
        try:
            df = pd.read_excel("salaries.xlsx")
            
            if 'الرقم الوظيفي' not in df.columns:
                st.error("❌ خطأ في ملف الإكسل: لا يوجد عمود باسم 'الرقم الوظيفي'. يرجى تعديل اسم العمود في الإكسل وإعادة رفعه.")
            else:
                df['الرقم الوظيفي'] = df['الرقم الوظيفي'].astype(str).str.strip()
                search_query = str(emp_id).strip()
                
                user_data = df[df['الرقم الوظيفي'] == search_query]
                
                if not user_data.empty:
                    st.success("✅ تم العثور على البيانات!")
                    row = user_data.iloc[0]
                    
                    st.markdown("<div style='direction: rtl;'>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f'<div class="info-card" style="border-bottom: 4px solid #10b981;"><div class="card-label">الصافي للاستلام</div><div class="salary-value">{row.get("الراتب الصافي بعد الاستقطاعات", "-")} <span style="font-size: 16px; color: #64748b;">د.ع</span></div></div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown(f'<div class="info-card" style="border-bottom: 4px solid #3b82f6;"><div class="card-label">المنصب / اللقب</div><div class="card-value">{row.get("المنصب", "-")} <br> <span style="font-size: 14px; color: #64748b;">{row.get("اللقب العلمي", "-")}</span></div></div>', unsafe_allow_html=True)
                    with c3:
                        st.markdown(f'<div class="info-card" style="border-bottom: 4px solid #6366f1;"><div class="card-label">معلومات الموظف</div><div class="card-value">{row.get("الاسم", "-")} <br> <span style="font-size: 14px; color: #64748b; background: #e2e8f0; padding: 2px 8px; border-radius: 8px;">ID: {row.get("الرقم الوظيفي", "-")}</span></div></div>', unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("<h4 style='text-align: right; color: #1e293b; direction: rtl; margin-top: 20px; font-weight: bold;'>📋 الكشف التفصيلي للمفردات:</h4>", unsafe_allow_html=True)
                    
                    # التصميم العمودي الجديد (شكل وصل) لضمان ملاءمته للطباعة والهاتف
                    html_vertical_table = f"""
                    <div class="receipt-container" style="direction: rtl; background: white; border-radius: 12px; padding: 20px; border: 2px solid #e2e8f0; max-width: 800px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                        <table style="width: 100%; border-collapse: collapse; font-size: 18px;">
                            <tbody>
                                <tr style="border-bottom: 1px solid #f1f5f9;">
                                    <td style="padding: 15px; font-weight: bold; color: #475569; width: 40%;">الراتب الاسمي</td>
                                    <td style="padding: 15px; font-weight: bold; color: #1e293b; text-align: left;">{row.get('الراتب الاسمي', '-')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #f1f5f9;">
                                    <td style="padding: 15px; font-weight: bold; color: #475569;">الخدمة الجامعية</td>
                                    <td style="padding: 15px; font-weight: bold; color: #1e293b; text-align: left;">{row.get('الخدمة الجامعية', '-')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #f1f5f9;">
                                    <td style="padding: 15px; font-weight: bold; color: #475569;">النقل</td>
                                    <td style="padding: 15px; font-weight: bold; color: #1e293b; text-align: left;">{row.get('النقل', '-')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #f1f5f9;">
                                    <td style="padding: 15px; font-weight: bold; color: #475569;">الزوجية</td>
                                    <td style="padding: 15px; font-weight: bold; color: #1e293b; text-align: left;">{row.get('الزوجية', '-')}</td>
                                </tr>
                                <tr style="border-bottom: 2px solid #0284c7; background-color: #f0f9ff;">
                                    <td style="padding: 15px; font-weight: bold; color: #0369a1; font-size: 19px;">الراتب الكامل</td>
                                    <td style="padding: 15px; font-weight: bold; color: #0369a1; text-align: left; font-size: 20px;">{row.get('الراتب الكامل', '-')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #f1f5f9;">
                                    <td style="padding: 15px; font-weight: bold; color: #b91c1c;">التقاعد (استقطاع)</td>
                                    <td style="padding: 15px; font-weight: bold; color: #ef4444; text-align: left;">{row.get('التقاعد', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 15px; font-weight: bold; color: #b91c1c;">الضريبة (استقطاع)</td>
                                    <td style="padding: 15px; font-weight: bold; color: #ef4444; text-align: left;">{row.get('الضريبة', '-')}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    """
                    st.markdown(html_vertical_table, unsafe_allow_html=True)

                    components.html(
                        """
                        <div style="text-align: center; margin-top: 30px;">
                            <button onclick="window.parent.print()" style="background: linear-gradient(90deg, #10b981 0%, #059669 100%); color: white; border-radius: 8px; border: none; padding: 12px 30px; font-size: 18px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);">
                                📥 طباعة / حفظ بصيغة PDF
                            </button>
                        </div>
                        """, height=80
                    )
                else:
                    st.error("❌ لم يتم العثور على موظف بهذا الرقم الوظيفي. تأكد من الرقم وحاول مجدداً.")
                    
        except Exception as e:
            st.error(f"⚠️ حدث خطأ فني أثناء المعالجة. تفاصيل الخطأ: {e}")
