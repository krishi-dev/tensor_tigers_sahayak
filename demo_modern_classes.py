import streamlit as st
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.modern_class_display import display_modern_class_management, create_class_form
from db_utils import get_db_manager

def main():
    st.set_page_config(
        page_title="Modern Class Management Demo",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Modern Class Management Demo")
    st.markdown("A beautiful, modern interface for managing classes with HTML styling")
    
    # Navigation tabs
    tab1, tab2 = st.tabs(["📚 View Classes", "➕ Add New Class"])
    
    with tab1:
        st.header("Modern Class Display")
        st.markdown("This demonstrates the modern HTML-based class display with:")
        st.markdown("- ✨ Beautiful gradient cards")
        st.markdown("- 🔍 Search and filter functionality")
        st.markdown("- 📊 Engagement metrics")
        st.markdown("- 🎨 Subject-specific color coding")
        st.markdown("- 📱 Responsive design")
        
        st.markdown("---")
        display_modern_class_management()
    
    with tab2:
        st.header("Add New Class")
        st.markdown("Create a new class with a comprehensive form")
        
        new_class = create_class_form()
        
        if new_class:
            st.success("✅ Class created successfully!")
            st.balloons()
            
            # Show created class details
            st.subheader("Created Class Details")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Class Name:** {new_class['name']}")
                st.write(f"**Grade:** {new_class['grade']}")
                st.write(f"**Subject:** {new_class['subject']}")
            
            with col2:
                st.write(f"**Teacher:** {new_class['teacher']}")
                st.write(f"**Capacity:** {new_class['capacity']} students")
                st.write(f"**Schedule:** {new_class['schedule']}")
            
            if new_class.get('description'):
                st.write(f"**Description:** {new_class['description']}")
    
    # Sidebar with additional info
    st.sidebar.title("🎓 Features")
    st.sidebar.markdown("""
    ### ✨ Modern Features
    - **Beautiful UI**: Gradient cards with hover effects
    - **Search & Filter**: Find classes quickly
    - **Responsive Design**: Works on all devices
    - **Database Integration**: Real-time data
    - **Form Validation**: Comprehensive input checking
    
    ### 🎨 Design Elements
    - Subject-specific colors
    - Engagement metrics
    - Activity timestamps
    - Professional typography
    - Smooth animations
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚀 Quick Actions")
    
    if st.sidebar.button("View All Classes"):
        st.rerun()
    
    if st.sidebar.button("Add New Class"):
        st.session_state['active_tab'] = "Add New Class"
        st.rerun()

if __name__ == "__main__":
    main() 