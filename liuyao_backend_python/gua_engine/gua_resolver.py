import os
import requests
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置 DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"

def gua_resolver(gua_data, question):
    system_prompt = "你是一个专业的六爻预测分析师。请根据提供的卦象数据进行详细分析。"
    
    user_prompt = f"""请根据以下六爻排盘信息进行专业分析：

卦象数据：
{gua_data}

问题：
{question}

请提供全面的卦象分析。"""

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
        "temperature": 0.3  # 移除了 response_format 参数
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        # 详细打印错误信息
        if response.status_code != 200:
            print(f"API错误: {response.status_code} - {response.text}")
            return None
            
        response.raise_for_status()
        response_data = response.json()
        
        if "choices" in response_data and response_data["choices"]:
            return response_data['choices'][0]['message']['content']
        else:
            print("API响应格式异常:", response_data)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"错误详情: {e.response.status_code} - {e.response.text}")
    except json.JSONDecodeError:
        print("API响应JSON解析失败")
    except KeyError:
        print("API响应结构异常")
    except Exception as e:
        print(f"未预期错误: {str(e)}")
    
    return None