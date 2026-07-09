from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

# ========== 语音转文字 ==========
@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': '没有音频文件'}), 400

    audio_file = request.files['audio']

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="zh"
        )

        return jsonify({
            'success': True,
            'text': transcription.text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== AI评分 ==========
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

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是HSKK专业评分考官，严格按官方标准评分。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content
        return jsonify({
            'success': True,
            'grading': json.loads(result)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
