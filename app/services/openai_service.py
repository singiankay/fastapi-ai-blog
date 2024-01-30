from app.services.main import AppService
from app.config.settings import settings
from openai import OpenAI


class OpenAIService(AppService):
    def __init__(
        self,
        key=settings.openai_api_key,
        model='gpt-3.5-turbo'
    ):
        self.key = key if key is not None else settings.openai_api_key
        self.model = model if model is not None else 'gpt-3.5-turbo'
        self.run_client()

    def run_client(self):
        if not hasattr(self, "client"):
            self.client = OpenAI(
                api_key=self.key
            )

    async def generate_content(self, title):
        system = "You are a content writer assistant. " \
            "You should generate content based on the topic " \
            "provided with a maximum of 100 words."
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": f"Write a content for the topic: {title}"
                }
            ],
            max_tokens=250
        )

        # return json.loads(response.choices[0].message.content)
        return response.choices[0].message.content

    async def rate_content(self, title, content):
        system = "You are an article analyst. " \
            "You should give a rating based on affinity of title" \
            "and the quality of the content" \
            "from 1 as the lowest, to 10 as the highest"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": "Give a rating for the following "
                    "'title: Garden, Content: Nestled between vibrant "
                    "blossoms and lush greenery, the garden emanates a "
                    "symphony of colors and fragrances, inviting visitors "
                    "into a tranquil sanctuary.'"
                },
                {
                    "role": "assistant",
                    "content": "7"
                },
                {
                    "role": "user",
                    "content": "Give a rating for the following "
                    "'title: House, Content: I have a very big house. "
                    "I live at my house. I eat and sleep at my house.'"
                },
                {
                    "role": "assistant",
                    "content": "2"
                },
                {
                    "role": "user",
                    "content": "Give a rating for the following "
                    f"'Title: {title}, Content: {content}'"
                }
            ],
            max_tokens=1000
        )

        return int(response.choices[0].message.content)
