import streamlit as st
from typing import List, Dict, Optional
import pandas as pd
from db_utils import get_db_manager
from datetime import datetime, timedelta
import random

def create_modern_class_card(class_data: Dict, index: int):
    """Create a modern class card with HTML styling"""
    
    # Generate random engagement and activity data for demo
    engagement = random.randint(70, 95)
    hours_ago = random.randint(1, 24)
    
    # Subject colors mapping
    subject_colors = {
        'Mathematics': '#3B82F6',  # Blue
        'Science': '#10B981',      # Green
        'English': '#F59E0B',      # Orange
        'Hindi': '#EF4444',        # Red
        'Social Studies': '#8B5CF6', # Purple
        'Computer Science': '#06B6D4' # Cyan
    }
    
    accent_color = subject_colors.get(class_data.get('subject', 'Mathematics'), '#3B82F6')
    
    # Format grade display
    grade = class_data.get('grade', '')
    if grade:
        grade_display = f"{grade}th Grade" if grade.isdigit() else f"{grade} Grade"
    else:
        grade_display = "Grade N/A"
    
    # Get student count
    student_count = class_data.get('capacity', random.randint(20, 35))
    
    # Create subject tags
    subjects = [class_data.get('subject', 'Mathematics')]
    if class_data.get('subject') == 'Science':
        subjects.extend(['Computer Science'])
    elif class_data.get('subject') == 'English':
        subjects.extend(['Hindi', 'Social Studies'])
    
    card_html = f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid {accent_color};
        transition: all 0.3s ease;
        position: relative;
    "> <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="
                        width: 40px;
                        height: 40px;
                        background: {accent_color};
                        border-radius: 8px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-right: 12px;
                    ">
                    <span style="color: white; font-size: 18px; font-weight: bold;">📚</span>
                    </div>
                    <div>
                        <h3 style="margin: 0; color: #1F2937; font-size: 18px; font-weight: 600;">
                            {class_data.get('name', 'Class Name')}
                        </h3>
                        <p style="margin: 4px 0 0 0; color: #6B7280; font-size: 14px;">
                            {grade_display} • 2024-25 • {student_count} students
                        </p>
                    </div>
                </div>
                <div style="margin: 12px 0;">
                    {''.join([f'<span style="background: #E5E7EB; color: #374151; padding: 4px 8px; border-radius: 12px; font-size: 12px; margin-right: 8px;">{subject}</span>' for subject in subjects])}
                </div>
                <div style="display: flex; align-items: center; gap: 16px; margin-top: 12px;">
                    <div style="display: flex; align-items: center; color: #6B7280; font-size: 12px;">
                        <span style="margin-right: 4px;">🕒</span>
                        Last activity: {hours_ago} hours ago
                    </div>
                    <div style="display: flex; align-items: center; color: #059669; font-size: 12px; font-weight: 500;">
                        <span style="margin-right: 4px;">📊</span>
                        Engagement: {engagement}%
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <button style="
                    background: none;
                    border: none;
                    padding: 8px;
                    border-radius: 6px;
                    cursor: pointer;
                    color: #6B7280;
                    transition: background 0.2s;
                " onmouseover="this.style.background='#F3F4F6'" onmouseout="this.style.background='none'">
                    📊
                </button>
                <button style="
                    background: none;
                    border: none;
                    padding: 8px;
                    border-radius: 6px;
                    cursor: pointer;
                    color: #6B7280;
                    transition: background 0.2s;
                " onmouseover="this.style.background='#F3F4F6'" onmouseout="this.style.background='none'">
                    ⚙️
                </button>
            </div>
        </div>
    </div>
    """
    
    return card_html

def display_modern_classes_list(classes: List[Dict], title: str = "My Classes"):
    """Display classes in a modern list format with search and filters"""
    
    # Header section
    header_html = f"""
    <div style="
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        padding: 32px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        color: white;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0; font-size: 28px; font-weight: 700;">{title}</h1>
                <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 16px;">
                    Manage your classes, students, and subjects all in one place
                </p>
            </div>
            <button style="
                background: #10B981;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: background 0.2s;
            " onmouseover="this.style.background='#059669'" onmouseout="this.style.background='#10B981'">
                <span>➕</span>
                Create New Class
            </button>
        </div>
    </div>
    """
    
    # Search and filter section
    search_html = """
    <div style="
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    ">
        <div style="display: flex; gap: 16px; align-items: center;">
            <div style="flex: 1; position: relative;">
                <span style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #9CA3AF;">🔍</span>
                <input type="text" placeholder="Search classes, grades, or subjects..." style="
                    width: 100%;
                    padding: 12px 12px 12px 40px;
                    border: 1px solid #D1D5DB;
                    border-radius: 8px;
                    font-size: 14px;
                    outline: none;
                " onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#D1D5DB'">
            </div>
            <button style="
                background: white;
                border: 1px solid #D1D5DB;
                padding: 12px 20px;
                border-radius: 8px;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                font-weight: 500;
                transition: all 0.2s;
            " onmouseover="this.style.borderColor='#3B82F6'; this.style.color='#3B82F6'" onmouseout="this.style.borderColor='#D1D5DB'; this.style.color='#374151'">
                <span>⚙️</span>
                Filters
            </button>
        </div>
    </div>
    """
    
    # Classes list
    classes_html = ""
    if classes:
        for i, class_data in enumerate(classes):
            classes_html += create_modern_class_card(class_data, i)
    else:
        classes_html = """
        <div style="
            background: white;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            color: #6B7280;
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">📚</div>
            <h3 style="margin: 0 0 8px 0; color: #374151;">No classes found</h3>
            <p style="margin: 0; opacity: 0.8;">Create your first class to get started</p>
        </div>
        """
    
    # Combine all sections
    full_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        {header_html}
        {search_html}
            {classes_html}
        
    </div>
    """
    
    st.markdown(full_html, unsafe_allow_html=True)
    
    # Add Streamlit buttons for each class
    if classes:
        st.markdown("### Quick Actions")
        cols = st.columns(3)
        
        for i, class_data in enumerate(classes):
            col_idx = i % 3
            with cols[col_idx]:
                if st.button(f"Manage {class_data.get('name', 'Class')}", key=f"manage_{i}"):
                    # Store class data in session state and redirect
                    st.session_state['selected_class'] = class_data
                    st.session_state['show_class_dashboard'] = True
                    st.rerun()

