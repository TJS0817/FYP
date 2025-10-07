import streamlit as st
import sqlite3
import hashlib
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------- DB connection ----------
def get_connection():
    return sqlite3.connect("fyp_personality.db")

# ---------- password hashing ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, provided_password):
    return stored_hash == hash_password(provided_password)

# ---------- Load scaler and kmeans ----------
try:
    scaler = joblib.load("scaler.joblib")
    kmeans = joblib.load("kmeans.joblib")
    model_ready = True
except Exception:
    scaler = None
    kmeans = None
    model_ready = False

# ---------- 30 Questions ----------
questions = [
    "I have a vivid imagination.",
    "I enjoy trying new and foreign foods, activities, or experiences.",
    "I enjoy thinking about abstract ideas.",
    "I have a rich vocabulary.",
    "I prefer routine over variety.",
    "I am original, creative, and inventive.",
    "I am always prepared.",
    "I pay attention to details.",
    "I finish tasks successfully.",
    "I like order and organization.",
    "I often forget to put things back in their proper place.",
    "I make plans and stick to them.",
    "I am the life of the party.",
    "I enjoy social gatherings.",
    "I feel comfortable around people.",
    "I start conversations easily.",
    "I am quiet around strangers.",
    "I enjoy meeting new people.",
    "I sympathize with others’ feelings.",
    "I take time out for others.",
    "I have a soft heart.",
    "I am interested in others’ problems.",
    "I insult people.",
    "I make people feel at ease.",
    "I get stressed out easily.",
    "I worry about things.",
    "I get irritated easily.",
    "I remain calm in tense situations.",
    "I often feel blue.",
    "I am relaxed most of the time."
]

reverse_idx = {4, 10, 16, 22, 27, 29}
trait_map = {
    "Openness": list(range(0,6)),
    "Conscientiousness": list(range(6,12)),
    "Extraversion": list(range(12,18)),
    "Agreeableness": list(range(18,24)),
    "Neuroticism": list(range(24,30))
}

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Personality Profiling", layout="centered")

