# Stock Sentiment Analyzer
## Video Demo: https://youtu.be/mgl6yQsJ4KY

## 📊 Overview

The **Stock Sentiment Analyzer** is a sophisticated command-line application that provides real-time market sentiment analysis for publicly traded stocks. By combining live stock market data from Alpha Vantage with recent news coverage analyzed through VADER sentiment analysis, this tool offers investors and traders an immediate, data-driven perspective on market sentiment surrounding any stock.

In today's fast-paced financial markets, understanding not just price movements but also the underlying sentiment driving those movements is crucial. This project bridges that gap by automatically collecting, processing, and analyzing news sentiment, presenting users with actionable insights in seconds.

## 🎯 Project Motivation

Traditional stock analysis tools focus primarily on technical indicators and price charts. However, market sentiment—how investors feel about a stock based on news and events—is equally important. This project was created to fill that gap by providing:

1. **Quick Sentiment Overview**: Get an instant read on whether recent news is positive, negative, or neutral
2. **Data-Driven Analysis**: Uses proven NLP techniques (VADER) rather than subjective human judgment
3. **Comprehensive Context**: Combines price data with news sentiment for a complete picture
4. **Accessibility**: Free APIs and open-source tools make this available to anyone

This tool is particularly useful for:
- Day traders wanting quick sentiment checks before making trades
- Long-term investors researching potential stocks
- Financial students learning about sentiment analysis
- Anyone curious about market psychology around specific companies

## ✨ Key Features

### 1. Real-Time Stock Data Integration
- Fetches current stock prices from Alpha Vantage API
- Displays daily price changes and percentage movements
- Shows trading volume and market capitalization
- Includes company information (sector, industry)
- Handles market closures and delayed data gracefully

### 2. Intelligent News Collection
- Retrieves 10-20 most recent articles from NewsAPI
- Searches using company name for better relevance
- Filters articles to last 7 days for timeliness
- Automatically deduplicates articles by title
- Sources from reputable outlets (Reuters, Bloomberg, CNBC, etc.)

### 3. Advanced Sentiment Analysis
- Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Analyzes sentiment at both article and aggregate levels
- Provides compound scores ranging from -1 (very negative) to +1 (very positive)
- Classifies sentiment as positive, neutral, or negative
- Shows distribution percentages across all articles

### 4. Professional Output Formatting
- Clean, organized terminal display with emojis for visual clarity
- Color-coded sentiment indicators (📈 positive, 📉 negative, ➡️ neutral)
- Human-readable number formatting (e.g., $2.50T for trillions)
- Sample article headlines with individual sentiment scores
- Comprehensive statistics and percentages

### 5. Robust Error Handling
- Validates stock symbols before making API calls
- Handles network timeouts and API failures gracefully
- Provides helpful error messages for common issues
- Continues execution even if news data is unavailable
- Rate limit awareness (respects API constraints)

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.7 or higher**: Check with `python --version`
- **pip**: Python package installer (comes with Python)
- **Internet connection**: Required for API calls

### Step-by-Step Installation

#### 1. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- `requests` - For making HTTP API calls
- `python-dotenv` - For managing environment variables securely
- `vaderSentiment` - For sentiment analysis
- `beautifulsoup4` - For HTML parsing and text cleaning
- `pytest` - For running automated tests

#### 2. Get Free API Keys

This project requires two free API keys:

**Alpha Vantage (Stock Market Data):**
1. Visit: https://www.alphavantage.co/support/#api-key
2. Enter your email address
3. Receive API key instantly (no credit card needed)
4. Free tier: 25 API calls per day

**NewsAPI (News Articles):**
1. Visit: https://newsapi.org/register
2. Sign up with your email
3. Copy your API key from the dashboard
4. Free tier: 100 API calls per day

#### 3. Configure API Keys
```bash
# Copy the example environment file
cp .env.example .env

# Open .env in your editor
nano .env
# Or use: code .env (VS Code) or vim .env
```

**Add your keys to `.env`:**
```
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_newsapi_key_here
```

**Important:**
- No quotes around the keys
- No spaces around the `=` sign
- Each key on its own line
- Never commit `.env` to version control

#### 4. Verify Installation
```bash
# Test that everything is installed correctly
python -c "import requests, dotenv, vaderSentiment, bs4; print('✅ All packages installed!')"

# Test that API keys are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Alpha Vantage:', bool(os.getenv('ALPHA_VANTAGE_API_KEY'))); print('NewsAPI:', bool(os.getenv('NEWS_API_KEY')))"
```

Both commands should complete without errors.

## 📖 Usage Guide

### Basic Usage
```bash
python project.py <STOCK_SYMBOL>
```

### Examples

**Analyze Apple Inc.:**
```bash
python project.py AAPL
```

**Analyze Tesla:**
```bash
python project.py TSLA
```

### Sample Output
```
======================================================================
STOCK SENTIMENT ANALYSIS: AAPL
======================================================================

Fetching stock data...
Apple Inc.

Fetching News Articles...
Found 18 articles

Analyzing sentiment...
Average sentiment: 0.325

======================================================================
ANALYSIS RESULTS
======================================================================

   Company Information:
   Name: Apple Inc.
   Sector: Technology
   Industry: Consumer Electronics

📈 Stock Price:
   Current: $185.92
   Change: $2.34 (1.27%)
   Previous Close: $183.58
   Volume: 52,341,234
   Market Cap: $2.89T
   Trading Day: 2024-01-08

 Sentiment Analysis:
 Overall score: 0.325
  Classification: POSITIVE 📈

   Distribution:
     • Positive: 61.1% (11 articles)
     • Neutral:  22.2% (4 articles)
     • Negative: 16.7% (3 articles)
   Total Articles: 18

📰 Recent Articles:

1. Apple Unveils New AI Features in Latest iPhone Update...
   📈 POSITIVE (+0.789)
   📰 TechCrunch | 2024-01-08

2. Apple Stock Hits Record High on Strong Q1 Earnings...
   📈 POSITIVE (+0.854)
   📰 Bloomberg | 2024-01-07

3. Analysts Raise Price Targets for AAPL Following Innovation Annou...
   📈 POSITIVE (+0.623)
   📰 Reuters | 2024-01-07

4. Apple Faces Regulatory Scrutiny in European Markets...
   📉 NEGATIVE (-0.456)
   📰 Financial Times | 2024-01-06

5. Apple Maintains Market Leadership Despite Competition...
   ➡️ NEUTRAL (+0.023)
   📰 MarketWatch | 2024-01-06

======================================================================
```

## 👨‍💻 Author

**[Gowtham]**
CS50P Final Project
Harvard University / edX
Date: January 2026

GitHub: [gowthxm15]
Location: [Chennai, India]

## 📄 License

This project was created as a final project for CS50P (CS50's Introduction to Programming with Python). It is for educational purposes only.

## 🙏 Acknowledgments

- **David J. Malan** - For inspiring teaching and course design
- **Alpha Vantage** - For providing free stock market data API
- **NewsAPI** - For aggregating news from thousands of sources
- **VADER Sentiment Analysis** - C.J. Hutto and Eric Gilbert for creating VADER
- **Python Community** - For excellent libraries and documentation
- **Stack Overflow** - For countless helpful answers during development
