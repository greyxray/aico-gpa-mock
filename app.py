from __future__ import annotations

from datetime import date, timedelta
from textwrap import dedent

import streamlit as st


DEPARTMENTS = [
    "GPA Banking",
    "Risk",
    "Compliance",
    "Treasury",
    "Sustainability",
    "Legal",
    "Markets",
]

CATEGORIES = [
    "Prudential",
    "capital markets",
    "sustainable finance",
    "payments",
    "digital",
    "U.S.",
    "N/A",
    "failed to process",
]

SOURCES = [
    "ECB Banking Supervision",
    "EBA",
    "Bundesbank",
    "European Commission",
    "FATF",
    "FSB",
    "IOSCO",
]

APP_VERSION = "2026-07-06-v8"
MAILING_LIST = "gpa-daily-regulatory-news@db.com"
SHAREPOINT_ARCHIVE = "/GPA/Daily-News/Published-Digests/"
EXPERT_REVIEW_LIST = "gpa-subject-matter-experts@db.com"

PAGES = {
    "Dashboard": "1. Dashboard",
    "Manual": "2. Add manual article",
}


def article(
    article_id: str,
    days_ago: int,
    source: str,
    title: str,
    category: str,
    departments: str,
    importance: str,
    tags: str,
    summary: str,
    status: str,
    selected: bool,
    owner: str,
    expert_notes: str = "",
    origin: str = "Scraped",
    editor_pick: bool | None = None,
) -> dict:
    return {
        "id": article_id,
        "date": (date.today() - timedelta(days=days_ago)).isoformat(),
        "source": source,
        "title": title,
        "url": f"https://example.com/{article_id.lower()}",
        "category": category,
        "departments": departments,
        "importance": importance,
        "tags": tags,
        "summary": summary,
        "status": status,
        "selected": selected,
        "editor_pick": selected if editor_pick is None else editor_pick,
        "owner": owner,
        "expert_notes": expert_notes,
        "origin": origin,
    }


def seed_articles() -> list[dict]:
    return [
        article(
            "A-1001",
            0,
            "ECB Banking Supervision",
            "ECB outlines supervisory priorities for significant institutions",
            "Prudential",
            "GPA Banking, Risk",
            "High",
            "SREP, governance, credit risk",
            "ECB priorities indicate continued focus on credit risk controls, governance quality, and remediation discipline across supervised institutions.",
            "AI shortlisted",
            True,
            "Daily editor",
            editor_pick=True,
        ),
        article(
            "A-1002",
            0,
            "EBA",
            "EBA publishes final technical standards on reporting templates",
            "Prudential",
            "Compliance, Treasury",
            "Medium",
            "reporting, ITS, templates",
            "The update changes selected supervisory reporting templates and may require downstream implementation checks by reporting and treasury teams.",
            "Needs expert review",
            True,
            "Reporting expert",
            "Check whether effective date affects Q4 reporting cycle.",
            editor_pick=True,
        ),
        article(
            "A-1003",
            0,
            "Bundesbank",
            "Bundesbank discusses bank profitability and interest-rate risk",
            "Prudential",
            "Treasury, Risk",
            "High",
            "IRRBB, profitability, deposits",
            "The publication flags margin sensitivity and deposit behavior as supervisory themes for banks in the current rate environment.",
            "Editor approved",
            True,
            "Risk expert",
            editor_pick=True,
        ),
        article(
            "A-1004",
            0,
            "FATF",
            "FATF consults on beneficial ownership guidance",
            "Prudential",
            "Compliance, Legal",
            "Medium",
            "AML, KYC, beneficial ownership",
            "The consultation may influence AML control expectations and client due diligence processes once finalized.",
            "AI shortlisted",
            False,
            "Compliance expert",
            editor_pick=False,
        ),
        article(
            "A-1005",
            1,
            "FSB",
            "FSB reviews progress on crypto-asset regulatory implementation",
            "digital",
            "Markets, Risk, Compliance",
            "High",
            "crypto, implementation, global standards",
            "The review highlights implementation gaps across jurisdictions and reinforces supervisory attention on crypto-asset risk management.",
            "Sent",
            True,
            "Daily editor",
            "Included in yesterday's digest.",
            editor_pick=False,
        ),
        article(
            "A-1006",
            1,
            "European Commission",
            "Commission proposes targeted amendments to payments framework",
            "payments",
            "GPA Banking, Legal",
            "Medium",
            "PSD, payments, consumer protection",
            "The proposal may affect future payments policy positioning and future engagement with payments product teams.",
            "Needs expert review",
            True,
            "Legal expert",
            editor_pick=True,
        ),
        article(
            "A-1007",
            1,
            "IOSCO",
            "IOSCO updates expectations for market outage management",
            "Prudential",
            "Markets, Risk",
            "Medium",
            "operational resilience, markets, outages",
            "The update reinforces expectations for outage playbooks, market participant communications, and post-incident remediation.",
            "AI shortlisted",
            True,
            "Markets expert",
            editor_pick=False,
        ),
        article(
            "A-1008",
            2,
            "EBA",
            "EBA launches climate risk scenario collection exercise",
            "sustainable finance",
            "Sustainability, Risk",
            "High",
            "climate, scenario analysis, data",
            "The exercise could require additional climate data collection and alignment with internal risk scenario capabilities.",
            "Editor approved",
            True,
            "Risk expert",
            editor_pick=False,
        ),
        article(
            "A-1009",
            3,
            "ECB Banking Supervision",
            "ECB publishes observations on leveraged finance risk controls",
            "Prudential",
            "Risk, GPA Banking",
            "High",
            "leveraged finance, credit risk, controls",
            "The observations point to continued supervisory scrutiny of underwriting standards, portfolio monitoring, and escalation processes.",
            "Sent",
            True,
            "Daily editor",
            "Published in prior digest.",
            editor_pick=False,
        ),
        article(
            "A-1010",
            4,
            "FSB",
            "FSB reports on cross-border payment targets and remaining frictions",
            "failed to process",
            "GPA Banking, Treasury",
            "Medium",
            "cross-border payments, G20, frictions",
            "The scraper captured the source but the AI processor could not extract a reliable summary.",
            "Excluded",
            False,
            "Daily editor",
            editor_pick=False,
        ),
    ]


