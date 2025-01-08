import streamlit as st
import pandas as pd

# Initial setup
st.title("PARAMEKKAVU VIDYA MANDIR")
st.subheader("      School Election 2024 ")
st.write("*********************************************")

# Voter database
voters = {"3752": "pass3752", "2230": "pass2230", "4840": "pass4840",
          "2620": "pass2620", "3458": "pass3458"}

import pandas as pd

# Save voters to a CSV file (this happens once, as an example)

voters_df = pd.DataFrame(voters.items(), columns=["Voter ID", "Password"])
voters_csv = "C:\\Users\\parni\\OneDrive\\Documents\\ip project 2024\\Untitled spreadsheet - Sheet1.csv"
voters_df.to_csv(voters_csv, index=False)  # Save voters to CSV

# Initialize state

if "votes" not in st.session_state:
    st.session_state.votes = {"Head Girl": {},"Head Boy": {}}
if "voted_users" not in st.session_state:
    st.session_state.voted_users = set()


# Add Candidates Functionality

def add_candidates():
    st.subheader("Add Candidates")
    
    with st.form(key="add_candidates_form"):
        head_girl_candidates = st.text_area("Enter Head Girl Candidates (one per line):",
                                            placeholder="Enter each candidate on a new line.")
        head_boy_candidates = st.text_area("Enter Head Boy Candidates (one per line):",
                                           placeholder="Enter each candidate on a new line.")
        submit_candidates = st.form_submit_button("Submit Candidates")
    
    if submit_candidates:
        # Update candidates in session state
        st.session_state.votes["Head Girl"] = {name: 0 for name in head_girl_candidates.splitlines() if name.strip()}
        st.session_state.votes["Head Boy"] = {name: 0 for name in head_boy_candidates.splitlines() if name.strip()}
        st.success("Candidates successfully added!")


# Voter Login Functionality

def voter_login():
    st.subheader("Voter Login")
    voter_id = st.text_input("Enter your Voter's ID")
    password = st.text_input("Enter your Password", type="password")
    
    if st.button("Login"):
        # Check voter credentials
        valid_voter = any(voter_id == row["Voter ID"] and password == row["Password"] for _, row in voters_df.iterrows())
        if valid_voter:
            if voter_id in st.session_state.voted_users:
                st.warning("You have already voted!")
            else:
                st.session_state.voted_users.add(voter_id)
                st.success("Login successful! Proceed to vote.")
                st.session_state.is_logged_in = True
        else:
            st.error("Invalid Voter's ID or Password.")


# Cast Vote Functionality

def cast_vote():
    if not st.session_state.votes["Head Girl"] or not st.session_state.votes["Head Boy"]:
        st.warning("No candidates available. Please add candidates first.")
        return

    st.subheader("Cast Your Vote")

    # Vote for Head Girl
    
    st.write("**Vote for Head Girl**")
    head_girl_candidates = list(st.session_state.votes["Head Girl"].keys())
    head_girl_choice = st.radio("Choose a candidate for Head Girl:", head_girl_candidates)
    if st.button("Vote for Head Girl"):
        st.session_state.votes["Head Girl"][head_girl_choice] += 1
        st.success(f"You voted for {head_girl_choice} as Head Girl!")

    # Vote for Head Boy
    
    st.write("**Vote for Head Boy**")
    head_boy_candidates = list(st.session_state.votes["Head Boy"].keys())
    head_boy_choice = st.radio("Choose a candidate for Head Boy:", head_boy_candidates)
    if st.button("Vote for Head Boy"):
        st.session_state.votes["Head Boy"][head_boy_choice] += 1
        st.success(f"You voted for {head_boy_choice} as Head Boy!")


# Display Results

def display_results():
    if not st.session_state.votes["Head Girl"] or not st.session_state.votes["Head Boy"]:
        st.warning("No results to display yet. Please add candidates and start voting.")
        return

    st.subheader("Election Results")
    
    # Head Girl Results
    
    st.write("### Head Girl Results")
    head_girl_votes = st.session_state.votes["Head Girl"]
    winner_girl = max(head_girl_votes, key=head_girl_votes.get)
    st.write(f"Winner: **{winner_girl}** with {head_girl_votes[winner_girl]} votes.")
    st.bar_chart(pd.DataFrame({"Votes": head_girl_votes}))

    # Head Boy Results
    
    st.write("### Head Boy Results")
    head_boy_votes = st.session_state.votes["Head Boy"]
    winner_boy = max(head_boy_votes, key=head_boy_votes.get)
    st.write(f"Winner: **{winner_boy}** with {head_boy_votes[winner_boy]} votes.")
    st.bar_chart(pd.DataFrame({"Votes": head_boy_votes}))


# Main Application

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ["Add Candidates", "Login", "Voting", "Results"])

    if choice == "Add Candidates":
        add_candidates()
    elif choice == "Login":
        voter_login()
    elif choice == "Voting":
        if "is_logged_in" in st.session_state and st.session_state.is_logged_in:
            cast_vote()
        else:
            st.warning("Please log in first.")
    elif choice == "Results":
        display_results()


if __name__ == "__main__":
    main()
