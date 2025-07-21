# Choose your rotating DALL·E prompts — all rooted in dark fantasy with fresh trippy/psychedelic/spacey twists
PROVIDER        = "DalleImageProvider"
PROVIDER_ARGS   = {
    "prompts": [
        "An ominous dark fantasy world rich with mountain ranges, bathed in psychedelic auroras",
        "A shadowy dark fantasy village",
        "A haunted forest of twisted black trees with luminescent mushrooms under a swirling galaxy",
        "Dark knights in ethereal armor wandering a floating labyrinth of swirling fractal portals",
        "A colossal ancient rune circle dripping with starlight in a ghostly, psychedelic wasteland"
    ]
}

CAPTIONER       = "TrendAwareCaptioner"
CAPTIONER_ARGS  = {"gpt_model": "gpt-4o-mini", "trending_kw_count": 3}

POSTER          = "FacebookPoster"
POSTER_ARGS     = {}  # uses FB_PAGE_ID & FB_PAGE_TOKEN env vars