def init_state() -> None:
    if st.session_state.get("app_version") != APP_VERSION:
        st.session_state.articles = seed_articles()
        st.session_state.app_version = APP_VERSION
        st.session_state.email_body = ""
        st.session_state.current_page = "Dashboard"
        st.session_state.shortlists = {}
        st.session_state.final_emails = {}
    if "articles" not in st.session_state:
        st.session_state.articles = seed_articles()
    if "sent_digests" not in st.session_state:
        st.session_state.sent_digests = [
            {
                "date": (date.today() - timedelta(days=1)).isoformat(),
                "subject": "Daily Banking Regulatory News - Yesterday",
                "article_count": 1,
                "sharepoint_path": "/GPA/Daily-News/Archive/yesterday-digest.html",
            }
        ]
    if "email_body" not in st.session_state:
        st.session_state.email_body = ""
    if "shortlists" not in st.session_state:
        st.session_state.shortlists = {}
    if "final_emails" not in st.session_state:
        st.session_state.final_emails = {}


def next_article_id() -> str:
    numbers = [int(article["id"].split("-")[1]) for article in st.session_state.articles]
    return f"A-{max(numbers) + 1}"


def selected_articles(today_only: bool = False, include_sent: bool = False) -> list[dict]:
    return [
        article
        for article in st.session_state.articles
        if article.get("editor_pick")
        and article["status"] != "Excluded"
        and (include_sent or article["status"] != "Sent")
        and (not today_only or article["date"] == date.today().isoformat())
    ]


def generate_email(articles: list[dict]) -> str:
    sorted_articles = sorted(
        articles,
        key=lambda item: {"High": 0, "Medium": 1, "Low": 2}.get(item["importance"], 9),
    )

    if not sorted_articles:
        return "No articles selected for today's digest."

    items = []
    for idx, article in enumerate(sorted_articles, start=1):
        items.append(
            dedent(
                f"""
                {idx}. {article["title"]}
                Source: {article["source"]} | Category: {article["category"]} | Departments: {article["departments"]}
                Summary: {article["summary"]}
                Link: {article["url"]}
                """
            ).strip()
        )

    return "\n\n".join(
        [
            "Subject: Daily Banking Regulatory News",
            "Dear colleagues,",
            "Please find below today's selected regulatory and banking news items.",
            *items,
            "Best regards,\nGPA Daily Editorial Team",
        ]
    )


def as_records(edited_rows) -> list[dict]:
    if hasattr(edited_rows, "to_dict"):
        return edited_rows.to_dict("records")
    return list(edited_rows)


def article_in_date_range(article: dict, start: date, end: date) -> bool:
    article_date = date.fromisoformat(article["date"])
    return start <= article_date <= end


def update_articles_from_editor(edited_rows: list[dict]) -> None:
    by_id = {article["id"]: article for article in st.session_state.articles}
    for row in as_records(edited_rows):
        if row["id"] in by_id:
            by_id[row["id"]].update(row)
    st.session_state.articles = list(by_id.values())


