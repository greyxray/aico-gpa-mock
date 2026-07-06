# Agent Instructions

This repository is a minimal Streamlit mock-up for a Deutsche Bank GPA-style daily regulatory news workflow.

## Purpose

This app is a front-end mock-up. It must not implement real scraping, LLM calls, email sending, or SharePoint writes unless explicitly requested.

The user wants the mock-up to feel like a website, not a generic Streamlit notebook/tool. Navigation is in the left sidebar. Generated shortlist and final-email workspaces appear as new sidebar entries after the editor creates them.

## Run Command

Use local project cache/env paths so `uv` does not touch global cache locations:

```bash
cd /Users/greyxray/work/aico-gpa-mock
UV_CACHE_DIR=.uv-cache UV_PROJECT_ENVIRONMENT=.venv uv run streamlit run app.py --server.port 8501 --server.headless true
```

Then open:

```text
http://localhost:8501
```

If binding the local server fails under a sandbox, rerun with permission to bind a local HTTP port.

## Current Workflow Model

1. Backend batch job runs outside the website.
   - Scrapes regulatory/news sources.
   - Runs AI classification and summarization.
   - Pushes resulting records to a database.
   - The mock simulates this database with `seed_articles()` and `st.session_state`.

2. Dashboard is the main database view.
   - Do not create a separate Article Database page.
   - Dashboard has date/category filters.
   - Default date range is the past 24 hours, represented as yesterday through today because mock data is date-only.
   - Default view shows only articles that passed criteria.
   - A button reveals articles that did not pass criteria.
   - Dashboard table includes a checkbox for the editor to cherry-pick articles for an initial draft.
   - Dashboard table should show `Was published`, not `editor shortlist` or `already published`.

3. Editor creates a shortlist.
   - Pressing `Create shortlist page` creates a generated `Shortlist S-...` page in the sidebar.
   - This page is a shared review workspace for editors and experts.
   - Users can modify summaries, categories, and notes there.

4. Shortlist generates a final email page.
   - Pressing `Generate final email page` creates `Final email E-...` in the sidebar.
   - The final email page has one editable generated email text area.
   - It has two distinct actions with warning/help text:
     - `Send draft to experts`: sends only to expert review list, does not archive, does not send to final list.
     - `Send final email and archive`: sends to final distribution list and archives to SharePoint.

## Avoid Reintroducing

- Do not show `Run scrape` or `Run AI classification`; those happen as backend batch jobs.
- Do not show a progress bar on the dashboard.
- Do not use dashboard metrics such as `Editor shortlist`, `Ready for final email`, or `Expert reviews`.
- Do not show `passed criteria` as a dashboard column; the default view already implies that.
- Do not use `already published`; use `Was published`.
- Do not make a separate Archive page. Archive is external SharePoint storage.
- Do not make a separate Article Database page; dashboard already is the filtered database view.

## Categories

Use only these category values:

- `Prudential`
- `capital markets`
- `sustainable finance`
- `payments`
- `digital`
- `U.S.`
- `N/A`
- `failed to process`

## Mock Constants

These placeholders are in `app.py`:

- Final mailing list: `gpa-daily-regulatory-news@db.com`
- Expert review list: `gpa-subject-matter-experts@db.com`
- SharePoint archive path: `/GPA/Daily-News/Published-Digests/`

## Implementation Notes

- `APP_VERSION` resets Streamlit session state when the mock data/workflow shape changes.
- Generated pages are stored in `st.session_state.shortlists` and `st.session_state.final_emails`.
- Article data is stored in `st.session_state.articles`.
- Mock article dates are dynamic, based on `date.today()`.
- Streamlit has no true generated URL routing here; generated pages are represented as sidebar entries like `Shortlist S-001` and `Final email E-001`, plus displayed URL-like captions.

## Verification

Syntax check:

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m py_compile app.py
```

Check server is listening:

```bash
lsof -nP -iTCP:8501 -sTCP:LISTEN
```
