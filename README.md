# 🎰 Gambling Products Unifier with CrewAI

## 📌 Project Overview
This project is an **internship assignment for CrowdWisdomTrading**.  
It is a **backend Python script using CrewAI** that scrapes prediction/gambling market data from multiple websites, unifies products, compares their prices, and generates structured outputs with confidence levels.  

---

## ⚙️ Tech Stack
- **Language**: Python 3.11+  
- **Framework**: [CrewAI](https://github.com/crewAIInc/crewAI) (latest)  
- **Tools**: `browser-use`, `litellm`, `RAG`  
- **Output Formats**: JSON, CSV  

---

## 🤖 Agent Workflow
### 🔹 Agent 1: Data Collector
- Scrapes data from at least 3 gambling/prediction sites (e.g. `polymarket.com`, `kalshi.com`, `prediction-market.com`)  
- Outputs structured data in **JSON**  

### 🔹 Agent 2: Product Identifier
- Analyzes collected data  
- Identifies and unifies products across websites  
- Outputs unified results in **JSON**  

### 🔹 Agent 3: Data Formatter
- Re-arranges unified data into a final format  
- Generates a **CSV file** with:  
  - Unified product list  
  - Prices across sites  
  - Confidence level for product matching  

---

## 📂 Project Scope
- Scrape market/product data from multiple sources  
- Build a **unified product comparison board**  
- Use **CrewAI Flow with guardrails** for multi-agent execution  
- Produce structured JSON + CSV outputs  

---

## 📑 Deliverables
- ✅ Python script with CrewAI implementation  
- ✅ Example input/output data  
- ✅ CSV file with unified products and confidence levels  
- ✅ Documentation (this README)  

---

## 📝 Example Output (CSV)

| Product Name         | Polymarket | Kalshi | Prediction-Market | Confidence Level |
|----------------------|------------|--------|-------------------|------------------|
| Election 2024 Winner | $0.55      | $0.57  | $0.56             | 92%              |
| BTC > 70K by Dec     | $0.48      | $0.50  | $0.49             | 88%              |

---

## 🚀 Extra Features
- Logging & error handling  
- Chatting with the RAG about products  
- Modular & clean code structure  

---

## 📌 References
- [CrewAI Quickstarts](https://github.com/crewAIInc/crewAI-quickstarts)  
- [CrewAI Crash Course](https://github.com/codebasics/crewai-crash-course)  
- [AI Crew Tutorial](https://medium.com/@ShaniCodes/so-i-built-my-own-social-media-ai-crew-because-i-didnt-want-to-pay-for-jasper-ai-40a279ffe89a)  

---

## 📧 Submission
- GitHub repo link  
- Example outputs (JSON + CSV)  
- Short demo video of script execution  

---

