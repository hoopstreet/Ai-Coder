# Hugging Face Space Dockerfile
# This file is auto-updated by GitHub Actions
# The TAG_VERSION is replaced during build

ARG TAG_VERSION=latest
FROM hoopstreet/tiktok-prompt-generator:${TAG_VERSION}

# Hugging Face Space metadata
LABEL name="TikTok Prompt Generator"
LABEL version="${TAG_VERSION}"
LABEL description="AI-Powered TikTok Affiliate Content Generator"

EXPOSE 7860

CMD ["python", "app.py"]
