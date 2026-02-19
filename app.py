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
    font_path = "arial.ttf"
    if not os.path.exists(font_path):
        st.error("ملف الخط arial.ttf غير موجود! تأكد من رفعه.")
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

    return pdf.output(dest='S').encode('latin-1')

# --- الواجهة ---
st.markdown("<h1 style='text-align: center;'>نظام الرواتب الإلكتروني</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>جامعة ابن سينا</h3>", unsafe_allow_html=True)

st.write("---")
emp_id = st.text_input("أدخل الرقم الوظيفي هنا:", max_chars=10)

if st.button("بحث واستخراج القسيمة"):
    if not emp_id:
        st.warning("الرجاء إدخال الرقم الوظيفي")
    else:
        try:
            # قراءة الملف (تم ضبط المسافات هنا بدقة)
            df = pd.read_excel('salary_data.xlsx')
            
            # تنظيف الرقم الوظيفي
            df['الرقم الوظيفي'] = df['الرقم الوظيفي'].astype(str).str.replace(r'\.0$', '', regex=True)
            
            # البحث
            result = df[df['الرقم الوظيفي'] == emp_id]

            if not result.empty:
                data = result.iloc[0].to_dict()
                st.success(f"تم العثور على الموظف: {data['الاسم']}")
                
                pdf_bytes = create_pdf(data)
                
                if pdf_bytes:
                    st.download_button(
                        label="📄 تحميل قسيمة الراتب (PDF)",
                        data=pdf_bytes,
                        file_name=f"salary_{emp_id}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("رقم وظيفي غير صحيح أو غير موجود")
        
        except FileNotFoundError:
            st.error("ملف البيانات salary_data.xlsx غير موجود")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

