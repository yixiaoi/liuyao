# ai_yongshen.py
import os
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置 DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"

def ask_deepseek_for_yongshen(gua_data,question):
    with open('python/prompt/yongshen_rules.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    user_prompt = f"""请根据以下六爻排盘信息，判断哪个爻为用神，并说明理由：

    
卦象数据如下：
{gua_data}
问题：
{question}

请严格返回 JSON 格式，例如：
{{
  "用神": {{
    "爻位": "三爻",
    "index": 3,
    "六亲": "官鬼",
    "五行": "火",
    "理由": "因为问题与求职相关，官鬼代表事业，是用神"
  }}
}}"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.3
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # 检查HTTP错误
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except Exception as e:
        print(f"DeepSeek API 请求失败: {str(e)}")
        print(f"响应状态码: {response.status_code if 'response' in locals() else '无响应'}")
        return None

def parse_yongshen_response(response):
    if response is None:
        print("未收到有效响应")
        return None
        
    try:
        data = json.loads(response)
        return data.get("用神")
    except json.JSONDecodeError:
        print("AI 返回结果不是有效 JSON，请手动检查")
        print(f"原始响应: {response}")
        return None

def add_yongshen_to_gua(gua_data, yongshen):
    if not yongshen:
        return gua_data
    
    for line in gua_data["lines"]:
        if line["index"] == yongshen["index"]:
            line["is_yongshen"] = True
        else:
            line["is_yongshen"] = False
    
    return gua_data