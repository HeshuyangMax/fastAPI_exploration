import time
import random
import logging
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import CollectorRegistry, Gauge, Histogram, Counter, make_asgi_app

# 创建fastapi应用
app = FastAPI()
# 创建一个 CollectorRegistry 对象，用于注册指标
registry = CollectorRegistry()
# 记录接口响应时长的值
responseTime = Gauge("response_time", "记录请求http://8.134.171.142/时的接口响应时长")
# 记录接口请求量
requestNum = Counter("request_number", "记录请求http://8.134.171.142/接口的数量")
# 注册指标
registry.register(responseTime)
registry.register(requestNum)
# 设置Prometheus的端点为/metrics
metrics_app = make_asgi_app(registry)
app.mount("/metrics", metrics_app, name="metrics")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

def random_sleep():
    # 生成随机睡眠时间（范围在 1 到 5 秒之间）
    sleep_time = random.randint(1, 5)  
    print(f"将睡眠 {sleep_time} 秒...")
    time.sleep(sleep_time)

@app.get("/")
@responseTime.time()
def read_root():
    random_sleep()
    requestNum.inc()
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}
