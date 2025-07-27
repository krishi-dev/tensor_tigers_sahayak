import mysql.connector
from typing import List, Dict, Optional, Tuple
import streamlit as st

# Database connection details
DB_USER = "sahayak1"
DB_PASS = "O-RKDu&nhg)MoX*;"
DB_NAME = "sahayak"
HOST = "35.200.219.219"
PORT = 3306

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=HOST,
                port=PORT,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
            return False
        except mysql.connector.Error as err:
            st.error(f"Database connection error: {err}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get column names for a table"""
        try:
            self.cursor.execute(f"DESCRIBE {table_name}")
            columns = [row['Field'] for row in self.cursor.fetchall()]
            return columns
        except mysql.connector.Error as err:
            st.error(f"Error getting table columns: {err}")
            return []
    
    def fetch_classes(self) -> List[Dict]:
        """Fetch all classes from the database"""
        try:
            self.cursor.execute("SELECT * FROM Class")
            classes = self.cursor.fetchall()
            return classes
        except mysql.connector.Error as err:
            st.error(f"Error fetching classes: {err}")
            return []
    
    def fetch_classes_by_grade(self, grade: str) -> List[Dict]:
        """Fetch classes filtered by grade"""
        try:
            self.cursor.execute("SELECT * FROM Class WHERE grade = %s", (grade,))
            classes = self.cursor.fetchall()
            return classes
        except mysql.connector.Error as err:
            st.error(f"Error fetching classes by grade: {err}")
            return []
    
    def fetch_class_by_id(self, class_id: int) -> Optional[Dict]:
        """Fetch a specific class by ID"""
        try:
            self.cursor.execute("SELECT * FROM Class WHERE id = %s", (class_id,))
            class_data = self.cursor.fetchone()
            return class_data
        except mysql.connector.Error as err:
            st.error(f"Error fetching class by ID: {err}")
            return None
    
    def create_class(self, class_data: Dict) -> bool:
        """Create a new class in the database"""
        try:
            # Extract grade number from grade string (e.g., "5th Grade" -> "5")
            grade = class_data.get('grade', '')
            if 'Grade' in grade:
                grade = grade.split('Grade')[0].strip()
            
            query = """
            INSERT INTO Class (name, grade, subject, teacher, capacity, schedule, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """
            
            values = (
                class_data.get('name', ''),
                grade,
                class_data.get('subject', ''),
                class_data.get('teacher', ''),
                class_data.get('capacity', 30),
                class_data.get('schedule', ''),
                class_data.get('description', '')
            )
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
            
        except mysql.connector.Error as err:
            st.error(f"Error creating class: {err}")
            return False
    
    def update_class(self, class_id: int, class_data: Dict) -> bool:
        """Update an existing class"""
        try:
            query = """
            UPDATE Class 
            SET name = %s, grade = %s, subject = %s, teacher = %s, 
                capacity = %s, schedule = %s, description = %s, updated_at = NOW()
            WHERE id = %s
            """
            
            values = (
                class_data.get('name', ''),
                class_data.get('grade', ''),
                class_data.get('subject', ''),
                class_data.get('teacher', ''),
                class_data.get('capacity', 30),
                class_data.get('schedule', ''),
                class_data.get('description', ''),
                class_id
            )
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
            
        except mysql.connector.Error as err:
            st.error(f"Error updating class: {err}")
            return False
    
    def delete_class(self, class_id: int) -> bool:
        """Delete a class from the database"""
        try:
            query = "DELETE FROM Class WHERE id = %s"
            self.cursor.execute(query, (class_id,))
            self.connection.commit()
            return True
            
        except mysql.connector.Error as err:
            st.error(f"Error deleting class: {err}")
            return False

def get_db_manager() -> DatabaseManager:
    """Get a database manager instance"""
    db_manager = DatabaseManager()
    if db_manager.connect():
        return db_manager
    return None 