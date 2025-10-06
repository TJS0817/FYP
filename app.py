import streamlit as st
import pymysql
import hashlib
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------- DB connection ----------
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="fyp_personality",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )

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
    # Openness (1-6)
    "I have a vivid imagination.",
    "I enjoy trying new and foreign foods, activities, or experiences.",
    "I enjoy thinking about abstract ideas.",
    "I have a rich vocabulary.",
    "I prefer routine over variety.",
    "I am original, creative, and inventive.",
    # Conscientiousness (7-12)
    "I am always prepared.",
    "I pay attention to details.",
    "I finish tasks successfully.",
    "I like order and organization.",
    "I often forget to put things back in their proper place.",
    "I make plans and stick to them.",
    # Extraversion (13-18)
    "I am the life of the party.",
    "I enjoy social gatherings.",
    "I feel comfortable around people.",
    "I start conversations easily.",
    "I am quiet around strangers.",
    "I enjoy meeting new people.",
    # Agreeableness (19-24)
    "I sympathize with others’ feelings.",
    "I take time out for others.",
    "I have a soft heart.",
    "I am interested in others’ problems.",
    "I insult people.",
    "I make people feel at ease.",
    # Neuroticism (25-30)
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

cluster_profiles = {
    0: {
        "title": "The Strategist",
        "subtitle": "Visionary, Analytical, and Independent Thinker",
        "description": (
            "Strategists are known for their ability to analyze complex situations, "
            "identify patterns, and devise innovative solutions. They enjoy working on "
            "challenging problems, approaching them with logic and objectivity. "
            "They often prefer independence and long-term planning over short-term tasks."
        ),
        "key_traits": [
            "Analytical and Logical", "Visionary and Forward-Thinking",
            "Innovative Problem-Solver", "Independent and Self-Reliant",
            "Objective and Rational", "Knowledge-Seeker"
        ],
        "strengths": [
            "Strategic Planning", "Problem Solving",
            "Intellectual Curiosity", "Self-Sufficiency"
        ],
        "weaknesses": [
            "Over-Analysis", "Difficulty with Emotion",
            "Perfectionism", "Impatience with Inefficiency"
        ]
    },

    1: {
        "title": "The Connector",
        "subtitle": "Friendly, Outgoing, and People-Oriented",
        "description": (
            "Connectors thrive in social settings and excel at building strong relationships. "
            "They are enthusiastic communicators who motivate others and enjoy teamwork. "
            "Their energy and people skills make them natural leaders in group settings."
        ),
        "key_traits": [
            "Sociable", "Energetic", "Empathetic", "Supportive",
            "Persuasive", "Enthusiastic"
        ],
        "strengths": [
            "Teamwork", "Communication", "Leadership", "Conflict Resolution"
        ],
        "weaknesses": [
            "Easily Distracted", "Overly Dependent on Approval",
            "May Avoid Solitude", "Can Overcommit"
        ]
    },

    2: {
        "title": "The Analyzer",
        "subtitle": "Detail-Oriented, Logical, and Methodical Thinker",
        "description": (
            "Analyzers are highly focused on accuracy, order, and structured problem-solving. "
            "They enjoy working with data, research, and systems where precision is important. "
            "They are reliable in handling responsibilities but may prefer working independently."
        ),
        "key_traits": [
            "Detail-Oriented", "Logical", "Organized", "Practical",
            "Reliable", "Thorough"
        ],
        "strengths": [
            "Research Skills", "Critical Thinking",
            "Time Management", "Accuracy"
        ],
        "weaknesses": [
            "Over-Cautious", "May Resist Change",
            "Workaholic Tendencies", "Difficulty Delegating"
        ]
    },

    3: {
        "title": "The Helper",
        "subtitle": "Compassionate, Supportive, and Service-Oriented",
        "description": (
            "Helpers are empathetic individuals who prioritize the well-being of others. "
            "They are caring, patient, and dedicated to making a positive impact on people’s lives. "
            "They excel in supportive roles and are motivated by helping and guiding others."
        ),
        "key_traits": [
            "Compassionate", "Empathetic", "Supportive", "Patient",
            "Nurturing", "Loyal"
        ],
        "strengths": [
            "Empathy", "Teaching and Mentoring",
            "Collaboration", "Emotional Support"
        ],
        "weaknesses": [
            "Self-Sacrificing", "Easily Overwhelmed",
            "Difficulty Saying No", "May Avoid Conflict"
        ]
    }
}

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Personality Profiling", layout="centered")

