# app.py  -  PC Learner 🖥️
# Run it with:  streamlit run app.py

import streamlit as st
import pandas as pd
from component_info import COMPONENTS, QUIZ

# ------------------------------------------------------------
# 1. PAGE SETUP
# ------------------------------------------------------------
st.set_page_config(page_title="PC Learner", page_icon="🖥️", layout="wide")

# Load our list of parts from the CSV file into a pandas table (DataFrame)
parts = pd.read_csv("components.csv")


# ------------------------------------------------------------
# 2. BUDGET SPLIT  (what % of the money goes to each part)
#    Each row adds up to 1.00 (= 100%)
# ------------------------------------------------------------
BUDGET_SPLIT = {
    "Gaming": {
        "CPU": 0.20, "GPU": 0.35, "RAM": 0.08, "Motherboard": 0.11,
        "Storage": 0.10, "PSU": 0.08, "Case": 0.08,
    },
    "Video Editing": {
        "CPU": 0.28, "GPU": 0.22, "RAM": 0.15, "Motherboard": 0.10,
        "Storage": 0.12, "PSU": 0.07, "Case": 0.06,
    },
    "School & Homework": {
        "CPU": 0.30, "GPU": 0.00, "RAM": 0.12, "Motherboard": 0.17,
        "Storage": 0.16, "PSU": 0.12, "Case": 0.13,
    },
    "Everyday & Streaming": {
        "CPU": 0.25, "GPU": 0.10, "RAM": 0.12, "Motherboard": 0.15,
        "Storage": 0.15, "PSU": 0.11, "Case": 0.12,
    },
}


# ------------------------------------------------------------
# 3. THE "BRAIN" - picks parts for a use case and budget
# ------------------------------------------------------------
def build_pc(use_case, budget):
    split = BUDGET_SPLIT[use_case]
    build = {}   # will hold one chosen part per category

    # Step A: for each category, pick the best part we can afford
    for category, share in split.items():
        money_for_part = budget * share
        options = parts[parts["category"] == category]
        affordable = options[options["price"] <= money_for_part]

        if len(affordable) > 0:
            # best score among the parts we can afford
            choice = affordable.sort_values("score").iloc[-1]
        else:
            # nothing fits, so take the cheapest one
            choice = options.sort_values("price").iloc[0]

        build[category] = choice

    # Step B: use leftover money to upgrade parts
    total = sum(choice["price"] for choice in build.values())

    for category, share in split.items():
        if share == 0:
            continue   # skip parts we don't need for this use case

        options = parts[parts["category"] == category].sort_values("score")
        better = options[options["score"] > build[category]["score"]]

        if len(better) > 0:
            next_up = better.iloc[0]
            extra_cost = next_up["price"] - build[category]["price"]
            if total + extra_cost <= budget:
                build[category] = next_up
                total = total + extra_cost

    return build


# ------------------------------------------------------------
# 4. OPTIONAL BONUS: Ask AI (Groq)
# ------------------------------------------------------------
def ask_ai_box(key):
    with st.expander("🤖 Bonus: Ask AI"):
        question = st.text_input("Ask anything about PCs:", key=key)

        if st.button("Ask", key=key + "_button"):
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                st.warning("No API key found. Add GROQ_API_KEY to .streamlit/secrets.toml")
                return

            try:
                from groq import Groq
                client = Groq(api_key=api_key)
                reply = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system",
                         "content": "You explain PC parts to a 15 year old. Keep it short and friendly."},
                        {"role": "user", "content": question},
                    ],
                )
                st.write(reply.choices[0].message.content)
            except Exception as error:
                st.error(f"Something went wrong: {error}")


