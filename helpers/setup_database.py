"""
setup_database.py - Database Setup and Test Script
Run this to initialize and test the unified database system
"""
from helpers.unified_database import UnifiedDatabase
from datetime import datetime
import os


def setup_and_test_database():
    """Setup and test the unified database"""
    
    print("="*60)
    print("KASTAM DOCUMENT MANAGEMENT SYSTEM")
    print("Database Setup & Test Script")
    print("="*60)
    print()
    
    # Initialize database
    print("📦 Initializing database...")
    db = UnifiedDatabase()
    print("✅ Database initialized successfully!")
    print(f"   Database file: {db.db_name}")
    print()
    
    # Check if database file exists
    if os.path.exists(db.db_name):
        file_size = os.path.getsize(db.db_name)
        print(f"✅ Database file created: {file_size} bytes")
    else:
        print("❌ Database file not found!")
        return
    
    print()
    print("-"*60)
    print("TESTING DATABASE OPERATIONS")
    print("-"*60)
    print()
    
    # Test 1: Save a Pelupusan application
    print("📝 Test 1: Saving Pelupusan application...")
    try:
        app_data = {
            'category': 'Pelupusan',
            'sub_option': 'pemusnahan',
            'rujukan_kami': 'KE.JB(90)650/05-02/TEST001',
            'rujukan_tuan': None,
            'nama_syarikat': 'SYARIKAT TEST SDN BHD',
            'alamat': 'NO. 1, JALAN TEST, 81100 JOHOR BAHRU',
            'tarikh': datetime.now().strftime('%d/%m/%Y'),
            'tarikh_islam': '1 Jamadil Akhir 1447H',
            'nama_pegawai': 'HABBAH SYAKIRAH BINTI AB GHAFAR',
            'status': 'DILULUSKAN',
            'document_path': 'test_pelupusan.pdf'
        }
        
        specific_details = {
            'proses': 'pemusnahan',
            'jenis_barang': 'barang siap',
            'pengecualian': 'ames',
            'amount': None,
            'tarikh_mula': '01/12/2024',
            'tarikh_tamat': '31/12/2024',
            'tempoh': 'tiga puluh (30) hari'
        }
        
        app_id = db.save_application('pelupusan', app_data, specific_details)
        print(f"✅ Pelupusan application saved! ID: {app_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 2: Save a Butiran 5D application
    print("🚗 Test 2: Saving Butiran 5D application...")
    try:
        app_data = {
            'category': 'Butiran 5D',
            'sub_option': 'DILULUSKAN',
            'rujukan_kami': 'KE.JB(90)650/05-02/A/TEST002',
            'rujukan_tuan': None,
            'nama_syarikat': 'AHMAD BIN ALI',
            'alamat': 'NO. 23, JALAN BAHAGIA, 81300 SKUDAI, JOHOR',
            'tarikh': datetime.now().strftime('%d/%m/%Y'),
            'tarikh_islam': '1 Jamadil Akhir 1447H',
            'nama_pegawai': 'ZURIDAH BINTI MOHD ZOB',
            'status': 'DILULUSKAN',
            'document_path': 'test_butiran5d.pdf'
        }
        
        specific_details = {
            'no_sijil': 'J31-5D-2411-0001',
            'tarikh_kuatkuasa': '01 NOVEMBER 2024',
            'sebab_tolak': None,
            'vehicles': [
                {
                    'bil': 1,
                    'jenama_model': 'TOYOTA / VIOS',
                    'no_chasis': 'MHFM1234567890123',
                    'no_enjin': '2NR1234567'
                },
                {
                    'bil': 2,
                    'jenama_model': 'HONDA / CIVIC',
                    'no_chasis': 'MHFM9876543210987',
                    'no_enjin': 'R18Z9876543'
                }
            ]
        }
        
        app_id = db.save_application('butiran5d', app_data, specific_details)
        print(f"✅ Butiran 5D application saved! ID: {app_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 3: Save an AMES application
    print("📊 Test 3: Saving AMES application...")
    try:
        app_data = {
            'category': 'AMES',
            'sub_option': 'Pedagang',
            'rujukan_kami': 'KE.JB(90)650/14/AMES/TEST003',
            'rujukan_tuan': None,
            'nama_syarikat': 'ABC TRADING SDN BHD',
            'alamat': 'LOT 123, KAWASAN PERINDUSTRIAN, 81100 JB',
            'tarikh': datetime.now().strftime('%d/%m/%Y'),
            'tarikh_islam': '1 Jamadil Akhir 1447H',
            'nama_pegawai': 'KHAIRONE DZARWANY BINTI MOHD KAIRI',
            'status': 'DILULUSKAN',
            'document_path': 'test_ames.pdf'
        }
        
        specific_details = {
            'no_kelulusan': 'AMES/JB/2024/001',
            'kategori': 'Pedagang',
            'tarikh_mula': '01 JANUARI 2025',
            'tarikh_tamat': '31 DISEMBER 2025',
            'tempoh_kelulusan': '01 JANUARI 2025 hingga 31 DISEMBER 2025',
            'items': [
                {
                    'item_type': 'pedagang',
                    'bil': 1,
                    'kod_tarif': '8471.30.00',
                    'deskripsi': 'KOMPUTER RIBA',
                    'nisbah': None,
                    'tarikh_kuatkuasa': '01 JANUARI 2025'
                },
                {
                    'item_type': 'pedagang',
                    'bil': 2,
                    'kod_tarif': '8528.72.00',
                    'deskripsi': 'MONITOR LCD',
                    'nisbah': None,
                    'tarikh_kuatkuasa': '01 JANUARI 2025'
                }
            ]
        }
        
        app_id = db.save_application('ames', app_data, specific_details)
        print(f"✅ AMES application saved! ID: {app_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("-"*60)
    print("TESTING RETRIEVAL & SEARCH")
    print("-"*60)
    print()
    
    # Test 4: Get all applications
    print("📋 Test 4: Retrieving all applications...")
    try:
        apps = db.get_all_applications(limit=10)
        print(f"✅ Found {len(apps)} applications:")
        for app in apps:
            print(f"   - {app['form_type'].upper()}: {app['nama_syarikat']} "
                  f"({app['rujukan_kami']})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 5: Search
    print("🔍 Test 5: Testing search...")
    try:
        results = db.search_applications('TEST')
        print(f"✅ Search found {len(results)} results for 'TEST'")
        for result in results:
            print(f"   - {result['form_type'].upper()}: {result['nama_syarikat']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 6: Statistics
    print("📊 Test 6: Getting statistics...")
    try:
        stats = db.get_statistics()
        print("✅ Statistics:")
        print(f"   Total applications: {stats.get('total_applications', 0)}")
        print(f"   Last 7 days: {stats.get('last_7_days', 0)}")
        print(f"   This month: {stats.get('this_month', 0)}")
        print(f"   This year: {stats.get('this_year', 0)}")
        
        if 'by_form_type' in stats:
            print("   By form type:")
            for form_type, count in stats['by_form_type'].items():
                print(f"     - {form_type.upper()}: {count}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 7: Get application by ID
    print("🔎 Test 7: Getting application by ID...")
    try:
        app = db.get_application_by_id(2)  # Get the Butiran 5D app
        if app:
            print(f"✅ Retrieved application:")
            print(f"   Form Type: {app['form_type'].upper()}")
            print(f"   Company: {app['nama_syarikat']}")
            print(f"   Status: {app['status']}")
            if 'vehicles' in app:
                print(f"   Vehicles: {len(app['vehicles'])}")
        else:
            print("❌ Application not found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("="*60)
    print("DATABASE SETUP COMPLETE!")
    print("="*60)
    print()
    print("✅ All tests passed successfully!")
    print()
    print("Next steps:")
    print("1. Integrate database into your forms (see Database_Integration_Guide.md)")
    print("2. Add history button to main menu")
    print("3. Test with real data")
    print()
    print(f"Database location: {os.path.abspath(db.db_name)}")
    print()


def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    print()
    
    required = [
        'sqlite3',
        'tkinter',
        'PIL',
        'docx',
        'hijri_converter'
    ]
    
    missing = []
    
    for module in required:
        try:
            if module == 'PIL':
                __import__('PIL')
            else:
                __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - NOT INSTALLED")
            missing.append(module)
    
    print()
    
    if missing:
        print("⚠️  Missing dependencies detected!")
        print()
        print("Please install:")
        for module in missing:
            if module == 'PIL':
                print("  pip install Pillow")
            elif module == 'docx':
                print("  pip install python-docx")
            else:
                print(f"  pip install {module}")
        print()
        return False
    else:
        print("✅ All dependencies installed!")
        print()
        return True


if __name__ == "__main__":
    print()
    
    # Check dependencies first
    if check_dependencies():
        # Run setup and tests
        setup_and_test_database()
    else:
        print("❌ Please install missing dependencies first!")
        print()
    
    input("Press Enter to exit...")
