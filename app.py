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
# 2. التصميم الاحترافي (CSS) - النسخة المدمجة والمخططة
# ==========================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
        color: white; border-radius: 8px; border: none; padding: 8px;
        font-size: 16px; font-weight: bold; transition: all 0.3s ease;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px); background: linear-gradient(90deg, #0369a1 0%, #075985 100%);
    }

    /* بطاقات المعلومات العلوية - مساحة أصغر */
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #cbd5e1;
    }
    .card-label { color: #64748b; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
    .card-value { color: #1e293b; font-size: 16px; font-weight: bold; }
    .salary-value { color: #059669; font-size: 24px; font-weight: 900; }

    /* إعدادات الطباعة */
    @media print {
        * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        @page { size: A4 portrait; margin: 15mm; }
        [data-testid="stSidebar"], header, [data-testid="stForm"], iframe, button { display: none !important; }
        .stApp { background: white !important; }
        .info-card, .receipt-container { page-break-inside: avoid !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. شريط الإدارة الجانبي
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='text-align: center; direction: rtl;'>⚙️ الإدارة</h3>", unsafe_allow_html=True)
    password = st.text_input("رمز المرور:", type="password", key="admin_pass")
    if password == "1234":
        st.success("✅ تم الدخول")
        uploaded_file = st.file_uploader("📂 رفع ملف Excel:", type=["xlsx", "xls"])
        if uploaded_file is not None:
            with open("salaries.xlsx", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("✨ تم التحديث!")

# ==========================================
# 4. ترويسة النظام
# ==========================================
st.markdown("""
<div style='background: white; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 20px; border: 1px solid #cbd5e1;'>
    <h2 style='color: #0f172a; margin: 0;'>🏛️ بوابة الرواتب الإلكترونية</h2>
    <h4 style='color: #475569; margin-top: 5px; font-weight: normal;'>جامعة ابن سينا للعلوم الطبية والصيدلانية</h4>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. منطقة البحث الآمنة
# ==========================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.form(key='search_form'):
        emp_id = st.text_input("الرقم الوظيفي", placeholder="أدخل الرقم الوظيفي هنا...", label_visibility="collapsed")
        search_button = st.form_submit_button("🔐 عرض كشف الراتب", use_container_width=True)

st.write("---")

# ==========================================
# 6. معالجة البيانات وعرض النتائج
# ==========================================
if search_button:
    if not emp_id.strip():
        st.warning("⚠️ يرجى كتابة الرقم الوظيفي أولاً.")
    elif not os.path.exists("salaries.xlsx"):
        st.error("❌ ملف قاعدة البيانات غير موجود.")
    else:
        try:
            df = pd.read_excel("salaries.xlsx")
            if 'الرقم الوظيفي' not in df.columns:
                st.error("❌ لا يوجد عمود باسم 'الرقم الوظيفي'.")
            else:
                df['الرقم الوظيفي'] = df['الرقم الوظيفي'].astype(str).str.strip()
                search_query = str(emp_id).strip()
                user_data = df[df['الرقم الوظيفي'] == search_query]
                
                if not user_data.empty:
                    row = user_data.iloc[0]
                    
                    # البطاقات العلوية المدمجة
                    st.markdown("<div style='direction: rtl;'>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f'<div class="info-card" style="border-top: 3px solid #10b981;"><div class="card-label">الصافي للاستلام</div><div class="salary-value">{row.get("الراتب الصافي بعد الاستقطاعات", "-")} <span style="font-size: 14px; color: #64748b;">د.ع</span></div></div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown(f'<div class="info-card" style="border-top: 3px solid #3b82f6;"><div class="card-label">المنصب / اللقب</div><div class="card-value">{row.get("المنصب", "-")} <br> <span style="font-size: 12px; color: #64748b;">{row.get("اللقب العلمي", "-")}</span></div></div>', unsafe_allow_html=True)
                    with c3:
                        st.markdown(f'<div class="info-card" style="border-top: 3px solid #6366f1;"><div class="card-label">معلومات الموظف</div><div class="card-value">{row.get("الاسم", "-")} <br> <span style="font-size: 12px; color: #64748b; background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">ID: {row.get("الرقم الوظيفي", "-")}</span></div></div>', unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # الجدول المخطط والمدمج (مساحة أصغر وتخطيط واضح)
                    html_compact_table = f"""
                    <div class="receipt-container" style="direction: rtl; background: white; border-radius: 8px; padding: 15px; border: 1px solid #cbd5e1; max-width: 450px; margin: 0 auto; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                        <h4 style="text-align: center; color: #1e293b; margin-top: 0; margin-bottom: 15px; border-bottom: 2px dashed #cbd5e1; padding-bottom: 10px;">🧾 كشف مفردات الراتب</h4>
                        <table style="width: 100%; border-collapse: collapse; font-size: 14px; text-align: right;">
                            <tbody>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; color: #475569; width: 45%; border: 1px solid #cbd5e1; background-color: #f8fafc;">الراتب الاسمي</td>
                                    <td style="padding: 8px; font-weight: bold; color: #1e293b; border: 1px solid #cbd5e1;">{row.get('الراتب الاسمي', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; color: #475569; border: 1px solid #cbd5e1; background-color: #f8fafc;">الخدمة الجامعية</td>
                                    <td style="padding: 8px; font-weight: bold; color: #1e293b; border: 1px solid #cbd5e1;">{row.get('الخدمة الجامعية', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; color: #475569; border: 1px solid #cbd5e1; background-color: #f8fafc;">النقل</td>
                                    <td style="padding: 8px; font-weight: bold; color: #1e293b; border: 1px solid #cbd5e1;">{row.get('النقل', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; color: #475569; border: 1px solid #cbd5e1; background-color: #f8fafc;">الزوجية</td>
                                    <td style="padding: 8px; font-weight: bold; color: #1e293b; border: 1px solid #cbd5e1;">{row.get('الزوجية', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; color: #0369a1; border: 1px solid #93c5fd; background-color: #eff6ff;">الراتب الكامل</td>
                                    <td style="padding: 8px; font-weight: bold; color: #0369a1; border: 1px solid #93c5fd; background-color: #eff6ff;">{row.get('الراتب الكامل', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; color: #b91c1c; border: 1px solid #fca5a5; background-color: #fef2f2;">التقاعد (استقطاع)</td>
                                    <td style="padding: 8px; font-weight: bold; color: #ef4444; border: 1px solid #fca5a5; background-color: #fef2f2;">{row.get('التقاعد', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; color: #b91c1c; border: 1px solid #fca5a5; background-color: #fef2f2;">الضريبة (استقطاع)</td>
                                    <td style="padding: 8px; font-weight: bold; color: #ef4444; border: 1px solid #fca5a5; background-color: #fef2f2;">{row.get('الضريبة', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 10px 8px; font-weight: 900; color: #059669; border: 2px solid #10b981; background-color: #ecfdf5; font-size: 15px;">الصافي للاستلام</td>
                                    <td style="padding: 10px 8px; font-weight: 900; color: #059669; border: 2px solid #10b981; background-color: #ecfdf5; font-size: 16px;">{row.get('الراتب الصافي بعد الاستقطاعات', '-')}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    """
                    st.markdown(html_compact_table, unsafe_allow_html=True)

                    components.html(
                        """
                        <div style="text-align: center; margin-top: 20px;">
                            <button onclick="window.parent.print()" style="background: linear-gradient(90deg, #334155 0%, #0f172a 100%); color: white; border-radius: 6px; border: none; padding: 10px 25px; font-size: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);">
                                🖨️ طباعة الكشف
                            </button>
                        </div>
                        """, height=70
                    )
                else:
                    st.error("❌ لم يتم العثور على موظف بهذا الرقم الوظيفي.")
                    
        except Exception as e:
            st.error(f"⚠️ حدث خطأ فني: {e}")
