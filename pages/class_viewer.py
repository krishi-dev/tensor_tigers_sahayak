import streamlit as st
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.class_display import (
    display_classes_card_view,
    display_classes_table,
    display_class_details,
    display_classes_with_filters
)
from db_utils import get_db_manager

def main():
    st.set_page_config(
        page_title="Class Viewer",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Class Viewer")
    st.markdown("A reusable component for displaying classes in a beautiful way")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    view_mode = st.sidebar.selectbox(
        "Choose View Mode",
        ["Browse with Filters", "Card View", "Table View", "Class Details"]
    )
    
    # Get database connection
    db_manager = get_db_manager()
    if not db_manager:
        st.error("❌ Unable to connect to database. Please check your connection.")
        return
    
    try:
        # Fetch classes
        classes = db_manager.fetch_classes()
        
        if not classes:
            st.info("📚 No classes found in the database.")
            return
        
        st.success(f"✅ Successfully loaded {len(classes)} classes from database")
        
        # Display based on selected view mode
        if view_mode == "Browse with Filters":
            display_classes_with_filters()
            
        elif view_mode == "Card View":
            st.header("📋 Classes - Card View")
            display_classes_card_view(classes, "Available Classes")
            
        elif view_mode == "Table View":
            st.header("📊 Classes - Table View")
            display_classes_table(classes, "Class Information")
            
        elif view_mode == "Class Details":
            st.header("🔍 Class Details")
            
            # Let user select a class
            if classes:
                selected_class = st.selectbox(
                    "Select a class to view details:",
                    options=classes,
                    format_func=lambda x: f"{x.get('name', 'Unknown')} - Grade {x.get('grade', 'N/A')} - {x.get('subject', 'N/A')}"
                )
                
                if selected_class:
                    display_class_details(selected_class)
        
        # Additional information
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Database Info")
        st.sidebar.info(f"Total Classes: {len(classes)}")
        
        # Show sample data structure
        if classes:
            st.sidebar.markdown("### Sample Class Data")
            sample_class = classes[0]
            for key, value in sample_class.items():
                st.sidebar.text(f"{key}: {value}")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main() 