import os, requests, datetime

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=3"
data = requests.get(url).json()

videos = []
for item in data["items"]:
    if item["id"]["kind"] == "youtube#video":
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        published = item["snippet"]["publishedAt"][:10]
        thumb = f"https://img.youtube.com/vi/{video_id}/0.jpg"
        link = f"https://www.youtube.com/watch?v={video_id}"
        videos.append(f"""
<p align="center">
  <a href="{link}" target="_blank">
    <img src="{thumb}" width="250" /><br>
    <b>{title}</b><br>
    {published}
  </a>
</p>
""")

# Update README.md
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start = "<!-- YOUTUBE:START -->"
end = "<!-- YOUTUBE:END -->"
new_section = start + "".join(videos) + end

import re
readme = re.sub(f"{start}.*{end}", new_section, readme, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
