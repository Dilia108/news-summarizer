# API and Integration Patterns Lab

## Project Overview
This project is a **News Summarizer** that combines a News API with two LLM providers: **OpenAI** and **Cohere**. The application fetches recent news articles by category, summarizes each article using OpenAI, and then analyzes the sentiment of the generated summary using Cohere.

The project also includes fallback logic. If OpenAI fails during summarization, the application falls back to Cohere so the article can still be processed. Each LLM request is tracked using a cost tracker, which calculates the estimated cost based on input and output tokens.

## How to Run the Project

=> main.py

The application fetches the articles, summarizes them, analyzes sentiment, and prints a report.

## Example output

1. Example Technology Article
   Source: Example News | Published: 2026-01-19
   URL: https://example.com/article

   SUMMARY:
   This article discusses recent developments in technology. It explains the main event and its possible impact on users and companies.

   SENTIMENT:
   The sentiment is neutral to positive. The tone is informative, with moderate confidence.

COST SUMMARY:
* Total requests: 4
* Total cost: $0.0004
* Total tokens: 1,200
*   Input: 900
*   Output: 300
* Average cost per request: $0.000100

## Cost Analysis
The project includes a CostTracker class that estimates the cost of each LLM request. Costs are calculated using the number of input and output tokens and the pricing configured in llm_providers.py.
For each article, the application normally makes two LLM requests:
* -> 1 request to OpenAI for summarization
* -> 1 request to Cohere for sentiment analysis

Therefore, processing 2 articles normally results in 4 LLM requests. The final report displays the total number of requests, total estimated cost, total input and output tokens, and average cost per request.

The project also includes a daily budget setting through DAILY_BUDGET, with a default value of $5.00. If the estimated cost reaches or exceeds the budget, the application raises an exception to prevent further spending.




