<div align="center">
 <h1>🎬 Douban Movie Reviews Scraper</h1>
 <p>A powerful tool for collecting and analyzing Douban movie reviews</p>

 <img src="https://img.shields.io/badge/python-v3.8+-blue.svg">
 <img src="https://img.shields.io/badge/license-MIT-green.svg">
 <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
 <img src="https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg">
</div>
<br/>

# 🚀 Features

- 🔄 Robust scraping with rate limiting and retry mechanisms
- 🧹 Advanced data cleaning and normalization
- 📊 Sentiment analysis categorization
- 💾 Efficient CSV export functionality
- 🔍 Comprehensive error handling and logging
- 🛡️ Built-in protection against API rate limits
- 📝 Detailed comment metadata extraction
- 🎯 Configurable scraping parameters

# 🛠️ Requirements

- Python 3.8+
- Required packages:
  ```
  beautifulsoup4==4.12.3
  numpy==2.1.3
  pandas==2.2.3
  python-dateutil==2.9.0.post0
  pytz==2024.2
  requests~=2.32.3
  six==1.16.0
  soupsieve==2.6
  tzdata==2024.2
  ```

# 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/ChanMeng666/douban-review-scraper.git
```

2. Navigate to the project directory:
```bash
cd douban-review-scraper
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

# ⚙️ Configuration

Edit `config.py` to customize your scraping parameters:

```python
MOVIE_ID = 'your_movie_id'  # Douban movie ID
MAX_PAGES = 50              # Maximum pages to scrape
REQUEST_TIMEOUT = 30        # Request timeout in seconds
RETRY_TIMES = 3            # Number of retry attempts
```

# 🚀 Usage

1. Configure your target movie ID in `config.py`
2. Run the scraper:
```bash
python main.py
```

# 📊 Output Format

The scraper generates CSV files containing:
- `timestamp`: Comment timestamp
- `content`: Cleaned comment text
- `rating`: User rating (1-5)
- `user_id`: Douban user ID
- `category`: Comment category (positive/negative/neutral)

# ⚠️ Important Notes

- Respect Douban's robots.txt and API limitations
- Update cookies periodically for reliable operation
- Consider using proxies for large-scale scraping
- Check Douban's terms of service before use

# 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here's how you can contribute:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

# 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

# 👥 Author

**Chan Meng**
- LinkedIn: [chanmeng666](https://www.linkedin.com/in/chanmeng666/)
- GitHub: [ChanMeng666](https://github.com/ChanMeng666)

# 🌟 Show your support

Give a ⭐️ if this project helped you!

---

<div align="center">
Made with ❤️ by <a href="https://github.com/ChanMeng666">Chan Meng</a>
</div>