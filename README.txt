=======================================
HSKK AI口语评分系统 - 完整版
=======================================

【文件说明】
├── app.py              # 后端主程序（Flask）
├── .env                # API密钥配置文件
├── requirements.txt    # Python依赖包列表
├── templates/
│   └── index.html      # 前端页面
└── README.txt          # 本说明文件

【安装步骤】

1. 确保已安装Python 3.8+
   检查方法：cmd中输入 python --version

2. 创建虚拟环境
   python -m venv venv

3. 激活虚拟环境
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

4. 安装依赖
   pip install -r requirements.txt

5. 配置API密钥
   打开 .env 文件，将 sk-你的OpenAI密钥 替换为你的真实密钥
   获取方法：访问 https://platform.openai.com → API keys → Create new secret key

6. 运行网站
   python app.py

7. 打开浏览器访问
   http://127.0.0.1:5000

【功能特性】
✅ HSKK初/中/高级别选择
✅ 30+道预设题目，支持随机换题
✅ 浏览器录音功能（带波形图可视化）
✅ 手动输入答案
✅ AI语音转文字（Whisper）
✅ AI智能评分（5维度）
✅ 即时成绩报告
✅ 改进建议与练习指导
✅ 成绩复制分享
✅ 本地历史记录（最多50条）
✅ 历史记录详情查看
✅ 响应式设计，支持手机/平板

【注意事项】
• .env 文件包含敏感信息，请勿上传到公开仓库
• 录音需要浏览器允许麦克风权限
• 首次使用需要OpenAI API密钥（新用户送$5额度）
• 历史记录保存在浏览器本地，清除浏览器数据会丢失

【技术支持】
如有问题，请检查：
1. Python版本是否 >= 3.8
2. 虚拟环境是否已激活（cmd前面有(venv)）
3. API密钥是否正确配置
4. 网络连接是否正常