def create_class_form():
    """Create a form for adding new classes"""
    
    st.markdown("""
    <div style="
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    ">
        <h2 style="margin: 0 0 20px 0; color: #1F2937;">Create New Class</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            class_name = st.text_input("Class Name", placeholder="e.g., Mathematics Excellence")
            grade = st.selectbox("Grade Level", ["1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade", "6th Grade", "7th Grade", "8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade"])
            subject = st.selectbox("Primary Subject", ["Mathematics", "Science", "English", "Hindi", "Social Studies", "Computer Science", "Physics", "Chemistry", "Biology"])
        
        with col2:
            teacher = st.text_input("Teacher Name", placeholder="e.g., Dr. Smith")
            capacity = st.number_input("Student Capacity", min_value=1, max_value=100, value=30)
            schedule = st.text_input("Schedule", placeholder="e.g., Mon, Wed, Fri 9:00 AM")
        
        description = st.text_area("Class Description", placeholder="Describe the class objectives and curriculum...")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("Create Class", type="primary", use_container_width=True):
                # Here you would save to database
                st.success("Class created successfully!")
                return {
                    'name': class_name,
                    'grade': grade,
                    'subject': subject,
                    'teacher': teacher,
                    'capacity': capacity,
                    'schedule': schedule,
                    'description': description
                }
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.rerun()
    
    return None

def display_modern_class_management():
    """Main function to display modern class management interface"""
    
    # Get classes from database
    db_manager = get_db_manager()
    if not db_manager:
        st.error("❌ Unable to connect to database.")
        return
    
    try:
        classes = db_manager.fetch_classes()
        
        # Add some demo classes if none exist
        if not classes:
            demo_classes = [
                {
                    'name': 'Mathematics Excellence',
                    'grade': '5',
                    'subject': 'Mathematics',
                    'teacher': 'Dr. Johnson',
                    'capacity': 32,
                    'schedule': 'Mon, Wed, Fri 9:00 AM'
                },
                {
                    'name': 'Science Explorers',
                    'grade': '6',
                    'subject': 'Science',
                    'teacher': 'Ms. Williams',
                    'capacity': 28,
                    'schedule': 'Tue, Thu 10:30 AM'
                },
                {
                    'name': 'Young Scholars',
                    'grade': '4-5',
                    'subject': 'English',
                    'teacher': 'Mrs. Davis',
                    'capacity': 25,
                    'schedule': 'Mon, Wed 2:00 PM'
                }
            ]
            classes = demo_classes
        
        # Display modern interface
        display_modern_classes_list(classes, "My Classes")
        
        # Add class creation option
        if st.button("➕ Add New Class", type="secondary"):
            st.session_state['show_add_form'] = True
        
        if st.session_state.get('show_add_form', False):
            st.markdown("---")
            new_class = create_class_form()
            if new_class:
                st.session_state['show_add_form'] = False
                st.rerun()
    
    finally:
        db_manager.disconnect()

def main():
    """Demo function"""
    st.set_page_config(
        page_title="Modern Class Management",
        page_icon="🎓",
        layout="wide"
    )
    
    display_modern_class_management()

if __name__ == "__main__":
    main() 