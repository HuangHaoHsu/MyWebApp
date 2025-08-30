from flask import Flask, render_template, request
import random
import os
import logging
from dotenv import load_dotenv
from utils.llm_service import get_poem_for_mood

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量，从.env文件
load_dotenv()
logger.info("环境变量已加载")

# 打印环境变量状态（不打印敏感信息）
if os.environ.get("OPENAI_API_KEY"):
    logger.info("OPENAI_API_KEY 已配置")
else:
    logger.info("OPENAI_API_KEY 未配置")

if os.environ.get("AZURE_OPENAI_API_KEY") and os.environ.get("AZURE_OPENAI_ENDPOINT"):
    logger.info("Azure OpenAI API 已配置")
else:
    logger.info("Azure OpenAI API 未配置或配置不完整")

if os.environ.get("HUGGINGFACE_API_KEY"):
    logger.info("HUGGINGFACE_API_KEY 已配置")
else:
    logger.info("HUGGINGFACE_API_KEY 未配置")

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
    
    logger.info(f"生成诗意文字: 心情='{mood}', 诗人='{poet}'")
    
    # 可以通过修改api_type参数选择不同的API: "azure_openai", "openai", "huggingface"
    # 默认情况下会按照优先级依次尝试: azure_openai > openai > huggingface
    poem = get_poem_for_mood(mood, poet, api_type="")
    logger.info("诗意文字生成完成")
    return poem

@app.route('/', methods=['GET', 'POST'])
def index():
    poem = None
    if request.method == 'POST':
        mood = request.form.get('mood', '')
        logger.info(f"用户提交心情: '{mood}'")
        poem = generate_poem(mood)
    return render_template('index.html', poem=poem)

# 添加一个用于测试API连接的路由
@app.route('/api-test', methods=['GET'])
def api_test():
    """测试各种API连接状态"""
    from utils.llm_service import LLMService
    llm = LLMService()
    available_apis = llm.available_apis
    
    results = {
        "available_apis": available_apis,
        "env_vars": {
            "OPENAI_MODEL": os.environ.get("OPENAI_MODEL", "未设置"),
            "AZURE_OPENAI_DEPLOYMENT_NAME": os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "未设置"),
            "HUGGINGFACE_MODEL": os.environ.get("HUGGINGFACE_MODEL", "未设置"),
        }
    }
    
    return results

if __name__ == '__main__':
    app.run(debug=True)
