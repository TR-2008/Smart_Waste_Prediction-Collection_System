
from pathlib import Path
import json
import os

import pandas as pd
import streamlit as st

from core.settings_manager import load_settings, save_settings

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"


def read_csv_safe(path):
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def read_json_safe(path):
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def build_project_context():
    main = read_csv_safe(DATA_DIR / "main.csv")
    feedback = read_csv_safe(DATA_DIR / "feedback.csv")

    facts = []

    facts.append("PROJECT: Smart Waste Management & Prediction System")
    facts.append("Data is classroom/sample project data, not live municipal telemetry.")

    if not main.empty:
        facts.append(f"Main dataset records: {len(main)}")

        if "fill_pct" in main.columns:
            fill = pd.to_numeric(main["fill_pct"], errors="coerce").dropna()

            if not fill.empty:
                facts.append(f"Average bin fill: {fill.mean():.2f}%")
                facts.append(f"Maximum observed fill: {fill.max():.2f}%")
                facts.append(f"Minimum observed fill: {fill.min():.2f}%")
                facts.append(
                    f"Records with fill >= 80%: {(fill >= 80).sum()}"
                )

        if "location_type" in main.columns:
            locations = main["location_type"].value_counts().to_dict()
            facts.append(f"Records by location: {locations}")

        label_column = next(
            (
                c for c in [
                    "collection_required",
                    "needs_collection",
                    "collection_label",
                    "label",
                    "target"
                ]
                if c in main.columns
            ),
            None
        )

        if label_column:
            facts.append(
                "Collection label distribution: "
                + str(main[label_column].value_counts(dropna=False).to_dict())
            )
    else:
        facts.append("Main dataset is unavailable.")

    if not feedback.empty:
        facts.append(f"Feedback records: {len(feedback)}")

        if "sentiment_label" in feedback.columns:
            sentiments = (
                feedback["sentiment_label"]
                .astype(str)
                .str.lower()
                .value_counts()
                .to_dict()
            )
            facts.append(f"Feedback sentiment distribution: {sentiments}")

    report_names = [
        "supervised_metrics.json",
        "mobilenetv2_test_metrics.json",
        "nlp_metrics.json"
    ]

    for name in report_names:
        report = read_json_safe(REPORTS_DIR / name)
        if report:
            facts.append(f"{name}: {report}")

    return main, feedback, "\n".join(facts)


def generate_offline_summary(main, feedback):
    sections = [
        "## Offline Waste Management Summary",
        "This report is generated locally from available project files."
    ]

    if main.empty:
        sections.append(
            "Main dataset is unavailable. Dataset-based recommendations "
            "cannot be calculated."
        )
    else:
        sections.append(f"**Dataset records:** {len(main)}")

        if "fill_pct" in main.columns:
            fill = pd.to_numeric(
                main["fill_pct"], errors="coerce"
            ).dropna()

            if not fill.empty:
                average = fill.mean()
                high = int((fill >= 80).sum())

                sections.append(f"**Average bin fill:** {average:.2f}%")
                sections.append(f"**Bins/records at 80% or above:** {high}")

                if high:
                    sections.append(
                        "Review high-fill records first and prioritize "
                        "collection according to location and operational "
                        "capacity."
                    )
                else:
                    sections.append(
                        "No records at or above the 80% review threshold "
                        "were found in the available data."
                    )

        if "location_type" in main.columns:
            distribution = main["location_type"].value_counts()

            sections.append("### Location distribution")
            for location, count in distribution.items():
                sections.append(f"- {location}: {count} records")

    if not feedback.empty and "sentiment_label" in feedback.columns:
        sentiments = (
            feedback["sentiment_label"]
            .astype(str)
            .str.lower()
            .value_counts()
        )

        sections.append("### Feedback sentiment")

        for sentiment, count in sentiments.items():
            sections.append(f"- {sentiment.title()}: {count}")

        if "negative" in sentiments.index:
            sections.append(
                "Review negative feedback to identify recurring service "
                "or collection issues."
            )

    sections.append(
        "\n**Limitations:** These are descriptive insights from the supplied "
        "sample data. They are not live sensor readings or guaranteed "
        "operational predictions."
    )

    return "\n\n".join(sections)


def get_groq_key():
    key = os.getenv("GROQ_API_KEY")

    if not key:
        try:
            key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            key = None

    return key


def generate_groq_summary(context):
    from groq import Groq

    api_key = get_groq_key()

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY was not found. Add it to "
            ".streamlit/secrets.toml or your environment variables."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert waste management data analyst. "
                    "Analyze only the supplied project facts. "
                    "Never invent statistics, sensor readings, model "
                    "accuracy, or missing information. "
                    "Clearly identify sample data. "
                    "Write a professional report with headings, "
                    "key findings, limitations, and practical recommendations."
                )
            },
            {
                "role": "user",
                "content": (
                    "Generate a detailed Smart Waste Management report "
                    "from these actual project statistics:\n\n"
                    + context
                )
            }
        ],
        temperature=0.3,
        max_completion_tokens=1200
    )

    return response.choices[0].message.content


# ---------------- PAGE UI ----------------

st.title("✨ AI Waste Management Summary")
st.caption(
    "Generate project insights using local analysis or Groq AI."
)

settings = load_settings()
current_mode = settings.get("summary_mode", "Offline")

mode = st.selectbox(
    "Select AI Summary Mode",
    ["Offline", "Groq"],
    index=0 if current_mode == "Offline" else 1
)

if st.button("Save Summary Preference"):
    settings["summary_mode"] = mode
    save_settings(settings)
    st.success(f"{mode} mode preference saved.")

main_df, feedback_df, project_context = build_project_context()

with st.expander("View data sources used"):
    st.write("Main dataset:", len(main_df), "records")
    st.write("Feedback dataset:", len(feedback_df), "records")
    st.caption(
        "Only available local project statistics are used. "
        "Raw image files and API secrets are not sent."
    )

if mode == "Offline":
    st.info("Offline mode: no internet connection or API key is required.")

    if st.button("Generate Offline Summary", type="primary"):
        with st.spinner("Analyzing local project data..."):
            summary = generate_offline_summary(main_df, feedback_df)

        st.session_state["ai_summary_result"] = summary
        st.session_state["ai_summary_source"] = "Offline"

else:
    st.info("Groq mode: requires internet access and a valid API key.")

    if st.button("Generate Groq AI Summary", type="primary"):
        try:
            with st.spinner("Groq AI is analyzing your project data..."):
                summary = generate_groq_summary(project_context)

            st.session_state["ai_summary_result"] = summary
            st.session_state["ai_summary_source"] = "Groq AI"

        except Exception as error:
            st.error(f"Groq request failed: {error}")
            st.warning("Generating an offline summary instead.")

            fallback = generate_offline_summary(main_df, feedback_df)
            st.session_state["ai_summary_result"] = fallback
            st.session_state["ai_summary_source"] = "Offline fallback"

if st.session_state.get("ai_summary_result"):
    st.divider()
    st.subheader("Generated Report")
    st.caption(
        "Generated using: "
        + st.session_state.get("ai_summary_source", "Unknown")
    )

    st.markdown(st.session_state["ai_summary_result"])

    st.download_button(
        "Download Summary",
        data=st.session_state["ai_summary_result"],
        file_name="smart_waste_ai_summary.md",
        mime="text/markdown"
    )