def article_table(articles: list[dict], key: str) -> None:
    edited = st.data_editor(
        articles,
        key=key,
        hide_index=True,
        width="stretch",
        disabled=["id", "url", "origin"],
        column_config={
            "selected": st.column_config.CheckboxColumn("Passed criteria"),
            "editor_pick": st.column_config.CheckboxColumn("Editor shortlist"),
            "date": st.column_config.TextColumn("Date", width="small"),
            "source": st.column_config.SelectboxColumn("Source", options=SOURCES, width="medium"),
            "title": st.column_config.TextColumn("Title", width="large"),
            "category": st.column_config.SelectboxColumn("Category", options=CATEGORIES),
            "importance": st.column_config.SelectboxColumn(
                "Importance", options=["High", "Medium", "Low", "Ignore"]
            ),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=[
                    "New",
                    "AI shortlisted",
                    "Needs expert review",
                    "Editor approved",
                    "Sent",
                    "Excluded",
                ],
            ),
            "summary": st.column_config.TextColumn("AI / editor summary", width="large"),
            "expert_notes": st.column_config.TextColumn("Expert notes", width="large"),
        },
    )
    update_articles_from_editor(edited)


def render_header() -> None:
    st.set_page_config(page_title="GPA Daily News", layout="wide")
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.4rem; max-width: 1280px; }
        [data-testid="stSidebar"] {
            background: #f7f9fc;
            border-right: 1px solid #d9e1ec;
        }
        [data-testid="stSidebar"] h1 {
            font-size: 1.15rem;
            margin-bottom: 0;
        }
        [data-testid="stSidebar"] .stRadio label {
            font-size: 0.95rem;
        }
        .page-kicker {
            color: #5f6f85;
            font-size: 0.88rem;
            font-weight: 600;
            letter-spacing: 0;
            margin-bottom: 0.15rem;
            text-transform: uppercase;
        }
        .page-title {
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 0.2rem 0;
        }
        .page-subtitle {
            color: #4d5f73;
            font-size: 1rem;
            margin-bottom: 1.1rem;
        }
        .section-band {
            border-top: 1px solid #e2e8f0;
            padding-top: 1rem;
            margin-top: 1rem;
        }
        .status-pill {
            border: 1px solid #d8e0ea;
            border-radius: 999px;
            color: #35465c;
            display: inline-block;
            font-size: 0.82rem;
            margin: 0 0.35rem 0.35rem 0;
            padding: 0.18rem 0.6rem;
            background: #ffffff;
        }
        [data-testid="stMetricValue"] { font-size: 1.35rem; }
        div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMetric"]) {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 0.6rem 0.8rem;
            background: #fbfcfd;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    with st.sidebar:
        st.title("GPA News Desk")
        st.caption("Daily regulatory intelligence")
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"
        page_options = dict(PAGES)
        for shortlist_id in st.session_state.get("shortlists", {}):
            page_options[f"Shortlist:{shortlist_id}"] = f"Shortlist {shortlist_id}"
        for email_id in st.session_state.get("final_emails", {}):
            page_options[f"Email:{email_id}"] = f"Final email {email_id}"
        page_keys = list(page_options)
        if st.session_state.current_page not in page_keys:
            st.session_state.current_page = "Dashboard"
        page = st.radio(
            "Navigation",
            page_keys,
            format_func=lambda page_key: page_options[page_key],
            index=page_keys.index(st.session_state.current_page),
            label_visibility="collapsed",
        )
        st.session_state.current_page = page
        st.divider()
        st.markdown("**Today**")
        st.write(date.today().strftime("%d %b %Y"))
        st.markdown(
            """
            <span class="status-pill">Database updated</span>
            <span class="status-pill">AI fields ready</span>
            <span class="status-pill">Ready for editor selection</span>
            """,
            unsafe_allow_html=True,
        )
    return page


def go_to(page: str) -> None:
    st.session_state.current_page = page
    st.rerun()


