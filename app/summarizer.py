import nltk
from newspaper import Article

from app.models.tortoise import TextSummary


async def generate_summary(summary_id: int, url: str) -> None:
    article = Article(url)
    article.download()
    article.parse()

    try:
        nltk.data.find("/workspace/app/nltk_data/tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", download_dir="/data/project/fastapi-blueprint/nltk_data")
    finally:
        article.nlp()

    summary = article.summary

    await TextSummary.filter(id=summary_id).update(summary=summary)