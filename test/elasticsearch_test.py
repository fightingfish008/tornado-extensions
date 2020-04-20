import json

from elasticsearch import Elasticsearch

# es = Elasticsearch()
es = Elasticsearch([{'host':'192.168.2.31','port':9200}])
# 增加
# result = es.indices.create(index='news', ignore=400)
# print(result)

#删除
result = es.indices.delete(index='news', ignore=[400, 404])

# 插入
# data = {'title':'美国留给伊拉克的是个烂摊子吗','url':'http://view.news.qq.com/zt2011/usa_iraq/index.htm'}
# result=es.create(index='news',doc_type='politics',id=2,body=data)
# print(result)

# 查询
# 1.1 先插入
# mapping = {
#     'properties': {
#         'title': {
#         'type': 'text',
#         'analyzer': 'ik_max_word',
#         'search_analyzer': 'ik_max_word'
#     }}
# }

#
# es.indices.delete(index='news', ignore=[400, 404])
# es.indices.create(index='news', ignore=400)

# 设置mapping 信息：指定字段的类型 type 为 text，分词器 analyzer 和 搜索分词器 search_analyzer 为 ik_max_word，即中文分词插件，默认的英文分词器。
# result = es.indices.put_mapping(index='news', doc_type='politics', body=mapping)
# print(result)
# datas=[{'title':'美国留给伊拉克的是个烂摊子吗',
#     'url':'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
#     'date':'2011-12-16'},
#     {'title':'公安部：各地校车将享最高路权',
#      'url':'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
#    'date':'2011-12-16'},
#     {'title':'中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
#      'url':'https://news.qq.com/a/20111216/001044.htm',
#      'date':'2011-12-17'},
#     {'title':'中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
#      'url':'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
#      'date':'2011-12-18'}
# ]
# for data in datas:
#     es.index(index='news',doc_type = 'politics',body = data)

# 1.2 查询  his 中没数据。具体原因还不清楚
# result = es.search(index='news', doc_type='politics')
#
# print(result)
#
# # 查询pluse 体现搜索引擎
# dsl = {
#     'query': {
#         'match': {
#             'title': '中国 领事'
#         }
#     }
# }
#
# result = es.search(index='news', doc_type='politics', body=dsl)
#
# print(json.dumps(result, indent=2, ensure_ascii=False))
pass