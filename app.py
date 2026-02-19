import streamlit as st
import pandas as pd
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import os

# --- إعداد الصفحة ---
st.set_page_config(page_title="نظام الرواتب", layout="centered")

# --- دالة معالجة النص العربي ---
def fix_text(text):
    if pd.isna(text): return ""
    text = str(text)
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text, base_dir='R')

# --- دالة إنشاء PDF ---
def create_pdf(data_row):
    # الخط سيكون مرفوعاً بجانب الكود
    font_path = "arial.ttf" 
    
    # التحقق من وجود الخط
    if not os.path.exists(font_path):
        st.error("ملف الخط arial.ttf غير موجود! تأكد من رفعه مع الملفات.")
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArabicFont', '', font_path, uni=True)

    # العنوان
    pdf.set_font('ArabicFont', '', 16)
    title = fix_text("شعبة المالية / جامعة ابن سينا للعلوم الطبية والصيدلانية")
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.line(10, 20, 200, 20)
    pdf.ln(10)

    # المعلومات
    pdf.set_font('ArabicFont', '', 14)
    pdf.cell(0, 8, txt=fix_text(f"الاسم : {data_row['الاسم']}"), ln=1, align='R')
    pdf.cell(0, 8, txt=fix_text(f"الرقم الوظيفي : {data_row['الرقم الوظيفي']}"), ln=1, align='R')
    pdf.ln(5)

    # الجدول
    cols = [
        'الراتب الاسمي', 'الخدمة الجامعية', 'اللقب العلمي', 
        'التقاعد', 'الضريبة', 'النقل', 'المنصب', 'الزوجية', 
        'الراتب الكامل', 'الراتب الصافي بعد الاستقطاعات'
    ]

    for col in cols:
        val = data_row.get(col, "0")
        text = fix_text(f"{col} : {val}")
        pdf.set_fill_color(245, 245, 245)
        pdf.cell(0, 10, txt=text, ln=1, align='R', fill=True, border=0)

    pdf.ln(20)
    pdf.set_font('ArabicFont', '', 12)
    footer = fix_text("توقيع المدير المالي: __________________")
    pdf.cell(0, 10, txt=footer, ln=1, align='L')

    # إرجاع محتوى الملف كـ bytes
    return pdf.output(dest='S').encode('latin-1')

# --- الواجهة ---
st.title("نظام الرواتب - جامعة ابن سينا")
st.write("أدخل الرقم الوظيفي لتحميل قسيمة الراتب")

emp_id = st.text_input("الرقم الوظيفي", max_chars=10)

if st.button("بحث"):
    if not emp_id:
        st.warning("الرجاء كتابة الرقم الوظيفي")
    else:
        try:
            # قراءة ملف الإكسل المرفوع
           df = pd.read_excel('salary_data.xlsx', engine='openpyxl')
            
            # تنظيف الرقم الوظيفي
            df['الرقم الوظيفي'] = df['الرقم الوظيفي'].astype(str).str.replace(r'\.0$', '', regex=True)
            
            result = df[df['الرقم الوظيفي'] == emp_id]

            if not result.empty:
                data = result.iloc[0].to_dict()
                st.success(f"مرحباً: {data['الاسم']}")
                
                pdf_bytes = create_pdf(data)
                if pdf_bytes:
                    st.download_button(
                        label="📥 تحميل القسيمة (PDF)",
                        data=pdf_bytes,
                        file_name=f"Salary_{emp_id}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("رقم وظيفي غير صحيح")
        except FileNotFoundError:
            st.error("ملف البيانات غير موجود")
        except Exception as e:

            st.error(f"حدث خطأ: {e}")
