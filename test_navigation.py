import streamlit as st
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.modern_class_display import display_modern_class_management
from components.class_dashboard import display_class_dashboard_page

def main():
    st.set_page_config(
        page_title="Navigation Test",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Navigation Test")
    st.markdown("Testing the class dashboard navigation")
    
    # Check if we should show class dashboard
    if st.session_state.get('show_class_dashboard', False) and st.session_state.get('selected_class'):
        st.success("✅ Showing class dashboard!")
        display_class_dashboard_page(st.session_state['selected_class'])
        
        # Add back button
        if st.sidebar.button("← Back to Classes"):
            st.session_state['show_class_dashboard'] = False
            st.session_state['selected_class'] = None
            st.rerun()
        return
    
    # Show the modern class management
    st.subheader("Class Management")
    display_modern_class_management()
    
    # Sidebar info
    st.sidebar.title("Test Info")
    st.sidebar.write("This page tests the navigation between class list and class dashboard.")
    st.sidebar.write("Click 'Manage' on any class to see the dashboard.")

if __name__ == "__main__":
    main() 