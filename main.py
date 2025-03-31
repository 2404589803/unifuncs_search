#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UniFuncs 网络搜索工具主程序

可以运行以下几种模式：
1. 命令行模式 (cli)
2. 交互式模式 (interactive)
3. Web界面模式 (web)
"""

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="UniFuncs 网络搜索工具")
    parser.add_argument("mode", choices=["cli", "interactive", "web"], 
                        help="运行模式: 命令行(cli)、交互式(interactive)或Web界面(web)")
    
    parser.add_argument("query", nargs="?", 
                        help="搜索查询词 (仅在cli模式下使用)")
    parser.add_argument("-f", "--freshness", choices=["Day", "Week", "Month", "Year"], 
                        help="结果时效性 (仅在cli模式下使用)")
    parser.add_argument("-c", "--count", type=int, default=10, 
                        help="结果数量 (仅在cli模式下使用)")
    parser.add_argument("-o", "--output", choices=["text", "json", "markdown"], default="text", 
                        help="输出格式 (仅在cli模式下使用)")
    parser.add_argument("-s", "--save", 
                        help="将结果保存到文件 (仅在cli模式下使用)")
    parser.add_argument("-k", "--key", 
                        help="API密钥 (可用于所有模式)")
    
    # 解析命令行参数
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # 根据模式选择运行方式
    if args.mode == "cli":
        from cli import main as cli_main
        sys.argv = [sys.argv[0]] + sys.argv[2:]  # 调整参数以适应cli.py的解析
        cli_main()
    
    elif args.mode == "interactive":
        from interactive import interactive_search
        if args.key:
            os.environ["UNIFUNCS_API_KEY"] = args.key
        interactive_search()
    
    elif args.mode == "web":
        from web_ui import main as web_main
        if args.key:
            os.environ["UNIFUNCS_API_KEY"] = args.key
        web_main()

if __name__ == "__main__":
    main() 