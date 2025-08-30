from flask import Flask, render_template, request
import requests
import json
import random

app = Flask(__name__)

def generate_poem(mood, poet="李白"):
    # 使用HuggingFace免费API生成诗意文字
    API_URL = "https://api-inference.huggingface.co/models/THUDM/chatglm3-6b"
    
    # 构建提示词
    poets = ["李白", "杜甫", "苏轼", "白居易", "李清照"]
    poet = random.choice(poets) if poet == "李白" else poet
    
    prompt = f"请你扮演中国古代诗人{poet}，针对一个人现在的心情是「{mood}」，写一段富有诗意的文字，字数100字左右，要有古典韵味和哲理性。"
    
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        # 发送请求到HuggingFace
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                return f"【{poet}】\n\n{result[0]['generated_text'].replace(prompt, '')}"
            return f"【{poet}】\n\n无法理解你的心情，再试一次吧。"
        else:
            # 如果API调用失败，返回备用生成内容
            backup_poems = [
                f"【{poet}】\n\n{mood}如溪水潺潺，时而欢快，时而低沉。\n我心如山间竹，虽经风雨，依然傲然挺立。\n一叶一菩提，一花一世界，心念所至，皆是诗意。",
                f"【{poet}】\n\n{mood}似江南烟雨，轻盈而又深沉。\n人生如棋，落子无悔，静待山长水远。\n且将诗酒趁年华，莫负好时光。",
                f"【{poet}】\n\n{mood}犹如夜空繁星，看似散乱，实则有序。\n心有所念，便有所得；心有所安，便有所适。\n且行且珍惜，莫负韶华。"
            ]
            return random.choice(backup_poems)
    except Exception as e:
        # 异常处理，返回错误信息
        return f"【{poet}】\n\n{mood}如天边云彩，变幻莫测。\n人生不过是一场梦，何必执着于一时一事。\n顺其自然，随心而行，自在逍遥。"

@app.route('/', methods=['GET', 'POST'])
def index():
    poem = None
    if request.method == 'POST':
        mood = request.form.get('mood', '')
        poem = generate_poem(mood)
    return render_template('index.html', poem=poem)

if __name__ == '__main__':
    app.run(debug=True)
