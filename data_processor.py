import re
from datetime import datetime
import pandas as pd
import logging
from typing import Dict, List, Optional


class ReviewDataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def clean_text(self, text: str) -> str:
        """清理评论文本"""
        if not text:
            return ""

        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)

        # 清理特殊字符，但保留中文标点
        text = re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef\u0000-\u007F]', '', text)

        # 替换多个空格为单个空格
        text = re.sub(r'\s+', ' ', text)

        # 去除首尾空白
        text = text.strip()

        return text

    def normalize_timestamp(self, timestamp: str) -> Optional[str]:
        """统一时间戳格式"""
        try:
            # 解析时间字符串
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            # 转换为标准格式
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            self.logger.error(f"时间格式转换错误: {e}")
            return None

    def validate_rating(self, rating: int) -> Optional[int]:
        """验证评分"""
        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                return rating
        except (TypeError, ValueError):
            pass
        return None

    def determine_category(self, rating: int, text_length: int) -> str:
        """确定评论类别"""
        if rating >= 4:
            return 'positive'
        elif rating <= 2:
            return 'negative'

        # 根据评论长度细分中性评论
        if text_length > 100:
            return 'detailed_neutral'
        return 'neutral'

    def process_review(self, review: Dict) -> Optional[Dict]:
        """处理单条评论数据"""
        try:
            # 清理和验证必需字段
            timestamp = self.normalize_timestamp(review.get('timestamp', ''))
            text = self.clean_text(review.get('content', ''))
            rating = self.validate_rating(review.get('rating'))

            # 验证必需字段
            if not all([timestamp, text, rating]):
                return None

            # 验证文本长度
            if len(text) < 10 or len(text) > 1000:
                return None

            # 构建标准化的评论数据
            processed_review = {
                'timestamp': timestamp,
                'content': text,
                'rating': rating,
                'user_id': review.get('user_id', ''),
                'category': self.determine_category(rating, len(text))
            }

            return processed_review

        except Exception as e:
            self.logger.error(f"处理评论数据失败: {e}")
            return None

    def process_reviews(self, reviews: List[Dict]) -> pd.DataFrame:
        """处理所有评论数据"""
        processed_reviews = []

        for review in reviews:
            processed_review = self.process_review(review)
            if processed_review:
                processed_reviews.append(processed_review)

        # 创建DataFrame
        df = pd.DataFrame(processed_reviews)

        # 确保列顺序
        columns = ['timestamp', 'content', 'rating', 'user_id', 'category']
        df = df.reindex(columns=columns)

        return df

    def save_to_csv(self, df: pd.DataFrame, filename: str) -> None:
        """保存为CSV文件"""
        try:
            # 使用proper quoting确保正确处理逗号和引号
            df.to_csv(filename,
                      index=False,
                      encoding='utf-8',
                      quoting=1,  # QUOTE_ALL
                      quotechar='"',
                      doublequote=True,
                      escapechar='\\')

            self.logger.info(f"成功保存 {len(df)} 条评论到 {filename}")

        except Exception as e:
            self.logger.error(f"保存CSV文件失败: {e}")