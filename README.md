# Google Analytics Metrics Tools (FastMCP Integration)

This project provides a set of asynchronous tools to fetch user metrics from Google Analytics 4 using the [Google Analytics Data API](https://developers.google.com/analytics) and expose them via the [FastMCP](https://github.com/IntuitionMachine/FastMCP) framework.

## 🚀 Features

- Fetch **1-day**, **7-day**, **28-day**, or total **active users**.
- Optionally group results using supported **dimensions** (like country, platform, browser, etc.).
- Built using FastMCP – no API key required.
- Modular and easy to extend.

## 🧩 Tools Provided

- `get_active_users`: Fetch active users for a custom date range.
- `get_1_day_active_users`: Fetch users active in the last 1 day.
- `get_7_day_active_users`: Fetch users active in the last 7 days.
- `get_28_day_active_users`: Fetch users active in the last 28 days.

All tools support optional grouping by dimensions like `date`, `country`, `browser`, `platform`, etc.

## 📦 Installation

```bash
pip install fastmcp google-analytics-data

Execution commands:
server side = python server.py
client side = adk web --port 9000

Note : MCP Server and ADK LLM AGENT should be created in two separate windows
