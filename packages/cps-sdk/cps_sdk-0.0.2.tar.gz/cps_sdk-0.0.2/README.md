# Python 电商CPS SDK 整合
#### 目前仅支持:
1. 淘宝CPS
2. 京东CPS
3. 拼多多CPS
4. 唯品会CPS
5. 抖店CPS

#### 安装:
```
pip install cps_sdk
```

#### 使用示例: 
##### 1.淘宝CPS(其他供应商大同小异, 返回response均为requests模块返回的response对象)

```python
from third_sdk import TbClient

client = TbClient(host='', appkey='', secret='')

# 商品查询
resp = client.taobao_tbk_dg_item_info_get(**{'num_iid': 'xxx'})
print(resp.text)  # res.json 直接获取dict结构数据

# 物料搜索
client.taobao_tbk_dg_material_optional(**{'q': 'xxx', 'pid': ''})
print(resp.text)

# -----------------------------------------

# 尚未录入的api调用方式 (以物料精选为例)
from third_sdk.top.api.rest.TbkDgOptimusMaterialRequest import TbkDgOptimusMaterialRequest

req = TbkDgOptimusMaterialRequest()
resp = client.api_invoke(req, **{'pid': ''})
print(resp)
```
##### 2.京东CPS
```python
from third_sdk import JdClient

client = JdClient(appkey='', secret='')

resp = client.jd_union_open_goods_query(**{
    'goodsReqDTO': {
        'keyword': "手机"
    }
})
print(resp.text)

# 尚未录入的api调用方式
from third_sdk.jd.api.rest.UnionOpenGoodsQueryRequest import UnionOpenGoodsQueryRequest

resp = client.api_invoke(UnionOpenGoodsQueryRequest(), **{
    'goodsReqDTO': {
        'keyword': "手机"
    }
})
print(resp.text)
```
##### 3.拼多多CPS
```python
from third_sdk import PddClient

client = PddClient(appkey='', secert='')

resp = client.pdd_ddk_goods_search(**{
    'keyword': '手机'
})
print(resp.text)

# 尚未录入的api调用方式
resp = client.api_invoke('pdd.ddk.goods.search', **{
    'keyword': '手机'
})
print(resp.text)
```
##### 4.唯品会CPS
```python
from third_sdk import VipClient

client = VipClient(appkey='', secret='')
resp = client.get_by_goods_ids_v2(**{
    'request': {
        'goodsIds': ['xxxx']
    }
})
print(resp.text)

# 尚未录入的api调用方式
resp = client.api_invoke('getByGoodsIdsV2', **{
    'request': {
        'goodsIds': ['xxxx']
    }
})
print(resp.text)
```
##### 5.抖店CPS
```python
from third_sdk import DouDianClient

def get_access_token():
    """
    :return access_token
    """
    # 需要自己实现
    pass

client = DouDianClient(appkey='', secret='', get_access_token_func=get_access_token)

resp = client.buyin_kolMaterialsProductsSearch(**{
    "title": "手机"
})
print(resp.text)

# 尚未录入api的调用方式
resp = client.api_invoke('buyin.kolMaterialsProductsSearch', **{
    'title': '手机'
})
print(resp.text)
```