def page_header(title: str, subtitle: str, kicker: str = "GPA Daily Banking News") -> None:
    st.markdown(f'<div class="page-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def render_dashboard() -> None:
    page_header(
        "Dashboard",
        "Filtered database view of scraped articles. The editor cherry-picks items here and creates a shortlist page.",
    )

    st.markdown("### Filters")
    f1, f2 = st.columns([1.4, 1.6])
    default_range = (date.today() - timedelta(days=1), date.today())
    date_range = f1.date_input("Publication date range", value=default_range)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = default_range
    categories = f2.multiselect("Category", CATEGORIES, default=[])

    if "show_failed_articles" not in st.session_state:
        st.session_state.show_failed_articles = False
    label = "Hide articles that did not pass criteria" if st.session_state.show_failed_articles else "Show articles that did not pass criteria"
    if st.button(label):
        st.session_state.show_failed_articles = not st.session_state.show_failed_articles
        st.rerun()
    show_failed = st.session_state.show_failed_articles

    filtered_articles = [
        article
        for article in st.session_state.articles
        if article_in_date_range(article, start_date, end_date)
        and (show_failed or article["selected"])
        and (not categories or article["category"] in categories)
    ]

    rows = [
        {
            "pick": bool(article.get("editor_pick")),
            "id": article["id"],
            "date": article["date"],
            "source": article["source"],
            "title": article["title"],
            "url": article["url"],
            "summary": article["summary"],
            "category": article["category"],
            "was_published": "Yes" if article["status"] == "Sent" else "No",
        }
        for article in filtered_articles
    ]

    edited_picks = st.data_editor(
        rows,
        key="dashboard_pick_editor",
        hide_index=True,
        width="stretch",
        disabled=["id", "date", "source", "title", "url", "summary", "category", "was_published"],
        column_config={
            "pick": st.column_config.CheckboxColumn("Pick for initial draft", width="small"),
            "id": st.column_config.TextColumn("Article ID", width="small"),
            "title": st.column_config.TextColumn("Title", width="large"),
            "url": st.column_config.LinkColumn("Link", display_text="Open", width="small"),
            "summary": st.column_config.TextColumn("Summary", width="large"),
            "category": st.column_config.SelectboxColumn("Category", options=CATEGORIES, width="medium"),
            "was_published": st.column_config.TextColumn("Was published", width="small"),
        },
    )

    by_id = {article["id"]: article for article in st.session_state.articles}
    picked_ids = {row["id"] for row in as_records(edited_picks) if row["pick"]}
    for article in filtered_articles:
        by_id[article["id"]]["editor_pick"] = article["id"] in picked_ids

    if filtered_articles:
        st.markdown("#### Edit one dashboard article")
        st.caption("Select one article, edit allowed fields, then submit. The table above is read-only.")
        article_options = [article["id"] for article in filtered_articles]
        selected_article_id = st.selectbox(
            "Article ID",
            article_options,
            format_func=lambda article_id: f"{article_id} - {by_id[article_id]['title']}",
            key="dashboard_selected_article",
        )
        selected_article = by_id[selected_article_id]

        with st.form(f"dashboard_article_form_{selected_article_id}"):
            c1, c2 = st.columns([1.3, 1])
            with c1:
                st.text_input("Title", value=selected_article["title"], disabled=True)
                st.link_button("Open publication", selected_article["url"])
                new_summary = st.text_area(
                    "Summary",
                    value=selected_article["summary"],
                    height=140,
                )
                new_expert_notes = st.text_area(
                    "Expert note",
                    value=selected_article.get("expert_notes", ""),
                    height=90,
                )
            with c2:
                st.text_input("Article ID", value=selected_article["id"], disabled=True)
                st.text_input("Source", value=selected_article["source"], disabled=True)
                st.text_input("Date", value=selected_article["date"], disabled=True)
                st.text_input("Was published", value="Yes" if selected_article["status"] == "Sent" else "No", disabled=True)
                new_category = st.selectbox(
                    "Category",
                    CATEGORIES,
                    index=CATEGORIES.index(selected_article["category"]) if selected_article["category"] in CATEGORIES else 0,
                )

            submitted = st.form_submit_button("Submit article changes", type="primary")

        if submitted:
            selected_article["summary"] = new_summary
            selected_article["expert_notes"] = new_expert_notes
            selected_article["category"] = new_category
            st.success(f"Updated {selected_article_id}.")
            st.rerun()

    picked_ids_in_order = [article["id"] for article in filtered_articles if article["id"] in picked_ids]

    c1, c2 = st.columns([1, 2])
    if c1.button("Create shortlist page", type="primary", width="stretch"):
        if not picked_ids:
            st.error("Select at least one article before creating a shortlist.")
        else:
            shortlist_id = f"S-{len(st.session_state.shortlists) + 1:03d}"
            st.session_state.shortlists[shortlist_id] = {
                "id": shortlist_id,
                "created": date.today().isoformat(),
                "status": "Draft",
                "article_ids": picked_ids_in_order,
                "review": {
                    article_id: {
                        "recommended_for_publishing": True,
                        "selected_for_publishing": False,
                        "expert_note": by_id[article_id].get("expert_notes", ""),
                    }
                    for article_id in picked_ids_in_order
                },
            }
            go_to(f"Shortlist:{shortlist_id}")
    c2.caption("Creating a shortlist generates a dedicated workspace page that can be shared with editors and experts.")


def render_manual_entry() -> None:
    page_header(
        "Manual Entry",
        "Add editor-discovered publications that were not found by the automated scrape.",
    )

    with st.form("manual_entry", clear_on_submit=True):
        c1, c2 = st.columns(2)
        title = c1.text_input("Title")
        url = c2.text_input("URL")
        source = c1.text_input("Source", placeholder="New website or publication name")
        category = c2.selectbox("Category", CATEGORIES)
        departments = st.multiselect("Departments", DEPARTMENTS, default=["GPA Banking"])
        importance = st.selectbox("Importance", ["High", "Medium", "Low", "Ignore"])
        tags = st.text_input("Tags", placeholder="comma-separated topics")
        passed_criteria = st.checkbox("Passed criteria", value=True)
        was_published = st.checkbox("Was published", value=False)
        summary = st.text_area("Initial summary", height=110)
        submitted = st.form_submit_button("Add article to database", type="primary")

    if submitted:
        if not title or not url:
            st.error("Title and URL are required for the manual entry.")
            return
        st.session_state.articles.insert(
            0,
            {
                "id": next_article_id(),
                "date": date.today().isoformat(),
                "source": source or "Manual source",
                "title": title,
                "url": url,
                "category": category,
                "departments": ", ".join(departments),
                "importance": importance,
                "tags": tags,
                "summary": summary or "Manual article added by editor; summary pending.",
                "status": "Sent" if was_published else "New",
                "selected": passed_criteria,
                "editor_pick": False,
                "owner": "Daily editor",
                "expert_notes": "",
                "origin": "Manual",
            },
        )
        st.success("Manual publication added to the article database.")


def articles_for_ids(article_ids: list[str]) -> list[dict]:
    by_id = {article["id"]: article for article in st.session_state.articles}
    return [by_id[article_id] for article_id in article_ids if article_id in by_id]


def parse_article_ids(raw_ids: str) -> list[str]:
    normalized = raw_ids.replace(",", " ").replace("\n", " ")
    seen = set()
    article_ids = []
    for article_id in normalized.split():
        article_id = article_id.strip().upper()
        if article_id and article_id not in seen:
            seen.add(article_id)
            article_ids.append(article_id)
    return article_ids


def ensure_shortlist_review(shortlist: dict) -> None:
    if "status" not in shortlist:
        shortlist["status"] = "Draft"
    if "review" not in shortlist:
        shortlist["review"] = {}
    by_id = {article["id"]: article for article in st.session_state.articles}
    for article_id in shortlist.get("article_ids", []):
        article = by_id.get(article_id, {})
        shortlist["review"].setdefault(
            article_id,
            {
                "recommended_for_publishing": True,
                "selected_for_publishing": False,
                "expert_note": article.get("expert_notes", ""),
            },
        )


def render_shortlist_page(shortlist_id: str) -> None:
    shortlist = st.session_state.shortlists.get(shortlist_id)
    if not shortlist:
        page_header("Shortlist not found", "This generated shortlist page no longer exists.")
        return
    ensure_shortlist_review(shortlist)

    page_header(
        f"Shortlist {shortlist_id}",
        "Shared review workspace for the editor and experts. Summaries, categories, and notes can be adjusted here.",
    )
    st.caption(f"Generated page: /shortlists/{shortlist_id}")
    st.markdown(f"**Status:** {shortlist['status']}")

    articles = articles_for_ids(shortlist["article_ids"])
    review = shortlist["review"]
    recommended_count = sum(
        1 for article in articles if review.get(article["id"], {}).get("recommended_for_publishing")
    )
    selected_count = sum(
        1 for article in articles if review.get(article["id"], {}).get("selected_for_publishing")
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Recommended", recommended_count)
    c2.metric("Selected for publishing", selected_count)
    c3.metric("Shortlist articles", len(articles))
    if selected_count > 4:
        st.warning("More than four articles are selected for publishing. The draft will still use the selected articles.")

    share_col, add_col = st.columns([1, 1])
    if share_col.button("Share with experts", width="stretch"):
        shortlist["status"] = "Shared with experts"
        shortlist["shared_at"] = date.today().isoformat()
        st.success(f"Mock shortlist shared with {EXPERT_REVIEW_LIST}.")
    if add_col.button("Add more articles", width="stretch"):
        st.session_state[f"show_add_more_{shortlist_id}"] = not st.session_state.get(
            f"show_add_more_{shortlist_id}", False
        )
        st.rerun()

    if st.session_state.get(f"show_add_more_{shortlist_id}", False):
        st.markdown("#### Add from dashboard")
        existing_ids = set(shortlist["article_ids"])
        available = [
            article
            for article in st.session_state.articles
            if article["id"] not in existing_ids and article["status"] != "Excluded"
        ]
        if not available:
            st.info("No additional dashboard articles are available for this shortlist.")
        else:
            st.caption("Use the IDs from the dashboard/database view. Enter one or more IDs separated by commas or spaces.")
            st.dataframe(
                [
                    {
                        "id": article["id"],
                        "date": article["date"],
                        "source": article["source"],
                        "title": article["title"],
                        "category": article["category"],
                        "was_published": "Yes" if article["status"] == "Sent" else "No",
                    }
                    for article in available
                ],
                hide_index=True,
                width="stretch",
                column_config={
                    "id": st.column_config.TextColumn("Article ID", width="small"),
                    "title": st.column_config.TextColumn("Title", width="large"),
                    "category": st.column_config.TextColumn("Category", width="medium"),
                    "was_published": st.column_config.TextColumn("Was published", width="small"),
                },
            )
            requested_ids = st.text_input(
                "Article IDs to add",
                placeholder="A-1004, A-1008",
                key=f"shortlist_add_ids_{shortlist_id}",
            )
            if st.button("Add selected articles to shortlist", type="primary"):
                ids_to_add = parse_article_ids(requested_ids)
                by_id = {article["id"]: article for article in st.session_state.articles}
                available_ids = {article["id"] for article in available}
                invalid_ids = [article_id for article_id in ids_to_add if article_id not in available_ids]
                if invalid_ids:
                    st.error(f"These IDs are not available to add: {', '.join(invalid_ids)}")
                    return
                for article_id in ids_to_add:
                    if article_id not in shortlist["article_ids"]:
                        shortlist["article_ids"].append(article_id)
                        review[article_id] = {
                            "recommended_for_publishing": False,
                            "selected_for_publishing": False,
                            "expert_note": by_id[article_id].get("expert_notes", ""),
                        }
                st.session_state[f"show_add_more_{shortlist_id}"] = False
                st.success(f"Added {len(ids_to_add)} article(s) to shortlist {shortlist_id}.")
                st.rerun()

    rows = [
        {
            "id": article["id"],
            "title": article["title"],
            "source": article["source"],
            "url": article["url"],
            "summary": article["summary"],
            "category": article["category"],
            "expert_note": review[article["id"]].get("expert_note", article.get("expert_notes", "")),
            "recommended_for_publishing": bool(review[article["id"]].get("recommended_for_publishing")),
            "selected_for_publishing": bool(review[article["id"]].get("selected_for_publishing")),
            "was_published": "Yes" if article["status"] == "Sent" else "No",
        }
        for article in articles
    ]

    st.dataframe(
        rows,
        hide_index=True,
        width="stretch",
        column_config={
            "id": st.column_config.TextColumn("Article ID", width="small"),
            "title": st.column_config.TextColumn("Title", width="large"),
            "source": st.column_config.TextColumn("Source", width="medium"),
            "url": st.column_config.LinkColumn("Link", display_text="Open", width="small"),
            "summary": st.column_config.TextColumn("Summary", width="large"),
            "category": st.column_config.SelectboxColumn("Category", options=CATEGORIES),
            "expert_note": st.column_config.TextColumn("Expert note", width="large"),
            "recommended_for_publishing": st.column_config.CheckboxColumn("Recommended for publishing"),
            "selected_for_publishing": st.column_config.CheckboxColumn("Selected for publishing"),
            "was_published": st.column_config.TextColumn("Was published", width="small"),
        },
    )

    st.markdown("#### Edit one article")
    st.caption("Select one shortlist row, edit the allowed fields, then submit. The article ID, title, source, link, and publication status are read-only.")
    article_options = [article["id"] for article in articles]
    selected_article_id = st.selectbox(
        "Article ID",
        article_options,
        format_func=lambda article_id: f"{article_id} - {next((article['title'] for article in articles if article['id'] == article_id), '')}",
        key=f"shortlist_selected_article_{shortlist_id}",
    )
    selected_article = next(article for article in articles if article["id"] == selected_article_id)
    selected_review = review[selected_article_id]

    with st.form(f"shortlist_row_form_{shortlist_id}_{selected_article_id}"):
        c1, c2 = st.columns([1.3, 1])
        with c1:
            st.text_input("Title", value=selected_article["title"], disabled=True)
            st.link_button("Open publication", selected_article["url"])
            new_summary = st.text_area(
                "Summary",
                value=selected_article["summary"],
                height=140,
            )
            new_expert_note = st.text_area(
                "Expert note",
                value=selected_review.get("expert_note", selected_article.get("expert_notes", "")),
                height=90,
            )
        with c2:
            st.text_input("Article ID", value=selected_article["id"], disabled=True)
            st.text_input("Source", value=selected_article["source"], disabled=True)
            st.text_input("Was published", value="Yes" if selected_article["status"] == "Sent" else "No", disabled=True)
            new_category = st.selectbox(
                "Category",
                CATEGORIES,
                index=CATEGORIES.index(selected_article["category"]) if selected_article["category"] in CATEGORIES else 0,
            )
            new_recommended = st.checkbox(
                "Recommended for publishing",
                value=bool(selected_review.get("recommended_for_publishing")),
            )
            new_selected = st.checkbox(
                "Selected for publishing",
                value=bool(selected_review.get("selected_for_publishing")),
            )

        submitted = st.form_submit_button("Submit article changes", type="primary")

    if submitted:
        by_id = {article["id"]: article for article in st.session_state.articles}
        by_id[selected_article_id]["summary"] = new_summary
        by_id[selected_article_id]["category"] = new_category
        by_id[selected_article_id]["expert_notes"] = new_expert_note
        review[selected_article_id] = {
            "expert_note": new_expert_note,
            "recommended_for_publishing": new_recommended,
            "selected_for_publishing": new_selected,
        }
        st.success(f"Updated {selected_article_id}.")
        st.rerun()

    selected_articles_for_email = [
        article for article in articles if review.get(article["id"], {}).get("selected_for_publishing")
    ]
    if st.button("Present draft email", type="primary", width="stretch"):
        if not selected_articles_for_email:
            st.error("Select at least one article for publishing before creating the draft email.")
            return
        email_id = f"E-{len(st.session_state.final_emails) + 1:03d}"
        st.session_state.final_emails[email_id] = {
            "id": email_id,
            "shortlist_id": shortlist_id,
            "article_ids": [article["id"] for article in selected_articles_for_email],
            "body": generate_email(selected_articles_for_email),
        }
        go_to(f"Email:{email_id}")


def render_final_email_page(email_id: str) -> None:
    final_email = st.session_state.final_emails.get(email_id)
    if not final_email:
        page_header("Final email not found", "This generated final email page no longer exists.")
        return

    page_header(
        f"Final Email {email_id}",
        "Single editor space for modifying the generated email before draft review or final send.",
    )
    st.caption(f"Generated page: /final-emails/{email_id}")

    articles = articles_for_ids(final_email["article_ids"])
    if not final_email.get("body"):
        final_email["body"] = generate_email(articles)

    final_email["body"] = st.text_area("Editable final email text", value=final_email["body"], height=460)

    st.caption(f"Final action: sends to {MAILING_LIST} and archives the email to SharePoint space {SHAREPOINT_ARCHIVE}.")
    if st.button("Send final email and archive", type="primary", width="stretch"):
        for article in articles:
            article["status"] = "Sent"
        st.session_state.sent_digests.insert(
            0,
            {
                "date": date.today().isoformat(),
                "subject": "Daily Banking Regulatory News",
                "article_count": len(articles),
                "sharepoint_path": f"{SHAREPOINT_ARCHIVE}{date.today().isoformat()}-digest.html",
            },
        )
        st.success(f"Mock final email sent to {MAILING_LIST} and archived to {SHAREPOINT_ARCHIVE}.")


def render_review() -> None:
    page_header(
        "Editor Shortlist / Review Draft",
        "The editor-owned shortlist. Experts can be asked for feedback, but final changes are applied by the editor here.",
    )

    default_range = (date.today() - timedelta(days=1), date.today())
    date_range = st.date_input("Review publication date range", value=default_range)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = default_range

    selected = [
        article
        for article in selected_articles()
        if article_in_date_range(article, start_date, end_date)
    ]
    if not selected:
        st.info("No articles are currently selected.")
        return

    st.info(
        f"Simple initial model: this page is owned by the daily editor. The review button sends this packet to {EXPERT_REVIEW_LIST}; expert comments are handled outside the platform and recorded here by the editor."
    )

    if st.button("Send review draft to experts", width="stretch"):
        for article in selected:
            if article["status"] not in ["Editor approved", "Sent"]:
                article["status"] = "Needs expert review"
        st.success(f"Mock review draft sent to {EXPERT_REVIEW_LIST}.")

    for article in selected:
        with st.expander(f"{article['importance']} · {article['title']}", expanded=article["importance"] == "High"):
            c1, c2 = st.columns([2, 1])
            with c1:
                article["summary"] = st.text_area(
                    "Summary",
                    value=article["summary"],
                    key=f"summary_{article['id']}",
                    height=120,
                )
                article["expert_notes"] = st.text_area(
                    "Expert notes",
                    value=article["expert_notes"],
                    key=f"notes_{article['id']}",
                    height=90,
                )
            with c2:
                article["status"] = st.selectbox(
                    "Decision",
                    [
                        "AI shortlisted",
                        "Needs expert review",
                        "Editor approved",
                        "Excluded",
                    ],
                    index=[
                        "AI shortlisted",
                        "Needs expert review",
                        "Editor approved",
                        "Excluded",
                    ].index(article["status"])
                    if article["status"] in [
                        "AI shortlisted",
                        "Needs expert review",
                        "Editor approved",
                        "Excluded",
                    ]
                    else 0,
                    key=f"status_{article['id']}",
                )
                owners = [
                    "Daily editor",
                    "Compliance expert",
                    "Risk expert",
                    "Reporting expert",
                    "Legal expert",
                    "Markets expert",
                ]
                article["owner"] = st.selectbox(
                    "Owner",
                    owners,
                    key=f"owner_{article['id']}",
                    index=owners.index(article["owner"]) if article["owner"] in owners else 0,
                )
                st.link_button("Open publication", article["url"])


def render_email_builder() -> None:
    page_header(
        "Final Email",
        "Filter reviewed articles, choose the final set, generate the digest, then send and archive it externally.",
    )

    st.info(f"Send action: email will be sent to {MAILING_LIST} and archived to SharePoint space {SHAREPOINT_ARCHIVE}.")

    default_range = (date.today() - timedelta(days=1), date.today())
    date_range = st.date_input("Publication date range", value=default_range)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = default_range

    candidates = [
        article
        for article in st.session_state.articles
        if article["selected"]
        and article["status"] != "Excluded"
        and article_in_date_range(article, start_date, end_date)
    ]

    rows = [
        {
            "include": bool(article.get("editor_pick")) and article["status"] != "Sent",
            "id": article["id"],
            "date": article["date"],
            "title": article["title"],
            "summary": article["summary"],
            "category": article["category"],
            "status": article["status"],
        }
        for article in candidates
    ]

    edited = st.data_editor(
        rows,
        key="final_email_article_selector",
        hide_index=True,
        width="stretch",
        disabled=["id", "date", "title", "summary", "category", "status"],
        column_config={
            "include": st.column_config.CheckboxColumn("Include"),
            "title": st.column_config.TextColumn("Title", width="large"),
            "summary": st.column_config.TextColumn("Summary", width="large"),
            "category": st.column_config.TextColumn("Category", width="medium"),
            "status": st.column_config.TextColumn("Workflow status", width="medium"),
        },
    )

    included_ids = {row["id"] for row in as_records(edited) if row["include"]}
    selected = [article for article in candidates if article["id"] in included_ids]

    c1, c2 = st.columns([1, 1])
    if c1.button("Generate email draft", type="primary", width="stretch"):
        st.session_state.email_body = generate_email(selected)
    if c2.button("Clear draft", width="stretch"):
        st.session_state.email_body = ""

    if not st.session_state.email_body:
        st.session_state.email_body = generate_email(selected)
    st.session_state.email_body = st.text_area(
        "Editable email",
        value=st.session_state.email_body,
        height=430,
    )

    if st.button("Send email and archive to SharePoint", type="primary", width="stretch"):
        for article in selected:
            article["status"] = "Sent"
        st.session_state.sent_digests.insert(
            0,
            {
                "date": date.today().isoformat(),
                "subject": "Daily Banking Regulatory News",
                "article_count": len(selected),
                "sharepoint_path": f"{SHAREPOINT_ARCHIVE}{date.today().isoformat()}-digest.html",
            },
        )
        st.success(f"Mock send complete: sent to {MAILING_LIST} and archived to {SHAREPOINT_ARCHIVE}.")


def render_archive() -> None:
    page_header(
        "Archive",
        "Look back at previous daily articles and sent digests.",
    )

    st.markdown("**Sent digests**")
    st.dataframe(st.session_state.sent_digests, hide_index=True, width="stretch")

    st.markdown("**Article history**")
    historical = sorted(st.session_state.articles, key=lambda item: item["date"], reverse=True)
    st.dataframe(
        [
            {
                "date": a["date"],
                "source": a["source"],
                "title": a["title"],
                "category": a["category"],
                "importance": a["importance"],
                "status": a["status"],
                "departments": a["departments"],
            }
            for a in historical
        ],
        hide_index=True,
        width="stretch",
    )


def main() -> None:
    render_header()
    init_state()
    page = render_sidebar()

    if page == "Dashboard":
        render_dashboard()
    elif page == "Manual":
        render_manual_entry()
    elif page.startswith("Shortlist:"):
        render_shortlist_page(page.split(":", 1)[1])
    elif page.startswith("Email:"):
        render_final_email_page(page.split(":", 1)[1])


if __name__ == "__main__":
    main()
