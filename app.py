from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# إعداد مفتاح API من متغيرات البيئة
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

# قراءة قاعدة المعرفة
with open('knowledge.txt', 'r', encoding='utf-8') as f:
    knowledge = f.read()

def answer_question(question):
    # التحقق من أن السؤال عن الأكاديمية (بدون كلمات مفتاحية محددة)
    prompt = f"""
    أنت مساعد أكاديمية منة الله لتحفيظ القرآن.
    استخدم المعلومات التالية للإجابة على سؤال المستخدم:

    المعلومات:
    {knowledge}

    السؤال: {question}

    أجب بأسلوب ودود، واضح، ومختصر. استخدم الإيموجي 🎓🌟💚.
    إذا كان السؤال عن الباقات، شجع المستخدم على تجربة الحصة المجانية.
    إذا كان السؤال خارج نطاق الأكاديمية (مثل السياسة، الطب، التكنولوجيا)، قل:
    'أنا مساعد أكاديمية منة الله فقط. أستطيع مساعدتك في أي استفسار عن الباقات، الحصص، التسجيل، أو الحصة التجريبية المجانية.'
    """
    
    response = model.generate_content(prompt)
    return response.text

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    answer = answer_question(question)
    return jsonify({'answer': answer})

@app.route('/')
def home():
    return "مرحباً بك في أكاديمية منة الله 🤖"

if __name__ == '__main__':
    app.run(debug=True)