# ---------- Custom Styling ----------
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #C0C9EE, #A2AADB);
    }
    h1 {
        color: #898AC4;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    h2, h3 { color: #898AC4; }
    div.stButton > button {
        background-color: #898AC4;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #A2AADB;
        transform: scale(1.05);
    }
    input, select, textarea {
        border-radius: 8px !important;
        border: 1px solid #A2AADB !important;
        padding: 10px !important;
    }
    .stAlert {
        border-radius: 10px;
        background-color: #C0C9EE !important;
        color: #444 !important;
    }
    [data-testid="stSegmentedControl"] label {
        background-color: #fff;
        border-radius: 20px;
        padding: 8px 15px;
        margin: 3px;
        border: 1px solid #A2AADB;
        transition: all 0.3s;
    }
    [data-testid="stSegmentedControl"] label[data-selected="true"] {
        background-color: #898AC4;
        color: white;
        border: 1px solid #898AC4;
    }
    .stForm {
        background-color: #fff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(137,138,196,0.2);
        margin-top: 15px;
    }
    .js-plotly-plot .plotly .main-svg { border-radius: 12px; }
    .stSuccess {
        background-color: #A2AADB !important;
        color: #fff !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("PersonaPath")

# ---------- Navigation ----------
if "user_id" in st.session_state:
    menu_options = ["Personality Test", "Personality Profile", "Job Recommendations", "Dataset Trends", "Logout"]
else:
    menu_options = ["Login", "Register"]

if "menu" not in st.session_state:
    st.session_state.menu = "Login"

choice = st.segmented_control("", options=menu_options, default=st.session_state.menu)
st.session_state.menu = choice

# ---------- Register ----------
if choice == "Register":
    st.subheader("Register Account")
    username = st.text_input("Username")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not username or not email or not password:
            st.error("Please fill all fields")
        else:
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("SELECT id FROM users WHERE email=?", (email,))
                if cur.fetchone():
                    st.error("Email already registered.")
                else:
                    cur.execute(
                        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                        (username, email, hash_password(password))
                    )
                    conn.commit()
                    st.success("Registration successful! Redirecting to login...")
                    st.session_state.menu = "Login"
                    st.rerun()
            except Exception as e:
                st.error("Error: " + str(e))
            finally:
                cur.close()
                conn.close()

# ---------- Login ----------
elif choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, username, password FROM users WHERE email=?", (email,))
            row = cur.fetchone()
            if row:
                user_id, username, stored_hash = row
                if verify_password(stored_hash, password):
                    st.session_state['user_id'] = user_id
                    st.session_state['username'] = username
                    st.success(f"✅ Logged in as {username}.")
                    st.session_state.menu = "Personality Test"
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.error("No account found with that email")
        except Exception as e:
            st.error("DB error: " + str(e))
        finally:
            cur.close()
            conn.close()

# ---------- Personality Test ----------
elif choice == "Personality Test":
    if 'user_id' not in st.session_state:
        st.warning("Please login to take the test")
    else:
        st.subheader("Personality Test (30 Questions)")
        st.info("Choose: Strongly disagree, Disagree, Neutral, Agree, Strongly agree")

        with st.form("test_form"):
            answers = []
            for i, q in enumerate(questions, start=1):
                ans = st.radio(
                    f"Q{i}. {q}",
                    ("Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"),
                    key=f"q{i}",
                    index=None
                )
                val = None if ans is None else {
                    "Strongly disagree": 1,
                    "Disagree": 2,
                    "Neutral": 3,
                    "Agree": 4,
                    "Strongly agree": 5
                }[ans]
                answers.append(val)

            submitted = st.form_submit_button("Submit Test")

        if submitted:
            if None in answers:
                st.error("⚠️ Please answer all questions before submitting.")
            else:
                # reverse scoring
                scored = [(6 - v if idx in reverse_idx else v) for idx, v in enumerate(answers)]

                # compute trait totals
                openness = sum(scored[i] for i in trait_map["Openness"])
                conscientiousness = sum(scored[i] for i in trait_map["Conscientiousness"])
                extraversion = sum(scored[i] for i in trait_map["Extraversion"])
                agreeableness = sum(scored[i] for i in trait_map["Agreeableness"])
                neuroticism = sum(scored[i] for i in trait_map["Neuroticism"])

                # cluster
                feats = np.array([[openness, conscientiousness, extraversion, agreeableness, neuroticism]])
                if not model_ready:
                    st.warning("⚠️ Clustering model not found (scaler.joblib / kmeans.joblib).")
                    cluster_label = None
                else:
                    Xs = scaler.transform(feats)
                    cluster_label = int(kmeans.predict(Xs)[0])
                    st.session_state["cluster_label"] = cluster_label

                # save results to DB
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    sql = """
                    INSERT INTO personality_results (
                        user_id, taken_at,
                        q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,
                        q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,
                        q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,
                        openness_raw, conscientiousness_raw, extraversion_raw,
                        agreeableness_raw, neuroticism_raw, cluster_id
                    ) VALUES (
                        ?, ?, 
                        ?,?,?,?,?,?,?,?,?,?, 
                        ?,?,?,?,?,?,?,?,?,?, 
                        ?,?,?,?,?,?,?,?,?,?, 
                        ?,?,?,?,?,?,?
                    )
                    """
                    params = (
                        st.session_state['user_id'],
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        *answers,  # 30 answers
                        openness, conscientiousness, extraversion, agreeableness, neuroticism,
                        cluster_label
                    )
                    cur.execute(sql, params)
                    conn.commit()
                    st.success("✅ Your responses have been saved successfully.")
                    st.session_state.menu = "Personality Profile"
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save results: {e}")
                finally:
                    conn.close()

# ---------- Personality Profile ----------
elif choice == "Personality Profile":
    if "cluster_label" not in st.session_state:
        st.warning("⚠️ Please take the personality test first.")
    else:
        cluster = st.session_state["cluster_label"]
        st.subheader(f"Your Personality Cluster: {cluster}")
        st.write("View your strengths, traits, and job matches.")

# ---------- Job Recommendations ----------
elif choice == "Job Recommendations":
    if "cluster_label" not in st.session_state:
        st.warning("⚠️ Please take the personality test first.")
    else:
        cluster = st.session_state["cluster_label"]
        st.subheader("Top Recommendations for You")

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, job_title, company, job_desc, requirements FROM jobs WHERE cluster_id=?", (cluster,))
            jobs = cur.fetchall()
        except Exception as e:
            st.error("DB error: " + str(e))
            jobs = []
        finally:
            cur.close()
            conn.close()

        if not jobs:
            st.info("No jobs found for your profile yet.")
        else:
            for job in jobs:
                job_id, title, company, desc, req = job
                with st.container():
                    st.markdown(f"#### {title}")
                    st.caption(company)
                    st.write(desc[:150] + "...")
                    if st.button("View Details", key=f"job_{job_id}"):
                        with st.expander(f"Details for {title}"):
                            st.write("**Job Description:**", desc)
                            st.write("**Requirements:**", req)

# ---------- Dataset Trends ----------
elif choice == "Dataset Trends":
    # --- Page Header ---
    st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <h2 style="color:#898AC4;">📊 Dataset Trends & Insights</h2>
            <p style="font-size:16px; color:#555;">
                Explore personality distributions, average satisfaction, and emerging skill trends among Malaysian users.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 1️⃣ Personality Distribution (Donut Chart)
    st.subheader("🧠 Personality Type Distribution")

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT cluster_id, COUNT(*) FROM personality_results GROUP BY cluster_id")
        rows = cur.fetchall()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        rows = []
    finally:
        conn.close()

    cluster_labels = {
        0: "The Strategist",
        1: "The Connector",
        2: "The Analyzer",
        3: "The Helper"
    }

    if rows:
        clusters = [cluster_labels.get(r[0], f"Unknown ({r[0]})") for r in rows]
        counts = [r[1] for r in rows]

        fig = go.Figure(
            data=[go.Pie(
                labels=clusters,
                values=counts,
                hole=0.5,
                textinfo='label+percent',
                textfont_size=16
            )]
        )
        fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
        fig.update_layout(
            showlegend=True,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available yet to display personality distribution.")

    st.markdown("---")

    # 2️⃣ Job Satisfaction by Personality Type (Vertical Bar Chart)
    st.subheader("💼 Average Job Satisfaction by Personality Type")

    # You can later replace these values with data from your DB
    job_satisfaction = {
        "The Strategist": 3.8,
        "The Connector": 4.2,
        "The Analyzer": 3.5,
        "The Helper": 4.0
    }

    fig = go.Figure([
        go.Bar(
            x=list(job_satisfaction.keys()),
            y=list(job_satisfaction.values()),
            text=[f"{v:.1f}" for v in job_satisfaction.values()],
            textposition='auto',
            marker_color=['#C0C9EE', '#A2AADB', '#898AC4', '#6C63FF']
        )
    ])
    fig.update_layout(
        yaxis=dict(title="Satisfaction Level (1–5)"),
        xaxis=dict(title="Personality Type"),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 3️⃣ Top Soft Skills (Horizontal Bar Chart)
    st.subheader("🌟 Top Soft Skills in Demand (2025 Trends)")

    skills = ["Communication", "Problem Solving", "Adaptability", "Teamwork", "Leadership"]
    percentages = [90, 82, 78, 73, 69]

    fig = go.Figure([
        go.Bar(
            x=percentages,
            y=skills,
            orientation='h',
            text=[f"{v}%" for v in percentages],
            textposition='auto',
            marker_color='#898AC4'
        )
    ])
    fig.update_layout(
        xaxis=dict(title="Demand Percentage (%)"),
        yaxis=dict(title="Skill"),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<p style='text-align:center;color:#555;'>Data source: Simulated insights (for demo purpose)</p>", unsafe_allow_html=True)

# ---------- Logout ----------
elif choice == "Logout":
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("✅ You have been logged out.")
    st.session_state.menu = "Login"
    st.rerun()




