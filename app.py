from flask import Flask, render_template, request

app = Flask(__name__)

def generate_poem(mood, poet="李白"):
    # TODO: 调用大模型API，返回诗意文字
    # 这里只做占位，后续可接入OpenAI/HuggingFace等
    return f"{poet}：\n你此刻的心情是『{mood}』，\n仿佛江水东流，诗意无穷。\n（此处为大模型生成内容占位）"

@app.route('/', methods=['GET', 'POST'])
def index():
    poem = None
    if request.method == 'POST':
        mood = request.form.get('mood', '')
        poem = generate_poem(mood)
    return render_template('index.html', poem=poem)

if __name__ == '__main__':
    app.run(debug=True)
