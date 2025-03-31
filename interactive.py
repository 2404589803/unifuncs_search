#!/usr/bin/env python
# -*- coding: utf-8 -*-

from search_api import UniFuncsSearch

def interactive_search():
    """交互式命令行搜索界面"""
    
    print("="*50)
    print("  UniFuncs 网络搜索交互界面")
    print("="*50)
    
    # 创建搜索客户端
    search_client = UniFuncsSearch()
    
    while True:
        # 获取用户输入
        query = input("\n请输入搜索关键词 (输入q退出): ")
        
        if query.lower() in ('q', 'quit', 'exit'):
            print("\n谢谢使用，再见!")
            break
            
        if not query.strip():
            print("请输入有效的搜索关键词")
            continue
            
        # 获取时效性选择
        print("\n请选择搜索结果时效性:")
        print("1. 一天内")
        print("2. 一周内")
        print("3. 一个月内")
        print("4. 一年内")
        print("5. 不限")
        
        choice = input("请选择 (默认不限): ").strip()
        
        freshness_map = {
            "1": "Day",
            "2": "Week",
            "3": "Month",
            "4": "Year"
        }
        
        freshness = freshness_map.get(choice)
        
        # 获取结果数量
        count_input = input("\n请输入返回结果数量 (1-50，默认5): ").strip()
        try:
            count = int(count_input) if count_input else 5
            if count < 1 or count > 50:
                print("结果数量超出范围，使用默认值5")
                count = 5
        except ValueError:
            print("输入无效，使用默认值5")
            count = 5
            
        # 获取输出格式
        print("\n请选择输出格式:")
        print("1. 文本 (默认)")
        print("2. JSON")
        print("3. Markdown")
        
        format_choice = input("请选择: ").strip()
        
        format_map = {
            "1": "text",
            "2": "json",
            "3": "markdown"
        }
        
        output_format = format_map.get(format_choice, "text")
        
        # 执行搜索
        print("\n正在搜索，请稍候...\n")
        results = search_client.search(query, freshness, True, 1, count)
        formatted_results = search_client.format_results(results, output_format)
        
        # 显示结果
        print(formatted_results)
        
        # 询问是否保存结果
        save_choice = input("\n是否保存结果到文件? (y/n): ").lower()
        if save_choice == 'y':
            filename = input("请输入文件名: ")
            if not filename:
                print("未提供文件名，跳过保存")
            else:
                if '.' not in filename:
                    # 根据输出格式添加适当的扩展名
                    if output_format == "json":
                        filename += ".json"
                    elif output_format == "markdown":
                        filename += ".md"
                    else:
                        filename += ".txt"
                
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(formatted_results)
                    print(f"结果已保存到: {filename}")
                except Exception as e:
                    print(f"保存失败: {e}")

if __name__ == "__main__":
    interactive_search() 