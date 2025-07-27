import streamlit as st
from typing import List, Dict, Optional
import pandas as pd
from db_utils import get_db_manager

def display_classes_card_view(classes: List[Dict], title: str = "Available Classes"):
    """Display classes in a card view format"""
    st.header(title)
    
    if not classes:
        st.info("No classes found.")
        return
    
    # Create columns for responsive layout
    cols = st.columns(3)
    
    for i, class_data in enumerate(classes):
        col_idx = i % 3
        
        with cols[col_idx]:
            with st.container():
                st.markdown("""
                <div style="
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                """, unsafe_allow_html=True)
                
                # Display class information
                if 'name' in class_data:
                    st.markdown(f"### {class_data['name']}")
                
                if 'grade' in class_data:
                    st.markdown(f"**Grade:** {class_data['grade']}")
                
                if 'subject' in class_data:
                    st.markdown(f"**Subject:** {class_data['subject']}")
                
                if 'teacher' in class_data:
                    st.markdown(f"**Teacher:** {class_data['teacher']}")
                
                if 'schedule' in class_data:
                    st.markdown(f"**Schedule:** {class_data['schedule']}")
                
                if 'capacity' in class_data:
                    st.markdown(f"**Capacity:** {class_data['capacity']} students")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Add action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"View Details", key=f"view_{i}"):
                        st.session_state['selected_class'] = class_data
                        st.rerun()
                
                with col2:
                    if st.button(f"Join Class", key=f"join_{i}"):
                        st.success(f"Successfully joined {class_data.get('name', 'the class')}!")
                
                st.markdown("---")

def display_classes_table(classes: List[Dict], title: str = "Class Information"):
    """Display classes in a table format"""
    st.header(title)
    
    if not classes:
        st.info("No classes found.")
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(classes)
    
    # Reorder columns if they exist
    column_order = ['name', 'grade', 'subject', 'teacher', 'schedule', 'capacity']
    existing_columns = [col for col in column_order if col in df.columns]
    other_columns = [col for col in df.columns if col not in column_order]
    
    if existing_columns:
        df = df[existing_columns + other_columns]
    
    # Display the table with styling
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "name": st.column_config.TextColumn("Class Name", width="medium"),
            "grade": st.column_config.TextColumn("Grade", width="small"),
            "subject": st.column_config.TextColumn("Subject", width="medium"),
            "teacher": st.column_config.TextColumn("Teacher", width="medium"),
            "schedule": st.column_config.TextColumn("Schedule", width="medium"),
            "capacity": st.column_config.NumberColumn("Capacity", width="small"),
        }
    )

def display_class_details(class_data: Dict):
    """Display detailed information about a specific class"""
    if not class_data:
        st.warning("No class selected.")
        return
    
    st.header("Class Details")
    
    # Create a nice layout for class details
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="
            border: 2px solid #4CAF50;
            border-radius: 15px;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 10px 0;
        ">
        """, unsafe_allow_html=True)
        
        if 'name' in class_data:
            st.markdown(f"## {class_data['name']}")
        
        details = []
        if 'grade' in class_data:
            details.append(f"**Grade:** {class_data['grade']}")
        if 'subject' in class_data:
            details.append(f"**Subject:** {class_data['subject']}")
        if 'teacher' in class_data:
            details.append(f"**Teacher:** {class_data['teacher']}")
        if 'schedule' in class_data:
            details.append(f"**Schedule:** {class_data['schedule']}")
        if 'capacity' in class_data:
            details.append(f"**Capacity:** {class_data['capacity']} students")
        if 'description' in class_data:
            details.append(f"**Description:** {class_data['description']}")
        
        for detail in details:
            st.markdown(detail)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Quick Actions")
        
        if st.button("📚 View Materials", use_container_width=True):
            st.info("Course materials will be displayed here.")
        
        if st.button("📝 Take Quiz", use_container_width=True):
            st.info("Quiz functionality will be available here.")
        
        if st.button("👥 View Students", use_container_width=True):
            st.info("Student list will be displayed here.")
        
        if st.button("📊 View Progress", use_container_width=True):
            st.info("Progress tracking will be available here.")

def display_classes_with_filters():
    """Display classes with filtering options"""
    st.header("Browse Classes")
    
    # Get database connection
    db_manager = get_db_manager()
    if not db_manager:
        st.error("Unable to connect to database.")
        return
    
    try:
        # Get all classes
        all_classes = db_manager.fetch_classes()
        
        if not all_classes:
            st.info("No classes available.")
            return
        
        # Filter options
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Grade filter
            grades = list(set([cls.get('grade', '') for cls in all_classes if cls.get('grade')]))
            selected_grade = st.selectbox("Filter by Grade", ["All"] + grades)
        
        with col2:
            # Subject filter
            subjects = list(set([cls.get('subject', '') for cls in all_classes if cls.get('subject')]))
            selected_subject = st.selectbox("Filter by Subject", ["All"] + subjects)
        
        with col3:
            # View mode
            view_mode = st.selectbox("View Mode", ["Cards", "Table"])
        
        # Apply filters
        filtered_classes = all_classes
        
        if selected_grade != "All":
            filtered_classes = [cls for cls in filtered_classes if cls.get('grade') == selected_grade]
        
        if selected_subject != "All":
            filtered_classes = [cls for cls in filtered_classes if cls.get('subject') == selected_subject]
        
        # Display filtered results
        st.subheader(f"Results ({len(filtered_classes)} classes)")
        
        if view_mode == "Cards":
            display_classes_card_view(filtered_classes)
        else:
            display_classes_table(filtered_classes)
        
        # Show selected class details if any
        if 'selected_class' in st.session_state:
            st.markdown("---")
            display_class_details(st.session_state['selected_class'])
            
    finally:
        db_manager.disconnect()

def main():
    """Main function to demonstrate the class display components"""
    st.title("🎓 Class Management System")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose a view",
        ["Browse Classes", "Class Details", "Quick View"]
    )
    
    if page == "Browse Classes":
        display_classes_with_filters()
    
    elif page == "Class Details":
        db_manager = get_db_manager()
        if db_manager:
            try:
                classes = db_manager.fetch_classes()
                if classes:
                    selected_class = st.selectbox(
                        "Select a class for details",
                        options=classes,
                        format_func=lambda x: x.get('name', 'Unknown Class')
                    )
                    display_class_details(selected_class)
                else:
                    st.info("No classes available.")
            finally:
                db_manager.disconnect()
    
    elif page == "Quick View":
        db_manager = get_db_manager()
        if db_manager:
            try:
                classes = db_manager.fetch_classes()
                display_classes_table(classes, "All Classes")
            finally:
                db_manager.disconnect()

if __name__ == "__main__":
    main() 