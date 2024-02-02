from typing import Union
import time
import random

from fastapi import FastAPI
from pydantic import BaseModel

from prometheus_client import CollectorRegistry, Gauge

app = FastAPI()

# 创建一个 CollectorRegistry 对象，用于注册指标
registry = CollectorRegistry()

# 创建一个 Gauge 指标，用于度量"my_metric"的值
my_metric = Gauge("response_time", "记录请求“http://8.134.171.142/”时的接口响应时长")

registry.register(my_metric)

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
def read_root():
    startTime = time.time()
    random_sleep()
    endTime = time.time()
    responseTime = endTime - startTime
    my_metric.set(responseTime)
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}
