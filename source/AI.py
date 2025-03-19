from openai import OpenAI
import json
from settings import prompt
import os
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv("AI_BASE_URL")
api_key = os.getenv("AI_API_KEY")
prompt = prompt


class Gpt:
    def __init__(
            self,
            base_url: str,
            api_key: str,
            prompt: str,
            model: str = 'openai/gpt-4o-mini',
            temperature: float = 0.7,
            presence_penalty: float = -1.0,
            frequency_penalty: float = 0.0,
            max_history_length: int = 10,
    ):
        self.conversation_history = [{"role": "system", "content": prompt}]
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.max_history = max_history_length

        self.conversation_history = [{"role": "system", "content": prompt}]

    def response(self, message):
        try:
            self.conversation_history.extend(message)
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-(self.max_history - 1):]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=self.temperature,
                presence_penalty=self.presence_penalty,
                frequency_penalty=self.frequency_penalty,
                )
            reply = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply

        except Exception as e:
            print(f'!!! API AI !!! Error: {str(e)}')
            return None


if __name__ == '__main__':
    a = Gpt(base_url, api_key, prompt)
    print(a.response('что надо?'))

