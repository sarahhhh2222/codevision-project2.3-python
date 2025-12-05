# 🛒 Mini Home Market Intelligence System

## 📌 Overview
*Mini Home Market Intelligence* is an automated Python-based system designed to monitor competitor prices (e.g., IKEA) in real-time. The system scrapes product data, stores it in a database, and alerts the business owner if prices drop below a specific threshold, enabling smart pricing strategies.

## 🚀 Key Features
* *Real-time Scraping:* Uses *Playwright* for fast and reliable data extraction from dynamic websites.
* *Smart Database Storage:* Uses *SQLAlchemy ORM* with *SQLite* to manage data efficiently.
* *CRUD Operations:* Fully implements Create, Read, Update, and Delete operations for data management.
* *Automated Scheduling:* Runs a continuous monitoring loop (checks every 10 seconds).
* *Price Alerts:* Triggers alerts when competitor prices fall below the target price.

## 🛠 Technology Stack
* *Language:* Python 3.x
* *Web Scraping:* Playwright
* *Database:* SQLite + SQLAlchemy ORM
* *Architecture:* OOP, Abstract Base Classes (ABC), DataClasses

## 👥 Development Team
* *SHAMS BUKHARI*
* *JUWAN ALQARNI*
* *SARAH ALZUBAIRI*
* *Abdulilah Al Rifai*
* *Rahaf Ali*

---

## Setup & Installation
# *How to Run This Project:*
## Make sure Python 3.8+ is installed.

## Check using:
python --version

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/MiniHome-Market-Monitor.git](https://github.com/YourUsername/MiniHome-Market-Monitor.git)
cd MiniHome-Market-Monitor

### 2. Install Required Libraries
We use sqlalchemy for the database and playwright for scraping.
```bash
pip install sqlalchemy playwright
# Run the following commands in your terminal:
pip install sqlalchemy playwright
playwright install
