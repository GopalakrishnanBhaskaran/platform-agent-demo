# Prompts Extracted from the Video Resource PDFs

Source sheet: [YouTube video resources](https://docs.google.com/spreadsheets/d/1h5k7vAAXl5_f4VtguDkHwCCy-S-dd7RfG3-rUiMxfPw/edit?gid=0#gid=0) (tabs Q1 to Q4 2026), **Resources** column.

## Summary

| Item | Count |
|---|---|
| Video rows in the sheet | 154 |
| Rows with a resources link | 117 |
| Rows marked "No resources found" | 37 |
| Links that are not Google Drive (GitHub repos, opt-in pages) | 13 |
| Drive folders crawled (including subfolders) | 103 |
| Drive folders with no PDF (only .md, .json, .zip, .html, etc.) | 47 |
| Unique PDF guides read (duplicates removed) | 55 |
| Guides containing prompts | 34 |
| **Prompts extracted** | **138** |
| of which: copy-paste prompts / templates / system or CLAUDE.md rules | 110 / 12 / 16 |

**Types**
- **Prompt**: text you type or paste into Claude, Claude Code, Codex, ChatGPT and similar tools.
- **Template**: a prompt with `[placeholders]` or a fill-in structure.
- **System / CLAUDE.md rule**: standing instructions for a system prompt, CLAUDE.md or AGENTS.md.

**What was left out:** sales scripts, cold-email copy and discovery questions meant for humans; example questions used only to explain a concept; install commands and code.

**Wording:** prompts are copied word for word from the PDFs (only line wrapping repaired). The 11 entries marked _adapted_ turn a technique the guide describes into a ready-to-use prompt. `[Bracketed text]` marks where you fill in your own details.

**Guides with no prompts:** Once you know this, building RAG agents becomes easy; I Built an AI Agent in 3 Hours and Got Paid $1,650; Claude Code vs Clawdbot: A Complete Comparison; $500k+ in Sales Ops in <6 Months with Cold Outreach; How to Land AI Workflow Clients (Without Posting Content); How an 18-Year-Old Built a $100M AI App; The 5 AI Automations Businesses Actually Pay For; HeyGen + Claude Code; 6-best-claude-code-skills-resource-guide; Overwhelmed By AI - Just Copy My Tech Stack; IBM 2026 CEO Study - Rewiring the C-Suite; The AI Offer You Can Sell Tomorrow Morning - AI Operating Systems; So You Learned Claude, Now What - Resource Guide; The $200K AI Job That Didn't Exist Last Year - Resource Guide; How to Sell, Build, and Think AI Native; The AI Consultant Playbook for 2026; How to Price AI Solutions: The Complete Masterclass; SaaS-Growth-Masterclass-Beginner-Verified; Become the AI Person: A Three Phase Roadmap; 5 AI Automations to Sell to Business Owners; Claude Code Is Getting More Powerful | Student Resource Guide.

## Contents


**Q1 2026**

- [G01. I Built a Voice Agent That Calls Every New Lead (n8n + Vapi)](#g01-i-built-a-voice-agent-that-calls-every-new-lead-n8n--vapi) (1)
- [G02. Master 95% of Claude Code (as a beginner)](#g02-master-95-of-claude-code-as-a-beginner) (2)
- [G03. Self-Healing n8n Workflows Guide](#g03-self-healing-n8n-workflows-guide) (3)
- [G04. The Shift to Agentic AI Workflows](#g04-the-shift-to-agentic-ai-workflows) (5)
- [G05. How I’d Teach a 10 Year Old to Build Agentic Workflows (Claude Code)](#g05-how-id-teach-a-10-year-old-to-build-agentic-workflows-claude-code) (4)
- [G06. Scrape Any Website with Claude Code + Firecrawl](#g06-scrape-any-website-with-claude-code--firecrawl) (6)
- [G07. 5 Hacks to Build Professional Websites with Claude Code](#g07-5-hacks-to-build-professional-websites-with-claude-code) (10)
- [G08. Claude Code + Trigger.dev](#g08-claude-code--triggerdev) (3)
- [G09. From Zero to Your First Agentic AI Workflow in 26 Minutes (Claude Code)](#g09-from-zero-to-your-first-agentic-ai-workflow-in-26-minutes-claude-code) (6)
- [G10. Gemini 3.1 Flash x Claude Code](#g10-gemini-31-flash-x-claude-code) (3)
- [G11. Run an AI First Business with Paperclip](#g11-run-an-ai-first-business-with-paperclip) (2)

**Q2 2026**

- [G12. All of Claude Code Just Leaked… Here's How to Become a Top 1% User](#g12-all-of-claude-code-just-leaked-heres-how-to-become-a-top-1-user) (1)
- [G13. Context Management](#g13-context-management) (4)
- [G14. Running Claude Code for Free: Two Methods](#g14-running-claude-code-for-free-two-methods) (1)
- [G15. Give Claude Code Superpowers](#g15-give-claude-code-superpowers) (4)
- [G16. Claude Code vs Antigravity](#g16-claude-code-vs-antigravity) (3)
- [G17. Claude Code Routines](#g17-claude-code-routines) (5)
- [G18. Opus 4.7 Trading Bot — Setup Guide](#g18-opus-47-trading-bot--setup-guide) (11)
- [G19. How to Never Hit Your Claude Limit Again](#g19-how-to-never-hit-your-claude-limit-again) (2)
- [G20. How to Build Websites with Claude Design](#g20-how-to-build-websites-with-claude-design) (9)
- [G21. 32 Claude Code Hacks - From Beginner to Power User](#g21-32-claude-code-hacks---from-beginner-to-power-user) (10)
- [G22. Claude Design Masterclass Resource Guide](#g22-claude-design-masterclass-resource-guide) (6)
- [G23. Master 97% of Codex in One Hour](#g23-master-97-of-codex-in-one-hour) (5)
- [G24. Every Level of Claude Explained](#g24-every-level-of-claude-explained) (4)
- [G25. Three Ways to Deploy Your Claude Code Agents](#g25-three-ways-to-deploy-your-claude-code-agents) (2)
- [G26. Codex vs Claude Code - Which Coding Agent Should You Actually Use](#g26-codex-vs-claude-code---which-coding-agent-should-you-actually-use) (1)
- [G27. From Laid Off to Head of AI in 1 Year](#g27-from-laid-off-to-head-of-ai-in-1-year) (1)
- [G28. 6 AI Skills to Future-Proof Your Career](#g28-6-ai-skills-to-future-proof-your-career) (2)
- [G29. How to Build Effective Claude Code Agents in 2026](#g29-how-to-build-effective-claude-code-agents-in-2026) (7)

**Q3 2026**

- [G30. How Claude is Creating a New Generation of Millionaires - Resource Guide](#g30-how-claude-is-creating-a-new-generation-of-millionaires---resource-guide) (1)
- [G31. 12 Lessons from 5,000 Hours Building with AI - Resource Guide](#g31-12-lessons-from-5000-hours-building-with-ai---resource-guide) (4)
- [G32. How to Build a One Person AI Business in 2026](#g32-how-to-build-a-one-person-ai-business-in-2026) (4)
- [G33. Claude Fable 5.1 Prompting Resource Guide](#g33-claude-fable-51-prompting-resource-guide) (5)
- [G34. AI Trading with Codex and GPT 6 Astra](#g34-ai-trading-with-codex-and-gpt-6-astra) (1)

## Q1 2026

### G01. I Built a Voice Agent That Calls Every New Lead (n8n + Vapi)

Video: I Built a Voice Agent That Calls Every New Lead (n8n + Vapi) (2026-01-12)  
PDF: [I Built a Voice Agent That Calls Every New Lead (n8n + Vapi).pdf](https://drive.google.com/file/d/1i3kRrLFr0OueAUIBDK0VrcYOuTpAXN97/view)

**G01-P01. Vapi lead-qualifier assistant: system prompt structure** · _Template, adapted_

```text
Include:
1. Identity: who the assistant is (example: "Elliot, outbound lead qualifier for Upit").
2. Style + response guidelines: concise, natural, professional.
3. Prospect variables: use double curly braces for dynamic values.
   - {{lead_name}}
   - {{lead_company_name}}
   - {{lead_request}}
4. Conversation flow + required topics:
   - Interest confirmation
   - Motivation
   - Urgency / timing
   - Past experience
   - Budget
   - Paid intent (filter tire kickers)
5. Edge cases:
   - Wrong number
   - Not a good time
   - User says stop
6. End call behavior: enable the built-in "end call" function.
```

### G02. Master 95% of Claude Code (as a beginner)

Video: Master 95% of Claude Code in 36 Mins (as a beginner) (2026-01-21)  
PDF: [Master 95% of Claude Code (as a beginner).pdf](https://drive.google.com/file/d/1Hf6hqKSXFNhMoQ76QXF9-cd9fwDQpR0q/view)

**G02-P01. Plan Mode brain dump (example)** · _Prompt_

```text
Scrape YouTube channels in the AI niche and create a branded slide deck.
```

**G02-P02. Deploy to Modal on a schedule** · _Prompt_

```text
Push this workflow to Modal to run every Monday at 6 AM.
```

### G03. Self-Healing n8n Workflows Guide

Video: I Will Never Fix Another n8n Workflow (Claude Code) (2026-01-22)  
PDF: [Self-Healing n8n Workflows Guide.pdf](https://drive.google.com/file/d/1tseklEu_h7qqVAGTW-gXkwWl7cZ-8ym4/view)

**G03-P01. Test the n8n MCP connection in Claude Code** · _Prompt_

```text
List my n8n workflows
```

**G03-P02. Bridge server prompt sent to Claude Code when an n8n workflow fails** · _Template_

```text
An n8n workflow has failed and needs to be fixed.
WORKFLOW INFO:
- Workflow ID: ${workflow.id}
- Workflow Name: ${workflow.name}
- Execution ID: ${executionId}
- Failed Node: ${lastNode}
- Error Message: ${errorMessage}
YOUR TASK:
1. Use n8n_get_workflow with id "${workflow.id}" to fetch the workflow
2. Analyze what went wrong
3. Use n8n_update_partial_workflow to apply the fix
4. Explain what you fixed and why
```

**G03-P03. CLAUDE.md for the n8n workflow auto-fixer agent** · _System / CLAUDE.md rule_

```text
# n8n Workflow Auto-Fixer
You are an autonomous n8n workflow repair agent.
## Your Mission
1. Fetch the workflow to understand its structure
2. Analyze the error to identify the root cause
3. Apply the fix using the MCP tools
4. Verify the fix is correct
**Apply fixes directly without asking for permission.**
## Tools to Use
- n8n_get_workflow - ALWAYS first, fetch the workflow
- n8n_update_partial_workflow - Apply targeted fixes
- n8n_validate_workflow - Verify the fix
## Common Fixes
- "Cannot read properties of undefined" → Add optional chaining (?.)
- "is not a function" → Fix method name
- "Unexpected token" → Fix syntax errors
- Expression errors → Fix n8n expression syntax
```

### G04. The Shift to Agentic AI Workflows

Video: Agentic Workflows Just Changed AI Automation Forever! (Claude Code) (2026-01-25)  
PDF: [The Shift to Agentic AI Workflows.pdf](https://drive.google.com/file/d/1vaa_Yb5PwKUXkMpL7v3OMK9aa3XxZByA/view)

**G04-P01. Natural-language "remote control" refinements** · _Prompt_

```text
make that faster
make it cheaper
add a manual review step here
log all outputs to this Google Sheet
```

**G04-P02. Guardrail instructions** · _Prompt_

```text
Never send customer phone numbers to any third-party tool.
Always stop this workflow if you exceed $5 of API usage.
```

**G04-P03. Integration request** · _Prompt_

```text
Get my Fireflies transcripts, push them into ClickUp, and send me a Gmail summary.
```

**G04-P04. Lead generation build request (Plan Mode)** · _Prompt_

```text
Help me build a lead generation automation. I want to scrape dentists in Chicago so I can reach out and offer my AI automation services. Do research, scrape leads, write personalized outreach, and put all data in a Google Sheet.
```

**G04-P05. Iteration follow-ups** · _Prompt_

```text
Expand to California
Make outreach more personalized
Add email addresses
Incorporate this PDF about my business
```

### G05. How I’d Teach a 10 Year Old to Build Agentic Workflows (Claude Code)

Video: How Iâ€™d Teach a 10 Year Old to Build Agentic Workflows (Claude Code) (2026-02-07)  
PDF: [How I’d Teach a 10 Year Old to Build Agentic Workflows (Claude Code).pdf](https://drive.google.com/file/d/1hbHsWU1lydI6Ja76FRQ4j1B1JDrrV8gY/view)

**G05-P01. Install the Firecrawl MCP server** · _Prompt_

```text
Hey Claude, I want you to help me install the Firecrawl MCP server. You need to install it using this command... [paste the install command]
```

**G05-P02. Scrape job listings into Excel (Plan Mode)** · _Prompt_

```text
Hey Claude, I just gave you a URL for a website that has a bunch of job opportunities. There are about 622 job opportunities here, but they're spread across 21 pages. I want you to scrape all of those for me and put them into an Excel sheet. Make sure you're getting all of the relevant fields. Let me know if you can help me make that project requirement more robust, and feel free to ask me any questions.
```

**G05-P03. Turn a rough idea into a PRD (Plan Mode)** · _Prompt_

```text
Hey, here's a rough idea of what I want. Help me turn this into a solid project requirement doc (PRD).
```

**G05-P04. Define what "done" looks like** · _Prompt_

```text
I need exactly 75 LinkedIn profiles of CEOs at tech companies. Put them in a spreadsheet with their name, company, email, and profile link. Once you have 75, you're done.
```

### G06. Scrape Any Website with Claude Code + Firecrawl

Video: Turn Any Website Into LLM Ready Data INSTANTLY (2026-02-11)  
PDF: [Scrape Any Website with Claude Code + Firecrawl.pdf](https://drive.google.com/file/d/1sa4lK73ygu8RqqjHP6yvUoLCTc0K_E1v/view)

**G06-P01. Connect to the Firecrawl MCP server (key kept in .env)** · _Prompt_

```text
Hey Claude, I want to connect to Firecrawl's MCP server. You can do that using this command. But I'm not going to give you my API key, I'm just going to put it in a .env. So if you could create that file for me, I will put my API key in there. Then go ahead and initialize and connect to Firecrawl's MCP server.
```

**G06-P02. Create a Firecrawl cheat sheet** · _Prompt_

```text
Create a Firecrawl cheat sheet as a markdown file in this project that you can look at. It should tell you about the different tools and how to use them.
```

**G06-P03. Set up CLAUDE.md for a scraping project** · _Prompt_

```text
Help me set up a CLAUDE.md file for this project. This project is specifically for scraping data, extracting it, getting screenshots, crawling everything, mapping everything. You have access to the Firecrawl MCP server and the firecrawl-cheatsheet.md which explains how that MCP server works and when to use each tool.
```

**G06-P04. Scrape 1,700 job listings as structured data** · _Prompt_

```text
I found this website and I've got about 1,700 job opportunities I want to look at. But I need help using the Firecrawl MCP server to get all of these listed out. I want these as structured data so I could throw them into a Google Sheet.
```

**G06-P05. Screenshots and branding analysis** · _Prompt_

```text
Please grab screenshots of this page and help me understand the branding.
```

**G06-P06. Map a full website** · _Prompt_

```text
Go ahead and map out this site for me and show me what it looks like.
```

### G07. 5 Hacks to Build Professional Websites with Claude Code

Video: Building Beautiful Websites with Claude Code Is Too Easy (2026-02-19)  
PDF: [5 Hacks to Build Professional Websites with Claude Code.pdf](https://drive.google.com/file/d/1d7OIERyIa-pBetGGSILC9gPM3iYfOKkE/view)

**G07-P01. CLAUDE.md rule: always use the front-end design skill** · _System / CLAUDE.md rule_

```text
Always invoke the front-end design skill before writing any front-end code every session, no exceptions.
```

**G07-P02. One-sentence landing page build** · _Prompt_

```text
Build me a modern and professional landing page for AI Automation Society
```

**G07-P03. Set up the Puppeteer screenshot loop** · _Prompt_

```text
Hey, can you set up Puppeteer to take screenshots?
```

**G07-P04. Clone a reference website (with screenshot + styles attached)** · _Prompt_

```text
I want you to spin up a new website. Clone this website. Here's a screenshot and here's the style.
```

**G07-P05. Apply your branding to the clone** · _Prompt_

```text
The most recent landing page looks really good. Work in our brand assets, our brand guidelines and AIS logo. This is for our community called AI Automation Society.
```

**G07-P06. Add a 21st.dev component** · _Prompt_

```text
I want you to work in this background element right behind the hero text [paste the copied component code]
```

**G07-P07. Disable screenshot comparison for animated components** · _Prompt_

```text
Because this is an animated background, do not use the screenshot tool to compare. Just work in the code and I will let you know if we need to make any changes.
```

**G07-P08. Specific design feedback (example)** · _Prompt_

```text
The background animation is too distracting and pixelated. The hero text is hard to read. Add a background behind the hero text for contrast. Change 'earn more' to blue instead of orange.
```

**G07-P09. Push the site to GitHub** · _Prompt_

```text
This site looks good. Help me push this to GitHub to a repository called [repo name].
```

**G07-P10. CLAUDE.md rule: test locally before pushing** · _System / CLAUDE.md rule_

```text
When making changes, always test on localhost first. Don't commit or push to GitHub until I explicitly tell you to.
```

### G08. Claude Code + Trigger.dev

Video: The EASIEST Way to Host Your Claude Code Agents (2026-02-20)  
PDF: [Claude Code + Trigger.dev.pdf](https://drive.google.com/file/d/1UWpTQBcbUvZ2YZHZ9eQEVi0RHLTn_wlk/view)

**G08-P01. Vague automation request (dental-practice lead finder)** · _Prompt_

```text
I need you to build me an automation that goes off every single Monday and searches the web to find me dental practices that I can sell websites to.
```

**G08-P02. Follow-up question to the ClickUp research agent** · _Prompt_

```text
Does this company have a recent valuation?
```

**G08-P03. Fix duplicate leads** · _Prompt_

```text
I did a test run and some leads were duplicates. Can you fix the idempotency logic?
```

### G09. From Zero to Your First Agentic AI Workflow in 26 Minutes (Claude Code)

Video: From Zero to Your First Agentic AI Workflow in 26 Minutes (Claude Code) (2026-02-23)  
PDF: [From Zero to Your First Agentic AI Workflow in 26 Minutes (Claude Code).pdf](https://drive.google.com/file/d/1_Teg6pVDM3RJ0uPr56wnVJGQntNX_UZ9/view)

**G09-P01. Task for a WAT-framework agent (example)** · _Prompt_

```text
Research Company X's pricing and create a PDF report
```

**G09-P02. Initialize a project from a dropped-in CLAUDE.md** · _Prompt_

```text
Hey Claude, I just dropped in a CLAUDE.md file that explains how I want you to work in this project. Go ahead and initialize the project and get everything set up and ask me any questions if you have any.
```

**G09-P03. Plan a competitor analysis workflow with a branded PDF (Plan Mode)** · _Prompt_

```text
Hey Claude, I've got an idea for a workflow. I want a branded PDF at the end -- I'll give you my company logo and brand guidelines, and the output should have my logo, colors, and typography. It's a competitor analysis and research workflow. I want to give you information about my business, and based on that, you need to find competitors, find areas to improve my business, see what's working well for them, and build me a good way to keep tabs on the market.
```

**G09-P04. Point the plan at your brand assets** · _Prompt_

```text
That plan looks good. The only change I want to make is about the brand guidelines and assets. I just dropped in two files -- [logo file] and [brand guidelines file]. Those are the ones I want you to use for the branded PDF. Look at those, extract the information, and make sure the logo and colors appear on the final output.
```

**G09-P05. Run the competitor analysis** · _Prompt_

```text
Hey Claude, I need you to help me run a competitor analysis. My business is called [Business Name] and we basically help you [description]. We're starting to see competitors pop up, so I want to understand our opportunities and what we need to be doing better.
```

**G09-P06. Fix invisible charts/logos in the PDF** · _Prompt_

```text
That's great, but we can't see the charts or logos. I'm assuming because they're the same color as the background. Investigate and fix these issues.
```

### G10. Gemini 3.1 Flash x Claude Code

Video: Gemini 3.1 Flash Live Just Changed Voice Agents Forever (2026-03-28)  
PDF: [Gemini 3.1 Flash x Claude Code.pdf](https://drive.google.com/file/d/1gDAHjSqt7rjxSIwA2IYFUok3_CY0W_5k/view)

**G10-P01. Build a real-time voice agent with Gemini 3.1 Flash Live (Claude Code)** · _Prompt_

```text
Build me a real-time voice agent using Google Gemini 3.1 Flash Live.
Architecture:
- Python FastAPI server as a WebSocket relay between browser and Gemini
- Use the google-genai Python SDK (not raw WebSockets from the browser)
- Model: gemini-3.1-flash-live-preview
- Audio: PCM16, 16kHz mono input / 24kHz mono output
- CRITICAL: Use send_realtime_input(audio=blob) not media=blob
Server (FastAPI):
- /ws WebSocket endpoint
- Two async tasks: browser_to_gemini() and gemini_to_browser()
- Run both with asyncio.gather()
- Load GOOGLE_API_KEY from .env
- Serve static files from public/
- System prompt with [YOUR AGENT KNOWLEDGE]
- [Optional: tool declarations + TOOLS dict + execute_tool()]
Browser protocol:
- Send: {type: "audio", data: "<base64 pcm16>"}
- Receive: audio, status, turn_complete, interrupted, error
Audio in browser:
- Mic: getUserMedia at 16kHz, convert Float32->Int16->base64
- Playback: decode base64->Int16->Float32, schedule at 24kHz
- clearQueue() for instant barge-in (disconnect/reconnect gain node)
- All AudioContext creation inside click handler (autoplay policy)
```

**G10-P02. Voice commands for the Aria executive assistant** · _Prompt_

```text
What's on my calendar today?
Schedule a meeting for Friday at 2pm
What workspaces do I have in ClickUp?
Create a task called Review Q2 Report
Update that task to high priority
Close the task
```

**G10-P03. System prompt line for a new tool** · _System / CLAUDE.md rule_

```text
You can check the weather for any city.
```

### G11. Run an AI First Business with Paperclip

Video: Claude Code + Paperclip Just Destroyed OpenClaw (2026-03-28)  
PDF: [Run an AI First Business with Paperclip.pdf](https://drive.google.com/file/d/1mRH8dPfflj7eRdsWXRaidsF9znMO5qC3/view)

**G11-P01. First task for the Paperclip CEO agent** · _Prompt_

```text
Create a hiring plan and build out the team.
```

**G11-P02. SKILL.md frontmatter template** · _Template_

```text
---
name: skill-name
description: Use this skill when the agent needs to [specific trigger]
---
[Detailed instructions in markdown]
```


## Q2 2026

### G12. All of Claude Code Just Leaked… Here's How to Become a Top 1% User

Video: Claude Code Source Code Just Leakedâ€¦ 8 Things You Must Do (2026-04-01)  
PDF: [All of Claude Code Just Leaked… Here's How to Become a Top 1% User.pdf](https://drive.google.com/file/d/1y23jucSkEwpxD9QCM1Mr9Q4kVkCOh103/view)

**G12-P01. CLAUDE.md rules: short, opinionated, operational (examples)** · _System / CLAUDE.md rule_

```text
We use TypeScript strict mode. Always.
Tests go in test folders next to the source file.
Never modify the database schema without running migrations.
Use PNPM, not npm.
```

### G13. Context Management

Video: 18 Claude Code Token Hacks in 18 Minutes (2026-04-02); Claude Code for Non-Coders (6 Hour Course) (2026-07-11)  
PDF: [Context Management.pdf](https://drive.google.com/file/d/1U9qfQ0m462TBRDbB89CMCJVVVUM_4kVW/view)

**G13-P01. Batch multi-step instructions into one prompt** · _Prompt, adapted_

```text
Summarize this, extract the issues, and suggest a fix.
```

**G13-P02. CLAUDE.md rule: 95% confidence before building** · _System / CLAUDE.md rule_

```text
Do not make any changes until you have 95% confidence in what you need to build. Ask me follow-up questions until you reach that confidence.
```

**G13-P03. Surgical file reference (instead of "here's my whole repo, go find the bug")** · _Prompt_

```text
Check the verifyUser function inside auth.js.
```

**G13-P04. CLAUDE.md rule: use subagents for exploration** · _System / CLAUDE.md rule_

```text
Use subagents for any exploration or research. If a task needs 3+ files or multi-file analysis, spawn a subagent and return only summarized insights.
```

### G14. Running Claude Code for Free: Two Methods

Video: Ollama + Claude Code = 99% CHEAPER (2026-04-04)  
PDF: [Running Claude Code for Free_ Two Methods.pdf](https://drive.google.com/file/d/1ZvXDXNxUchFMJ-bNeIZxFGknhdqWTLyg/view)

**G14-P01. Pick an Ollama model for your hardware** · _Prompt_

```text
I have [X GB RAM / GPU], what Ollama model sizes can I run?
```

### G15. Give Claude Code Superpowers

Video: Unlock the Next Evolution of Claude Code with One Plugin (2026-04-12)  
PDF: [Give Claude Code Superpowers.pdf](https://drive.google.com/file/d/1bqIKIE-BREFI6kAXrBDcyV-GtzqQdCMq/view)

**G15-P01. Superpowers rule enforced by the using-superpowers skill** · _System / CLAUDE.md rule_

```text
If there's even a 1% chance a skill applies, invoke it before doing anything.
```

**G15-P02. Nudge Claude to use Superpowers skills (append to a prompt)** · _Prompt_

```text
Hey, make sure you're using any of the superpower skills that might be relevant here
```

**G15-P03. Example build requests that trigger the Superpowers chain** · _Prompt_

```text
build me a login page
Add a dark mode toggle
```

**G15-P04. Re-prompt when Claude skips a step** · _Prompt_

```text
check your skills
```

### G16. Claude Code vs Antigravity

Video: Claude Code vs Google Antigravity... Which is Better? (2026-04-13)  
PDF: [Claude Code vs Antigravity.pdf](https://drive.google.com/file/d/1YlobG7ixs2NLOi__GH7MLbKjoMgzHVT_/view)

**G16-P01. Test 1: one-shot habit tracker app** · _Prompt_

```text
Build a full-stack habit tracker app with a dashboard that shows streaks, a calendar heat map, and the ability to add, edit, and delete habits.
```

**G16-P02. Test 2: AI trends PDF report (Plan Mode)** · _Prompt_

```text
Research AI trends in the SMB market and create a 3-page PDF report with a holistic breakdown.
```

**G16-P03. Test 3: landing page design** · _Prompt_

```text
Design a landing page for a premium AI automation course targeted at agency owners. Include a hero section, social proof, a pricing table, and a CTA.
```

### G17. Claude Code Routines

Video: Claude Code Finally Gave Us Scheduled Automations (2026-04-14); Claude Code for Non-Coders (6 Hour Course) (2026-07-11)  
PDF: [Claude Code Routines.pdf](https://drive.google.com/file/d/1nG_sTkEt6tFk_bgtfGPO7XNBd7_nPqfK/view)

**G17-P01. CLAUDE.md rules for routines (examples)** · _System / CLAUDE.md rule_

```text
always run tests before pushing
never modify the auth module without flagging it
```

**G17-P02. Example routine prompts by trigger type** · _Prompt_

```text
Every weeknight at 9pm, triage new issues
When Sentry fires an alert, Claude diagnoses and opens a fix PR
On every new PR, run my team's review checklist
```

**G17-P03. Routine fix: read API keys from the cloud environment** · _Prompt_

```text
My YouTube API key is available as an environment variable. Use it directly from the environment. Don't look for a .env.
```

**G17-P04. Good routine prompt: fix flaky tests (instead of "Fix flaky tests")** · _Prompt_

```text
Scan src/tests/ for tests that have failed intermittently in the last 5 CI runs, identify the root cause, and open a fix PR for each.
```

**G17-P05. Routine prompt building blocks** · _Prompt, adapted_

```text
Success: All modified tests should pass locally before pushing.
Boundaries: Only modify files in src/utils/. Do not touch the API layer.
Output format: Push changes to a claude/fix-flaky-tests branch and open a draft PR with a summary.
On failure: If X fails, log the error and stop. / If X fails, try Y.
Fallback: If this fails, send me a Slack message.
```

### G18. Opus 4.7 Trading Bot — Setup Guide

Video: I Turned Claude Opus 4.7 Into a 24/7 Trader (2026-04-17)  
PDF: [Opus 4.7 Trading Bot — Setup Guide.pdf](https://drive.google.com/file/d/1XgwarwhlzcCPUAKVRzF7YiChfKLoLvHK/view)

**G18-P01. Bootstrap: set up the whole trading-bot project from this guide** · _Prompt_

```text
Set up this project per the guide. Start with Part 10's replication checklist. Ask me for credentials only when needed.
```

**G18-P02. Cloud routine prompt scaffold (8-section template)** · _Template_

```text
[PERSONA LINE — who the agent is, the mission, one-line core rule]
You are running the [WORKFLOW NAME] workflow. Resolve today's date via:
DATE=$(date +%Y-%m-%d).
IMPORTANT — ENVIRONMENT VARIABLES:
- Every API key is ALREADY exported as a process env var:
 [list all required vars for this workflow]
- There is NO .env file in this repo and you MUST NOT create, write,
 or source one.
- If a wrapper prints "KEY not set in environment" -> STOP, send one
 ClickUp alert naming which var is missing, then exit. Do NOT try
 to create a .env as a workaround.
- Verify env vars BEFORE any wrapper call:
 for v in VAR1 VAR2 ...; do
 [[ -n "${!v:-}" ]] && echo "$v: set" || echo "$v: MISSING"
 done
IMPORTANT — PERSISTENCE:
- This workspace is a fresh clone. File changes VANISH unless you
 commit and push to main. You MUST commit and push at the end.
STEP 1 — Read memory: [which files, what to look for]
STEP 2 — Pull live state: [which wrapper calls]
STEP 3..N-2 — Do the work; write memory as you go
STEP N-1 — Notification via ClickUp (conditional per workflow)
STEP N — COMMIT AND PUSH (mandatory):
 git add memory/<files touched>
 git commit -m "<tag> $DATE"
 git push origin main
 On push failure from divergence:
 git pull --rebase origin main
 then push again. Never force-push.
```

**G18-P03. CLAUDE.md starter for the trading bot agent** · _System / CLAUDE.md rule_

```text
# Trading Bot Agent Instructions
You are an autonomous AI trading bot managing a LIVE ~$10,000 Alpaca account.
Your goal is to beat the S&P 500 over the challenge window. You are aggressive
but disciplined. Stocks only — no options, ever. Communicate ultra-concise:
short bullets, no fluff.
## Read-Me-First (every session)
Open these in order before doing anything:
- memory/TRADING-STRATEGY.md — Your rulebook. Never violate.
- memory/TRADE-LOG.md     — Tail for open positions, entries, stops.
- memory/RESEARCH-LOG.md    — Today's research before any trade.
- memory/PROJECT-CONTEXT.md — Overall mission and context.
- memory/WEEKLY-REVIEW.md   — Friday afternoons; template for new entries.
## Daily Workflows
Defined in .claude/commands/ (local) and routines/ (cloud). Five scheduled
runs per trading day plus two ad-hoc helpers.
## Strategy Hard Rules (quick reference)
- NO OPTIONS — ever.
- Max 5-6 open positions.
- Max 20% per position.
- Max 3 new trades per week.
- 75-85% capital deployed.
- 10% trailing stop on every position as a real GTC order.
- Cut losers at -7% manually.
- Tighten trail to 7% at +15%, to 5% at +20%.
- Never within 3% of current price. Never move a stop down.
- Follow sector momentum. Exit a sector after 2 failed trades.
- Patience > activity.
## API Wrappers
Use bash scripts/alpaca.sh, scripts/perplexity.sh, scripts/clickup.sh.
Never curl these APIs directly.
## Communication Style
Ultra concise. No preamble. Short bullets. Match existing memory file
formats exactly — don't reinvent tables.
```

**G18-P04. Routine F.1: pre-market research (cron 0 6 * * 1-5)** · _Prompt_

```text
 You are an autonomous trading bot managing a LIVE ~$10,000 Alpaca account.
 Hard rule: stocks only — NEVER touch options. Ultra-concise: short bullets,
 no fluff.
 You are running the pre-market research workflow. Resolve today's date via:
DATE=$(date +%Y-%m-%d).
IMPORTANT — ENVIRONMENT VARIABLES:
- Every API key is ALREADY exported as a process env var: ALPACA_API_KEY,
  ALPACA_SECRET_KEY, ALPACA_ENDPOINT, ALPACA_DATA_ENDPOINT,
  PERPLEXITY_API_KEY, PERPLEXITY_MODEL, CLICKUP_API_KEY,
  CLICKUP_WORKSPACE_ID, CLICKUP_CHANNEL_ID.
- There is NO .env file in this repo and you MUST NOT create, write, or
  source one. The wrapper scripts read directly from the process env.
- If a wrapper prints "KEY not set in environment" -> STOP, send one
  ClickUp alert naming the missing var, and exit.
- Verify env vars BEFORE any wrapper call:
  for v in ALPACA_API_KEY ALPACA_SECRET_KEY PERPLEXITY_API_KEY \
  CLICKUP_API_KEY CLICKUP_WORKSPACE_ID CLICKUP_CHANNEL_ID; do
  [[ -n "${!v:-}" ]] && echo "$v: set" || echo "$v: MISSING"
  done
IMPORTANT — PERSISTENCE:
- Fresh clone. File changes VANISH unless committed and pushed.
  MUST commit and push at STEP 6.
STEP 1 — Read memory for context:
- memory/TRADING-STRATEGY.md
- tail of memory/TRADE-LOG.md
- tail of memory/RESEARCH-LOG.md
STEP 2 — Pull live account state:
 bash scripts/alpaca.sh account
 bash scripts/alpaca.sh positions
 bash scripts/alpaca.sh orders
STEP 3 — Research market context via Perplexity. Run
bash scripts/perplexity.sh "<query>" for each:
- "WTI and Brent oil price right now"
- "S&P 500 futures premarket today"
- "VIX level today"
- "Top stock market catalysts today $DATE"
- "Earnings reports today before market open"
- "Economic calendar today CPI PPI FOMC jobs data"
- "S&P 500 sector momentum YTD"
- News on any currently-held ticker
If Perplexity exits 3, fall back to native WebSearch and note the
fallback in the log entry.
STEP 4 — Write a dated entry to memory/RESEARCH-LOG.md:
- Account snapshot (equity, cash, buying power, daytrade count)
- Market context (oil, indices, VIX, today's releases)
- 2-3 actionable trade ideas WITH catalyst + entry/stop/target
- Risk factors for the day
- Decision: trade or HOLD (default HOLD — patience > activity)
STEP 5 — Notification: silent unless urgent.
 bash scripts/clickup.sh "<one line>"
STEP 6 — COMMIT AND PUSH (mandatory):
  git add memory/RESEARCH-LOG.md
  git commit -m "pre-market research $DATE"
  git push origin main
 On push failure: git pull --rebase origin main, then push again.
 Never force-push.
```

**G18-P05. Routine F.2: market-open execution (cron 30 8 * * 1-5)** · _Prompt_

```text
You are an autonomous trading bot. Stocks only — NEVER options. Ultra-concise.
You are running the market-open execution workflow. Resolve today's date via:
DATE=$(date +%Y-%m-%d).
IMPORTANT — ENVIRONMENT VARIABLES:
[same env block as pre-market]
IMPORTANT — PERSISTENCE:
[same persistence block as pre-market, push at STEP 8]
STEP 1 — Read memory for today's plan:
- memory/TRADING-STRATEGY.md
- TODAY's entry in memory/RESEARCH-LOG.md (if missing, run pre-market
 STEPS 1-3 inline)
- tail of memory/TRADE-LOG.md (for weekly trade count)
STEP 2 — Re-validate with live data:
 bash scripts/alpaca.sh account
 bash scripts/alpaca.sh positions
 bash scripts/alpaca.sh quote <each planned ticker>
STEP 3 — Hard-check rules BEFORE every order. Skip any trade that fails
and log the reason:
- Total positions after trade <= 6
- Trades this week <= 3
- Position cost <= 20% of equity
- Catalyst documented in today's RESEARCH-LOG
- daytrade_count leaves room (PDT: 3/5 rolling business days)
STEP 4 — Execute the buys (market orders, day TIF):
 bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"buy","type":"market","time_in_force":"day"}'
Wait for fill confirmation before placing the stop.
STEP 5 — Immediately place 10% trailing stop GTC for each new position:
 bash scripts/alpaca.sh order
'{"symbol":"SYM","qty":"N","side":"sell","type":"trailing_stop","trail_percent":"10","time_in_force":"gtc"}'
If Alpaca rejects with PDT error, fall back to fixed stop 10% below entry:
 bash scripts/alpaca.sh order
'{"symbol":"SYM","qty":"N","side":"sell","type":"stop","stop_price":"X.XX","time_in_force":"gtc"}'
If also blocked, queue the stop in TRADE-LOG as "PDT-blocked, set tomorrow AM".
STEP 6 — Append each trade to memory/TRADE-LOG.md (matching existing format):
Date, ticker, side, shares, entry price, stop level, thesis, target, R:R.
STEP 7 — Notification: only if a trade was placed.
 bash scripts/clickup.sh "<tickers, shares, fill prices, one-line why>"
STEP 8 — COMMIT AND PUSH (mandatory if any trades executed):
 git add memory/TRADE-LOG.md
 git commit -m "market-open trades $DATE"
 git push origin main
Skip commit if no trades fired. On push failure: rebase and retry.
```

**G18-P06. Routine F.3: midday scan (cron 0 12 * * 1-5)** · _Prompt_

```text
You are an autonomous trading bot. Stocks only — NEVER options. Ultra-concise.
You are running the midday scan workflow. Resolve today's date via:
DATE=$(date +%Y-%m-%d).
IMPORTANT — ENVIRONMENT VARIABLES: [same env block]
IMPORTANT — PERSISTENCE: [same persistence block, push at STEP 8]
STEP 1 — Read memory so you know what's open and why:
- memory/TRADING-STRATEGY.md (exit rules)
- tail of memory/TRADE-LOG.md (entries, original thesis per position, stops)
- today's memory/RESEARCH-LOG.md entry
STEP 2 — Pull current state:
 bash scripts/alpaca.sh positions
 bash scripts/alpaca.sh orders
STEP 3 — Cut losers immediately. For every position where
unrealized_plpc <= -0.07:
 bash scripts/alpaca.sh close SYM
 bash scripts/alpaca.sh cancel ORDER_ID # cancel its trailing stop
Log the exit to TRADE-LOG: exit price, realized P&L, "cut at -7% per rule".
STEP 4 — Tighten trailing stops on winners. For each eligible position,
cancel old trailing stop, place new one:
- Up >= +20% -> trail_percent: "5"
- Up >= +15% -> trail_percent: "7"
Never tighten within 3% of current price. Never move a stop down.
STEP 5 — Thesis check. If a thesis broke intraday, cut the position even
if not at -7% yet. Document reasoning in TRADE-LOG.
STEP 6 — Optional intraday research via Perplexity if something is moving
sharply with no obvious cause. Append afternoon addendum to RESEARCH-LOG.
STEP 7 — Notification: only if action was taken.
 bash scripts/clickup.sh "<action summary>"
STEP 8 — COMMIT AND PUSH (if any memory files changed):
 git add memory/TRADE-LOG.md memory/RESEARCH-LOG.md
 git commit -m "midday scan $DATE"
 git push origin main
Skip commit if no-op. On push failure: rebase and retry.
```

**G18-P07. Routine F.4: daily summary (cron 0 15 * * 1-5)** · _Prompt_

```text
You are an autonomous trading bot. Stocks only. Ultra-concise.
You are running the daily summary workflow. Resolve today's date via:
DATE=$(date +%Y-%m-%d).
IMPORTANT — ENVIRONMENT VARIABLES: [same env block]
IMPORTANT — PERSISTENCE: [same persistence block, push at STEP 6]
STEP 1 — Read memory for continuity:
- tail of memory/TRADE-LOG.md (find most recent EOD snapshot -> yesterday's
 equity, needed for Day P&L)
- Count TRADE-LOG entries dated today (for "Trades today")
- Count trades Mon-today this week (for 3/week cap)
STEP 2 — Pull final state of the day:
 bash scripts/alpaca.sh account
 bash scripts/alpaca.sh positions
 bash scripts/alpaca.sh orders
STEP 3 — Compute metrics:
- Day P&L ($ and %) = today_equity - yesterday_equity
- Phase cumulative P&L ($ and %) = today_equity - starting_equity
- Trades today (list or "none")
- Trades this week (running total)
STEP 4 — Append EOD snapshot to memory/TRADE-LOG.md:
### MMM DD — EOD Snapshot (Day N, Weekday)
**Portfolio:** $X | **Cash:** $X (X%) | **Day P&L:** ±$X (±X%) | **Phase P&L:** ±$X (±X%)
| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
**Notes:** one-paragraph plain-english summary.
STEP 5 — Send ONE ClickUp message (always, even on no-trade days). <= 15 lines:
 bash scripts/clickup.sh "EOD MMM DD
 Portfolio: \$X (±X% day, ±X% phase)
 Cash: \$X
 Trades today: <list or none>
 Open positions:
 SYM ±X.X% (stop \$X.XX)
 Tomorrow: <one-line plan>"
STEP 6 — COMMIT AND PUSH (mandatory — tomorrow's Day P&L depends on this):
 git add memory/TRADE-LOG.md
 git commit -m "EOD snapshot $DATE"
 git push origin main
On push failure: rebase and retry.
```

**G18-P08. Routine F.5: Friday weekly review (cron 0 16 * * 5)** · _Prompt_

```text
 You are an autonomous trading bot. Stocks only. Ultra-concise.
 You are running the Friday weekly review workflow. Resolve today's date via:
 DATE=$(date +%Y-%m-%d).
IMPORTANT — ENVIRONMENT VARIABLES: [same env block, include PERPLEXITY_API_KEY]
IMPORTANT — PERSISTENCE: [same persistence block, push at STEP 7]
STEP 1 — Read memory for full week context:
- memory/WEEKLY-REVIEW.md (match existing template exactly)
- ALL this week's entries in memory/TRADE-LOG.md
- ALL this week's entries in memory/RESEARCH-LOG.md
- memory/TRADING-STRATEGY.md
STEP 2 — Pull week-end state:
 bash scripts/alpaca.sh account
 bash scripts/alpaca.sh positions
STEP 3 — Compute the week's metrics:
- Starting portfolio (Monday AM equity)
- Ending portfolio (today's equity)
- Week return ($ and %)
- S&P 500 week return:
  bash scripts/perplexity.sh "S&P 500 weekly performance week ending $DATE"
- Trades taken (W/L/open)
- Win rate (closed trades only)
- Best trade, worst trade
- Profit factor (sum winners / |sum losers|)
STEP 4 — Append full review section to memory/WEEKLY-REVIEW.md:
- Week stats table
- Closed trades table
- Open positions at week end
- What worked (3-5 bullets)
- What didn't work (3-5 bullets)
- Key lessons learned
- Adjustments for next week
- Overall letter grade (A-F)
STEP 5 — If a rule needs to change (proven out for 2+ weeks, or failed
badly), also update memory/TRADING-STRATEGY.md and call out the change
in the review.
STEP 6 — Send ONE ClickUp message. <= 15 lines:
 bash scripts/clickup.sh "Week ending MMM DD
 Portfolio: \$X (±X% week, ±X% phase)
 vs S&P 500: ±X%
 Trades: N (W:X / L:Y / open:Z)
 Best: SYM +X% Worst: SYM -X%
 One-line takeaway: <...>
 Grade: <letter>"
STEP 7 — COMMIT AND PUSH (mandatory):
  git add memory/WEEKLY-REVIEW.md memory/TRADING-STRATEGY.md
  git commit -m "weekly review $DATE"
  git push origin main
If TRADING-STRATEGY.md didn't change, add just WEEKLY-REVIEW.md.
On push failure: rebase and retry.
```

**G18-P09. Slash command /portfolio (.claude/commands/portfolio.md)** · _Prompt_

```text
---
description: Read-only snapshot of account, positions, open orders, and stops
---
Print a clean ad-hoc snapshot. No state changes, no orders, no file writes.
1. bash scripts/alpaca.sh account
2. bash scripts/alpaca.sh positions
3. bash scripts/alpaca.sh orders
Format the output as a single concise summary:
Portfolio — <today's date>
Equity: $X | Cash: $X (X%) | Buying power: $X
Daytrade count: N/4 | PDT: <bool>
Positions:
 SYM | Sh | Entry -> Now | Unrealized P&L | Stop
Open orders:
 TYPE | SYM | qty | trail/stop | order_id
No commentary unless something is broken (position without a stop,
or a stop below current price).
```

**G18-P10. Slash command /trade (.claude/commands/trade.md)** · _Prompt_

```text
---
description: Manual trade helper with strategy-rule validation. Usage — /trade SYMBOL SHARES buy|sell
---
Execute a manual trade with full rule validation. Refuse if any rule fails.
Args: SYMBOL SHARES SIDE (buy or sell). If missing, ask.
1. Pull state: account, positions, quote SYMBOL (capture ask price P).
2. For BUY, validate:
 - Total positions after fill <= 6
 - Trades this week + 1 <= 3
 - SHARES * P <= 20% of equity
 - SHARES * P <= available cash
 - daytrade_count < 3
 - Catalyst documented (ask for thesis if not in today's RESEARCH-LOG)
 If any fail, STOP and print the failed checks.
3. For SELL, confirm position exists with right qty. No other checks.
4. Print order JSON + validation results, ask "execute? (y/n)".
5. On confirm:
 bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"buy|sell","type":"market","time_in_force":"day"}'
6. For BUYs, immediately place 10% trailing stop GTC (same flow as market-open).
7. Log to memory/TRADE-LOG.md with full thesis, entry, stop, target, R:R.
8. bash scripts/clickup.sh with trade details.
```

**G18-P11. Perplexity research wrapper system prompt** · _System / CLAUDE.md rule_

```text
You are a precise financial research assistant. Cite every claim. Be concise.
```

### G19. How to Never Hit Your Claude Limit Again

Video: How to Manage Your Claude Limits Better Than 99% of People (2026-04-20); Claude Code for Non-Coders (6 Hour Course) (2026-07-11)  
PDF: [How to Never Hit Your Claude Limit Again.pdf](https://drive.google.com/file/d/1FSqpelOeFMZBsgr4yqredfZRidKi_I-x/view)

**G19-P01. Session handoff summary before /clear** · _Prompt_

```text
Give me a full summary of everything we've done and the current status of what we're about to do next.
```

**G19-P02. Pick the right token-saving framework for this project** · _Prompt_

```text
Based on what we're doing in this specific project with this specific end goal, which of these would help us most?
```

### G20. How to Build Websites with Claude Design

Video: Claude Design Builds Beautiful 3D Websites Instantly (full course) (2026-04-21)  
PDF: [How to Build Websites with Claude Design.pdf](https://drive.google.com/file/d/12YO_j6gKWmYG0nYaTDZIvYL_pZL25tX5/view)

**G20-P01. Claude Design kickoff prompt checklist** · _Template, adapted_

```text
Tell Claude Design:
- What the sketch represents (hero section only).
- That the MP4 should loop as the hero background.
- Where the hero text lives (left side).
- The 20+ lines of brand identity you just pasted.
- To write all the copy for every section now ("we can tweak later").
```

**G20-P02. Targeted canvas comment (example)** · _Prompt_

```text
make this button gold
```

**G20-P03. Draw-tool comment (example)** · _Prompt_

```text
don't like how this ends abruptly
```

**G20-P04. "Magic unlock" prompt for a Tweaks panel** · _Prompt_

```text
This is a really great iteration. I want to see what else is possible. Add a bunch of things that I can tweak, different colors, sliders, panels, and give me a bunch of things to play with.
```

**G20-P05. Push the exported site to GitHub** · _Prompt_

```text
Push this to a private GitHub repository and call it whatever you want.
```

**G20-P06. Test on localhost** · _Prompt_

```text
Make sure the website works as expected and open it up in a local host for me to view.
```

**G20-P07. Fix a Vercel 404** · _Prompt_

```text
I just pushed to GitHub, synced to Vercel, and got a 404. What does this mean? How do I fix it?
```

**G20-P08. Mobile optimization** · _Prompt_

```text
Optimize this for mobile without affecting the desktop view. Move the video below the text, reduce font size, etc.
```

**G20-P09. Use negatives and real references in design prompts** · _Prompt_

```text
no Inter, no Roboto, no YC gradients, no weird punctuation
Linear 2023 with higher density
```

### G21. 32 Claude Code Hacks - From Beginner to Power User

Video: 32 Claude Code Hacks in 16 Mins (2026-04-27)  
PDF: [32 Claude Code Hacks - From Beginner to Power User.pdf](https://drive.google.com/file/d/1p2PZWSdj24h3MABg5-8QoDQZKsZ_qbtQ/view)

**G21-P01. Compact with keep-instructions** · _Prompt_

```text
/compact but keep all API integration decisions and database schema
```

**G21-P02. Give Claude problems, not commands** · _Prompt_

```text
How should we handle growth tracking?
```

**G21-P03. Make Claude ask questions until aligned** · _Prompt_

```text
Continuously ask me questions until you are 95% confident that you understand exactly what I need and what you need to do.
```

**G21-P04. Self-checking to-do list (example sequence)** · _Prompt_

```text
1) Build the website, 2) Take a screenshot and check that everything looks right, 3) Open Chrome DevTools and confirm there are no functionality errors.
```

**G21-P05. To-do quality rule** · _System / CLAUDE.md rule_

```text
Do not move on to the next to-do until you are 95% confident that the current one is good.
```

**G21-P06. Challenge a mediocre output** · _Prompt_

```text
scrap that, do a more elegant version
this is not good enough, try again with a completely different approach
```

**G21-P07. Screenshot self-check** · _Prompt_

```text
Take a screenshot of the website and tell me if the layout looks right.
```

**G21-P08. Clone an inspiration site (with screenshots attached)** · _Prompt_

```text
make it look like this
```

**G21-P09. /loop recurring task and one-time reminder** · _Prompt_

```text
every 5 minutes, check in on the deployment
remind me at 3 p.m. to check in with the team on X
```

**G21-P10. Plain-English analytics via a CLI (e.g., BigQuery bq)** · _Prompt_

```text
What were our top 10 revenue sources last quarter?
```

### G22. Claude Design Masterclass Resource Guide

Video: Claude Design Masterclass: Websites, Videos & More (2 Hours) (2026-04-30)  
PDF: [Claude Design Masterclass Resource Guide.pdf](https://drive.google.com/file/d/1xh9-UfR6Jg5qelCvEMXTvInVqNzyd_ad/view)

**G22-P01. Design system feedback: protect your logo** · _Prompt_

```text
the logo should not be modified from the PNG I uploaded
```

**G22-P02. Ask for a Tweaks panel** · _Prompt_

```text
give me a bunch of tweaks I can play around with
```

**G22-P03. Mobile app spec request (Claude Chat)** · _Prompt_

```text
full spec for a mobile app, requirement doc, text-based, that I can turn into a high-fidelity breakdown
```

**G22-P04. Launch video creative direction** · _Prompt_

```text
more dynamic, tell a story, more motion graphics, keep audience attention
```

**G22-P05. Verify the export locally** · _Prompt_

```text
open this on a local host so I can view it
```

**G22-P06. Negatives to include in design prompts** · _Prompt_

```text
no en dashes, no this font, no this color scheme
```

### G23. Master 97% of Codex in One Hour

Video: Master 97% of Codex in 1 Hour (full course) (2026-05-06)  
PDF: [Master 97% of Codex in One Hour.pdf](https://drive.google.com/file/d/1ZoiGbU-tE4HOfhueUb_j6XTFjqZlhRyl/view)

**G23-P01. Turn a workflow into a reusable skill (Codex)** · _Prompt_

```text
Turn that into a skill so every time I ask for [X], you do this exact flow.
```

**G23-P02. Change a skill's scope (Codex)** · _Prompt_

```text
Move this skill to global
Keep this skill local to this project
```

**G23-P03. Invoke a skill in natural language (Codex)** · _Prompt_

```text
grab my YouTube comments and give me insights
```

**G23-P04. Scheduled automation (Codex)** · _Prompt_

```text
Every Sunday at 5:00 PM, run the YouTube comment insights skill, refresh the data, and push the update to GitHub
```

**G23-P05. Migrate a Claude Code project to Codex** · _Prompt_

```text
Help me figure out what files to create to make this compatible with Codex.
```

### G24. Every Level of Claude Explained

Video: Every Level of Claude Explained in 21 Minutes (2026-05-12)  
PDF: [Every Level of Claude Explained.pdf](https://drive.google.com/file/d/1roxnL8945jtDcTuxqGPVRoC75yqP_Wtg/view)

**G24-P01. Ask a Claude Project about a past decision** · _Prompt_

```text
What was the thing we decided about the Q2 launch last week?
```

**G24-P02. Clean up a downloads folder (Cowork)** · _Prompt_

```text
sort everything by type, rename consistently, write me a summary
```

**G24-P03. Cowork folder rules** · _System / CLAUDE.md rule_

```text
Read about-me first. Never edit my templates. Always deliver to the outputs folder.
```

**G24-P04. CLAUDE.md negative instructions (examples)** · _System / CLAUDE.md rule_

```text
never do X
never write with em dashes
```

### G25. Three Ways to Deploy Your Claude Code Agents

Video: I Tested 3 Ways to Deploy Claude Agents (Here's When to Use Each) (2026-05-15)  
PDF: [Three Ways to Deploy Your Claude Code Agents.pdf](https://drive.google.com/file/d/1BQ0ySX4yfCd4TZPrzwiTuJKEyik2PxRX/view)

**G25-P01. Set up a /loop reminder** · _Prompt_

```text
Set up a loop every 10 minutes to remind me to take out the trash.
```

**G25-P02. Self-terminating loop** · _Prompt_

```text
Run this every 10 minutes, then kill the loop after 24 hours.
```

### G26. Codex vs Claude Code - Which Coding Agent Should You Actually Use

Video: 100 Hours Testing Claude Code vs ChatGPT Codex (honest results) (2026-05-26)  
PDF: [Codex vs Claude Code - Which Coding Agent Should You Actually Use.pdf](https://drive.google.com/file/d/1yJmwdfxWekUjWCHHIwIcRB3JM6JG5xdP/view)

**G26-P01. Switch a project from Claude Code to Codex** · _Prompt_

```text
I built this in Claude Code, you are Codex now. Walk through it, understand it, update what needs to change.
```

### G27. From Laid Off to Head of AI in 1 Year

Video: From Zero to Head of AI in 1 Year (as a regular person) (2026-06-12)  
PDF: [From Laid Off to Head of AI in 1 Year.pdf](https://drive.google.com/file/d/1uF_Td45_IpcfioKqF4F6ZuYEeGvNmdb-/view)

**G27-P01. Start from the work you already do** · _Prompt_

```text
Every day I do X, Y, and Z. How could AI help me here?
```

### G28. 6 AI Skills to Future-Proof Your Career

Video: Learn These 6 AI Skills Now (Before AI Replaces You) (2026-06-15)  
PDF: [6 AI Skills to Future-Proof Your Career.pdf](https://drive.google.com/file/d/1a_txv73VQlci-Km1KWykKClr9BC_22q1/view)

**G28-P01. Feed your edits back so the AI learns your taste** · _Prompt_

```text
Here are the five things I changed and why.
```

**G28-P02. Deterministic workflow vs. AI task (examples)** · _Prompt_

```text
Every morning at 9 a.m., pull last week's revenue from Stripe and post it in Slack.
Read these incoming customer emails, understand what they actually want, and draft a tailored response.
```

### G29. How to Build Effective Claude Code Agents in 2026

Video: 1000+ Hours in Claude Code in 60 Mins (2026-06-18)  
PDF: [How to Build Effective Claude Code Agents in 2026.pdf](https://drive.google.com/file/d/16VuVpBUlmAoBZe9UAp4WlZbqylPa6jPj/view)

**G29-P01. Single-file build spec (plan with context)** · _Template, adapted_

```text
Write one Markdown plan per build that answers:
- The goal: What are we building here?
- What success looks like: What does "done" actually mean?
- The validation strategy: How will the agent know the work is done and working well?
- The integration points: Which parts of the codebase do we need to touch, and which files will we create or edit?
```

**G29-P02. Homework: explain an agent harness** · _Prompt, adapted_

```text
Explain an agent harness.
```

**G29-P03. Ask the model to verify, not to judge** · _Prompt_

```text
Does this automation handle this input?
```

**G29-P04. Edge-case check after implementation** · _Prompt_

```text
How could this go wrong?
```

**G29-P05. System evolution after every issue** · _Prompt_

```text
What rule, document, or skill update would prevent this next time?
```

**G29-P06. Debate panel / war room (agent team personas)** · _Prompt, adapted_

```text
One of you is a CEO, one is a beginner, one is a college student. Each of you do independent research, form your own opinion, then debate. Keep debating until you reach consensus.
```

**G29-P07. Adversarial review of a finished build** · _Prompt, adapted_

```text
Play devil's advocate and be mean to the first session's work. Surface real problems instead of being happy-go-lucky.
```


## Q3 2026

### G30. How Claude is Creating a New Generation of Millionaires - Resource Guide

Video: How Claude is Creating a New Generation of Millionaires (2026-07-03)  
PDF: [How Claude is Creating a New Generation of Millionaires - Resource Guide.pdf](https://drive.google.com/file/d/1B4OTJQ4-C1XwpkShm5oJA7JYkDjpdgrG/view)

**G30-P01. Describe your first task, then make Claude push back** · _Template, adapted_

```text
Describe the task as clearly as you can:
- What it is
- How you do it today
- What a win looks like
Before building anything, have Claude push back on the idea (e.g., run "The Roast": a council of sub-agents that returns one verdict: Go, Reshape, or Kill, with every point backed by something real).
```

### G31. 12 Lessons from 5,000 Hours Building with AI - Resource Guide

Video: 5000 Hours of Building AI in Just 17 Minutes (2026-08-04)  
PDF: [12 Lessons from 5,000 Hours Building with AI - Resource Guide.pdf](https://drive.google.com/file/d/1cQp_Ib8KWhAccPWwH-Cq6MDthHMb0pKO/view)

**G31-P01. Negative prompting guardrails (examples)** · _System / CLAUDE.md rule_

```text
Do not add unrequested features.
Do not create error handling for impossible scenarios.
```

**G31-P02. Challenge the plan from several perspectives** · _Prompt, adapted_

```text
Challenge this plan from three perspectives:
- A skeptical customer who must trust or buy the result.
- A competitor looking for weaknesses or differentiation.
- An engineer responsible for long term maintenance.
```

**G31-P03. Website verification loop (have the AI prove it's done)** · _Prompt, adapted_

```text
1. Capture screenshots and check that every element stays in bounds.
2. Inspect the mobile layout and visual quality.
3. Click every important button and complete the signup flow.
4. Confirm that forms are formatted correctly and reach the correct webhook.
Prove that the work is complete before you report completion.
```

**G31-P04. Permission rule (example)** · _System / CLAUDE.md rule_

```text
only draft emails
```

### G32. How to Build a One Person AI Business in 2026

Video: How to Build a One Person AI Business (Using Claude Code) (2026-08-11)  
PDF: [How to Build a One Person AI Business in 2026.pdf](https://drive.google.com/file/d/1pfF0uMUJAahHcgxAbA_LNHHZDSbYr5Nq/view)

**G32-P01. Outreach prompt: warm first-touch message** · _Prompt_

```text
Act as a B2B outreach copywriter. Write a casual, friendly first touch message for a warm contact. I am a one person AI consultant and I built [specific system]. My goal is not to pitch. It is to get a 20 minute call to learn about their business and show them what I built. Keep it under 100 words. Avoid corporate language. Write it like a real person who built something useful.
```

**G32-P02. Four Blank Test (scoping formula)** · _Template_

```text
This automation is in the [outcome bucket]. The specific KPI is [metric]. The baseline today is [number]. After 60 days, we expect [target].
```

**G32-P03. Smallest Valuable Product prompt** · _Prompt_

```text
I am targeting [specific niche], and they struggle with [specific problem]. Help me scope the smallest valuable product I can ship in two weeks as a solo founder. Give me the core feature that solves 80% of the pain, the features I should explicitly exclude from V1, the technology stack you recommend for a nontechnical founder using Claude Code, and the potential competitors plus my differentiation.
```

**G32-P04. Pricing prompt: three tiers with psychological anchoring** · _Prompt_

```text
I am a one person AI consultant offering [service] to [customer type]. They currently solve this through [manual alternative]. Build three pricing tiers using psychological anchoring. Map the tiers to education and setup, an audit or single project, and a monthly retainer. For each tier, provide the deliverable, price range, and most important value message.
```

### G33. Claude Fable 5.1 Prompting Resource Guide

Video: I Analyzed How Anthropic ACTUALLY Prompts Fable 5.1 (2026-09-02)  
PDF: [Claude Fable 5.1 Prompting Resource Guide.pdf](https://drive.google.com/file/d/1vjnp5UbMVRTDkHeY6lqIEHrGiEJPQRGc/view)

**G33-P01. Rule 1 better prompt: give the outcome, not every task** · _Prompt_

```text
Create an appealing landing page that offers voice agent solutions to our target audience. Use current research and our business context to decide what the page needs. The result should be complete, accurate, persuasive, and ready to publish.
```

**G33-P02. Rule 1 template: define done, then tell it to finish** · _Template_

```text
Goal: Here is the outcome I need and why it matters: [goal and context].
Success: The work is complete when: [definition of done].
Completion: Complete this end to end. Make routine reversible decisions yourself. Do not stop with a plan or ask permission for steps already included in the request.
```

**G33-P03. Rule 3 template: require verification, not confidence** · _Template_

```text
Verification: Before calling this complete, test the result using the same checks a capable human reviewer would use. Show what passed, what failed, what you fixed, and anything that remains unverified.
```

**G33-P04. Rule 4 template: parallelize and delegate** · _Template_

```text
Execution: Identify which parts of this task are independent. Run independent tool calls at the same time. Delegate substantial independent workstreams when useful, continue productive work while they run, and keep dependent operations sequential.
```

**G33-P05. Master prompt: all four rules together** · _Template_

```text
Goal: Here is what I need to accomplish and why it matters: [goal and context].
Definition of Done: The work is complete when: [observable success criteria].
Completion: Complete the task end to end. Make routine reversible decisions yourself. Stop only for a destructive action, a material scope change, or information only I can provide.
Effort: Use the lowest effort level that reliably produces the required quality. Increase effort for difficult reasoning and reduce it for routine execution.
Verification: Check every material result before calling the task complete. Correct failures and clearly disclose anything unverified.
Execution: Run independent operations at the same time. Delegate substantial independent workstreams and continue useful work while they run.
```

### G34. AI Trading with Codex and GPT 6 Astra

Video: I Turned GPT-6 Astra Into a 24/7 Stock Trader (tutorial) (2026-09-07)  
PDF: [AI Trading with Codex and GPT 6 Astra.pdf](https://drive.google.com/file/d/13cBUT-Sj_rIhZ5ldVqR90fpvLkeAWGo0/view)

**G34-P01. Starter prompt: 7-day trading research & monitoring project (Codex)** · _Prompt_

```text
Use GPT 6 Astra to help me build a seven market day trading research and monitoring project. First ask for my dates, budget, allowed instruments, and loss limits. Research official calendars and company announcements, and save a cited Markdown strategy. Create project instructions, readiness tracking, a project local Alpaca .env template, read only account/data checks, and a durable progress journal. Keep real credentials out of chat and shared files. Configure the check times in this guide through one automation returning to this conversation, adjusted for my session dates and timezone. Connect my chosen ClickUp channel and send midday and after close reports, including no trade days. Test account reads, handoff recovery, schedule dates, and notification delivery. Leave live orders disabled until execution controls and paper trading tests have passed and I explicitly authorize execution.
```
