# 📊 Pre Configged Dashboard

This repo contains the configuration files for a **self-hosted personal dashboard** using [Glance](https://github.com/glanceapp/glance), a lightweight startpage and monitoring tool.

It includes two main pages:
- **Startpage** (general tools and monitoring)
- **Finance** (custom finance visualizations and RSS feeds)

The goal is to have a **fast-loading, centralized homepage** to monitor services, manage bookmarks, visualize financial data, and stay up-to-date with curated feeds.

---

## 📂 Structure Overview

### `glance.yml`
- Core configuration file for Glance.
- Defines:
  - `server.assets-path`: where custom static assets like CSS live.
  - `theme.custom-css-file`: path to your custom styles (`/assets/user.css`).
  - `pages`: imports two page definitions:
    - `startpage.yml`
    - `finance.yml`
-  
> **Note:**  
> The `finance.yml` page references **iframe widgets** that expect a running instance of **pyNance Dashroad** on `http://localhost:3353`.  
> If the pyNance server is **not** running, those iframe sections will appear **blank**.

---

### `startpage.yml`
- A simple **landing page** focusing on quick search, service monitoring, and bookmarks.

**Widgets:**
- `search`  
  - Standard search bar with autofocus.
- `monitor`
  - Monitors key services running on localhost (e.g., Jellyfin, Sonarr, qBittorrent).
- `bookmarks`
  - Grouped into:
    - **Systems** (launchpads, admin panels)
    - **Finance** (finance dashboards and banking links)
    - **Other** (OpenAI, GitHub, ChatGPT)

**Purpose:**  
Quickly access commonly used apps and systems, with real-time service availability at a glance.

---

### `finance.yml`
- A **finance-focused page** to visualize personal finance metrics, monitor markets, and view curated financial news.

**Widgets:**
- `calendar`
  - Weekly calendar view (starting Monday).
- `rss`
  - Pulls articles from:
    - Hacker News
    - Ars Technica
    - Lobsters
    - Personal tech blogs (e.g., Josh Comeau, Ahmad Shadeed)
- `iframe`
  - Loads live dashboards from pyNance Dashroad:
    - Net worth (month-to-date)
    - Assets vs. Liabilities
    - Category breakdowns
    - Other custom financial widgets
- `markets`
  - Tracks real-time quotes for:
    - S&P 500 (SPY)
    - Bitcoin (BTC-USD)
    - Nvidia (NVDA)
    - Apple (AAPL)
    - Microsoft (MSFT)
- `releases`
  - Monitors new releases for selected GitHub repos (e.g., glanceapp, gitea, immich, syncthing).

**Purpose:**  
Centralized financial visibility and market tracking alongside curated tech/finance news.

---

## ⚡ Requirements
- [Glance](https://github.com/glanceapp/glance) running on your machine or server
- (Optional) [pyNance Dashroad](https://github.com/your-username/pynance) if you want the financial iframes to display content.
- Basic Docker setup or local development environment for running supporting services (Jellyfin, Sonarr, etc.).

---

## 🔧 Setup

1. Install and run Glance.
2. Point Glance to the `glance.yml` configuration file.
3. Make sure your services (e.g., Jellyfin, pyNance Dashroad) are running at the specified ports.
4. Optionally customize the bookmarks, RSS feeds, or services list.

---

## 📌 Notes

- Private IPs have been replaced with `http://localhost` so this repo is **safe for public sharing**.
- Some iframe sections (finance metrics) **depend on external services** — they won't load if the service is not running locally.
- Custom styles are referenced via `/assets/user.css`. Make sure you add or update that file if you want to modify the dashboard appearance.

---

# ✨ Example Screenshot
_(Optional section: Add a screenshot here later if you want to showcase your dashboard layout.)_
"""

with open("/mnt/data/README.md", "w") as f:
    f.write(readme_content)

"/mnt/data/README.md"

