import sys
import os
import re
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup

load_dotenv()

ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

sentiment_analyzer = SentimentIntensityAnalyzer()


def main():
    if not ALPHA_VANTAGE_KEY or not NEWS_API_KEY:
        print("Error: API keys not found!")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("\n📊 Stock Sentiment Analyzer")
        print("\nUsage: python project.py <STOCK_SYMBOL>")
        print("Example: python project.py AAPL")
        sys.exit(1)

    symbol = sys.argv[1].upper().strip()

    print(f"\n{'=' * 70}")
    print(f"STOCK SENTIMENT ANALYSIS: {symbol}")
    print(f"{'=' * 70}\n")

    print("Fetching stock data...")
    stock_data = get_stock_quote(symbol)

    if not stock_data:
        print(f"Could not fetch stock data for {symbol}")
        sys.exit(1)

    company_info = get_company_info(symbol)
    print(f"{company_info.get('Name', symbol)}\n")

    print("Fetching News Articles...")
    company_name = company_info.get('Name', symbol)
    articles = fetch_news(company_name, days=7)

    if not articles:
        print("No News articles found")
    else:
        print(f"Found {len(articles)} articles\n")

    analyzed_articles = []
    aggregate = None
    if articles:
        print("Analyzing sentiment...")
        for article in articles:
            sentiment = analyze_sentiment(article['clean_text'])
            article['sentiment'] = sentiment
            analyzed_articles.append(article)

        aggregate = aggregate_sentiment(analyzed_articles)
        print(f"Average sentiment: {aggregate['average']:.3f}\n")

    print('=' * 70)
    print("ANALYSIS RESULTS")
    print(f"{'=' * 70}\n")

    display_stock_info(stock_data, company_info)

    if articles and aggregate:
        display_sentiment_analysis(aggregate, analyzed_articles)


def get_stock_quote(symbol):
    """Fetch real-time stock quote from Alpha Vantage."""
    if not symbol or not isinstance(symbol, str):
        return None

    symbol = symbol.upper().strip()

    if not all(c.isalnum() or c == '.' for c in symbol):
        return None

    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'Global Quote' not in data:
            return None

        quote = data['Global Quote']

        if not quote or '05. price' not in quote:
            return None

        return {
            'symbol': quote.get('01. symbol', symbol),
            'price': float(quote.get('05. price', 0)),
            'change': float(quote.get('09. change', 0)),
            'change_percent': quote.get('10. change percent', '0%').rstrip('%'),
            'volume': int(quote.get('06. volume', 0)),
            'previous_close': float(quote.get('08. previous close', 0)),
            'trading_day': quote.get('07. latest trading day', 'N/A')
        }

    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None
    except (ValueError, KeyError):
        return None
    except Exception:
        return None


def get_company_info(symbol):
    """Fetch company overview info from Alpha Vantage."""
    if not symbol:
        return {}

    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'OVERVIEW',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'Symbol' not in data:
            return {'Name': symbol}

        return {
            'Name': data.get('Name', symbol),
            'Sector': data.get('Sector', 'N/A'),
            'Industry': data.get('Industry', 'N/A'),
            'MarketCapitalization': data.get('MarketCapitalization', '0'),
            'Description': data.get('Description', '')
        }
    except Exception:
        return {'Name': symbol}


def format_market_cap(market_cap):
    """Format market cap in human-readable form."""
    if not isinstance(market_cap, (int, float)):
        try:
            market_cap = float(market_cap)
        except (ValueError, TypeError):
            return str(market_cap)

    if market_cap >= 1_000_000_000_000:  # Trillions
        return f"${market_cap / 1_000_000_000_000:.2f}T"
    elif market_cap >= 1_000_000_000:  # Billions
        return f"${market_cap / 1_000_000_000:.2f}B"
    elif market_cap >= 1_000_000:  # Millions
        return f"${market_cap / 1_000_000:.2f}M"
    else:
        return f"${market_cap:,.0f}"


def fetch_news(query, days=7, max_articles=20):
    """Fetch news articles from NewsAPI."""
    if not query or not NEWS_API_KEY:
        return []

    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)

    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'from': from_date.strftime('%Y-%m-%d'),
        'to': to_date.strftime('%Y-%m-%d'),
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': min(max_articles, 100),
        'apiKey': NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('status') != 'ok':
            return []

        articles = data.get('articles', [])
        processed = []
        seen_titles = set()

        for article in articles:
            if not article.get('title') or not article.get('url'):
                continue

            title_lower = article['title'].lower()
            if title_lower in seen_titles:
                continue
            seen_titles.add(title_lower)

            text = ' '.join(filter(None, [
                article.get('title', ''),
                article.get('description', ''),
                article.get('content', '')
            ]))

            clean = clean_text(text)

            processed.append({
                'title': article['title'],
                'source': article.get('source', {}).get('name', 'Unknown'),
                'published_at': article.get('publishedAt', ''),
                'url': article['url'],
                'clean_text': clean
            })

        return processed

    except Exception:
        return []


