# 自己写的帮助自己科研的工具

## 已有模块

- ASCAT
  - [X]  ASCAT 数据下载
  - [X]  ASCAT nat数据读取

## 模块介绍

### ASCAT.Download

支持的产品，参见 [https://api.eumetsat.int/data/browse/collections](https://api.eumetsat.int/data/browse/collections)

### ASCAT.Reader

经过测试的产品

- ASCAT Level 1 Sigma0 Full Resolution - Metop - Global
- ASCAT Level 1 Sigma0 resampled at 25 km Swath Grid - Metop - Global
- ASCAT Level 1 Sigma0 resampled at 12.5 km Swath Grid - Metop - Global

## 安装方法

```bash
pip install -i https://test.pypi.org/simple/ kyTools
```

每个模块的使用方法可以参见[tests](./tests)文件夹
