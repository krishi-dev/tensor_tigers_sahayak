import streamlit as st
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.class_dashboard import display_class_dashboard_page

def main():
    st.set_page_config(
        page_title="Class Dashboard Demo",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Class Dashboard Demo")
    st.markdown("A detailed dashboard for individual classes with metrics, progress tracking, and quick actions")
    
    # Demo class data
    demo_classes = [
        {
            'name': 'Mathematics Excellence',
            'grade': '5th Grade',
            'subject': 'Mathematics',
            'teacher': 'Dr. Johnson',
            'capacity': 32,
            'description': 'Advanced mathematics program focusing on problem-solving and conceptual understanding'
        },
        {
            'name': 'Science Explorers',
            'grade': '6th Grade',
            'subject': 'Science',
            'teacher': 'Ms. Williams',
            'capacity': 28,
            'description': 'Interactive science program exploring experiments and discoveries'
        },
        {
            'name': 'Young Scholars',
            'grade': '4th-5th Grade',
            'subject': 'English',
            'teacher': 'Mrs. Davis',
            'capacity': 25,
            'description': 'Comprehensive English program developing reading and writing skills'
        }
    ]
    
    # Let user select which class to view
    st.subheader("Select a Class to View Dashboard")
    
    selected_class = st.selectbox(
        "Choose a class:",
        options=demo_classes,
        format_func=lambda x: f"{x['name']} - {x['grade']} - {x['subject']}"
    )
    
    if selected_class:
        st.markdown("---")
        display_class_dashboard_page(selected_class)
    
    # Sidebar with features
    st.sidebar.title("🎓 Dashboard Features")
    st.sidebar.markdown("""
    ### ✨ Dashboard Elements
    - **Header Section**: Class name, description, and action buttons
    - **Navigation Tabs**: Overview, Students, Content, Analytics
    - **Metrics Cards**: Total Content, Completion, Engagement, Active Students
    - **Subject Progress**: Visual progress bars with manage buttons
    - **Quick Actions**: Generate Content, Photo to Topic, Voice Input, Create Assessment
    
    ### 📊 Metrics Display
    - Real-time engagement tracking
    - Completion percentage
    - Student activity monitoring
    - Content management
    
    ### 🎯 Quick Actions
    - Content generation
    - Photo analysis
    - Voice input processing
    - Assessment creation
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚀 Navigation")
    
    if st.sidebar.button("← Back to Main Dashboard"):
        st.switch_page("pages/dashboard.py")

if __name__ == "__main__":
    main() 