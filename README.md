# UniFuncs 网络搜索工具

<div align="center">
  <img src="image.png" alt="UniFuncs Logo" width="200">
</div>

这是一个基于 UniFuncs Web Search API 的搜索工具包，提供了多种使用方式和丰富的搜索结果展示。

## 安装和配置

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置API密钥（以下三种方式任选其一）：

   a. 创建配置文件：
   ```bash
   # 复制示例配置文件
   cp config.example.py config.py
   # 编辑config.py，填入你的API密钥
   ```

   b. 设置环境变量：
   ```bash
   # Linux/Mac
   export UNIFUNCS_API_KEY="你的API密钥"
   
   # Windows
   set UNIFUNCS_API_KEY="你的API密钥"
   ```

   c. 在使用时直接传入API密钥

## 功能特点

- 多样化搜索结果
  - 网页搜索结果
  - 相关图片展示
  - 网站图标和来源信息
  
- 美观的界面设计
  - 卡片式布局
  - 图片网格展示
  - 响应式设计
  - 优雅的动画效果

- 搜索选项
  - 实时网络搜索
  - 时效性过滤（一天内、一周内、一个月内、一年内）
  - 自定义结果数量
  - 多种输出格式（文本、JSON、Markdown）

## 使用方法

### Web界面（推荐）

```bash
python web_ui.py
```

启动后在浏览器中访问 http://127.0.0.1:7860 即可使用Web界面。

Web界面功能：
- 输入搜索关键词
- 选择结果时效性
- 调整结果数量（1-20条）
- 选择输出格式
- 可选自定义API密钥

### 命令行工具

```bash
# 基本用法
python cli.py "搜索关键词"

# 高级用法
python cli.py "搜索关键词" -f Week -c 10 -o markdown -s results.md -k "你的API密钥"
```

参数说明：
- `-f, --freshness`: 结果时效性 (可选: Day, Week, Month, Year)
- `-c, --count`: 返回结果数量 (默认: 10)
- `-o, --output`: 输出格式 (可选: text, json, markdown)
- `-s, --save`: 保存结果到文件
- `-k, --key`: 自定义API密钥

### 交互式界面

```bash
python interactive.py
```

按照提示输入搜索关键词、选择时效性和输出格式即可。

## API用法

你也可以在自己的项目中直接使用搜索API：

```python
from search_api import UniFuncsSearch

# 创建搜索客户端（三种方式任选其一）
search = UniFuncsSearch(api_key="你的API密钥")  # 1. 直接传入API密钥
# 或者使用环境变量中的API密钥
search = UniFuncsSearch()  # 2. 使用环境变量UNIFUNCS_API_KEY
# 或者使用配置文件中的默认API密钥
search = UniFuncsSearch()  # 3. 使用config.py中的DEFAULT_API_KEY

# 执行搜索
results = search.search("搜索关键词", freshness="Week", count=5)

# 格式化结果
formatted = search.format_results(results, output_format="markdown")

# 输出结果
print(formatted)
```

## API返回数据说明

搜索结果包含以下信息：

### 网页搜索结果
- 网页标题 (name)
- 网页URL (url)
- 显示用URL (displayUrl)
- 内容片段 (snippet)
- 内容摘要 (summary)
- 网站名称 (siteName)
- 网站图标 (siteIcon)

### 图片搜索结果
- 缩略图URL (thumbnailUrl)
- 原始图片URL (contentUrl)
- 图片尺寸 (width, height)
- 图片所在页面URL (hostPageUrl)
- 图片所在页面显示URL (hostPageDisplayUrl)

## 错误处理

工具会自动处理常见错误并提供友好的错误提示：

- 服务器错误 (-20001)
- 权限问题 (-20011)
- 账户状态 (-20014)
- API密钥问题 (-20021)
- 余额不足 (-20025)
- 速率限制 (-20033)
- 搜索失败 (-30000)
- 关键词无效 (-30001)

## 安全说明

请注意：
1. 不要在公开仓库中提交包含API密钥的配置文件
2. 不要在代码中硬编码API密钥
3. 建议使用环境变量或配置文件来管理API密钥

## 许可证

本项目采用 MIT 许可证。
完整的许可证文本请查看 [LICENSE](LICENSE) 文件。 