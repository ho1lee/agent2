# Autonomous Agent Demo

This project demonstrates a simple autonomous agent using **LangGraph** to
route user questions to external tools and **Gradio** for a minimal web
interface.

Two placeholder tools are included:

- `crm_tool` &ndash; represents a CRM (SalesForce) API call.
- `scm_tool` &ndash; represents an SCM (o9) API call.

Each tool is executed with retry logic that retries failed calls up to three
 times using exponential backoff.

## Running

Install dependencies (for example using `pip`):

```bash
pip install -r requirements.txt
```

Then start the interface:

```bash
python -m app.main
```

Enter your question in the textbox. Mention **CRM** or **SCM** in the text to
route the call explicitly; otherwise the CRM tool is used by default.
