"""News summarizer with multi-provider support."""
from news_api import NewsAPI
from llm_providers import LLMProviders


class NewsSummarizer:
    """Summarize news articles using multiple LLM providers."""

    def __init__(self):
        self.news_api = NewsAPI()
        self.llm_providers = LLMProviders()

    def summarize_article(self, article):
        """
        Summarize a single article.

        Args:
            article: Article dictionary

        Returns:
            Dictionary with summary and sentiment
        """
        title = article.get("title") or "Untitled"
        description = article.get("description") or ""
        content = article.get("content") or ""
        source = article.get("source") or "Unknown"
        url = article.get("url") or ""
        published_at = article.get("published_at") or ""

        print(f"\nProcessing: {title[:60]}...")

        article_text = f"""Title: {title}
Description: {description}
Content: {content[:500]}"""

        summary_prompt = f"""Summarize this news article in 2-3 sentences:

{article_text}"""

        # Step 1: Summarize with OpenAI, then fall back to Cohere.
        try:
            print("  -> Summarizing with OpenAI...")
            summary = self.llm_providers.ask_openai(summary_prompt)
            print("  Summary generated")

        except Exception as e:
            print(f"  OpenAI summarization failed: {e}")
            print("  -> Falling back to Cohere for summary...")
            summary = self.llm_providers.ask_cohere(summary_prompt)

        # Step 2: Analyze sentiment with Cohere.
        try:
            print("  -> Analyzing sentiment with Cohere...")
            sentiment_prompt = f"""Analyze the sentiment of this text: "{summary}"

Provide:
- Overall sentiment (positive/negative/neutral)
- Confidence (0-100%)
- Key emotional tone

Be concise (2-3 sentences)."""

            sentiment = self.llm_providers.ask_cohere(sentiment_prompt)
            print("  Sentiment analyzed")

        except Exception as e:
            print(f"  Cohere sentiment analysis failed: {e}")
            sentiment = "Unable to analyze sentiment"

        return {
            "title": title,
            "source": source,
            "url": url,
            "summary": summary,
            "sentiment": sentiment,
            "published_at": published_at,
        }

    def process_articles(self, articles):
        """
        Process multiple articles.

        Args:
            articles: List of article dictionaries

        Returns:
            List of processed articles
        """
        results = []

        for article in articles:
            try:
                result = self.summarize_article(article)
                results.append(result)
            except Exception as e:
                print(f"Failed to process article: {e}")

        return results

    def generate_report(self, results):
        """Generate a summary report."""
        print("\n" + "=" * 80)
        print("NEWS SUMMARY REPORT")
        print("=" * 80)

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   Source: {result['source']} | Published: {result['published_at']}")
            print(f"   URL: {result['url']}")
            print("\n   SUMMARY:")
            print(f"   {result['summary']}")
            print("\n   SENTIMENT:")
            print(f"   {result['sentiment']}")
            print(f"\n   {'-' * 76}")

        summary = self.llm_providers.cost_tracker.get_summary()
        print("\n" + "=" * 80)
        print("COST SUMMARY")
        print("=" * 80)
        print(f"Total requests: {summary['total_requests']}")
        print(f"Total cost: ${summary['total_cost']:.4f}")
        print(f"Total tokens: {summary['total_input_tokens'] + summary['total_output_tokens']:,}")
        print(f"  Input: {summary['total_input_tokens']:,}")
        print(f"  Output: {summary['total_output_tokens']:,}")
        print(f"Average cost per request: ${summary['average_cost']:.6f}")
        print("=" * 80)


if __name__ == "__main__":
    summarizer = NewsSummarizer()

    print("Fetching news articles...")
    articles = summarizer.news_api.fetch_top_headlines(category="technology", max_articles=2)

    if not articles:
        print("No articles fetched. Check your News API key.")
    else:
        print(f"\nProcessing {len(articles)} articles...")
        results = summarizer.process_articles(articles)
        summarizer.generate_report(results)
