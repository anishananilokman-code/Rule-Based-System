import streamlit as st
import operator

# ------------------- JSON Rules -------------------
rules_json = [
 {
 "name": "Top merit candidate",
 "priority": 100,
 "conditions": [
   ["cgpa", ">=", 3.7],
   ["co_curricular_score", ">=", 80],
   ["family_income", "<=", 8000],
   ["disciplinary_actions", "==", 0],
   ["community_service_hours", ">=", 20]
 ],
 "action": {
   "decision": "AWARD_FULL",
   "reason": "Excellent academic & co-curricular performance, with acceptable need and community engagement"
 }
 },
 {
 "name": "Good candidate - partial scholarship",
 "priority": 80,
 "conditions": [
   ["cgpa", ">=", 3.3],
   ["co_curricular_score", ">=", 60],
   ["family_income", "<=", 12000],
   ["disciplinary_actions", "<=", 1]
 ],
 "action": {
   "decision": "AWARD_PARTIAL",
   "reason": "Good academic & involvement record with moderate need"
 }
 },
 {
 "name": "Need-based review",
 "priority": 70,
 "conditions": [
   ["cgpa", ">=", 2.5],
   ["family_income", "<=", 4000]
 ],
 "action": {
   "decision": "REVIEW",
   "reason": "High need but borderline academic score"
 }
 },
 {
 "name": "Low CGPA – not eligible",
 "priority": 95,
 "conditions": [
   ["cgpa", "<", 2.5]
 ],
 "action": {
   "decision": "REJECT",
   "reason": "CGPA below minimum scholarship requirement"
 }
 },
 {
 "name": "Serious disciplinary record",
 "priority": 90,
 "conditions": [
   ["disciplinary_actions", ">=", 2]
 ],
 "action": {
   "decision": "REJECT",
   "reason": "Too many disciplinary records"
 }
 }
]

# ------------------- Operators -------------------
ops = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le
}

rules_json.sort(key=lambda r: r['priority'], reverse=True)

def evaluate_rule(student, rule):
    for cond in rule["conditions"]:
        attr, op_str, value = cond
        if attr not in student or not ops[op_str](student[attr], value):
            return False
    return True

def decide_scholarship(student):
    for rule in rules_json:
        if evaluate_rule(student, rule):
            return rule
    return {"action": {"decision": "REJECT", "reason": "No matching rule found"}, "name": "No Match"}

# ------------------- Streamlit App -------------------
st.set_page_config(page_title="Scholarship Advisory System 🎓", layout="wide")

st.title("🎓 University Scholarship Advisory System")
st.markdown("""
Use this tool to evaluate scholarship eligibility based on **transparent, rule-based decisions**.  
Input applicant details in the sidebar and click **Evaluate Scholarship**.
""")

# ------------------- Sidebar Inputs -------------------
with st.sidebar:
    st.header("Applicant Details")
    cgpa = st.number_input("Cumulative GPA (CGPA)", min_value=0.0, max_value=4.0, step=0.01, value=3.5)
    co_curricular = st.number_input("Co-curricular score (0–100)", min_value=0, max_value=100, value=70)
    family_income = st.number_input("Monthly family income (RM)", min_value=0, value=9000)
    community_service = st.number_input("Community service hours", min_value=0, value=30)
    current_semester = st.number_input("Current semester", min_value=1, value=4)
    disciplinary_actions = st.number_input("Number of disciplinary actions", min_value=0, value=0)

# ------------------- Evaluate Button -------------------
if st.sidebar.button("Evaluate Scholarship"):
    student = {
        "cgpa": cgpa,
        "co_curricular_score": co_curricular,
        "family_income": family_income,
        "community_service_hours": community_service,
        "current_semester": current_semester,
        "disciplinary_actions": disciplinary_actions
    }

    matched_rule = decide_scholarship(student)
    action = matched_rule["action"]

    # ------------------- Result Display -------------------
    st.subheader("📝 Evaluation Result")

    # Prominent decision
    decision = action["decision"]
    reason = action["reason"]
    rule_name = matched_rule["name"]

    if decision == "AWARD_FULL":
        st.markdown(f"<h1 style='color:green'>🏆 {decision}</h1>", unsafe_allow_html=True)
    elif decision == "AWARD_PARTIAL":
        st.markdown(f"<h1 style='color:blue'>🎖️ {decision}</h1>", unsafe_allow_html=True)
    elif decision == "REVIEW":
        st.markdown(f"<h1 style='color:orange'>⚠️ {decision}</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='color:red'>❌ {decision}</h1>", unsafe_allow_html=True)

    st.markdown(f"**Reason:** {reason}")
    st.markdown(f"**Rule Matched:** {rule_name}")

    # ------------------- Transparency -------------------
    with st.expander("See All Rules Evaluated"):
        for r in rules_json:
            match = "✅" if evaluate_rule(student, r) else "❌"
            st.write(f"{match} {r['name']} (Priority: {r['priority']})")
