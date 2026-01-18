📊 Stock Sentiment Analyzer

🎥 Video Demo: https://youtu.be/mgl6yQsJ4KY

A command-line application that provides real-time market sentiment analysis for publicly traded stocks.
The tool combines live stock market data from Alpha Vantage with news sentiment analysis using VADER to give a fast, data-driven view of market sentiment.

This project was built as the Final Project for CS50P – Harvard University’s Introduction to Programming with Python, and follows production-style practices such as API integration, error handling, and environment-based configuration.

📖 Overview

In modern financial markets, understanding sentiment behind price movements is as important as understanding the price itself.
This project bridges that gap by automatically collecting, processing, and analyzing recent news sentiment around a given stock symbol — delivering actionable insights in seconds.

🎯 Project Motivation

Traditional stock analysis tools focus mainly on technical indicators and price charts.
However, market sentiment—how investors and media perceive a company—plays a major role in price movement.

This project was built to provide:

Quick sentiment overview — Positive, neutral, or negative

Data-driven analysis — Uses NLP instead of subjective judgment

Contextual insight — Combines price data with news sentiment

Accessibility — Built using free APIs and open-source tools

Useful for:

Day traders doing quick sentiment checks

Long-term investors researching stocks

Students learning sentiment analysis and APIs

Anyone curious about market psychology

✨ Key Features
1️⃣ Real-Time Stock Data Integration

Fetches current stock prices using Alpha Vantage

Displays daily price change and percentage movement

Shows trading volume and market capitalization

Handles market closures and delayed data gracefully

2️⃣ Intelligent News Collection

Retrieves 10–20 recent articles via NewsAPI

Searches using company names for relevance

Filters articles from the last 7 days

Deduplicates articles automatically

Uses reputable sources (Reuters, Bloomberg, CNBC, etc.)

3️⃣ Sentiment Analysis (NLP)

Uses VADER Sentiment Analysis

Produces compound scores from -1 (negative) to +1 (positive)

Classifies sentiment as positive, neutral, or negative

Aggregates sentiment across all articles

Displays sentiment distribution percentages

4️⃣ Clean CLI Output

Structured and readable terminal output

Emoji-based sentiment indicators (📈 📉 ➡️)

Human-readable number formatting (e.g., $2.5T)

Displays sample article headlines with sentiment scores

5️⃣ Robust Error Handling

Validates stock symbols before API calls

Handles network and API failures gracefully

Continues execution even if partial data is unavailable

Respects API rate limits

🚀 Installation & Setup
Prerequisites

Python 3.7 or higher

pip

Internet connection

Install dependencies
pip install -r requirements.txt

Configure API Keys

Create a .env file:

ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
NEWS_API_KEY=your_newsapi_key


⚠️ .env files should never be committed to GitHub.

▶️ Usage
python project.py <STOCK_SYMBOL>

Example
python project.py AAPL
python project.py TSLA


The program outputs:

Stock price details

Overall sentiment score

Sentiment classification

Distribution across recent news articles

🧪 Testing

Automated tests are included and can be run using:

pytest

🎓 Academic Context

This project was developed as the Final Project for CS50P (CS50’s Introduction to Programming with Python) offered by Harvard University / edX.

📄 License

This project is licensed under the MIT License.

👨‍💻 Author

Gowtham
GitHub: https://github.com/gowthxm15

Location: Chennai, India

🙏 Acknowledgments

David J. Malan — CS50

Alpha Vantage — Stock market data API

NewsAPI — News aggregation

VADER Sentiment Analysis — C.J. Hutto & Eric Gilbert

Python open-source community
