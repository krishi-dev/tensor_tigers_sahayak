import streamlit as st
from typing import Dict, List
import random

def create_class_dashboard(class_data: Dict):
    """Create a detailed class dashboard matching the design"""
    
    # Generate demo metrics
    total_content = random.randint(10, 20)
    completion_rate = random.randint(65, 85)
    avg_engagement = random.randint(75, 90)
    active_students = random.randint(2, 8)
    
    # Header section
    header_html = f"""
    <div style="
            background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
            padding: 32px 24px;
            border-radius: 12px;
            margin-bottom: 24px;
            color: white;
        "><div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <h1 style="margin: 0; font-size: 32px; font-weight: 700;">{class_data.get('name', 'Class Name')}</h1>
                <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 16px; line-height: 1.5;">
                    {class_data.get('description', 'Advanced program focusing on problem-solving and conceptual understanding')}
                </p>
                <div style="margin-top: 16px; display: flex; gap: 16px; font-size: 14px; opacity: 0.9;">
                    <span>📚 {class_data.get('grade', '5th')} Grade</span>
                    <span>📅 2024-25</span>
                    <span>👥 {class_data.get('capacity', 32)} students</span>
                </div>
            </div>
            <div style="display: flex; gap: 12px;">
                <button style="
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    padding: 10px 16px;
                    border-radius: 8px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    font-weight: 500;
                    transition: all 0.2s;
                " onmouseover="this.style.background='rgba(255, 255, 255, 0.2)'" onmouseout="this.style.background='rgba(255, 255, 255, 0.1)'">
                    <span>⚙️</span>
                    Settings
                </button>
                <button style="
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    padding: 10px 16px;
                    border-radius: 8px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    font-weight: 500;
                    transition: all 0.2s;
                " onmouseover="this.style.background='rgba(255, 255, 255, 0.2)'" onmouseout="this.style.background='rgba(255, 255, 255, 0.1)'">
                    <span>📤</span>
                    Share
                </button>
            </div>
        </div>
    </div>
    """
    
    # Navigation tabs
    tabs_html = """
    <div style="margin-bottom: 24px;">
        <div style="display: flex; border-bottom: 1px solid #E5E7EB;">
            <button style="
                background: #3B82F6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px 8px 0 0;
                font-weight: 600;
                cursor: pointer;
            ">Overview</button>
            <button style="
                background: none;
                color: #6B7280;
                border: none;
                padding: 12px 24px;
                font-weight: 500;
                cursor: pointer;
                transition: color 0.2s;
            " onmouseover="this.style.color='#3B82F6'" onmouseout="this.style.color='#6B7280'">Students</button>
            <button style="
                background: none;
                color: #6B7280;
                border: none;
                padding: 12px 24px;
                font-weight: 500;
                cursor: pointer;
                transition: color 0.2s;
            " onmouseover="this.style.color='#3B82F6'" onmouseout="this.style.color='#6B7280'">Content</button>
            <button style="
                background: none;
                color: #6B7280;
                border: none;
                padding: 12px 24px;
                font-weight: 500;
                cursor: pointer;
                transition: color 0.2s;
            " onmouseover="this.style.color='#3B82F6'" onmouseout="this.style.color='#6B7280'">Analytics</button>
        </div>
    </div>
    """
    
    # Metrics section
    metrics_html = f"""
    <div style="margin-bottom: 32px;">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
            <div style="
                background: white;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
            ">
            <div style="font-size: 32px; margin-bottom: 8px;">📄</div>
                <div style="font-size: 24px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">{total_content}</div>
                <div style="font-size: 14px; color: #6B7280;">Total Content</div>
            </div>
            <div style='
                background: white;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
            '>
            <div style='font-size: 32px; margin-bottom: 8px;'>🎯</div>
                <div style="font-size: 24px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">{completion_rate}%</div>
                <div style="font-size: 14px; color: #6B7280;">Completion</div>
                </div><div style="
                    background: white;
                    padding: 24px;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    text-align: center;
                ">      
                <div style="font-size: 32px; margin-bottom: 8px;">📈</div>
                <div style="font-size: 24px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">{avg_engagement}%</div>
                <div style="font-size: 14px; color: #6B7280;">Avg Engagement</div>
            </div>
            <div style="
                background: white;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                text-align: center;">
                <div style="font-size: 32px; margin-bottom: 8px;">👥</div>
                <div style="font-size: 24px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">{active_students}</div>
                <div style="font-size: 14px; color: #6B7280;">Active Students</div>
            </div>
        </div>
    </div>
    """
    
    # Subject progress section
    subject_progress_html = """
    <div style="margin-bottom: 32px;">
        <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
            <h3 style="margin: 0 0 8px 0; color: #1F2937; font-size: 18px; font-weight: 600;">Subject Progress</h3>
            <p style="margin: 0 0 20px 0; color: #6B7280; font-size: 14px;">Track progress across all subjects in this class</p>
            <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #3B82F6; font-size: 18px;">📚</span>
                        <span style="font-weight: 500; color: #1F2937;">Mathematics</span>
                    </div>
                    <button style="
                        background: #3B82F6;
                        color: white;
                        border: none;
                        padding: 6px 12px;
                        border-radius: 6px;
                        font-size: 12px;
                        font-weight: 500;
                        cursor: pointer;
                    ">Manage</button>
                </div>
                <div style="
                    background: #E5E7EB;
                    height: 8px;
                    border-radius: 4px;
                    overflow: hidden;
                ">
                    <div style="
                        background: #3B82F6;
                        height: 100%;
                        width: 78%;
                        border-radius: 4px;
                    "></div>
                </div>
                <div style="text-align: right; font-size: 12px; color: #6B7280; margin-top: 4px;">78% Complete</div>
            </div>
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #10B981; font-size: 18px;">🔬</span>
                        <span style="font-weight: 500; color: #1F2937;">Science</span>
                    </div>
                    <button style="
                        background: #10B981;
                        color: white;
                        border: none;
                        padding: 6px 12px;
                        border-radius: 6px;
                        font-size: 12px;
                        font-weight: 500;
                        cursor: pointer;
                    ">Manage</button>
                </div>
                <div style="
                    background: #E5E7EB;
                    height: 8px;
                    border-radius: 4px;
                    overflow: hidden;
                ">
                    <div style="
                        background: #10B981;
                        height: 100%;
                        width: 65%;
                        border-radius: 4px;
                    "></div>
                </div>
                <div style="text-align: right; font-size: 12px; color: #6B7280; margin-top: 4px;">65% Complete</div>
            </div>
        </div>
    </div>
    """
    
    # Quick actions section
    quick_actions_html = """
    <div>
        <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
            <h3 style="margin: 0 0 8px 0; color: #1F2937; font-size: 18px; font-weight: 600;">Quick Actions</h3>
            <p style="margin: 0 0 20px 0; color: #6B7280; font-size: 14px;">Common tasks for this class</p>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
                <button style="
                    background: white;
                    border: 1px solid #E5E7EB;
                    padding: 20px;
                    border-radius: 12px;
                    cursor: pointer;
                    text-align: center;
                    transition: all 0.2s;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 8px;
                " onmouseover="this.style.borderColor='#3B82F6'; this.style.boxShadow='0 4px 12px rgba(59, 130, 246, 0.1)'" onmouseout="this.style.borderColor='#E5E7EB'; this.style.boxShadow='none'">
                    <div style="font-size: 24px;">📝</div>
                    <div style="font-size: 14px; font-weight: 500; color: #1F2937;">Generate Content</div>
                </button>
                <button style="
                    background: white;
                    border: 1px solid #E5E7EB;
                    padding: 20px;
                    border-radius: 12px;
                    cursor: pointer;
                    text-align: center;
                    transition: all 0.2s;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 8px;
                " onmouseover="this.style.borderColor='#3B82F6'; this.style.boxShadow='0 4px 12px rgba(59, 130, 246, 0.1)'" onmouseout="this.style.borderColor='#E5E7EB'; this.style.boxShadow='none'">
                    <div style="font-size: 24px;">📷</div>
                    <div style="font-size: 14px; font-weight: 500; color: #1F2937;">Photo to Topic</div>
                </button><button style="
                    background: white;
                    border: 1px solid #E5E7EB;
                    padding: 20px;
                    border-radius: 12px;
                    cursor: pointer;
                    text-align: center;
                    transition: all 0.2s;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 8px;
                " onmouseover="this.style.borderColor='#3B82F6'; this.style.boxShadow='0 4px 12px rgba(59, 130, 246, 0.1)'" onmouseout="this.style.borderColor='#E5E7EB'; this.style.boxShadow='none'">
                    <div style="font-size: 24px;">🎤</div>
                    <div style="font-size: 14px; font-weight: 500; color: #1F2937;">Voice Input</div>
                </button><button style="
                    background: white;
                    border: 1px solid #E5E7EB;
                    padding: 20px;
                    border-radius: 12px;
                    cursor: pointer;
                    text-align: center;
                    transition: all 0.2s;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 8px;
                " onmouseover="this.style.borderColor='#3B82F6'; this.style.boxShadow='0 4px 12px rgba(59, 130, 246, 0.1)'" onmouseout="this.style.borderColor='#E5E7EB'; this.style.boxShadow='none'">
                    <div style="font-size: 24px;">🎯</div>
                    <div style="font-size: 14px; font-weight: 500; color: #1F2937;">Create Assessment</div>
                </button>
            </div>
        </div>
    </div>
    """
    
    # Combine all sections
    full_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        {header_html}
        {tabs_html}
        {metrics_html}
        {subject_progress_html}
        
    </div>
    """
    
    st.markdown(full_html, unsafe_allow_html=True)

def display_class_dashboard_page(class_data: Dict):
    """Display the complete class dashboard page"""
    
    # Page configuration
    st.set_page_config(
        page_title=f"{class_data.get('name', 'Class')} Dashboard",
        page_icon="🎓",
        layout="wide"
    )
    
    # Create the dashboard
    create_class_dashboard(class_data)
    
    # Add Streamlit functionality for the quick actions
    st.markdown("---")
    st.subheader("Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Generate Content", use_container_width=True):
            st.info("Content generation feature will be implemented here.")
    
    with col2:
        if st.button("📷 Photo to Topic", use_container_width=True):
            st.info("Photo analysis feature will be implemented here.")
    
    with col3:
        if st.button("🎤 Voice Input", use_container_width=True):
            st.info("Voice input feature will be implemented here.")
    
    with col4:
        if st.button("🎯 Create Assessment", use_container_width=True):
            st.info("Assessment creation feature will be implemented here.")
    
    # Sidebar with class info
    st.sidebar.markdown("---")
    st.sidebar.subheader("Class Information")
    st.sidebar.write(f"**Name:** {class_data.get('name', 'N/A')}")
    st.sidebar.write(f"**Grade:** {class_data.get('grade', 'N/A')}")
    st.sidebar.write(f"**Subject:** {class_data.get('subject', 'N/A')}")
    st.sidebar.write(f"**Teacher:** {class_data.get('teacher', 'N/A')}")
    st.sidebar.write(f"**Students:** {class_data.get('capacity', 'N/A')}")

def main():
    """Demo function for testing"""
    # Demo class data
    demo_class = {
        'name': 'Mathematics Excellence',
        'grade': '5th Grade',
        'subject': 'Mathematics',
        'teacher': 'Dr. Johnson',
        'capacity': 32,
        'description': 'Advanced mathematics program focusing on problem-solving and conceptual understanding'
    }
    
    display_class_dashboard_page(demo_class)

if __name__ == "__main__":
    main() 