import streamlit as st
import pandas as pd

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Agentic AI Workflow Evaluator",
    layout="wide"
)

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.markdown(
    """
    <h1 style='text-align:center;color:#1E3A8A;'>
    AI Agentic Workflow Evaluator System
    </h1>

    <p style='text-align:center;font-size:18px;'>
    Design Thinking Lab – AI Workflow Validation Platform
    </p>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# SCENARIOS
# -------------------------------------------------

scenarios = {

    "Travel Booking": {

        "description":
        "Book a trip from Kolkata to Mumbai with cheapest direct flight/train, 3-star hotel, cab booking and complete booking after user approval.",

        "correct_workflow": [

            "Search Agent",
            "Flight Search Agent",
            "Train Search Agent",
            "Hotel Search Agent",
            "Cab Booking Agent",
            "Approval Agent",
            "Payment Agent",
            "Notification Agent"

        ]
    },

    "Hospital Appointment": {

        "description":
        "Book a hospital appointment with doctor selection, slot confirmation, payment and notification.",

        "correct_workflow": [

            "Search Agent",
            "Approval Agent",
            "Payment Agent",
            "Notification Agent"

        ]
    }

}

# -------------------------------------------------
# AGENTS
# -------------------------------------------------

agents = [

    "Search Agent",
    "Flight Search Agent",
    "Train Search Agent",
    "Hotel Search Agent",
    "Cab Booking Agent",
    "Approval Agent",
    "Payment Agent",
    "Notification Agent",

]

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("Scenario Selection")

selected_scenario = st.sidebar.selectbox(
    "Choose Scenario",
    list(scenarios.keys())
)

scenario_data = scenarios[selected_scenario]

correct_workflow = scenario_data["correct_workflow"]

# -------------------------------------------------
# SCENARIO
# -------------------------------------------------

st.subheader("Scenario")

st.info(
    scenario_data["description"]
)

# -------------------------------------------------
# AVAILABLE AGENTS
# -------------------------------------------------

st.subheader("Available AI Agents")

col1, col2, col3, col4 = st.columns(4)

columns = [col1, col2, col3, col4]

for i, agent in enumerate(agents):

    columns[i % 4].success(agent)

# -------------------------------------------------
# WORKFLOW BUILDER
# -------------------------------------------------

st.subheader("Design Your AI Workflow")

workflow = []

workflow_cols = st.columns(4)

for i in range(8):

    with workflow_cols[i % 4]:

        step = st.selectbox(

            f"Step {i+1}",
            [""] + agents,
            key=f"step_{i}"

        )

        workflow.append(step)

# -------------------------------------------------
# ORCHESTRATION PATTERN
# -------------------------------------------------

st.subheader("Orchestration Pattern")

pattern = st.radio(

    "Choose Workflow Pattern",

    [
        "Sequential",
        "Parallel",
        "Hierarchical"
    ]

)

# -------------------------------------------------
# EVALUATE BUTTON
# -------------------------------------------------

if st.button("Evaluate Workflow"):

    score = 100

    feedback = []

    matched_steps = 0

    # ---------------------------------------------
    # STEP VALIDATION
    # ---------------------------------------------

    for i in range(len(correct_workflow)):

        if workflow[i] == correct_workflow[i]:

            matched_steps += 1

        else:

            score -= 8

    # ---------------------------------------------
    # MISSING AGENTS
    # ---------------------------------------------

    for agent in correct_workflow:

        if agent not in workflow:

            score -= 5

            feedback.append(
                f"Missing Agent: {agent}"
            )

    # ---------------------------------------------
    # APPROVAL VALIDATION
    # ---------------------------------------------

    if (
        "Approval Agent" in workflow
        and "Payment Agent" in workflow
    ):

        approval_index = workflow.index(
            "Approval Agent"
        )

        payment_index = workflow.index(
            "Payment Agent"
        )

        if payment_index < approval_index:

            score -= 20

            feedback.append(
                "Payment should happen after Approval"
            )

    # ---------------------------------------------
    # ORCHESTRATION FEEDBACK
    # ---------------------------------------------

    if pattern == "Parallel":

        feedback.append(
            "Parallel orchestration selected"
        )

    elif pattern == "Sequential":

        feedback.append(
            "Sequential orchestration selected"
        )

    else:

        feedback.append(
            "Hierarchical orchestration selected"
        )

    # ---------------------------------------------
    # SCORE LIMITS
    # ---------------------------------------------

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    # ---------------------------------------------
    # GOOD WORKFLOW
    # ---------------------------------------------

    if matched_steps >= 6:

        feedback.append(
            "Workflow structure looks strong"
        )

    # -------------------------------------------------
    # RESULTS
    # -------------------------------------------------

    st.divider()

    st.subheader("AI Evaluation Result")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Workflow Score",
        f"{score}/100"
    )

    metric2.metric(
        "Correct Steps",
        matched_steps
    )

    metric3.metric(
        "Pattern",
        pattern
    )

    # -------------------------------------------------
    # FEEDBACK
    # -------------------------------------------------

    st.subheader("Feedback")

    for item in feedback:

        st.warning(item)

    # -------------------------------------------------
    # CORRECT WORKFLOW
    # -------------------------------------------------

    st.subheader("Correct Workflow")

    df = pd.DataFrame({

        "Step": [
            f"Step {i+1}"
            for i in range(len(correct_workflow))
        ],

        "Agent": correct_workflow

    })

    st.table(df)

    # -------------------------------------------------
    # FINAL OUTPUT
    # -------------------------------------------------

    st.subheader("Final Output")

    st.success(
        "Workflow evaluated successfully using AI-based validation and scoring."
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.markdown(
    """
    ### Key Takeaway

    A good Agentic AI workflow connects the correct agents
    in the right order with minimal human intervention.
    """
)