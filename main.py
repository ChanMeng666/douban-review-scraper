# main.py
from scraper import DoubanScraper
from config import HEADERS, MOVIE_ID, MAX_PAGES
import logging


def run_scraper():
    """运行爬虫的主函数"""
    try:
        # 创建爬虫实例
        scraper = DoubanScraper(MOVIE_ID, HEADERS)

        # 开始爬取
        reviews = scraper.scrape_all_pages(MAX_PAGES)

        if not reviews:
            logging.error("未获取到任何评论数据")
            return

        # 保存结果
        scraper.save_reviews(reviews)

    except Exception as e:
        logging.error(f"爬取过程中发生错误: {str(e)}")
        raise


if __name__ == "__main__":
    run_scraper()