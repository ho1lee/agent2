# Autonomous Agent Demo

This project demonstrates a simple autonomous agent using **LangGraph** to
route user questions to external tools and **Gradio** for a minimal web
interface. An LLM determines which tool to call using OpenAI function
calling.

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

Set the `OPENAI_API_KEY` environment variable before running so the agent can
access the OpenAI API.

Enter your question in the textbox. The LLM will decide whether to call the
`crm_tool` or `scm_tool` based on your request.
