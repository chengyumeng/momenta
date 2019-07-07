# momenta
微信超级机器人 via 微软小冰

# Quick Start
```bash
# 机器人需要先关注微信公众号：中关村男子图鉴
# 启动 mongo 数据库
export MOMENTA_MONGO_HOST="127.0.0.1:27017"
export MOMENTA_MONGO_USER="root"
export MOMENTA_MONGO_PASSWORD="12345678"
pip install momenta
momenta run
```

# Feature
- 支持微软小冰自动回复
- 支持信息订阅
- 支持信息拦截

# example
- 特定群组订阅 calendar 服务
```bash
momenta subscription create --trigger=daily --nickname=momenta官方交流群 --action=calendar
```

- 拦截群内昵称不符合 名字_公司_职位 规范的人的信息
```bash
momenta filter create --nickname="momenta 官方交流群" --regular="^[^_]{2,3}(_[^_]{2,5})?(_[^_]{2,5})?$" --warning="请按照群公告修改群备注"```
```

# 插件开发
```buildoutcfg
待更新
```


