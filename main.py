"""Main application entry point."""
import sys
from summarizer import NewsSummarizer


def get_article_count():
    """Ask how many articles to process and keep the value between 1 and 10."""
    raw_count = input("How many articles to process? (1-10): ").strip()

    try:
        article_count = int(raw_count)
    except ValueError:
        return 3

    return max(1, min(10, article_count))


def main():
    """Fetch and process news articles."""
    print("=" * 80)
    print("NEWS SUMMARIZER - Multi-Provider Edition")
    print("=" * 80)

    category = input("\nEnter news category (technology/business/health/general): ").strip()
    category = category or "technology"
    num_articles = get_article_count()

    print(f"\nFetching {num_articles} articles from category: {category}")

    try:
        summarizer = NewsSummarizer()
        articles = summarizer.news_api.fetch_top_headlines(
            category=category,
            max_articles=num_articles,
        )

        if not articles:
            print("No articles fetched. Check your News API key or try another category.")
            return

        print(f"\nProcessing {len(articles)} articles...")
        results = summarizer.process_articles(articles)

        if not results:
            print("No articles were processed successfully.")
            return

        summarizer.generate_report(results)
        print("\nProcessing complete!")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
