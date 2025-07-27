import streamlit as st
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.class_dashboard import display_class_dashboard_page
from db_utils import get_db_manager

def main():
    st.set_page_config(
        page_title="Class Dashboard",
        page_icon="🎓",
        layout="wide"
    )
    
    # Get class ID from URL parameters
    class_id = st.experimental_get_query_params().get("class_id", [None])[0]
    action = st.experimental_get_query_params().get("action", [None])[0]
    
    if not class_id or action != "manage":
        st.error("Invalid class access. Please go back to the main dashboard.")
        if st.button("← Back to Dashboard"):
            st.switch_page("pages/dashboard.py")
        return
    
    # Get class data from database
    db_manager = get_db_manager()
    if not db_manager:
        st.error("❌ Unable to connect to database.")
        return
    
    try:
        # Try to get class by ID first
        class_data = db_manager.fetch_class_by_id(int(class_id))
        
        if not class_data:
            # If not found by ID, create demo data based on index
            demo_classes = [
                {
                    'id': 1,
                    'name': 'Mathematics Excellence',
                    'grade': '5',
                    'subject': 'Mathematics',
                    'teacher': 'Dr. Johnson',
                    'capacity': 32,
                    'schedule': 'Mon, Wed, Fri 9:00 AM',
                    'description': 'Advanced mathematics program focusing on problem-solving and conceptual understanding'
                },
                {
                    'id': 2,
                    'name': 'Science Explorers',
                    'grade': '6',
                    'subject': 'Science',
                    'teacher': 'Ms. Williams',
                    'capacity': 28,
                    'schedule': 'Tue, Thu 10:30 AM',
                    'description': 'Interactive science program exploring experiments and discoveries'
                },
                {
                    'id': 3,
                    'name': 'Young Scholars',
                    'grade': '4-5',
                    'subject': 'English',
                    'teacher': 'Mrs. Davis',
                    'capacity': 25,
                    'schedule': 'Mon, Wed 2:00 PM',
                    'description': 'Comprehensive English program developing reading and writing skills'
                }
            ]
            
            # Use the index to get demo class
            try:
                index = int(class_id) - 1
                if 0 <= index < len(demo_classes):
                    class_data = demo_classes[index]
                else:
                    class_data = demo_classes[0]  # Default to first class
            except:
                class_data = demo_classes[0]  # Default to first class
        
        # Display the class dashboard
        display_class_dashboard_page(class_data)
        
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main() 