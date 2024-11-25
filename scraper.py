# scraper.py
import requests
import json
import pandas as pd
import time
import random
import logging
import os
from datetime import datetime
from config import generate_bid, REQUEST_TIMEOUT, RETRY_TIMES, RETRY_DELAY, DELAY_MIN, DELAY_MAX
from data_processor import ReviewDataProcessor

class DoubanScraper:
    def __init__(self, movie_id, headers):
        self.movie_id = movie_id
        self.base_url = f'https://movie.douban.com/subject/{movie_id}/comments'
        self.headers = headers
        self.session = requests.Session()

        # 初始化配置参数
        self.timeout = REQUEST_TIMEOUT
        self.retry_times = RETRY_TIMES
        self.retry_delay = RETRY_DELAY
        self.delay_min = DELAY_MIN
        self.delay_max = DELAY_MAX

        self.data_processor = ReviewDataProcessor()

        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # 确保输出目录存在
        os.makedirs('output', exist_ok=True)

    def get_page(self, start=0):
        """获取单页评论数据"""
        params = {
            'start': start,
            'limit': 20,
            'status': 'P',
            'sort': 'new_score',
            'comments_only': 1,
            'ck': self.headers['Cookie'].split('ck=')[1].split(';')[0]
        }

        for retry in range(self.retry_times):
            try:
                # 添加随机延时
                delay = random.uniform(self.delay_min, self.delay_max)
                self.logger.info(f"等待 {delay:.2f} 秒...")
                time.sleep(delay)

                url = f"{self.base_url}"
                self.logger.info(f"发送请求: {url}, start={start}")

                response = self.session.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=self.timeout
                )

                response.raise_for_status()

                # 解析JSON响应
                data = response.json()

                # 检查是否包含评论数据
                if 'html' not in data or not data['html'].strip():
                    self.logger.warning("未获取到评论数据")
                    if retry < self.retry_times - 1:
                        time.sleep(self.retry_delay)
                        continue
                    return None

                return data['html']

            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                self.logger.error(f"获取页面失败 (尝试 {retry + 1}/{self.retry_times}): {e}")
                if retry < self.retry_times - 1:
                    time.sleep(self.retry_delay)
                continue

        return None

    def parse_page(self, html_content):
        """解析页面内容"""
        if not html_content:
            return []

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        reviews = []

        for comment in soup.find_all('div', class_='comment-item'):
            try:
                # 提取时间戳
                timestamp = comment.find('span', class_='comment-time')['title']

                # 提取评论文本
                content = comment.find('span', class_='short').get_text(strip=True)

                # 提取评分
                rating_span = comment.find('span', class_=lambda x: x and x.startswith('allstar'))
                rating = self._convert_rating(rating_span['class'][0]) if rating_span else None

                # 提取用户ID
                user_link = comment.find('a', class_='')
                user_id = self._extract_user_id(user_link['href']) if user_link else None

                # 提取地区
                location = comment.find('span', class_='comment-location')
                location = location.get_text(strip=True) if location else None

                if timestamp and content and rating:
                    reviews.append({
                        'timestamp': timestamp,
                        'content': content,
                        'rating': rating,
                        'user_id': user_id,
                        'location': location,
                        'category': 'positive' if rating >= 4 else 'negative' if rating <= 2 else 'neutral'
                    })

            except Exception as e:
                self.logger.error(f"解析评论失败: {e}")
                continue

        return reviews

    def _convert_rating(self, rating_class):
        """转换评分"""
        rating_map = {
            'allstar50': 5,
            'allstar40': 4,
            'allstar30': 3,
            'allstar20': 2,
            'allstar10': 1
        }
        return rating_map.get(rating_class, None)

    def _extract_user_id(self, href):
        """提取用户ID"""
        import re
        match = re.search(r'/people/([^/]+)/', href)
        return match.group(1) if match else None

    def scrape_all_pages(self, max_pages=50):
        """爬取所有页面"""
        all_reviews = []
        current_page = 0

        while current_page < max_pages:
            start = current_page * 20
            self.logger.info(f"正在爬取第 {current_page + 1} 页...")

            page_content = self.get_page(start)
            if not page_content:
                self.logger.warning(f"第 {current_page + 1} 页获取失败，停止爬取")
                break

            page_reviews = self.parse_page(page_content)
            if not page_reviews:
                self.logger.warning(f"第 {current_page + 1} 页没有评论，停止爬取")
                break

            all_reviews.extend(page_reviews)
            self.logger.info(f"已获取 {len(all_reviews)} 条评论")

            # 保存中间结果
            if len(all_reviews) % 100 == 0:
                self._save_intermediate(all_reviews)

            current_page += 1

        return all_reviews

    # def _save_intermediate(self, reviews):
    #     """保存中间结果"""
    #     df = pd.DataFrame(reviews)
    #     df.to_csv('output/reviews_intermediate.csv', index=False, encoding='utf-8')
    #
    # def save_reviews(self, reviews, filename='reviews_final.csv'):
    #     """保存最终结果"""
    #     if not reviews:
    #         self.logger.warning("没有数据需要保存")
    #         return
    #
    #     df = pd.DataFrame(reviews)
    #     output_path = os.path.join('output', filename)
    #     df.to_csv(output_path, index=False, encoding='utf-8')
    #     self.logger.info(f"已保存 {len(reviews)} 条评论到 {output_path}")

    def save_reviews(self, reviews, filename='reviews_final.csv'):
        """保存最终结果"""
        if not reviews:
            self.logger.warning("没有数据需要保存")
            return

        try:
            # 处理数据
            df = self.data_processor.process_reviews(reviews)

            if df.empty:
                self.logger.warning("处理后没有有效数据")
                return

            # 保存到CSV
            output_path = os.path.join('output', filename)
            self.data_processor.save_to_csv(df, output_path)

        except Exception as e:
            self.logger.error(f"保存评论数据失败: {e}")

    def _save_intermediate(self, reviews):
        """保存中间结果"""
        try:
            # 处理数据
            df = self.data_processor.process_reviews(reviews)

            if not df.empty:
                output_path = os.path.join('output', 'reviews_intermediate.csv')
                self.data_processor.save_to_csv(df, output_path)

        except Exception as e:
            self.logger.error(f"保存中间结果失败: {e}")