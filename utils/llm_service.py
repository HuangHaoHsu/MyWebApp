"""
大模型通用调用模块 - llm_service.py
支持多种大模型API，只需配置对应的API密钥即可使用
"""
import os
import requests
import json
import random
from functools import lru_cache

# API配置，从环境变量读取以保证安全性
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "")
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY", "")
HUGGINGFACE_MODEL = os.environ.get("HUGGINGFACE_MODEL", "THUDM/chatglm3-6b")

# 备用诗句库，当所有API都不可用时使用
BACKUP_POEMS = {
    "李白": [
        "{mood}如高山流水，意境深远。\n人生得意须尽欢，莫使金樽空对月。\n天生我材必有用，千金散尽还复来。",
        "{mood}似碧空云彩，变幻无常。\n抽刀断水水更流，举杯消愁愁更愁。\n人生如梦，一尊还酹江月。",
        "{mood}如飞花落叶，转瞬即逝。\n行路难，行路难，多歧路，今安在？\n长风破浪会有时，直挂云帆济沧海。"
    ],
    "杜甫": [
        "{mood}如细雨绵绵，润物无声。\n安得广厦千万间，大庇天下寒士俱欢颜。\n会当凌绝顶，一览众山小。",
        "{mood}似江河奔流，不舍昼夜。\n国破山河在，城春草木深。\n穷且益坚，不坠青云之志。",
        "{mood}如冬日暖阳，温暖人心。\n朱门酒肉臭，路有冻死骨。\n岁暮到家未，人间多薄情。"
    ],
    "苏轼": [
        "{mood}如明月清风，超然物外。\n人有悲欢离合，月有阴晴圆缺，此事古难全。\n但愿人长久，千里共婵娟。",
        "{mood}似东坡月色，旷达随和。\n大江东去，浪淘尽，千古风流人物。\n莫听穿林打叶声，何妨吟啸且徐行。",
        "{mood}如赤壁夜游，缥缈如梦。\n竹杖芒鞋轻胜马，谁怕？一蓑烟雨任平生。\n回首向来萧瑟处，归去，也无风雨也无晴。"
    ],
    "李清照": [
        "{mood}如梅花暗香，幽而不失其韵。\n知否？知否？应是绿肥红瘦。\n此情无计可消除，才下眉头，却上心头。",
        "{mood}似昨夜残灯，思绪绵长。\n莫道不消魂，帘卷西风，人比黄花瘦。\n生当作人杰，死亦为鬼雄。",
        "{mood}如雨打芭蕉，声声不息。\n寻寻觅觅，冷冷清清，凄凄惨惨戚戚。\n天不老，情难绝，心似双丝网。"
    ],
    "白居易": [
        "{mood}如庐山烟雨，亦真亦幻。\n离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。\n未觉池塘春草梦，阶前梧叶已秋声。",
        "{mood}似长安古道，沧桑历尽。\n日出江花红胜火，春来江水绿如蓝。\n长恨人心不如水，等闲平地起波澜。",
        "{mood}如细雨湿衣，润物无声。\n同是天涯沦落人，相逢何必曾相识。\n可怜夜半虚前席，不问苍生问鬼神。"
    ]
}


