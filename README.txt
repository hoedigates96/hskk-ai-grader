=======================================
HSKK AI口语评分系统 - Kimi完整版
=======================================

【技术架构】
• 语音转文字：讯飞语音听写API（国内，免费额度）
• AI评分：Kimi API（国内，新用户送15元额度）
• 前端：HTML/CSS/JavaScript
• 后端：Python Flask

【文件说明】
├── app.py              # 后端主程序
├── .env                # API密钥配置文件
├── requirements.txt    # Python依赖包列表
├── templates/
│   └── index.html      # 前端页面
└── README.txt          # 本说明文件

【API密钥获取】

1. Kimi API密钥
   - 访问 https://platform.moonshot.cn
   - 注册/登录 → API Key管理 → 创建新密钥
   - 复制 sk- 开头的密钥

2. 讯飞语音API密钥
   - 访问 https://www.xfyun.cn
   - 注册/登录 → 控制台 → 创建应用
   - 获取 APP_ID, API_KEY, API_SECRET
   - 开通"语音听写"服务（有免费额度）

【安装步骤】

1. 确保已安装Python 3.8+

2. 创建虚拟环境
   python -m venv venv

3. 激活虚拟环境
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

4. 安装依赖
   pip install -r requirements.txt

5. 配置API密钥
   打开 .env 文件，填入你的真实密钥

6. 运行网站
   python app.py

7. 打开浏览器访问
   http://127.0.0.1:5000

【功能特性】
✅ HSKK初/中/高级别选择
✅ 30+道预设题目，支持随机换题
✅ 浏览器录音功能（带波形图可视化）
✅ 讯飞语音转文字（国内API，稳定）
✅ Kimi AI智能评分（5维度）
✅ 即时成绩报告
✅ 改进建议与练习指导
✅ 成绩复制分享
✅ 本地历史记录（最多50条）
✅ 历史记录详情查看
✅ 响应式设计，支持手机/平板

【注意事项】
• .env 文件包含敏感信息，请勿上传到公开仓库
• 录音需要浏览器允许麦克风权限
• 讯飞语音有免费额度，超出后需付费
• Kimi新用户送15元额度，约可评分500-1000次
• 历史记录保存在浏览器本地

【技术支持】
如有问题，请检查：
1. API密钥是否正确配置
2. 讯飞应用是否开通了语音听写服务
3. 网络连接是否正常
4. Python版本是否 >= 3.8
