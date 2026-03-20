# 虚假引用检测工具

一个命令行工具，通过在 Google Scholar 上搜索引用标题，验证 `.bib` 参考文献文件中的引用是否真实存在。

## 背景

随着 AI 生成内容的兴起，虚假引用在学术写作中日益成为一个值得关注的问题。本工具帮助研究人员快速识别可能伪造的参考文献——通过将每条引用的标题与 Google Scholar 的搜索结果进行交叉验证。

## 工作原理

1. 解析输入的 `.bib` 文件，提取所有引用条目。
2. 通过 API（Scrapingdog 或 Serpapi）在 Google Scholar 上搜索每条引用的标题。
3. 将搜索结果与原始标题进行精确匹配比对。
4. 输出 CSV 报告，将每条引用标记为 **OK**（已找到）或 **Fake**（未找到），并附上 PDF 链接（如有）。

## 项目结构

```
fake_citation_check_tool/
├── main.py          # 入口文件，参数解析与主逻辑
├── spider.py        # Google Scholar API 客户端（Scrapingdog 与 Serpapi）
├── bib_process.py   # .bib 文件解析器
└── config.py        # API 密钥配置
```

## 环境要求

- Python 3
- `requests` 库

## 安装

```bash
pip install requests
```

## 配置

编辑 `config.py`，将占位字符串替换为你的实际 API 密钥：

```python
SCRAP_API_KEY = {
    "scrapingdog": ["你的_SCRAPINGDOG_API_KEY"],
    "serpapi": ["你的_SERPAPI_API_KEY"],
}
```

每个服务商可以配置多个密钥，工具会自动选择剩余额度最多的密钥。

| 服务商       | 免费额度                              |
|-------------|---------------------------------------|
| Scrapingdog | 每月 1000 次请求（每次搜索消耗 5 次）    |
| Serpapi     | 每月 250 次搜索（每次搜索消耗 1 次）     |

## 使用方法

```bash
python main.py --bib_file_path <bib文件路径> [--output_path <输出CSV路径>]
```

### 参数说明

| 参数               | 是否必填 | 默认值           | 说明                |
|-------------------|---------|-----------------|---------------------|
| `--bib_file_path` | 是      | `./ref.bib`     | `.bib` 文件路径      |
| `--output_path`   | 否      | `./results.csv` | 输出 CSV 文件路径    |

### 示例

```bash
python main.py --bib_file_path ./references.bib --output_path ./check_results.csv
```

### 输出格式

输出的 CSV 文件包含以下列：

```
Index,Status,Title,PDF link
1,OK,Attention Is All You Need,https://arxiv.org/pdf/...
2,Fake,Some Fabricated Paper Title,
```

## 许可证

MIT