class LLMService:
    """大模型服务类，支持多种API调用方式"""
    
    def __init__(self, api_type="azure_openai"):
        """
        初始化LLM服务
        
        Args:
            api_type: 使用的API类型，支持 'azure_openai', 'openai', 'huggingface'
        """
        self.api_type = api_type
        self.available_apis = self._check_available_apis()
    
    def _check_available_apis(self):
        """检查哪些API可用"""
        available = []
        if AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT:
            available.append("azure_openai")
            print(f"Azure OpenAI API 可用")
        else:
            print(f"Azure OpenAI API 不可用: API密钥或端点未配置")
            
        if OPENAI_API_KEY:
            available.append("openai")
            print(f"OpenAI API 可用, 模型: {OPENAI_MODEL}")
        else:
            print(f"OpenAI API 不可用: API密钥未配置")
            
        if HUGGINGFACE_API_KEY:
            available.append("huggingface")
            print(f"HuggingFace API 可用, 模型: {HUGGINGFACE_MODEL}")
        else:
            print(f"HuggingFace API 不可用: API密钥未配置")
            
        print(f"可用的API: {available}")
        return available
    
    def call_azure_openai(self, prompt, max_tokens=150, temperature=0.7):
        """调用Azure OpenAI API"""
        if "azure_openai" not in self.available_apis:
            return None
            
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY
        }
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        # 使用部署名称构建完整的API URL
        deployment_name = AZURE_OPENAI_DEPLOYMENT_NAME or "gpt-35-turbo"
        api_url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{deployment_name}/chat/completions?api-version=2023-05-15"
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            return None
        except Exception as e:
            print(f"Azure OpenAI API调用失败: {str(e)}")
            return None
    
    def call_openai(self, prompt, max_tokens=150, temperature=0.7):
        """调用OpenAI API"""
        if "openai" not in self.available_apis:
            print(f"OpenAI API不可用，API密钥未配置")
            return None
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        payload = {
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        api_url = "https://api.openai.com/v1/chat/completions"
        
        try:
            print(f"尝试调用OpenAI API，使用模型: {OPENAI_MODEL}")
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)  # 增加超时时间
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"OpenAI API调用失败，状态码: {response.status_code}, 响应: {response.text}")
            return None
        except Exception as e:
            print(f"OpenAI API调用失败: {str(e)}")
            return None
    
    def call_huggingface(self, prompt, max_tokens=150, temperature=0.7):
        """调用HuggingFace API"""
        if "huggingface" not in self.available_apis:
            return None
            
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
        }
        
        # 使用环境变量中配置的模型
        api_url = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and result:
                    return result[0]['generated_text'].replace(prompt, '')
                return None
            return None
        except Exception as e:
            print(f"HuggingFace API调用失败: {str(e)}")
            return None
    
    def get_backup_response(self, poet, mood):
        """获取备用诗句响应"""
        if poet not in BACKUP_POEMS:
            poet = random.choice(list(BACKUP_POEMS.keys()))
        
        poem_template = random.choice(BACKUP_POEMS[poet])
        return poem_template.format(mood=mood)
    
    def generate_poem(self, mood, poet="李白"):
        """生成诗意文字"""
        # 构建提示词
        poets = list(BACKUP_POEMS.keys())
        if poet not in poets:
            poet = random.choice(poets)
        
        prompt = f"请你扮演中国古代诗人{poet}，针对一个人现在的心情是「{mood}」，写一段富有诗意的文字，字数100字左右，要有古典韵味和哲理性。不要解释，直接输出诗意文字。"
        
        print(f"生成诗意文字: 心情 '{mood}', 诗人 '{poet}'")
        
        # 按优先级尝试不同的API
        response = None
        
        if self.api_type == "azure_openai" or not self.api_type:
            print("尝试使用 Azure OpenAI API...")
            response = self.call_azure_openai(prompt)
            if response:
                print("Azure OpenAI API 调用成功")
                return f"【{poet}】\n\n{response}"
            else:
                print("Azure OpenAI API 调用失败")
            
        if self.api_type == "openai" or (not response and "openai" in self.available_apis):
            print("尝试使用 OpenAI API...")
            response = self.call_openai(prompt)
            if response:
                print("OpenAI API 调用成功")
                return f"【{poet}】\n\n{response}"
            else:
                print("OpenAI API 调用失败")
            
        if self.api_type == "huggingface" or (not response and "huggingface" in self.available_apis):
            print("尝试使用 HuggingFace API...")
            response = self.call_huggingface(prompt)
            if response:
                print("HuggingFace API 调用成功")
                return f"【{poet}】\n\n{response}"
            else:
                print("HuggingFace API 调用失败")
        
        # 所有API都失败，使用备用响应
        print("所有API调用失败，使用备用诗句")
        backup = self.get_backup_response(poet, mood)
        return f"【{poet}】\n\n{backup}"


# 使用示例
def get_poem_for_mood(mood, poet="李白", api_type="azure_openai"):
    """获取与心情相关的诗意文字的便捷函数"""
    llm = LLMService(api_type=api_type)
    return llm.generate_poem(mood, poet)
