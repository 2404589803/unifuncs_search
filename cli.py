#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
from search_api import UniFuncsSearch

def main():
    parser = argparse.ArgumentParser(description="UniFuncs Web搜索API客户端")
    parser.add_argument("query", nargs="?", help="搜索查询词")
    parser.add_argument("-k", "--key", help="API密钥")
    parser.add_argument("-f", "--freshness", choices=["Day", "Week", "Month", "Year"], help="结果时效性")
    parser.add_argument("-p", "--page", type=int, default=1, help="页码")
    parser.add_argument("-c", "--count", type=int, default=10, help="每页结果数量")
    parser.add_argument("-o", "--output", choices=["text", "json", "markdown"], default="text", help="输出格式")
    parser.add_argument("-s", "--save", help="将结果保存到文件")
    
    args = parser.parse_args()
    
    # 创建搜索客户端
    search_client = UniFuncsSearch(args.key)
    
    if not args.query:
        # 如果没有通过命令行参数提供查询，则提示用户输入
        query = input("请输入搜索关键词: ")
        if not query.strip():
            print("错误: 未提供搜索关键词")
            sys.exit(1)
    else:
        query = args.query
    
    # 执行搜索
    results = search_client.search(
        query=query,
        freshness=args.freshness,
        page=args.page,
        count=args.count
    )
    
    # 格式化结果
    formatted_output = search_client.format_results(results, args.output)
    
    # 输出或保存结果
    if args.save:
        try:
            with open(args.save, "w", encoding="utf-8") as f:
                f.write(formatted_output)
            print(f"搜索结果已保存到: {args.save}")
        except Exception as e:
            print(f"保存结果时出错: {e}")
            print(formatted_output)
    else:
        print(formatted_output)

if __name__ == "__main__":
    main() 