# ------------------------------------------------------------
# 5. PAGE 1: LEARN
# ------------------------------------------------------------
def show_learn_page():
    st.title("📚 Learn PC Parts")
    st.write("Pick a part below and discover what it does!")

    # Make a list of labels like "🧠 CPU"
    labels = []
    for key, info in COMPONENTS.items():
        labels.append(info["emoji"] + " " + key)

    chosen_label = st.radio("Choose a part:", labels, horizontal=True)
    chosen_key = chosen_label.split(" ")[1]     # "🧠 CPU" -> "CPU"
    info = COMPONENTS[chosen_key]

    st.header(info["emoji"] + " " + info["title"])
    st.subheader(info["short"])

    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Easy way to think about it:**\n\n" + info["analogy"])
        st.success("🎉 **Fun fact:** " + info["fun_fact"])
    with col2:
        st.markdown("### 🔍 What to look for")
        for tip in info["look_for"]:
            st.write("✅ " + tip)

    # Show real parts from our CSV for this category
    with st.expander("👀 See example parts from our shop"):
        examples = parts[parts["category"] == chosen_key][["name", "price", "note"]]
        st.dataframe(examples, hide_index=True)

    # ---------------- QUIZ ----------------
    st.divider()
    st.header("🧪 Quick Quiz")
    st.write("Test what you learned!")

    for i, q in enumerate(QUIZ):
        st.radio(q["question"], q["options"], index=None, key="quiz_" + str(i))

    if st.button("Check my answers"):
        score = 0
        for i, q in enumerate(QUIZ):
            if st.session_state["quiz_" + str(i)] == q["answer"]:
                score = score + 1

        st.subheader("Your score: " + str(score) + " / " + str(len(QUIZ)))
        if score == len(QUIZ):
            st.balloons()
            st.success("Perfect! You're a PC expert! 🏆")
        elif score >= 3:
            st.info("Nice job! Read the parts again and try once more. 💪")
        else:
            st.warning("Keep learning, you'll get it! 📖")

    ask_ai_box("ai_learn")


# ------------------------------------------------------------
# 6. PAGE 2: RECOMMENDATION
# ------------------------------------------------------------
def show_recommend_page():
    st.title("🎯 Build My PC")
    st.write("Tell us what you'll use it for and how much you can spend.")

    col1, col2 = st.columns(2)
    with col1:
        use_case = st.selectbox("What will you use it for?", list(BUDGET_SPLIT.keys()))
    with col2:
        budget = st.slider("Your budget (€)", min_value=600, max_value=2500, value=1000, step=50)

    if st.button("🔧 Build my PC!"):
        build = build_pc(use_case, budget)

        # Turn the build into a list of rows for a nice table
        rows = []
        for category, choice in build.items():
            rows.append({
                "Part": category,
                "Name": choice["name"],
                "Price (€)": int(choice["price"]),
                "Why": choice["note"],
            })

        # Save in session_state so it stays when the page reruns
        st.session_state["rows"] = rows
        st.session_state["budget"] = budget
        st.session_state["use_case"] = use_case

    # Show the result if we have one
    if "rows" in st.session_state:
        rows = st.session_state["rows"]
        saved_budget = st.session_state["budget"]
        table = pd.DataFrame(rows)
        total = int(table["Price (€)"].sum())
        left = saved_budget - total

        st.divider()
        st.header("Your " + st.session_state["use_case"] + " PC")

        m1, m2, m3 = st.columns(3)
        m1.metric("Total price", "€" + str(total))
        m2.metric("Your budget", "€" + str(saved_budget))
        m3.metric("Money left", "€" + str(left))

        st.progress(min(total / saved_budget, 1.0))

        if left < 0:
            st.warning("This is over budget. Try a bigger budget or another use case.")
        else:
            st.success("Nice! This build fits your budget. 🎉")

        st.dataframe(table, hide_index=True)

        st.subheader("📊 Where does the money go?")
        st.bar_chart(table.set_index("Part")["Price (€)"])

    ask_ai_box("ai_recommend")


# ------------------------------------------------------------
# 7. NAVIGATION  (the sidebar decides which page to show)
# ------------------------------------------------------------
st.sidebar.title("🖥️ PC Learner")
page = st.sidebar.radio("Go to:", ["📚 Learn PC Parts", "🎯 Build My PC"])
st.sidebar.caption("Learn first, then build your dream PC!")

if page == "📚 Learn PC Parts":
    show_learn_page()
else:
    show_recommend_page()
