import streamlit as st
import json
import re

st.set_page_config(
    page_title="Agent OS | Elite Edition",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CATEGORIES_RAW = {
    "\ud83d\udcbc Business Operations Systems": [
        {
            "name": "\ud83e\uddec DataForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/CRM%20data%20enrichment%20agent",
            "desc": "Intelligence-led CRM enrichment & decision mapping."
        },
        {
            "name": "\ud83d\udcc4 InvoiceIntel",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Invoice%20processing%20agent",
            "desc": "Multi-model Vision layer for financial document extraction."
        },
        {
            "name": "\ud83c\udfaf LeadScore AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Lead%20qualification%20agent",
            "desc": "Precision lead qualification via BANT/CHAMP frameworks."
        },
        {
            "name": "\ud83e\udd1d SalesFollowAI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Sales%20follow-up%20agent",
            "desc": "High-conversion post-interaction narrative generator."
        },
        {
            "name": "\ud83d\udee1\ufe0f SupportCraft",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Customer%20support%20response%20agent",
            "desc": "Empathetic response intelligence & sentiment auditing."
        },
        {
            "name": "\ud83d\udcb8 ExpenseIQ",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Expense%20categorization%20agent",
            "desc": "Algorithmic category detection & anomaly audit."
        },
        {
            "name": "\ud83d\udccb SOPFlow AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Internal%20SOP%20generator%20agent",
            "desc": "Standardized Ops Architect for scaling procedures."
        },
        {
            "name": "\ud83d\udcb9 InsightCore",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/KPI%20dashboard%20insight%20agent",
            "desc": "Strategic KPI narrative & causality diagnostic."
        },
        {
            "name": "\ud83d\udcd1 ClauseClear",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Contract%20clause%20explanation%20agent",
            "desc": "Advanced legal plain-language engine & risk auditor."
        },
        {
            "name": "\u2696\ufe0f VendorFlow AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Vendor%20comparison%20agent",
            "desc": "Strategic vendor comparative analysis grid."
        }
    ],
    "\ud83e\uddea Marketing & Growth Systems": [
        {
            "name": "\ud83c\udfa8 AdForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Ad%20copy%20generator%20agent",
            "desc": "Growth-studio with persona simulation logic."
        },
        {
            "name": "\ud83d\udcc8 AdIntel AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Campaign%20performance%20analysis%20agent",
            "desc": "Budget utility auditor & leaky bucket detector."
        },
        {
            "name": "\ud83e\uddea OptiTest AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/A%20B%20test%20suggestion%20agent",
            "desc": "Strategic A/B test architect with ICE scoring."
        },
        {
            "name": "\ud83d\udee1\ufe0f Persona-Forge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Customer%20persona%20builder%20agent",
            "desc": "Market data synthesis & customer architect."
        },
        {
            "name": "\u26a1 Funnel-Force",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Funnel%20optimization%20agent",
            "desc": "Performance diagnostic & conversion strategy."
        },
        {
            "name": "\ud83d\udce9 Email-Mind",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Email%20marketing%20agent",
            "desc": "High-conversion multi-model copywriting."
        },
        {
            "name": "\ud83e\udd1d Influence-Core",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Influencer%20outreach%20agent",
            "desc": "Relationship-first influencer outreach engine."
        },
        {
            "name": "\ud83d\ude80 Launch-Pad AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Product%20launch%20checklist%20agent",
            "desc": "GTM operational readiness & launch architecture."
        },
        {
            "name": "\ud83d\udcc5 Social-Sync",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Social%20media%20scheduling%20agent",
            "desc": "Cross-platform orchestration & scheduling."
        },
        {
            "name": "\ud83c\udfad Voice-Verify",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Brand%20voice%20consistency%20agent",
            "desc": "Brand voice & linguistic integrity audit."
        }
    ],
    "\ud83d\udcca Data & Automation Systems": [
        {
            "name": "\ud83e\uddec NeuralData AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/CSV%20data%20cleaning%20agent",
            "desc": "Multi-cloud batch CSV cleaning & integrity auditing."
        },
        {
            "name": "\ud83d\udd22 Sheet-Logic AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Spreadsheet%20formula%20generator%20agent",
            "desc": "Multinational spreadsheet formula & logic architect."
        },
        {
            "name": "\ud83d\udee1\ufe0f Data-Guard AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Data%20validation%20agent",
            "desc": "Neural dataset integrity & schema governance."
        },
        {
            "name": "\ud83d\udd0c API-Insight",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/API%20response%20interpreter%20agent",
            "desc": "Neural API response forensic & interpreter."
        },
        {
            "name": "\ud83d\udee1\ufe0f Log-Sentinel",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Log%20anomaly%20detection%20agent",
            "desc": "System telemetry forensic & anomaly detection."
        },
        {
            "name": "\ud83c\udfbc Orchestra-Core",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Workflow%20orchestration%20agent",
            "desc": "Multi-step execution architecture for complex missions."
        },
        {
            "name": "\ud83d\udcbe Pipeline-Forge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/ETL%20pipeline%20design%20agent",
            "desc": "High-performance ETL & cloud data architect."
        },
        {
            "name": "\ud83d\ude91 Error-Forensics",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Error%20classification%20agent",
            "desc": "SRE incident diagnosis & error classification."
        },
        {
            "name": "\ud83d\udcca Alert-Insight",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Monitoring%20alert%20explanation%20agent",
            "desc": "Monitoring alert translation & root-cause diagnostic."
        },
        {
            "name": "\ud83c\udfd7\ufe0f Auto-Strategist",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Automation%20recommendation%20agent",
            "desc": "Process mining & high-ROI automation strategist."
        }
    ],
    "\ud83e\udde0 Personal Productivity Systems": [
        {
            "name": "\ud83e\udde0 PriorityBrain",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/daily-priority-agent",
            "desc": "NLP task ingestion & algorithmic urgency sorting."
        },
        {
            "name": "\ud83d\uddc4\ufe0f BrainVault",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Personal%20knowledge%20base%20agent",
            "desc": "Local RAG knowledge base via vector space."
        },
        {
            "name": "\u26a1 ActionForge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Note-to-action%20item%20agent",
            "desc": "Unstructured text-to-task neural extraction."
        },
        {
            "name": "\ud83d\udce7 MailMind AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Email%20summarization%20agent",
            "desc": "Intelligent thread logic & summary mapping."
        },
        {
            "name": "\ud83d\udcc5 SyncGuard",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Calendar%20conflict%20resolver%20agent",
            "desc": "Conflict detection & resolution engine."
        },
        {
            "name": "\ud83d\udccb AgendaCraft",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Meeting%20agenda%20generator%20agent",
            "desc": "High-fidelity meeting timeline architect."
        },
        {
            "name": "\ud83e\uddd8 Reflect AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Daily%20goal%20reflection%20agent",
            "desc": "Algorithmic daily target analytics."
        },
        {
            "name": "\ud83d\udd14 PingCraft",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Smart%20reminder%20agent",
            "desc": "Distributed deadline alerting engine."
        },
        {
            "name": "\u23f3 ChronoBlock",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Time-blocking%20planner%20agent",
            "desc": "Continuous task packing logic planner."
        },
        {
            "name": "\ud83d\udd25 StreakForge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Habit%20tracking%20agent",
            "desc": "Persistence density metrics & habit tracking."
        }
    ],
    "\ud83e\udd16 Work & Life Automation Systems": [
        {
            "name": "\ud83c\udfaf Goal Breakdown Architect",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Goal%20Breakdown%20Agent",
            "desc": "ProductivityOS: Precision Strategic Planning & Roadmap Deconstruction."
        },
        {
            "name": "\u26a1 Smart Task Planner",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Smart%20Task%20Planner%20Agent",
            "desc": "ProductivityOS: High-Performance Daily Strategy & Time-Blocking."
        },
        {
            "name": "\ud83d\udcc5 Calendar Scheduler",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Calendar%20Scheduling%20Agent",
            "desc": "Autonomous meeting architect & time-node optimizer."
        },
        {
            "name": "\ud83c\udfaf Focus Coach",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Focus%20Coach%20Agent",
            "desc": "ProductivityOS: Flow-State Orchestration & Pomodoro Strategy."
        },
        {
            "name": "\ud83d\udcdd Meeting Notes Agent",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Meeting%20Notes%20Agent",
            "desc": "ProductivityOS: Strategic Meeting Deconstruction & Action Tracking."
        },
        {
            "name": "\ud83d\udce7 Email Assistant",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Email%20Assistant%20Agent",
            "desc": "ProductivityOS: AI Email Architect & Tactical Communication engine."
        },
        {
            "name": "\ud83d\udcca Daily Reflection",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Daily%20Reflection%20Agent",
            "desc": "ProductivityOS: Self-Improving AI System & Habit-Loop Optimizer."
        },
        {
            "name": "\ud83d\udcda Knowledge Summarizer",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Knowledge%20Summarizer%20Agent",
            "desc": "ProductivityOS: High-Fidelity Knowledge Synthesis & Learning Accelerator."
        },
        {
            "name": "\ud83d\udd25 Habit Builder",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Habit%20Builder%20Agent",
            "desc": "ProductivityOS: Behavior Change Architecture & Dopamine-Led Consistency."
        },
        {
            "name": "\u2696\ufe0f Decision Intelligence",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Work%20&%20Life%20Automation%20AI%20Agents/Decision%20Agent",
            "desc": "ProductivityOS: Strategic Choice Architecture & Risk Synthesis."
        }
    ],
    "\ud83d\udcbc Career & Income Automation Systems": [],
    "\ud83d\udcbc CareerOS: The AI Operating System for Career & Income Automation": [
        {
            "name": "\ud83d\udcbc Resume Forge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Resume%20Optimizer%20Agent",
            "desc": "Expert ATS optimization & resume synchronization engine."
        },
        {
            "name": "\u2709\ufe0f Cover Letter AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Cover%20Letter%20Generator%20Agent",
            "desc": "Strategic, job-specific tailored cover letter architect."
        },
        {
            "name": "\ud83d\udd0e Job Finder Agent",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Job%20Finder%20Agent",
            "desc": "Real-time job extraction and AI match scoring hub."
        },
        {
            "name": "\ud83e\udd16 Auto Apply Agent",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Auto%20Apply%20Agent",
            "desc": "Advanced multi-agent orchestrator for automated application prep."
        },
        {
            "name": "\ud83c\udf99\ufe0f Interview Simulator",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Interview%20Simulator%20Agent",
            "desc": "High-fidelity interactive interview prep and evaluation hub."
        },
        {
            "name": "\ud83e\udde0 Skill Gap Analyzer",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Skill%20Gap%20Analyzer%20Agent",
            "desc": "Strategic AI node to identify missing skills and generate learning paths."
        },
        {
            "name": "\ud83d\udcda Learning Roadmap",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Learning%20Roadmap%20Agent",
            "desc": "Personalized 90-day mastery blueprint for target career roles."
        },
        {
            "name": "\ud83d\udcb0 Freelance Proposal AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Freelance%20Proposal%20Agent",
            "desc": "Expert high-conversion proposal architect for global gig platforms."
        },
        {
            "name": "\ud83d\udcc8 Salary Negotiation AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Salary%20Negotiation%20Agent",
            "desc": "High-leverage compensation coach for market-based offer optimization."
        },
        {
            "name": "\ud83d\udcca Profit.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Freelance%20Project%20Profitability%20Predictor",
            "desc": "Strategic freelance project analytics."
        },
        {
            "name": "\ud83c\udf10 Personal Brand AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Career%20&%20Income%20Automation%20AI%20Agents/Personal%20Branding%20Agent",
            "desc": "Digital identity strategist to architect authority-driven presence."
        }
    ],
    "\ud83d\udd2c Research & Analysis Systems": [
        {
            "name": "\ud83d\udd2c SWOT Horizon",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/SWOT%20analysis%20agent",
            "desc": "TOWS matrix & strategic opportunity analysis."
        },
        {
            "name": "\ud83c\udf10 Web Research",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Web%20research%20agent",
            "desc": "Autonomous multi-model executive research."
        },
        {
            "name": "\ud83c\udfac StreamBrief",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/YouTube%20video%20summary%20agent",
            "desc": "Neural video transcript distiller & insight mapper."
        },
        {
            "name": "\ud83d\udcb0 CapitalMind",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Investment%20thesis%20generator%20agent",
            "desc": "Evidence-driven investment thesis architect."
        },
        {
            "name": "\ud83d\udcb9 TrendSynthetix",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Market%20trend%20summarization",
            "desc": "Market context trend deconstruction."
        },
        {
            "name": "\ud83d\udcf0 NewsFlow",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/News%20aggregation%20agent",
            "desc": "Global thematic news intelligence digests."
        },
        {
            "name": "\u2696\ufe0f PolicyGuard",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Policy%20document%20summarizer%20agent",
            "desc": "Thematic synthesis for regulatory frameworks."
        }
    ],
    "\u270d\ufe0f Writing & Content Systems": [
        {
            "name": "\ud83d\udcdd Blog Architect",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Blog%20post%20generator%20agent",
            "desc": "SEO-optimized post pipeline."
        },
        {
            "name": "\ud83d\udcbc CoverCraft",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Cover%20letter%20writing%20agent",
            "desc": "Job-specific tailored cover letter architect."
        },
        {
            "name": "\ud83d\udcac AI FAQ Gen",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/FAQ%20generation%20agent",
            "desc": "Credentialed FAQ generator."
        },
        {
            "name": "\u2728 GrammarPlus",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Grammar%20correction%20agent",
            "desc": "Semantic deep-edit & tone correction."
        },
        {
            "name": "\ud83d\udd17 HookGen Pro",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/LinkedIn%20post%20ideation%20agent",
            "desc": "LinkedIn post & hook ideation studio."
        },
        {
            "name": "\ud83d\udecd\ufe0f ProductCopy",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Product%20description%20agent",
            "desc": "Outcome-driven product descriptions."
        },
        {
            "name": "\ud83d\udcc4 ResumeAI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Resume%20optimization%20agent",
            "desc": "ATS-optimized enhancement engine."
        },
        {
            "name": "\ud83d\udd0e SEOClusters",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/SEO%20keyword%20expansion%20agent",
            "desc": "Predictive keyword expansion clusters."
        },
        {
            "name": "\ud83d\udcfd\ufe0f SlideForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Script-to-slide%20outline%20agent",
            "desc": "Script-to-slide visual architect."
        },
        {
            "name": "\ud83c\udfad ToneWizard",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Tone%20rewriting%20agent",
            "desc": "Multi-persona voice rewriter."
        }
    ],
    "\ud83d\udee0\ufe0f AI & Engineering Systems": [
        {
            "name": "\ud83e\udde0 ModelMind AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Model%20comparison%20agent",
            "desc": "Deep architectural trade-off analysis."
        },
        {
            "name": "\u2728 PromptForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Prompt%20optimization%20agent",
            "desc": "Neural prompt engineering & linguistic structure optimization."
        },
        {
            "name": "\ud83d\udd0d SemanticForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/RAG%20document%20retrieval%20agent",
            "desc": "Orchestrated RAG document & contextual semantic retrieval."
        },
        {
            "name": "\u26a1 ToolForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Tool-calling%20agent",
            "desc": "Autonomous tool-call orchestration with multi-tool execution registry."
        },
        {
            "name": "\ud83e\udde9 ThinkForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Multi-step%20reasoning%20agent",
            "desc": "Structured multi-step decomposition & chain-of-thought reasoning engine."
        },
        {
            "name": "\ud83d\udee0\ufe0f CleanCode AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Code%20refactoring%20agent",
            "desc": "Advanced syntax architectural transformation & best practice adherence refactoring engine."
        },
        {
            "name": "\ud83d\udc1b BugSentinel AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Bug%20explanation%20agent",
            "desc": "Neural traceback analysis & root cause diagnostic forensics."
        },
        {
            "name": "\ud83d\udcd6 DocForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/API%20documentation%20agent",
            "desc": "Automated deterministic REST API schema documentation & contract logic compiler."
        },
        {
            "name": "\ud83e\uddea TestForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Test%20case%20generation%20agent",
            "desc": "Rigorous test suite & edge case regression validation framework."
        },
        {
            "name": "\ud83c\udfd7\ufe0f ArchForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/System%20architecture%20explainer%20agent",
            "desc": "Topological data-flow extraction & implicitly derived trade-off analytical engine."
        },
        {
            "name": "\ud83d\udcbb DevOS Architect",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20Agents%20for%20Developers%20&%20Builders/Code%20Generator%20Agent",
            "desc": "Universal code architect for multi-file project generation & rapid prototyping."
        },
        {
            "name": "\ud83d\udc1b DevOS Debugger",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20Agents%20for%20Developers%20&%20Builders/Debugging%20Agent",
            "desc": "Universal code debugger for multi-language logic analysis & automated bug isolation."
        }
    ],
    "\ud83d\uddc4\ufe0f HR, Legal & Compliance Systems": [
        {
            "name": "\ud83d\udcbc TalentForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Job%20description%20generator%20agent",
            "desc": "Inclusive requisition & job description intelligence pipeline."
        },
        {
            "name": "\ud83d\udd0e ScreenGenius Pro AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Candidate%20screening%20agent",
            "desc": "Multi-axis algorithmic candidate screening matrix with red-flag detection & custom interview probes."
        },
        {
            "name": "\ud83c\udf99\ufe0f QuestForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Interview%20question%20generator%20agent",
            "desc": "Autonomous technical interview question architect."
        },
        {
            "name": "\ud83d\udcc8 ReviewForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Performance%20review%20agent",
            "desc": "Professional tone synthesis and constructive performance appraisal engine."
        },
        {
            "name": "\u2696\ufe0f ComplianceGuard AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Policy%20compliance%20checker%20agent",
            "desc": "Automated enterprise policy enforcement & liability prevention matrix."
        },
        {
            "name": "\u26a0\ufe0f RiskForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Risk%20assessment%20agent",
            "desc": "Threat modeling architecture resolving operational and deployment liabilities conditionally."
        },
        {
            "name": "\ud83d\udee1\ufe0f BriefForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Legal%20clause%20summarization%20agent",
            "desc": "Legal clause syntactic translation mechanism into executive language logic."
        },
        {
            "name": "\ud83d\udd10 PrivacyForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Data%20privacy%20explanation%20agent",
            "desc": "Contextual data privacy regulation compliance matrix mapping features to legal bounds."
        },
        {
            "name": "\ud83c\udf93 SkillForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Training%20content%20generator%20agent",
            "desc": "Auto-architected corporate learning & objective enablement module generator."
        },
        {
            "name": "\ud83d\udccb AuditForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Audit%20preparation%20agent",
            "desc": "Pre-audit readiness scanner identifying critical evidence gaps and mandatory remediations."
        }
    ],
    "\ud83d\udcb0 Finance & Decision Making Systems": [
        {
            "name": "\ud83d\udcca BudgetForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Budget%20planning%20agent",
            "desc": "Intelligent capital allocation & goal-aligned budgeting."
        },
        {
            "name": "\ud83c\udf0a FlowForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Cash%20flow%20forecasting%20agent",
            "desc": "Autonomous liquidity architect & predictive cash flow modeling."
        },
        {
            "name": "\ud83c\udff7\ufe0f PriceForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Pricing%20strategy%20agent",
            "desc": "Strategic economic architect & value-based pricing optimization."
        },
        {
            "name": "\ud83d\udcc9 OptiForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Cost%20optimization%20agent",
            "desc": "Autonomous efficiency architect & predictive cost optimization."
        },
        {
            "name": "\ud83d\udcc8 RevForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Revenue%20breakdown%20agent",
            "desc": "Strategic revenue architect & structural performance auditor."
        },
        {
            "name": "\ud83d\udd75\ufe0f FinLens AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Financial%20report%20explainer%20agent",
            "desc": "JARVIS-grade neural auditor & predictive report explainer."
        },
        {
            "name": "\ud83d\udd2e SimuForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Scenario%20analysis%20agent",
            "desc": "Futuristic scenario engine & neural projection architect."
        },
        {
            "name": "\ud83e\udde0 RiskVault AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Investment%20risk%20agent",
            "desc": "Graph-based neural auditor & predictive investment risk engine."
        },
        {
            "name": "\ud83e\ude99 SentimentCore AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Crypto%20market%20sentiment%20agent",
            "desc": "Apple-level neural brain & predictive crypto sentiment architect."
        },
        {
            "name": "\ud83e\uddec StrategyLens AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Finance%20%20&%20%20Decision%20Making%20Agents/Trading%20strategy%20explanation%20agent",
            "desc": "Unicorn-grade neural auditor & predictive trading logic explainer."
        }
    ],
    "\ud83c\udfa8 Advanced & Creative Agents": [
        {
            "name": "\ud83d\udca0 Orchestra.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Multi-agent%20collaboration%20system",
            "desc": "Autonomous multi-agent orchestration for mission-critical collaboration."
        },
        {
            "name": "\ud83e\udde0 Decision AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Autonomous%20decision%20agent",
            "desc": "Neural decision-making framework with trade-off analysis."
        },
        {
            "name": "\ud83d\udce1 Sentinel.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Long-running%20monitoring%20agent",
            "desc": "Persistent telemetry monitor & autonomous threshold sentinel."
        },
        {
            "name": "\u2696\ufe0f Governance.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Human-in-the-loop%20approval%20agent",
            "desc": "High-fidelity human-in-the-loop authority & audit gateway."
        },
        {
            "name": "\ud83e\ude79 HealDesk.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Error%20recovery%20agent",
            "desc": "Autonomous anomaly detection & self-healing recovery engine."
        },
        {
            "name": "\ud83e\udde0 Neural.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Memory-enabled%20agent",
            "desc": "Memory-augmented persistent intelligence swarm."
        },
        {
            "name": "\ud83c\udfad Identity.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Persona-driven%20agent",
            "desc": "Neural role-projection & authoritative persona engine."
        },
        {
            "name": "\ud83d\udca0 Evolver.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Self-improving%20agent",
            "desc": "Feedback-driven self-optimizing neural agent."
        },
        {
            "name": "\u2696\ufe0f Ethics.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Ethics%20&%20guardrails%20agent",
            "desc": "High-fidelity ethical assessment & compliance guardrail engine."
        },
        {
            "name": "\ud83d\udc8e Apex.AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Advanced%20&%20Creative%20Agents/Production-ready%20autonomous%20AI%20agent",
            "desc": "The 100th Agent: Ultimate autonomous production-ready neural matrix."
        }
    ],
    "1. Initialize Runtime": [],
    "2. Configure Credentials": [],
    "3. Launch the Master Brain": []
}

# Sanitize data for surrogate-sensitive environments
def sanitize(text):
    if not isinstance(text, str): return text
    return text.encode('utf-8', 'ignore').decode('utf-8').replace('"', '\\"').replace("'", "\\'")

CATEGORIES = {sanitize(k): [{sanitize(key): sanitize(val) if isinstance(val, str) else val for key, val in a.items()} for a in v] for k, v in CATEGORIES_RAW.items()}

def apply_styles():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg: #000000;
        --nav-bg: rgba(0, 0, 0, 0.75);
        --accent: #00F5FF;
        --accent-alt: #7000FF;
        --card-bg: #111111;
        --text: #F5F5F7;
        --text-dim: #86868B;
        --border: #1D1D1F;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: 'Outfit', sans-serif;
    }

    header, footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    /* Elite Top Navigation Bar */
    .elite-nav {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 60px;
        background: var(--nav-bg);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 60px;
        z-index: 999999;
    }

    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 22px;
        letter-spacing: -1px;
        background: linear-gradient(135deg, var(--accent), var(--accent-alt));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-decoration: none;
    }

    .nav-links {
        display: flex;
        gap: 40px;
        align-items: center;
    }

    .nav-item {
        color: var(--text-dim);
        font-size: 13px;
        font-weight: 500;
        text-decoration: none;
        letter-spacing: 0.02em;
        transition: all 0.3s;
        position: relative;
    }

    .nav-item:hover {
        color: var(--text);
    }

    .nav-item::after {
        content: "";
        position: absolute;
        bottom: -4px; left: 0; width: 0%; height: 1.5px;
        background: var(--accent);
        transition: width 0.3s cubic-bezier(0.19, 1, 0.22, 1);
    }

    .nav-item:hover::after {
        width: 100%;
    }

    .nav-cta {
        background: #fff;
        color: #000;
        padding: 8px 18px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 600;
        text-decoration: none;
        transition: transform 0.2s;
    }

    .nav-cta:hover {
        transform: scale(1.05);
    }

    /* Layout & Hero */
    .block-container {
        padding-top: 140px !important;
        padding-bottom: 100px !important;
        max-width: 1300px !important;
    }

    .hero {
        text-align: center;
        margin-bottom: 100px;
    }

    .hero h1 {
        font-size: 84px !important;
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -3px;
        margin-bottom: 30px;
    }

    .hero p {
        font-size: 24px;
        color: var(--text-dim);
        max-width: 800px;
        margin: 0 auto;
    }

    /* Registry Display */
    .category-title {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin: 80px 0 40px;
        color: var(--text);
        scroll-margin-top: 100px;
    }

    .agent-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 32px;
        height: 100%;
        transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        cursor: pointer;
        display: flex;
        flex-direction: column;
    }

    .agent-card:hover {
        background: #161618;
        border-color: #323235;
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .agent-name {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 12px;
        color: #fff;
    }

    .agent-desc {
        color: var(--text-dim);
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 24px;
    }

    .card-footer {
        margin-top: auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .tag {
        font-size: 11px;
        font-weight: 700;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .arrow {
        color: var(--accent);
        font-size: 18px;
        transition: transform 0.3s;
    }

    .agent-card:hover .arrow {
        transform: translateX(5px);
    }

    .search-input input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        color: white !important;
        font-size: 16px !important;
    }

    </style>
    
    <div class="elite-nav">
        <a href="#" class="nav-logo">AGENT OS</a>
        <div class="nav-links">
            <a href="#registry" class="nav-item">Registry</a>
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub" class="nav-item">Core Repo</a>
            <a href="#" class="nav-cta">Deploy Nodes</a>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def main():
    apply_styles()

    st.markdown('''
    <div class="hero">
        <h1>Autonomous Operations.</h1>
        <p>A unified orchestration layer for 78 deterministic AI agents architected for the next-generation economic engine.</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div id="registry" class="search-input">', unsafe_allow_html=True)
    search_q = st.text_input("", placeholder="Search the decentralized node registry...").lower()
    st.markdown('</div>', unsafe_allow_html=True)

    if search_q:
        cols = st.columns(3)
        found = 0
        for cat_name, agents in CATEGORIES.items():
            for agent in agents:
                if search_q in agent['name'].lower() or search_q in agent['desc'].lower() or search_q in cat_name.lower():
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card">
                            <div class="agent-name">{name}</div>
                            <div class="agent-desc">{desc}</div>
                            <div class="card-footer">
                                <span class="tag">Active</span>
                                <span class="arrow">→</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[found % 3]:
                        st.markdown(card_html, unsafe_allow_html=True)
                    found += 1
    else:
        for idx, (cat_name, agents) in enumerate(CATEGORIES.items()):
            cat_id = cat_name.lower().replace(" ", "-").replace("&", "and")
            st.markdown(f'<div id="{cat_id}" class="category-title">{cat_name}</div>', unsafe_allow_html=True)
            
            chunk_size = 3
            for i in range(0, len(agents), chunk_size):
                chunk = agents[i:i+chunk_size]
                cols = st.columns(3)
                for j, agent in enumerate(chunk):
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card">
                            <div class="agent-name">{name}</div>
                            <div class="agent-desc">{desc}</div>
                            <div class="card-footer">
                                <span class="tag">Operational</span>
                                <span class="arrow">→</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[j]:
                        st.markdown(card_html, unsafe_allow_html=True)
                st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