# ---------- Custom Styling ----------
st.markdown("""
    <style>
    /* Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #f5f7fa, #c3cfe2);
    }

    /* Page Title */
    h1 {
        color: #2E86AB;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Subheaders */
    h2, h3 {
        color: #264653;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #2A9D8F;
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
        background-color: #21867a;
        transform: scale(1.05);
    }

    /* Input Fields */
    input, select, textarea {
        border-radius: 8px !important;
        border: 1px solid #a0aec0 !important;
        padding: 10px !important;
    }

    /* Info and Warning Boxes */
    .stAlert {
        border-radius: 10px;
    }

    /* Segment Control */
    [data-testid="stSegmentedControl"] label {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 8px 15px;
        margin: 3px;
        border: 1px solid #ccc;
        transition: all 0.3s;
    }
    [data-testid="stSegmentedControl"] label[data-selected="true"] {
        background-color: #2E86AB;
        color: white;
        border: 1px solid #2E86AB;
    }

    /* Forms */
    .stForm {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-top: 15px;
    }

    /* Chart backgrounds */
    .js-plotly-plot .plotly .main-svg {
        border-radius: 12px;
    }

    /* Success message */
    .stSuccess {
        background-color: #D1FAE5 !important;
        color: #065F46 !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("PersonaPath")

# Navigation
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
    username = st.text_input("Username", placeholder="Enter your username")
    email = st.text_input("Email Address", placeholder="Enter your email address")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Register"):
        if not username or not email or not password:
            st.error("Please fill all fields")
        else:
            conn = get_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
                    if cur.fetchone():
                        st.error("Email already registered. Please login instead.")
                    else:
                        cur.execute(
                            "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
                            (username, email, hash_password(password))
                        )
                        conn.commit()
                        st.success("Registration successful! Redirecting to login...")
                        st.session_state.menu = "Login"
                        st.rerun()
            except Exception as e:
                st.error("Error: " + str(e))
            finally:
                conn.close()

# ---------- Login ----------
elif choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email Address", placeholder="Enter your email address")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login"):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, password FROM users WHERE email=%s", (email,))
                row = cur.fetchone()
            if row:
                user_id, username, stored_hash = row
                if verify_password(stored_hash, password):
                    st.session_state['user_id'] = user_id
                    st.session_state['username'] = username
                    st.success(f"✅ Logged in as {username}. Redirecting...")
                    st.session_state.menu = "Personality Test"
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.error("No account found with that email")
        except Exception as e:
            st.error("DB error: " + str(e))
        finally:
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
                    ("Strongly disagree","Disagree","Neutral","Agree","Strongly agree"),
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
                scored = [(6-v if idx in reverse_idx else v) for idx, v in enumerate(answers)]

                # compute traits
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
                    with conn.cursor() as cur:
                        sql = """
                        INSERT INTO personality_results (
                          user_id, taken_at,
                          q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,
                          q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,
                          q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,
                          openness_raw, conscientiousness_raw, extraversion_raw, agreeableness_raw, neuroticism_raw, cluster_id
                        ) VALUES (
                          %s, %s,
                          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                          %s,%s,%s,%s,%s,%s
                        )
                        """
                        params = (
                            st.session_state['user_id'],
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            *answers,
                            openness, conscientiousness, extraversion, agreeableness, neuroticism,
                            cluster_label
                        )
                        cur.execute(sql, params)
                    conn.commit()
                    st.success("✅ Your responses have been saved.")
                    
                    # Automatically navigate to Personality Profile
                    st.session_state.menu = "Personality Profile"
                    st.rerun()
                except Exception as e:
                    st.error("Failed to save results: " + str(e))
                finally:
                    conn.close()

elif choice == "Personality Profile":
    if "cluster_label" not in st.session_state:
        st.warning("⚠️ Please take the personality test first.")
    else:
        cluster = st.session_state["cluster_label"]
        profile = cluster_profiles.get(cluster, {})
        
        st.header(profile.get("title", "Unknown Profile"))
        st.subheader(profile.get("subtitle", ""))
        st.write(profile.get("description", ""))

        st.markdown("### 🔑 Key Traits")
        st.write(", ".join(profile.get("key_traits", [])))

        st.markdown("### 💪 Strengths")
        for s in profile.get("strengths", []):
            st.success(s)

        st.markdown("### ⚠️ Weaknesses")
        for w in profile.get("weaknesses", []):
            st.error(w)

        if st.button("View Recommended Jobs"):
            st.session_state.menu = "Job Recommendations"
            st.rerun()

elif choice == "Job Recommendations":
    if "cluster_label" not in st.session_state:
        st.warning("⚠️ Please take the personality test first.")
    else:
        cluster = st.session_state["cluster_label"]
        st.subheader("Top Recommendations for You")

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, job_title, company, job_desc, requirements FROM jobs WHERE cluster_id=%s", (cluster,))
                jobs = cur.fetchall()
        finally:
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

elif choice == "Dataset Trends":
        # --- Page Header ---
    st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <h2 style="color:#2E86AB;">📊 Dataset Trends & Insights</h2>
            <p style="font-size:16px; color:#555;">
                Explore personality distributions, job satisfaction, and top soft skills among Malaysian users.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 1️⃣ Personality Distribution (Donut)
    st.subheader("🧠 Personality Type Distribution")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT cluster_id, COUNT(*) FROM personality_results GROUP BY cluster_id")
            rows = cur.fetchall()
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

    # 2️⃣ Job Satisfaction (Vertical Bar)
    st.subheader("💼 Average Job Satisfaction by Personality Type")
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
            marker_color=['#2E86AB', '#F4A261', '#E76F51', '#2A9D8F']
        )
    ])
    fig.update_layout(
        yaxis=dict(title="Satisfaction Level (1–5)"),
        xaxis=dict(title="Personality Type"),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 3️⃣ Top Soft Skills (Horizontal Bar)
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
            marker_color='#6C63FF'
        )
    ])
    fig.update_layout(
        xaxis=dict(title="Demand Percentage (%)"),
        yaxis=dict(title="Skill"),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Logout":
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.success("✅ You have been logged out.")
    st.session_state.menu = "Login"
    st.rerun()


