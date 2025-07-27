# 🎓 Reusable Class Display Components

This module provides beautiful, reusable components for displaying classes from your database in a modern and user-friendly way.

## 📁 File Structure

```
├── db_utils.py              # Database connection and management
├── components/
│   └── class_display.py     # Reusable display components
├── pages/
│   ├── exam_agent.py        # Your existing exam agent
│   └── class_viewer.py      # Example page using the components
└── example_usage.py         # Integration example with exam agent
```

## 🚀 Quick Start

### 1. Basic Usage

```python
import streamlit as st
from db_utils import get_db_manager
from components.class_display import display_classes_card_view

# Get database connection
db_manager = get_db_manager()
if db_manager:
    try:
        classes = db_manager.fetch_classes()
        display_classes_card_view(classes, "Available Classes")
    finally:
        db_manager.disconnect()
```

### 2. Available Components

#### `display_classes_card_view(classes, title)`
- Displays classes in beautiful cards with gradients
- Responsive 3-column layout
- Action buttons for each class
- Perfect for browsing classes

#### `display_classes_table(classes, title)`
- Displays classes in a clean table format
- Sortable and filterable
- Good for data-heavy views

#### `display_class_details(class_data)`
- Shows detailed information about a specific class
- Split layout with details and quick actions
- Perfect for class detail pages

#### `display_classes_with_filters()`
- Complete browsing experience with filters
- Grade and subject filtering
- Toggle between card and table views

## 🎨 Features

### ✨ Beautiful UI
- Modern gradient cards
- Responsive design
- Professional styling
- Interactive elements

### 🔧 Reusable Components
- Modular design
- Easy to customize
- Consistent styling
- Error handling

### 📊 Database Integration
- Safe database connections
- Proper error handling
- Connection pooling
- Type hints for better development

## 📋 Usage Examples

### Example 1: Simple Class Display

```python
import streamlit as st
from db_utils import get_db_manager
from components.class_display import display_classes_card_view

def show_classes():
    db_manager = get_db_manager()
    if db_manager:
        try:
            classes = db_manager.fetch_classes()
            display_classes_card_view(classes, "Our Classes")
        finally:
            db_manager.disconnect()

if __name__ == "__main__":
    st.title("🎓 Class Viewer")
    show_classes()
```

### Example 2: Filtered Class View

```python
import streamlit as st
from components.class_display import display_classes_with_filters

def main():
    st.title("Browse Classes")
    display_classes_with_filters()

if __name__ == "__main__":
    main()
```

### Example 3: Class Details with Exam Integration

```python
import streamlit as st
from db_utils import get_db_manager
from components.class_display import display_class_details
from pages.exam_agent import generate_quiz

def show_class_with_exam():
    db_manager = get_db_manager()
    if db_manager:
        try:
            classes = db_manager.fetch_classes()
            if classes:
                selected_class = st.selectbox("Select Class", classes)
                display_class_details(selected_class)
                
                # Add exam generation
                if st.button("Generate Quiz"):
                    quiz = generate_quiz(
                        selected_class.get('subject', 'Math'),
                        selected_class.get('grade', '5'),
                        5
                    )
                    # Display quiz...
        finally:
            db_manager.disconnect()
```

## 🔧 Customization

### Custom Styling

You can customize the appearance by modifying the CSS in the components:

```python
# In display_classes_card_view function
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
```

### Adding Custom Fields

To display additional class fields, modify the display functions:

```python
# Add new fields to display
if 'new_field' in class_data:
    st.markdown(f"**New Field:** {class_data['new_field']}")
```

## 🛠️ Database Requirements

The components expect a `Class` table with the following fields:
- `name` - Class name
- `grade` - Grade level
- `subject` - Subject name
- `teacher` - Teacher name
- `schedule` - Class schedule
- `capacity` - Student capacity
- `description` - Class description (optional)

## 🚀 Running the Examples

1. **Basic Class Viewer:**
   ```bash
   streamlit run pages/class_viewer.py
   ```

2. **Integrated System:**
   ```bash
   streamlit run example_usage.py
   ```

3. **Component Demo:**
   ```bash
   streamlit run components/class_display.py
   ```

## 📝 Integration with Existing Code

The components are designed to work seamlessly with your existing `exam_agent.py`. The `example_usage.py` shows how to integrate both systems together.

## 🎯 Benefits

1. **Reusable**: Use the same components across different pages
2. **Consistent**: Uniform styling and behavior
3. **Maintainable**: Centralized styling and logic
4. **Scalable**: Easy to add new features
5. **Professional**: Modern, beautiful UI

## 🔍 Troubleshooting

### Database Connection Issues
- Check your database credentials in `db_utils.py`
- Ensure the database server is running
- Verify network connectivity

### Import Errors
- Make sure all required packages are installed
- Check file paths and imports
- Use the provided example files as templates

### Display Issues
- Check if your Class table has the expected columns
- Verify data types match expectations
- Use the database manager's error handling

## 📞 Support

For issues or questions:
1. Check the example files for usage patterns
2. Verify database connectivity
3. Review the component functions for customization options 