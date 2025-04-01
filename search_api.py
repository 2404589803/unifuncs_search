#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os

try:
    from config import DEFAULT_API_KEY
except ImportError:
    DEFAULT_API_KEY = None

class UniFuncsSearch:
    def __init__(self, api_key=None):
        # 优先级：传入的API密钥 > 环境变量 > 配置文件中的默认密钥
        self.api_key = api_key or os.environ.get("UNIFUNCS_API_KEY") or DEFAULT_API_KEY
        
        if not self.api_key:
            raise ValueError("API密钥未设置。请通过以下方式之一设置API密钥：\n"
                           "1. 在初始化时传入api_key参数\n"
                           "2. 设置环境变量UNIFUNCS_API_KEY\n"
                           "3. 在config.py中设置DEFAULT_API_KEY")
        
        self.base_url = "https://api.unifuncs.com/api"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def read_webpage(self, url, format="markdown", include_images=True, include_videos=False,
                    include_position=False, only_css_selectors=None, wait_for_css_selectors=None,
                    exclude_css_selectors=None, link_summary=False):
        """
        解析网页内容
        
        参数:
            url (str): 需要解析的网页URL
            format (str): 返回格式，可选值：markdown、md、text、txt、json，默认为markdown
            include_images (bool): 是否包含图片，默认为True
            include_videos (bool): 是否包含视频，默认为False
            include_position (bool): 是否包含元素位置信息，默认为False
            only_css_selectors (list): 仅包含匹配CSS选择器的元素，默认为None
            wait_for_css_selectors (list): 等待这些CSS选择器元素出现后再解析页面，默认为None
            exclude_css_selectors (list): 排除匹配CSS选择器的元素，默认为None
            link_summary (bool): 是否包含链接摘要，默认为False
            
        返回:
            dict: API返回的结果
        """
        # 构建请求URL和参数
        endpoint = f"{self.base_url}/web-reader/read"
        
        payload = {
            "url": url,
            "format": format,
            "includeImages": include_images,
            "includeVideos": include_videos,
            "includePosition": include_position,
            "linkSummary": link_summary
        }
        
        # 添加可选的CSS选择器参数
        if only_css_selectors:
            payload["onlyCSSSelectors"] = only_css_selectors
        if wait_for_css_selectors:
            payload["waitForCSSSelectors"] = wait_for_css_selectors
        if exclude_css_selectors:
            payload["excludeCSSSelectors"] = exclude_css_selectors
            
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "code": -1}
        except json.JSONDecodeError:
            return {"error": "解析响应失败", "code": -1}

    def read_webpage_get(self, url, format="markdown", include_images=True, include_videos=False,
                        include_position=False, only_css_selectors=None, wait_for_css_selectors=None,
                        exclude_css_selectors=None, link_summary=False):
        """
        使用GET方法解析网页内容
        
        参数与read_webpage相同，但使用GET请求而不是POST
        """
        # URL编码处理
        import urllib.parse
        encoded_url = urllib.parse.quote(url, safe='')
        
        # 构建请求URL和参数
        endpoint = f"{self.base_url}/web-reader/{encoded_url}"
        
        params = {
            "format": format,
            "includeImages": str(include_images).lower(),
            "includeVideos": str(include_videos).lower(),
            "includePosition": str(include_position).lower(),
            "linkSummary": str(link_summary).lower()
        }
        
        # 添加可选的CSS选择器参数
        if only_css_selectors:
            params["onlyCSSSelectors"] = ",".join(only_css_selectors)
        if wait_for_css_selectors:
            params["waitForCSSSelectors"] = ",".join(wait_for_css_selectors)
        if exclude_css_selectors:
            params["excludeCSSSelectors"] = ",".join(exclude_css_selectors)
            
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "code": -1}
        except json.JSONDecodeError:
            return {"error": "解析响应失败", "code": -1}

    def read_webpage_post(self, params):
        """
        使用POST方法解析网页内容
        
        参数:
            params (dict): 请求参数，包含以下字段：
                url (str): 需要解析的URL
                format (str): 返回格式，可选值：markdown、md、text、txt、json
                includeImages (bool): 是否包含图片
                includeVideos (bool): 是否包含视频
                includePosition (bool): 是否包含元素位置信息
                onlyCSSSelectors (list): 仅包含匹配CSS选择器的元素
                waitForCSSSelectors (list): 等待这些CSS选择器元素出现后再解析页面
                excludeCSSSelectors (list): 排除匹配CSS选择器的元素
                linkSummary (bool): 是否包含链接摘要
            
        返回:
            dict: API返回的结果
        """
        endpoint = f"{self.base_url}/web-reader/read"
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "code": -1}
        except json.JSONDecodeError:
            return {"error": "解析响应失败", "code": -1}

    def search(self, query, freshness=None, summary=True, page=1, count=10):
        """
        执行网络搜索
        
        参数:
            query (str): 搜索关键词
            freshness (str, 可选): 结果时效性，可选值：Day、Week、Month、Year
            summary (bool, 可选): 是否返回摘要，默认值为True
            page (int, 可选): 页码，默认值为1
            count (int, 可选): 每页结果数量（1-50），默认值为10
            
        返回:
            dict: API返回的结果
        """
        endpoint = f"{self.base_url}/web-search/search"
        payload = {
            "query": query,
            "summary": summary,
            "page": page,
            "count": count
        }
        
        if freshness:
            payload["freshness"] = freshness
            
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "code": -1}
        except json.JSONDecodeError:
            return {"error": "解析响应失败", "code": -1}
            
    def format_results(self, results, output_format="text"):
        """
        格式化搜索结果
        
        参数:
            results (dict): 搜索结果
            output_format (str): 输出格式 (text, json, markdown)
            
        返回:
            str: 格式化后的结果
        """
        if "error" in results:
            return f"错误: {results['error']}"
            
        if results.get("code") != 0:
            return f"API错误: {results.get('message', '未知错误')} (代码: {results.get('code')})"
            
        if output_format == "json":
            return json.dumps(results, ensure_ascii=False, indent=2)
            
        data = results.get("data", {})
        web_pages = data.get("webPages", [])
        
        if not web_pages:
            return "未找到搜索结果"
            
        if output_format == "markdown":
            output = f"# 搜索结果: {results.get('data', {}).get('query', '')}\n\n"
            for i, page in enumerate(web_pages, 1):
                output += f"## {i}. [{page.get('name', '无标题')}]({page.get('url', '')})\n\n"
                output += f"**来源:** {page.get('siteName', '未知来源')}\n\n"
                output += f"{page.get('summary', page.get('snippet', '无摘要'))}\n\n"
                output += "---\n\n"
            return output
            
        # 默认文本格式
        output = f"搜索结果: {results.get('data', {}).get('query', '')}\n\n"
        for i, page in enumerate(web_pages, 1):
            output += f"{i}. {page.get('name', '无标题')}\n"
            output += f"   网址: {page.get('url', '')}\n"
            output += f"   来源: {page.get('siteName', '未知来源')}\n"
            output += f"   摘要: {page.get('summary', page.get('snippet', '无摘要'))}\n\n"
        return output

    def get_formatted_results(self, query, freshness=None, output_format="text", count=10):
        """
        搜索并返回格式化结果的便捷方法
        
        参数:
            query (str): 搜索关键词
            freshness (str, 可选): 结果时效性
            output_format (str): 输出格式
            count (int): 结果数量
            
        返回:
            str: 格式化后的结果
        """
        results = self.search(query, freshness, True, 1, count)
        return self.format_results(results, output_format) 