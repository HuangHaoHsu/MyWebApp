from flask import Flask, render_template, request
import random
import os
from dotenv import load_dotenv
from utils.llm_service import get_poem_for_mood

# 加载环境变量，从.env文件
load_dotenv()

app = Flask(__name__)

def generate_poem(mood, poet="李白"):
    """生成诗意文字，会尝试使用已配置的API，如未配置则使用备用诗句"""
    if not mood or mood.strip() == "":
        moods = ["喜悦", "忧伤", "思念", "孤独", "迷茫", "希望", "憧憬"]
        mood = random.choice(moods)
    
    # 选择要模拟的诗人，如未指定则随机选择
    poets = ["李白", "杜甫", "苏轼", "白居易", "李清照"]
    if poet not in poets:
        poet = random.choice(poets)
    
    # 使用LLM服务生成诗句
    # 可以通过修改api_type参数选择不同的API: "azure_openai", "openai", "huggingface"
    return get_poem_for_mood(mood, poet, api_type="azure_openai")

@app.route('/', methods=['GET', 'POST'])
def index():
    poem = None
    if request.method == 'POST':
        mood = request.form.get('mood', '')
        poem = generate_poem(mood)
    return render_template('index.html', poem=poem)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    poem = None
    if request.method == 'POST':
        mood = request.form.get('mood', '')
        poem = generate_poem(mood)
    return render_template('index.html', poem=poem)

if __name__ == '__main__':
    app.run(debug=True)
