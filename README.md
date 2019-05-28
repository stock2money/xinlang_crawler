# 新浪股票评论爬取

> `https://s.weibo.com/article?q={stock code}&Refer=weibo_article`



## Environment

- Python3 + Scrapy + MySQL



## Usage

```
# xinlang_stock_reviews_spider

scrapy crawl xinlang
```



## Note

* `cookies`认证相关，首先访问新浪微博的股票页面，获取一个临时的`cookies`，后续的请求携带该`cookies`进行数据爬取，不会被强制跳转到登陆界面

