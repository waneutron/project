#!/usr/bin/env python3
"""
Test script to verify GUI integration and placeholder mapping functionality
"""

def test_imports():
    """Test importing all GUI components"""
    print("Testing GUI component imports...")

    try:
        from helpers.template_selector_dialog import TemplateSelector
        print("✓ TemplateSelector imported successfully")
    except Exception as e:
        print(f"✗ TemplateSelector import failed: {e}")

    try:
        from helpers.template_completeness_dialog import TemplateScannerDialog, PlaceholderMappingDialog
        print("✓ TemplateScannerDialog and PlaceholderMappingDialog imported successfully")
    except Exception as e:
        print(f"✗ TemplateScannerDialog/PlaceholderMappingDialog import failed: {e}")

    try:
        from helpers.template_management_dialog import TemplateManagementDialog
        print("✓ TemplateManagementDialog imported successfully")
    except Exception as e:
        print(f"✗ TemplateManagementDialog import failed: {e}")

    try:
        from helpers.placeholder_mapper import PlaceholderMapper
        print("✓ PlaceholderMapper imported successfully")
    except Exception as e:
        print(f"✗ PlaceholderMapper import failed: {e}")

def test_placeholder_mapper():
    """Test placeholder mapper functionality"""
    print("\nTesting PlaceholderMapper functionality...")

    try:
        from helpers.placeholder_mapper import PlaceholderMapper
        mapper = PlaceholderMapper()

        # Test getting field options
        field_options = mapper.get_field_options()
        print(f"✓ Field options loaded: {len(field_options)} options")

        # Test template configuration check
        is_configured = mapper.is_template_configured("test_template.docx")
        print(f"✓ Template configuration check works: {is_configured}")

        # Test getting template mapping
        mapping = mapper.get_template_mapping("test_template.docx")
        print(f"✓ Template mapping retrieval works: {mapping}")

    except Exception as e:
        print(f"✗ PlaceholderMapper functionality test failed: {e}")

def test_template_validator():
    """Test template field validator"""
    print("\nTesting TemplateFieldValidator functionality...")

    try:
        from helpers.template_field_validator import TemplateFieldValidator
        validator = TemplateFieldValidator()

        # Test basic functionality
        print("✓ TemplateFieldValidator imported successfully")

    except Exception as e:
        print(f"✗ TemplateFieldValidator test failed: {e}")

if __name__ == "__main__":
    print("=== GUI Integration Test ===\n")

    test_imports()
    test_placeholder_mapper()
    test_template_validator()

    print("\n=== Test Complete ===")
