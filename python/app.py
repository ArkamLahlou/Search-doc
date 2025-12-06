import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# مفاتيحك التي تم توفيرها:
# ملاحظة: تم استخراج API Key و CX ID من المعلومات التي أرسلتها.
API_KEY = "AIzaSyDNpQV-_82Pz5Ymuu-P5DTyKvec-VFKI8U"
CX_ID = "846588cfb56ba49d6"
SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

@app.route('/search', methods=['GET'])
def custom_search():
    query = request.args.get('q') # الحصول على استعلام البحث من الواجهة الأمامية
    
    if not query:
        return jsonify({"error": "الرجاء إدخال استعلام بحث."}), 400

    params = {
        'key': API_KEY,
        'cx': CX_ID,
        'q': query,
        'num': 10 # عدد النتائج المطلوبة (يمكنك تغييرها)
    }

    # إرسال الطلب إلى جوجل
    response = requests.get(SEARCH_URL, params=params)
    
    if response.status_code != 200:
        # إذا فشل الاتصال، قد يكون المفتاح غير مفعل أو يوجد خطأ في الإعدادات
        return jsonify({"error": f"حدث خطأ في الاتصال بواجهة جوجل. رمز الخطأ: {response.status_code}"}), 500

    data = response.json()
    
    # استخلاص النتائج المطلوبة
    results = []
    if 'items' in data:
        for item in data['items']:
            results.append({
                'title': item.get('title'),
                'snippet': item.get('snippet'), # الملخص
                'url': item.get('link')
            })

    return jsonify(results)

if __name__ == '__main__':
    # تأكد من تثبيت Flask و requests: pip install flask requests
    app.run(debug=True)
