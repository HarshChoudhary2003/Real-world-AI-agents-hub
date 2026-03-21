# 🛡️ Log-Sentinel AI (Log Anomaly Detection)

Perform deep heuristic analysis on system logs to detect anomalies, security threats, and performance regressions with neural telemetry audits.

## 🚀 Overview
**Log-Sentinel AI v2.0** is an enterprise-grade Systems Reliability & Cyber-Forensics OS. It moves beyond simple keyword matching, using multi-model intelligence to identify **behavioral anomalies**, calculate **System Health Indexes**, and architect **SRE Response Blueprints** for system architects and Dev-Ops teams.

## ⚡ Key Features
- **Neural Health Indexing**: Calculates a real-time health score (0-100) based on log signal frequency, severity, and context.
- **Heuristic Anomaly Detection**: Identifies unusual patterns, auth-failure spikes, or protocol-level regressions that standard monitors miss.
- **SRE Response Plan**: Automatically generates a "Blueprint" of strategic investigation steps for any detected incident.
- **Security Threat Mapping**: Specifically flags potential intrusion attempts, PII leaks, or administrative deviations.
- **Multi-Provider Architecture**: Choose your intelligence brain from OpenAI, Gemini, Claude, DeepSeek, or Groq.

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Premium Creative UI with Animated Health Gauge)
- **Intelligence**: LiteLLM (Multi-model support)
- **Data Protocols**: JSON for forensic telemetry export, TXT for SRE brief summaries.

## 📂 Structure
- `agent.py`: Core heuristic engine and multi-provider CLI wrapper.
- `app.py`: Premium animated Streamlit dashboard with incident diagnostics.
- `logs.txt`: Sample system telemetry logs for testing.
- `requirements.txt`: Project dependencies.

## 🚀 Quick Launch

### 1. CLI Usage
```bash
python agent.py
```

### 2. Dashboard Usage
```bash
streamlit run app.py
```

## 📊 Strategic Output
The agent outputs a structured JSON analysis including:
- **Sentinel Assessment**: A numerical health index, a status verdict, and a technical diagnostic summary.
- **Incident Diagnostics**: Detected events with their signatures, frequencies, and technical impacts.
- **Security Alerts**: Identification of high-risk patterns in the system logs.

---
*Part of the [Real-world-AI-agents-hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub)*
