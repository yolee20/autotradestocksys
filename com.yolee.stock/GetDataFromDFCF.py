import requests
import json

url = "https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid=1.600839&klt=101&fqt=1&cb=jsonp1731769339315"

try:
    response = requests.get(url)
    if response.status_code == 200:
        # 判断是否是JSONP格式（依据URL中含cb参数推测可能是）
        if 'cb' in url and response.text.startswith("jsonp") and response.text.endswith(");"):
            # 去除JSONP的函数包装部分，提取真正的JSON字符串
            json_str = response.text[response.text.find("(") + 1: -2]
            result = json.loads(json_str)
        else:
            # 若本身就是常规JSON格式，直接解析
            result = response.json()
        # 此时result就是解析为Python数据结构（如字典、列表等）的结果
        # 你可以根据需求对解析后的结果进行操作，以下是将其重新转换为JSON格式字符串示例
        json_result = json.dumps(result, indent=4, ensure_ascii=False)
        print(json_result)
    else:
        print(f"请求失败，状态码: {response.status_code}")
except requests.RequestException as e:
    print(f"请求发生异常: {e}")