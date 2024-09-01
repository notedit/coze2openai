import asyncio
import requests
import json
from typing import List, Dict, AsyncGenerator, Optional
from sseclient import SSEClient
from concurrent.futures import ThreadPoolExecutor

class AsyncCozeClient:
    def __init__(self, api_key: str, bot_id: str, user_id: str):
        self.api_key = api_key
        self.bot_id = bot_id
        self.user_id = user_id
        self.base_url = "https://api.coze.cn/v3/chat"
        self.conversation_url = "https://api.coze.cn/v1/conversation/create"
        self.session = requests.Session()
        

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.executor.shutdown(wait=False)

    def _prepare_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        return [
            {
                "role": msg["role"],
                "content": msg["content"],
                "content_type": "text"
            }
            for msg in messages
        ]

    async def create_conversation(self, uuid: Optional[str] = None) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {}
        if uuid:
            data["meta_data"] = {"uuid": uuid}

        response = self.session.post(self.conversation_url, headers=headers, json=data)
        response_data = response.json()
        if response_data["code"] != 0:
            raise Exception(f"Failed to create conversation: {response_data['msg']}")
        return response_data["data"]

    async def chat_completion_stream(
        self, 
        messages: List[Dict[str, str]], 
        conversation_id: Optional[str] = None
    ) -> AsyncGenerator[Dict, None]:
        url = self.base_url
        if conversation_id:
            url += f"?conversation_id={conversation_id}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "bot_id": self.bot_id,
            "user_id": self.user_id,
            "stream": True,
            "auto_save_history": True,
            "additional_messages": self._prepare_messages(messages)
        }
        
        response = self.session.post(url, headers=headers, json=data, stream=True)
        client = SSEClient(response)
        for event in client.events():
            if event.event == 'conversation.message.delta':
                data = json.loads(event.data)
                content = data.get('content', '')
                yield {
                    "choices": [
                        {
                            "delta": {
                                "content": content
                            },
                            "finish_reason": None
                        }
                    ]
                }
            elif event.event == 'done':
                yield {
                    "choices": [
                        {
                            "delta": {},
                            "finish_reason": "stop"
                        }
                    ]
                }
                break