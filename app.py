from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests
import json
import hashlib
import base64
import hmac
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ========== API密钥配置 ==========
KIMI_API_KEY = os.getenv('KIMI_API_KEY')
XUNFEI_APP_ID = os.getenv('XUNFEI_APP_ID')
XUNFEI_API_KEY = os.getenv('XUNFEI_API_KEY')
XUNFEI_API_SECRET = os.getenv('XUNFEI_API_SECRET')

# ========== 扩展题库 ==========
HSKK_QUESTIONS = {
    '初级': [
        '你好，请介绍一下你自己。',
        '你喜欢吃什么？',
        '你家有几口人？',
        '你喜欢什么颜色？',
        '你住在哪里？',
        '你平时喜欢做什么？',
        '请描述一下你的学校或工作。',
        '你喜欢什么运动？'
    ],
    '中级': [
        '请介绍一下你的家乡。',
        '你最喜欢的节日是什么？为什么？',
        '描述一下你的一天。',
        '谈谈你的兴趣爱好。',
        '你认为学习汉语难吗？为什么？',
        '请描述一次难忘的旅行。',
        '你喜欢什么样的电影？为什么？',
        '谈谈你最好的朋友。',
        '你认为网络购物好吗？为什么？',
        '描述一下你喜欢的季节。'
    ],
    '高级': [
        '谈谈你对环境保护的看法。',
        '你认为科技对生活的影响是什么？',
        '描述一个你敬佩的人。',
        '如何看待传统文化与现代生活的关系？',
        '谈谈你对未来职业的规划。',
        '你认为教育最重要的目的是什么？',
        '描述一次你遇到的困难以及如何克服的。',
        '谈谈你对人工智能发展的看法。',
        '你认为健康的生活方式应该包括哪些方面？',
        '描述一个改变你人生观的事件。'
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

# ========== 获取题目 ==========
@app.route('/api/questions/<level>')
def get_questions(level):
    questions = HSKK_QUESTIONS.get(level, [])
    return jsonify({'questions': questions})

# ========== 讯飞语音转文字 ==========
@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': '没有音频文件'}), 400

    audio_file = request.files['audio']

    try:
        # 读取音频文件内容
        audio_file.seek(0)
        audio_data = audio_file.read()

        # 使用讯飞语音听写API
        result = xunfei_asr(audio_data)

        if result and 'data' in result:
            text = result['data']
            return jsonify({
                'success': True,
                'text': text
            })
        else:
            return jsonify({'error': '语音识别失败：' + str(result)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def xunfei_asr(audio_data):
    """讯飞语音听写API"""
    url = "https://iat-api.xfyun.cn/v2/iat"

    # 生成鉴权参数
    date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature_origin = "host: iat-api.xfyun.cn"
date: {}
GET /v2/iat "HTTP/1.1".format(date)
    signature_sha = hmac.new(XUNFEI_API_SECRET.encode('utf-8'), 
                              signature_origin.encode('utf-8'), 
                              hashlib.sha256).digest()
    signature = base64.b64encode(signature_sha).decode('utf-8')
    authorization = f'api_key="{XUNFEI_API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'

    # 构建请求体
    import base64
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    body = {
        "common": {
            "app_id": XUNFEI_APP_ID
        },
        "business": {
            "language": "zh_cn",
            "domain": "iat",
            "accent": "mandarin"
        },
        "data": {
            "status": 2,
            "format": "audio/L16;rate=16000",
            "encoding": "raw",
            "audio": audio_base64
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Date': date,
        'Authorization': authorization
    }

    response = requests.post(url, headers=headers, json=body)
    return response.json()

# ========== Kimi AI评分 ==========
@app.route('/api/grade', methods=['POST'])
def grade_speaking():
    data = request.json
    question = data.get('question')
    answer = data.get('answer')
    level = data.get('level', '中级')

    prompt = f"""你是一位专业的HSKK（汉语水平口语考试）评分考官。

【考试级别】：HSKK{level}
【题目】：{question}
【考生回答】：{answer}

请按以下维度评分（每项满分100分）：
1. 发音准确度（声调、声母、韵母）
2. 语法正确性
3. 词汇运用
4. 流利度
5. 内容完整度

请用JSON格式返回结果：
{{
    "pronunciation": {{"score": 分数, "comment": "评价"}},
    "grammar": {{"score": 分数, "comment": "评价"}},
    "vocabulary": {{"score": 分数, "comment": "评价"}},
    "fluency": {{"score": 分数, "comment": "评价"}},
    "content": {{"score": 分数, "comment": "评价"}},
    "total": 总分,
    "level_assessment": "能否通过该级别",
    "improvements": ["改进点1", "改进点2", "改进点3"],
    "practice_suggestions": "具体练习建议"
}}"""

    headers = {
        'Authorization': f'Bearer {KIMI_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'moonshot-v1-8k',
        'messages': [
            {'role': 'system', 'content': '你是HSKK专业评分考官，严格按官方标准评分。只返回JSON格式结果，不要有任何其他文字。'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.3
    }

    try:
        response = requests.post(
            'https://api.moonshot.cn/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=60
        )
        result = response.json()

        if 'choices' not in result:
            return jsonify({'error': 'Kimi API返回异常：' + str(result)}), 500

        content_text = result['choices'][0]['message']['content']

        # 解析JSON
        try:
            grading = json.loads(content_text)
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
            if json_match:
                grading = json.loads(json_match.group())
            else:
                raise ValueError('返回内容不是JSON格式')

        return jsonify({
            'success': True,
            'grading': grading
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
