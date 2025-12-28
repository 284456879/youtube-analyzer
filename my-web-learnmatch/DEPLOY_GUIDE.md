# 部署指南 (Deployment Guide)

本项目已经准备好部署到云平台（如 Render, Heroku 等）。以下是使用 [Render](https://render.com) 进行免费部署的步骤：

## 准备工作

1.  **代码推送**: 确保你已经将 `my-web-learnmatch` 文件夹内的代码推送到 GitHub 仓库。
    *   如果这是一个大仓库的子目录，你可能需要配置 "Root Directory"。
    *   建议：将 `my-web-learnmatch` 的内容作为一个新的 GitHub 仓库，或者在部署时指定根目录。

## 部署到 Render (推荐)

1.  注册并登录 [Render.com](https://render.com)。
2.  点击 **"New +"** 按钮，选择 **"Web Service"**。
3.  连接你的 GitHub 账号，并选择包含此代码的仓库。
4.  配置服务：
    *   **Name**: 给你的服务起个名字 (例如 `my-game-app`)。
    *   **Region**: 选择离你最近的节点 (例如 `Singapore` 或 `Oregon`)。
    *   **Branch**: 选择代码所在的分支 (通常是 `main` 或 `master`)。
    *   **Root Directory**: 输入 `my-web-learnmatch` (如果你的代码在这个子目录下)。
    *   **Runtime**: 选择 **Python 3**。
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`
5.  选择 **"Free"** 套餐。
6.  点击 **"Create Web Service"**。

Render 将会自动构建并部署你的应用。部署完成后，你会获得一个 `https://xxxx.onrender.com` 的网址，即可在网上访问你的应用。

## 注意事项

*   **数据库**: 本项目默认使用 SQLite (`games_v3.db`)。在 Render 的免费服务中，文件系统是临时的，这意味着**每次重新部署或重启后，数据库数据会重置**。
    *   如果需要永久保存数据，建议升级使用 Render 的 PostgreSQL 数据库，或者挂载 Render Disk（需要付费）。
*   **Python 版本**: Render 默认使用较新的 Python 版本。如果遇到版本问题，可以在 `my-web-learnmatch` 目录下创建一个 `runtime.txt` 文件，内容如 `python-3.9.18` 来指定版本。

## 本地测试生产环境运行

在部署前，你可以在本地模拟生产环境运行（需要安装 gunicorn，Windows下可能不支持 gunicorn，建议使用 waitress 或直接测试 Flask 开发服务器）：

```bash
# Windows 下通常直接用 python app.py 测试即可
python app.py
```
