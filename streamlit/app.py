import streamlit as st


def main():
    st.title("Epic and Project Selector")

    # Static list of epics
    epics = ["Epic 1", "Epic 2", "Epic 3", "Epic 4"]

    # Static list of projects
    projects = ["Project 1", "Project 2", "Project 3", "Project 4"]

    # Create a dropdown for selecting an epic
    selected_epic = st.selectbox("Select an Epic", epics)

    # Create a dropdown for selecting a project
    selected_project = st.selectbox("Select a Project", projects)

    if st.button('Duplicate'):
        # As this is a simple example, I'm just going to print to the screen.
        # In a real app, this might create a new epic/project in your backend
        st.write(f'Duplicating Epic: {selected_epic} and Project: {selected_project}...')

if __name__ == "__main__":
    main()
