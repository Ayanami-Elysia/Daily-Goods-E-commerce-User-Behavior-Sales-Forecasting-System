from datetime import datetime, timedelta

class CacheManager:
    def __init__(self):
        self.cache = {}
        self.expire_times = {}
    
    def get(self, key):
        """获取缓存值"""
        if key in self.cache:
            # 检查是否过期
            if key in self.expire_times:
                if datetime.now() > self.expire_times[key]:
                    self.delete(key)
                    return None
            return self.cache[key]
        return None
    
    def set(self, key, value, expire_seconds=None):
        """设置缓存值"""
        self.cache[key] = value
        if expire_seconds:
            self.expire_times[key] = datetime.now() + timedelta(seconds=expire_seconds)
    
    def delete(self, key):
        """删除缓存"""
        if key in self.cache:
            del self.cache[key]
        if key in self.expire_times:
            del self.expire_times[key]

cache = CacheManager() 