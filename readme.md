# Railway‑Deployed Facebook Bot (Dark Fantasy / Trippy / Psychedelic / Spacey)

This repo contains a fully automated bot that:
1. Randomly generates dark‑fantasy / trippy / psychedelic / spacey images via DALL·E
2. Crafts captions & hashtags based on Google Trends + GPT
3. Posts to your Facebook Page daily

## Setup

1. **Environment Variables** (on Railway Settings → Variables):
   - `OPENAI_API_KEY`
   - `FB_PAGE_ID`
   - `FB_PAGE_TOKEN`

2. **Deploy**
   - Connect this repo to Railway
   - In **Plugins → Scheduled Jobs**, add a job:
     ```
     Command: python main.py
     Schedule: 0 8 * * *   # runs at 09:00 BST
     ```

3. **Enjoy**! Each run uses a fresh, rotating prompt for a vibrant, otherworldly feed.
