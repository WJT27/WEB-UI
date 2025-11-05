🧩 Web UI 自动化测试框架 (Python + Selenium + Pytest + Allure)
📘 项目简介

本项目是一个基于 Python + Selenium + Pytest + Allure 的 Web UI 自动化测试框架，
实现了浏览器驱动统一管理、页面对象封装（POM）、数据驱动测试、日志记录与 Allure 报告集成。
适用于企业级 Web 系统的 UI 自动化测试场景。

📁 目录结构
Py_Selenium/
│
├── config/
│   └── config.json                # 全局配置文件
│
├── utils/
│   ├── config.py                  # 加载配置
│   ├── logger.py                  # 日志封装
│   └── browser_factory.py         # 浏览器驱动工厂
│
├── pages/
│   ├── base_page.py               # 基础页面操作封装
│   └── login_page.py              # 登录页面对象
│
├── tests/
│   └── test_login.py              # 示例测试用例
│
├── reports/
│   └── allure_results/            # Allure 报告生成目录
│
├── conftest.py                    # Pytest 全局配置与 Hooks
└── pytest.ini                     # Pytest 配置文件

⚙️ 环境依赖
依赖项	版本	说明
Python	≥3.8	运行环境
Selenium	≥4.0	UI 自动化核心库
Pytest	≥7.0	测试框架
Allure-pytest	≥2.9	报告生成
webdriver-manager	≥4.0	自动管理浏览器驱动
🧩 安装依赖

在项目根目录下执行：

pip install -r requirements.txt


若你没有 requirements.txt，可使用以下命令生成：

pip freeze > requirements.txt

🧠 主要功能

✅ 页面对象模式（POM）
将每个页面的元素与操作独立封装，减少代码重复，提高可维护性。

✅ 数据驱动测试（Data Driven）
支持通过 pytest.mark.parametrize 参数化多组测试数据。

✅ 日志记录（Logging）
自动生成日志文件，并在控制台与 Allure 报告中输出关键信息。

✅ 失败截图与 Allure 集成
当用例失败时自动截图，并附加到 Allure 报告中。

✅ 灵活配置（config.json）
支持切换浏览器类型、是否开启无头模式、目标 URL 等。

🚀 运行测试
方式一：直接运行 Pytest
pytest

方式二：生成 Allure 报告
pytest --alluredir=reports/allure_results
allure serve reports/allure_results

🧾 示例输出

执行成功后，命令行输出如下：

[INFO] 启动浏览器 Chrome
[INFO] 开始登录：用户名=testUser01
[INFO] 登录操作已提交


在 Allure 报告中将展示：

测试步骤（Steps）

参数数据（Parameters）

截图（Screenshots）

日志（Logs）

🧑‍💻 作者与说明

作者： jt W
框架语言： Python 3
测试框架： Pytest + Selenium + Allure
主要用途： Web UI 自动化测试框架搭建与实践