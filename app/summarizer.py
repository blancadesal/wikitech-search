from newspaper import Article
from transformers import T5ForConditionalGeneration, T5Tokenizer

from app.models.tortoise import TextSummary

async def generate_summary(summary_id: int, url: str) -> None:
    article = Article(url)
    article.download()
    article.parse()
    text = article.text

    # Load the model and tokenizer
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")

    # Generate the summary
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, num_return_sequences=1, length_penalty=2.0)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    await TextSummary.filter(id=summary_id).update(summary=summary)