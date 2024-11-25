# Douban Movie Comments Scraper

A Python-based web scraper designed to collect and process movie comments from Douban.com, with robust data processing and analysis capabilities.

## Features

- Scrapes movie comments from Douban.com with configurable parameters
- Handles rate limiting and retry mechanisms
- Processes and cleans comment data
- Supports data export to CSV format
- Includes comment categorization (positive/negative/neutral)
- Maintains session cookies and headers management
- Implements logging for debugging and monitoring

## Requirements

- Python 3.8+
- Required packages listed in requirements.txt:
  - beautifulsoup4==4.12.3
  - numpy==2.1.3
  - pandas==2.2.3
  - python-dateutil==2.9.0.post0
  - pytz==2024.2
  - requests~=2.32.3
  - six==1.16.0
  - soupsieve==2.6
  - tzdata==2024.2

## Installation

1. Clone the repository: 

```bash
git clone https://github.com/ChanMeng666/DoubanReviewScraper.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```


## Configuration

Edit `config.py` to set your preferences:

- `MOVIE_ID`: The Douban movie ID to scrape
- `MAX_PAGES`: Maximum number of pages to scrape
- `REQUEST_TIMEOUT`: Request timeout in seconds
- `RETRY_TIMES`: Number of retry attempts
- `DELAY_MIN/MAX`: Random delay between requests
- Cookie and header configurations

## Usage

Run the scraper:

```bash
python main.py
```


The scraper will:
1. Collect comments from the specified movie
2. Process and clean the data
3. Save results to CSV files in the `output` directory

## Data Processing

The `ReviewDataProcessor` class handles:
- Text cleaning and normalization
- Timestamp standardization
- Rating validation
- Comment categorization
- Data export to CSV

## Output Format

The processed data includes:
- timestamp: Comment timestamp
- content: Cleaned comment text
- rating: User rating (1-5)
- user_id: Douban user ID
- category: Comment category (positive/negative/neutral/detailed_neutral)

## Notes

- Respect Douban's robots.txt and rate limiting
- Update cookies periodically
- Consider using proxies for large-scale scraping
- Check Douban's terms of service before use

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**Chan Meng**

- LinkedIn: [chanmeng666](https://www.linkedin.com/in/chanmeng666/)
- GitHub: [ChanMeng666](https://github.com/ChanMeng666)