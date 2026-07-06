# GPA Daily News Mock-up

Minimal Streamlit prototype for a Deutsche Bank GPA-style daily banking news workflow.

The website-style mock-up demonstrates:

- left-side page navigation
- daily scraped article intake
- LLM-style relevance, department, category, tag, and summary fields
- editor selection and manual article entry
- expert review notes
- editable daily email generation
- send action with external SharePoint archive destination

No real scraping, LLM, email, or SharePoint integration is performed. All data is local Streamlit session state.

## Run

```bash
uv run streamlit run app.py
```
