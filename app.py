import streamlit as st
from question_generator import generate_questions
from validate_answer import validate_answers  
from candidate_email import init_db, email_exists,insert_email,get_leaderboard,update_score

init_db()




# Initialize session state for conversation
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.candidate_info = {}
    st.session_state.questions = []
    st.session_state.answers = {}
    st.session_state.validation_results = {}

st.title("ChatBot")

# Greeting
if st.session_state.step == 1:
    st.write("Hello! Let's Start")
    if st.button("Start"):
        st.session_state.step = 2
        st.rerun()

# Step 2: Candidate Info
elif st.session_state.step == 2:
    st.subheader("Profile Information")
    
    if st.session_state.get("form_incomplete", False):
        st.warning("Please fill in all the fields before proceeding.")
        st.session_state.form_incomplete = False

    with st.form("candidate_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")
        submitted = st.form_submit_button("Next")

        if submitted:
            if not all([name.strip(), email.strip(), phone.strip(), position.strip(), location.strip()]):
                st.session_state.form_incomplete = True
                # st.warning("Please fill in all the fields before proceeding.")
                
                st.rerun()
            else:
                st.session_state.candidate_info = {
                "Name": name, "Email": email, "Phone": phone,
                "Experience": experience, "Position": position,
                "Location": location
            }
                if email_exists(email):
                    st.session_state.step=6
                    st.rerun()
                else:
                    insert_email(email)
                    st.session_state.step = 3
                    st.rerun()

# Step 3: Tech Stack Input
elif st.session_state.step == 3:
    st.subheader("Skills you are aware of")
    tech_stack = st.text_input("List technologies you're familiar with (comma-separated)", key="tech_input")
    col1, space, col2 = st.columns([1, 2, 1])
    with col1:
        if st.button("Generate Questions"):
            tech_list = [tech.strip() for tech in tech_stack.split(",") if tech.strip()]
            st.session_state.questions = generate_questions(tech_list)
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Previous Tab"):
            st.session_state.step = 2
            st.session_state.candidate_info = {}
            st.session_state.questions = []
            st.rerun()

# Step 4: Show Generated Questions
elif st.session_state.step == 4:
    st.subheader("Technical Questions")
    answers = {}  # Dictionary to store user answers

    for tech, questions in st.session_state.questions.items():
        st.subheader(f"Questions on {tech}")
        for i, q in enumerate(questions):
            st.markdown(f"{q}")
            # Add a text area for the user to write their answer
            answer_key = f"answer_{tech}_{i}"  # Unique key for each answer
            answers[answer_key] = st.text_area(f"Your answer for question {i + 1}", key=answer_key)

    # Store answers in session state
    st.session_state.answers = answers

    col1, space, col2 = st.columns([1, 2, 1])
    with col1:
        if st.button("Finish"):
            # Validate answers using the AI in answer_validator
            validation_results = validate_answers(st.session_state.answers)
            st.session_state.validation_results = validation_results  # Store validation results
            
            if isinstance(validation_results, dict):
                scores = [v.get("score", 0) for v in validation_results.values() if isinstance(v, dict)]
                if scores:  
                    update_score(st.session_state.candidate_info["Email"], scores)

            st.session_state.step = 5
            st.rerun()
    with col2:
        if st.button("Previous Tab"):
            st.session_state.step = 3
            st.rerun()

# Step 5: End of Conversation
elif st.session_state.step == 5:
    st.success("Thank you for using ChatBot")
    
    # Display validation results
    st.subheader("Validation Results")

    results = st.session_state.validation_results

    if isinstance(results, dict) and "score" in results:
        st.markdown(f"**Overall Score:** {results['score']}/100")
        st.markdown(f"**Feedback:** {results['feedback']}")
    else:
        st.warning("No validation results found.")

    st.header("Submitted Successfully")
    st.write("Your Details has been Saved and our recruitment team will contact you")
    if st.button("Complete"):
        st.session_state.candidate_info = {}
        st.session_state.questions = []
        st.session_state.answers = {}
        st.session_state.validation_results = {}
        st.session_state.step = 1
        st.rerun()


if st.session_state.step==6:
        st.warning("User already exists. Please change your Email.")
        if st.button("OK"):
            st.session_state.step=1
            st.rerun()  
