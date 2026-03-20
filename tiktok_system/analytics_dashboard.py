#!/usr/bin/env python3
"""
View Tracking Dashboard for TikTok/Instagram Posts
Tracks views, likes, comments over time
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

DATA_DIR = Path('/root/life/elternratgeber-system/tiktok_system/data')
DATA_DIR.mkdir(parents=True, exist_ok=True)


class AnalyticsTracker:
    """Track and analyze post performance"""
    
    def __init__(self):
        self.tracking_file = DATA_DIR / 'post_analytics.json'
        self.data = self._load_data()
    
    def _load_data(self):
        if self.tracking_file.exists():
            with open(self.tracking_file) as f:
                return json.load(f)
        return {"posts": {}, "summary": {}}
    
    def _save_data(self):
        with open(self.tracking_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    async def track_tiktok_post(self, post_url, post_id):
        """Track a single TikTok post"""
        print(f"📊 Tracking: {post_url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(post_url)
                await page.wait_for_timeout(5000)
                
                # Extract metrics
                metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "views": None,
                    "likes": None,
                    "comments": None,
                    "shares": None
                }
                
                # Try multiple selectors for views
                view_selectors = [
                    '[data-e2e="browse-video-views"]',
                    '[data-e2e="video-views"]',
                    '.video-count',
                    '[class*="view"]',
                ]
                
                for selector in view_selectors:
                    try:
                        elem = await page.query_selector(selector)
                        if elem:
                            text = await elem.inner_text()
                            if text:
                                metrics['views'] = text.strip()
                                break
                    except:
                        continue
                
                # Likes
                try:
                    like_elem = await page.query_selector('[data-e2e="like-count"]')
                    if like_elem:
                        metrics['likes'] = await like_elem.inner_text()
                except:
                    pass
                
                # Comments
                try:
                    comment_elem = await page.query_selector('[data-e2e="comment-count"]')
                    if comment_elem:
                        metrics['comments'] = await comment_elem.inner_text()
                except:
                    pass
                
                # Store data
                if post_id not in self.data["posts"]:
                    self.data["posts"][post_id] = {
                        "url": post_url,
                        "platform": "tiktok",
                        "first_seen": datetime.now().isoformat(),
                        "metrics_history": []
                    }
                
                self.data["posts"][post_id]["metrics_history"].append(metrics)
                self.data["posts"][post_id]["latest"] = metrics
                
                self._save_data()
                
                print(f"   Views: {metrics.get('views', 'N/A')}")
                print(f"   Likes: {metrics.get('likes', 'N/A')}")
                print(f"   Comments: {metrics.get('comments', 'N/A')}")
                
                return metrics
                
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
                return None
                
            finally:
                await browser.close()
    
    def get_performance_report(self, post_id=None, days=7):
        """Generate performance report"""
        print(f"\n📈 PERFORMANCE REPORT (Last {days} days)")
        print("="*60)
        
        if post_id and post_id in self.data["posts"]:
            post = self.data["posts"][post_id]
            print(f"\n📝 Post: {post_id}")
            print(f"   URL: {post['url']}")
            print(f"   Platform: {post['platform']}")
            
            if post.get('latest'):
                latest = post['latest']
                print(f"\n📊 Latest Metrics:")
                print(f"   Views: {latest.get('views', 'N/A')}")
                print(f"   Likes: {latest.get('likes', 'N/A')}")
                print(f"   Comments: {latest.get('comments', 'N/A')}")
            
            if len(post.get('metrics_history', [])) > 1:
                print(f"\n📈 History ({len(post['metrics_history'])} data points)")
                
        else:
            # Show all posts summary
            print(f"\n📊 All Tracked Posts: {len(self.data['posts'])}")
            for pid, post in self.data["posts"].items():
                latest = post.get('latest', {})
                print(f"\n   {pid[:30]}...")
                print(f"      Views: {latest.get('views', 'N/A')}")
                print(f"      Likes: {latest.get('likes', 'N/A')}")
    
    def compare_posts(self):
        """Compare performance across posts"""
        print("\n🏆 POST COMPARISON")
        print("="*60)
        
        posts = []
        for pid, post in self.data["posts"].items():
            latest = post.get('latest', {})
            posts.append({
                'id': pid,
                'views': latest.get('views', '0'),
                'likes': latest.get('likes', '0'),
                'comments': latest.get('comments', '0')
            })
        
        # Sort by views
        posts.sort(key=lambda x: int(x['views'].replace('K', '000').replace('M', '000000').replace('.', '') or 0), reverse=True)
        
        for i, post in enumerate(posts[:10], 1):
            print(f"{i}. Views: {post['views']} | Likes: {post['likes']} | {post['id'][:30]}...")


async def scheduled_tracking():
    """Run tracking every X hours"""
    tracker = AnalyticsTracker()
    
    # Load post URLs from tracking file
    tracking_file = DATA_DIR / 'post_tracking.json'
    if not tracking_file.exists():
        print("⚠️  No posts to track yet. Upload first!")
        return
    
    with open(tracking_file) as f:
        data = json.load(f)
    
    for post in data.get('posts', []):
        if post.get('status') == 'posted' and post.get('tracking_url'):
            await tracker.track_tiktok_post(
                post['tracking_url'],
                post['timestamp']
            )
    
    # Generate report
    tracker.get_performance_report()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "track":
            # Track specific URL
            url = sys.argv[2]
            post_id = sys.argv[3] if len(sys.argv) > 3 else datetime.now().isoformat()
            tracker = AnalyticsTracker()
            asyncio.run(tracker.track_tiktok_post(url, post_id))
            
        elif sys.argv[1] == "report":
            # Show report
            tracker = AnalyticsTracker()
            tracker.get_performance_report()
            
        elif sys.argv[1] == "compare":
            tracker = AnalyticsTracker()
            tracker.compare_posts()
            
        elif sys.argv[1] == "scheduled":
            # Run scheduled tracking
            asyncio.run(scheduled_tracking())
    else:
        print("Usage:")
        print("  python analytics_dashboard.py track <URL> [post_id]")
        print("  python analytics_dashboard.py report")
        print("  python analytics_dashboard.py compare")
        print("  python analytics_dashboard.py scheduled")