def clean_text(text):
    """Clean HTML tags and URLs from text."""
    if not text:
        return ""

    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'http\S+|www\S+', '', text, flags=re.MULTILINE)
    text = ' '.join(text.split())
    return text.strip()


def analyze_sentiment(text):
    """Analyze sentiment of text using VADER."""
    if not text:
        return {
            'compound': 0.0,
            'positive': 0.0,
            'neutral': 1.0,
            'negative': 0.0,
            'classification': 'neutral'
        }

    scores = sentiment_analyzer.polarity_scores(text)
    compound = scores['compound']

    if compound >= 0.05:
        classification = 'positive'
    elif compound <= -0.05:
        classification = 'negative'
    else:
        classification = 'neutral'

    return {
        'compound': round(compound, 3),
        'positive': round(scores['pos'], 3),
        'neutral': round(scores['neu'], 3),
        'negative': round(scores['neg'], 3),
        'classification': classification
    }


def aggregate_sentiment(articles):
    """Calculate aggregate sentiment from multiple articles."""
    if not articles:
        return {
            'average': 0.0,
            'total': 0,
            'positive_count': 0,
            'neutral_count': 0,
            'negative_count': 0,
            'positive_percent': 0.0,
            'neutral_percent': 0.0,
            'negative_percent': 0.0
        }

    compounds = []
    classifications = {'positive': 0, 'neutral': 0, 'negative': 0}

    for article in articles:
        sentiment = article.get('sentiment', {})
        if sentiment:
            compounds.append(sentiment.get('compound', 0))
            classification = sentiment.get('classification', 'neutral')
            classifications[classification] = classifications.get(classification, 0) + 1

    total = len(articles)
    average = sum(compounds) / len(compounds) if compounds else 0.0

    return {
        'average': round(average, 3),
        'total': total,
        'positive_count': classifications['positive'],
        'neutral_count': classifications['neutral'],
        'negative_count': classifications['negative'],
        'positive_percent': round(classifications['positive'] / total * 100, 1) if total else 0.0,
        'neutral_percent': round(classifications['neutral'] / total * 100, 1) if total else 0.0,
        'negative_percent': round(classifications['negative'] / total * 100, 1) if total else 0.0
    }


def display_stock_info(stock_data, company_info):
    """Display formatted stock and company information."""
    if stock_data['change'] > 0:
        emoji = "📈"
    elif stock_data['change'] < 0:
        emoji = "📉"
    else:
        emoji = "➡️"

    print(f"   Company Information:")
    print(f"   Name: {company_info.get('Name', 'N/A')}")
    print(f"   Sector: {company_info.get('Sector', 'N/A')}")
    print(f"   Industry: {company_info.get('Industry', 'N/A')}\n")

    print(f"{emoji} Stock Price:")
    print(f"   Current: ${stock_data['price']:.2f}")
    print(f"   Change: ${stock_data['change']:.2f} ({stock_data['change_percent']}%)")
    print(f"   Previous Close: ${stock_data['previous_close']:.2f}")
    print(f"   Volume: {stock_data['volume']:,}")

    market_cap = company_info.get('MarketCapitalization', '0')
    if market_cap and market_cap != '0':
        print(f"   Market Cap: {format_market_cap(float(market_cap))}")

    print(f"   Trading Day: {stock_data['trading_day']}\n")


def display_sentiment_analysis(aggregate, articles):
    """Display formatted sentiment analysis results."""
    print(f"📊 Sentiment Analysis:")
    print(f"   Overall score: {aggregate['average']:.3f}")

    if aggregate['average'] >= 0.05:
        overall = "POSITIVE 📈"
    elif aggregate['average'] <= -0.05:
        overall = "NEGATIVE 📉"
    else:
        overall = "NEUTRAL ➡️"

    print(f"   Classification: {overall}\n")

    print(f"   Distribution:")
    print(f"     • Positive: {aggregate['positive_percent']:.1f}% ({aggregate['positive_count']} articles)")
    print(f"     • Neutral:  {aggregate['neutral_percent']:.1f}% ({aggregate['neutral_count']} articles)")
    print(f"     • Negative: {aggregate['negative_percent']:.1f}% ({aggregate['negative_count']} articles)")
    print(f"   Total Articles: {aggregate['total']}\n")

    print(f"📰 Recent Articles:\n")
    for i, article in enumerate(articles[:5], 1):
        sent = article['sentiment']
        emoji_map = {'positive': '📈', 'negative': '📉', 'neutral': '➡️'}
        emoji = emoji_map.get(sent['classification'], '📰')

        print(f"{i}. {article['title'][:70]}...")
        print(f"   {emoji} {sent['classification'].upper()} ({sent['compound']:+.3f})")
        print(f"   📰 {article['source']} | {article['published_at'][:10]}\n")


if __name__ == "__main__":
    main()
