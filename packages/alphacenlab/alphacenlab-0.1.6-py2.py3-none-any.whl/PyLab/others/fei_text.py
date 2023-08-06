import requests


class FeishuAPI():
    def __init__(self,chat_name):
        self.app_id="cli_a274b9f994fc900e"
        self.app_secret="znSyz9exyj5XhvnBU1EhVg7LLWAfOjuo"
        self.chat_name=chat_name
        self.access_token=self.get_access_token()
        self.headers={
            "Authorization": "Bearer {}".format(self.access_token),
            "Content-Type": "application/json"
        }

    # 获取token
    def get_access_token(self):
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        try:
            res = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/", json=data)
            if res.status_code == 200:
                res_json = res.json()
                access_token = res_json.get("tenant_access_token")
                print(access_token)
                return access_token
        except Exception as e:
            return {"error": e}

    # 获取群列表
    def get_chat_list(self):
        params = {
            "page_size": 100,
            "page_token": ""
        }
        try:
            res = requests.get("https://open.feishu.cn/open-apis/chat/v4/list", params=params, headers=self.headers)
            if res.status_code == 200:
                res_json = res.json()
                data = res_json.get("data")
                groups = data.get("groups")
                for i in groups:
                    print(i.get("name"))
                    if i.get("name") == self.chat_name:
                        return i
        except Exception as e:
            return {"error": e}

    def send_msg(self,text):
        res = self.get_chat_list()
        chat_id = res.get("chat_id")

        data = {
            "chat_id": chat_id,
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        try:
            res=requests.post("https://open.feishu.cn/open-apis/message/v4/send/", headers=self.headers,json=data)
            return res.json()
        except Exception as e:
            return {"error":e}

if __name__ == '__main__':
    chat_name="请改成你和机器人的群聊名"
    fei=FeishuAPI(chat_name)
    res=fei.send_msg("Test12飞鸽bot在线播报")
    print(res)
