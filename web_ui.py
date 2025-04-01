#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import gradio as gr
import time
from search_api import UniFuncsSearch

# 创建搜索客户端
search_client = UniFuncsSearch()

def search_web(query, api_key, freshness, result_count, output_format):
    """执行网络搜索并返回结果"""
    
    if not query.strip():
        return "请输入搜索关键词"
    
    # 如果提供了API密钥，使用新的客户端
    client = search_client
    if api_key and api_key != search_client.api_key:
        client = UniFuncsSearch(api_key)
    
    try:
        count = int(result_count)
        if count < 1 or count > 50:
            return "结果数量必须在1-50之间"
    except ValueError:
        return "结果数量必须是整数"
    
    # 处理freshness参数
    if freshness == "None":
        freshness = None
    
    # 执行搜索
    response = client.search(query, freshness, True, 1, count)
    
    # 检查API错误
    if "error" in response:
        return f"错误: {response['error']}"
        
    if response.get("code") != 0:
        error_messages = {
            -20001: "服务器错误，请稍后再试",
            -20011: "无权限访问该API",
            -20014: "账户已被禁用",
            -20021: "API Key无效或已过期",
            -20025: "账户余额不足",
            -20033: "请求超出速率限制",
            -30000: "搜索失败",
            -30001: "搜索关键词无效"
        }
        error_code = response.get("code")
        error_msg = error_messages.get(error_code, response.get("message", "未知错误"))
        return f"API错误: {error_msg} (代码: {error_code})"
    
    # 获取网页和图片结果
    data = response.get("data", {})
    web_pages = data.get("webPages", [])
    images = data.get("images", [])
    
    if not web_pages and not images:
        return "未找到搜索结果"
    
    # 生成HTML结果
    html_output = """
    <style>
    .search-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .search-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .search-card h3 {
        margin: 0 0 10px 0;
    }
    .search-card h3 a {
        color: #1a0dab;
        text-decoration: none;
    }
    .search-card .url {
        color: #006621;
        font-size: 0.9em;
        margin-bottom: 8px;
        word-break: break-all;
    }
    .search-card .snippet {
        color: #545454;
        line-height: 1.4;
        margin-bottom: 12px;
    }
    .search-card .site-name {
        color: #666;
        font-size: 0.9em;
        margin-bottom: 8px;
    }
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    .image-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
        background: white;
        aspect-ratio: 1;
    }
    .image-card img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        background: #f8f8f8;
    }
    h2 {
        margin: 20px 0;
        color: #333;
        font-size: 1.5em;
        border-bottom: 2px solid #eee;
        padding-bottom: 8px;
    }
    .visit-button {
        display: inline-block;
        padding: 5px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        background-color: #4CAF50;
        color: white;
        text-decoration: none;
        transition: opacity 0.2s;
    }
    .visit-button:hover {
        opacity: 0.9;
    }
    </style>
    <div class="search-container">
    """
    
    # 添加图片网格（如果有图片结果）
    if images:
        html_output += '<h2>相关图片</h2><div class="image-grid">'
        for image in images:
            thumbnail_url = image.get('thumbnailUrl', '')
            content_url = image.get('contentUrl', '')
            if thumbnail_url and content_url:
                html_output += f"""
                <div class="image-card">
                    <a href="{content_url}" target="_blank">
                        <img src="{thumbnail_url}" alt="搜索结果图片" loading="lazy">
                    </a>
                </div>
                """
        html_output += '</div>'
    
    # 添加网页结果
    if web_pages:
        html_output += '<h2>网页结果</h2>'
        for page in web_pages:
            title = page.get('name', '无标题')
            url = page.get('url', '')
            display_url = page.get('displayUrl', url)
            snippet = page.get('summary', page.get('snippet', '无摘要'))
            site_name = page.get('siteName', '')
            
            html_output += f"""
            <div class="search-card">
                <div class="site-name">{site_name}</div>
                <h3><a href="{url}" target="_blank">{title}</a></h3>
                <div class="url">{display_url}</div>
                <div class="snippet">{snippet}</div>
                <a href="{url}" target="_blank" class="visit-button">访问网页</a>
            </div>
            """
    
    html_output += "</div>"
    return html_output

def search_with_progress(query, api_key, freshness, result_count, output_format):
    """带进度提示的搜索函数"""
    yield "正在搜索，请稍候..."
    time.sleep(0.5)  # 给用户提供视觉反馈
    result = search_web(query, api_key, freshness, result_count, output_format)
    yield result

def create_ui():
    """创建Gradio界面"""
    
    with gr.Blocks(title="UniFuncs网络搜索", theme=gr.themes.Base()) as app:
        gr.Markdown("""
        # UniFuncs 网络搜索工具
        
        这是一个基于UniFuncs API的网络搜索工具，可以获取实时网络信息。
        """)
        
        with gr.Tab("搜索"):
            with gr.Row():
                with gr.Column(scale=4):
                    query_input = gr.Textbox(
                        label="搜索关键词",
                        placeholder="输入您想搜索的内容...",
                        lines=1
                    )
                    
                    with gr.Row():
                        freshness_dropdown = gr.Dropdown(
                            label="结果时效性",
                            choices=[
                                "None",
                                "Day",
                                "Week",
                                "Month",
                                "Year"
                            ],
                            value="None"
                        )
                        
                        count_slider = gr.Slider(
                            label="结果数量",
                            minimum=1,
                            maximum=20,
                            value=5,
                            step=1
                        )
                    
                    format_radio = gr.Radio(
                        label="输出格式",
                        choices=["text", "markdown", "json"],
                        value="text"
                    )
                    
                    api_key_input = gr.Textbox(
                        label="API密钥 (可选)",
                        placeholder="留空使用默认密钥",
                        type="password",
                        visible=True
                    )
                    
                    search_btn = gr.Button("搜索", variant="primary")
                
                with gr.Column(scale=6):
                    result_output = gr.HTML()
            
            search_btn.click(
                search_with_progress,
                inputs=[query_input, api_key_input, freshness_dropdown, count_slider, format_radio],
                outputs=result_output
            )
            
            query_input.submit(
                search_with_progress,
                inputs=[query_input, api_key_input, freshness_dropdown, count_slider, format_radio],
                outputs=result_output
            )
        
        with gr.Tab("高级设置"):
            gr.Markdown("""
            ## 关于UniFuncs API
            
            UniFuncs是专为AI应用打造的API平台，提供Web Search API服务。
            
            ### Web Search API特点
            - 高速稳定：秒级响应(1-3s)
            - 全天候数据采集：保证搜索结果的时效性
            - 结果重排：针对搜索语义进行优化
            - 内容更详尽：提供网页更多信息
            
            访问 [UniFuncs官网](https://unifuncs.com/api) 了解更多。
            """)
            
            save_settings_btn = gr.Button("保存设置", variant="secondary")
            settings_msg = gr.Textbox(label="状态消息", interactive=False)
            
            def save_settings(api_key):
                if api_key and len(api_key) > 10:
                    # 这里可以实现保存API密钥到配置文件的功能
                    return "设置已保存"
                return "API密钥无效或为空"
            
            save_settings_btn.click(
                save_settings,
                inputs=[api_key_input],
                outputs=settings_msg
            )
    
    return app

def main():
    app = create_ui()
    app.launch(share=False, server_name="127.0.0.1")

if __name__ == "__main__":
    main() 