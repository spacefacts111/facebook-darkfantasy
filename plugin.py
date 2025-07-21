import os
import time
import random
import requests
import openai
from pytrends.request import TrendReq
from typing import Tuple

# ---- Shared interfaces & data class ----
class ContentItem:
    def __init__(self, *, image_path: str, description: str):
        self.image_path = image_path
        self.description = description

class ContentProvider:
    def get_next_item(self) -> ContentItem:
        raise NotImplementedError

class Captioner:
    def make_caption(self, item: ContentItem) -> Tuple[str, str]:
        raise NotImplementedError

class Poster:
    def publish(self, item: ContentItem, message: str) -> str:
        raise NotImplementedError

# ---- 1) DALL·E Provider with rotating prompts ----
class DalleImageProvider(ContentProvider):
    def __init__(self,
                 prompts: list,
                 n_images: int = 1,
                 size: str = "1024x1024",
                 output_dir: str = "/tmp/dalle_images"):
        """
        prompts: list of text prompts for DALL·E (rotated randomly)
        n_images: number of images per call
        size: one of 256x256, 512x512, 1024x1024
        output_dir: directory to save output images
        """
        self.prompts = prompts
        self.n_images = n_images
        self.size = size
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_next_item(self):
        prompt = random.choice(self.prompts)
        resp = openai.Image.create(
            prompt=prompt,
            n=self.n_images,
            size=self.size
        )
        url = resp['data'][0]['url']
        img_bytes = requests.get(url).content
        fname = f"dalle_{int(time.time())}.png"
        path = os.path.join(self.output_dir, fname)
        with open(path, 'wb') as f:
            f.write(img_bytes)
        return ContentItem(image_path=path, description=prompt)

# ---- 2) Trend‑Aware Captioner ----
class TrendAwareCaptioner(Captioner):
    def __init__(self, gpt_model: str = "gpt-4o-mini", trending_kw_count: int = 3):
        self.gpt_model = gpt_model
        self.trending_kw_count = trending_kw_count
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.pytrends = TrendReq(hl='en-UK', tz=360)

    def _fetch_trending(self):
        trending = self.pytrends.trending_searches(pn='united_kingdom')
        return trending[0:self.trending_kw_count].tolist()

    def make_caption(self, item: ContentItem) -> Tuple[str, str]:
        trending = self._fetch_trending()
        prompt = (
            f"Write an engaging social‑media caption for an image described as: '{item.description}'. "
            f"Mention at least one of these trending topics: {', '.join(trending)}. "
            "Also generate 5 relevant hashtags.\n\n"
            "Format:\nCaption: <text>\nHashtags: <#tag1 #tag2 ...>"
        )
        resp = openai.ChatCompletion.create(
            model=self.gpt_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        text = resp.choices[0].message.content.strip()
        caption = text.split("Hashtags:")[0].replace("Caption:", "").strip()
        hashtags = text.split("Hashtags:")[1].strip()
        return caption, hashtags

# ---- 3) Facebook Poster ----
class FacebookPoster(Poster):
    def __init__(self):
        self.page_id    = os.getenv("FB_PAGE_ID")
        self.page_token = os.getenv("FB_PAGE_TOKEN")

    def publish(self, item: ContentItem, message: str) -> str:
        url = f"https://graph.facebook.com/v17.0/{self.page_id}/photos"
        files = {"source": open(item.image_path, "rb")}
        data = {"caption": message, "access_token": self.page_token}
        r = requests.post(url, files=files, data=data)
        r.raise_for_status()
        return r.json()["id"]
