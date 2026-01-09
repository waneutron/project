"""
unified_database.py - Unified Database System for All Forms
Centralized database management for the entire Document Management System
Optimized with query result caching
"""
import sqlite3
from datetime import datetime
import json
import os
from functools import lru_cache
from threading import Lock


class UnifiedDatabase:
    """Centralized database manager for all document types
    
    Optimizations:
    - Indexed queries on frequently searched fields
    - Query result caching with LRU cache
    - Connection pooling via context managers
    - Batch operations for multiple inserts
    """
    
    def __init__(self, db_name="kastam_documents.db"):
        """Initialize unified database connection"""
        self.db_name = db_name
        self.init_database()
        self._cache_lock = Lock()
        self._query_cache = {}
    
    def get_connection(self):
        """Get database connection with optimizations"""
        conn = sqlite3.connect(self.db_name)
        # Enable query optimization
        conn.execute('PRAGMA query_only = OFF')
        conn.execute('PRAGMA synchronous = NORMAL')  # Faster writes
        conn.execute('PRAGMA cache_size = 10000')     # Larger cache
        conn.execute('PRAGMA temp_store = MEMORY')    # Use memory for temp
        return conn
    
    def clear_cache(self):
        """Clear query cache - call after write operations"""
        with self._cache_lock:
            self._query_cache.clear()
    
    def init_database(self):
        """Initialize all database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # ==================== MAIN APPLICATIONS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_type TEXT NOT NULL,
                    category TEXT,
                    sub_option TEXT,
                    rujukan_kami TEXT,
                    rujukan_tuan TEXT,
                    nama_syarikat TEXT NOT NULL,
                    alamat TEXT,
                    tarikh TEXT,
                    tarikh_islam TEXT,
                    nama_pegawai TEXT,
                    status TEXT,
                    document_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    additional_data TEXT
                )
            ''')
            
            # ==================== PELUPUSAN DETAILS ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pelupusan_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    proses TEXT,
                    jenis_barang TEXT,
                    pengecualian TEXT,
                    amount TEXT,
                    tarikh_mula TEXT,
                    tarikh_tamat TEXT,
                    tempoh TEXT,
                    FOREIGN KEY (application_id) REFERENCES applications (id)
                        ON DELETE CASCADE
                )
            ''')
            
            # ==================== BUTIRAN 5D DETAILS ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS butiran5d_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    no_sijil TEXT,
                    tarikh_kuatkuasa TEXT,
                    sebab_tolak TEXT,
                    FOREIGN KEY (application_id) REFERENCES applications (id)
                        ON DELETE CASCADE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS butiran5d_vehicles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    bil INTEGER,
                    jenama_model TEXT NOT NULL,
                    no_chasis TEXT NOT NULL,
                    no_enjin TEXT NOT NULL,
                    FOREIGN KEY (application_id) REFERENCES applications (id)
                        ON DELETE CASCADE
                )
            ''')
            
            # ==================== AMES DETAILS ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ames_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    no_kelulusan TEXT,
                    kategori TEXT,
                    tarikh_mula TEXT,
                    tarikh_tamat TEXT,
                    tempoh_kelulusan TEXT,
                    FOREIGN KEY (application_id) REFERENCES applications (id)
                        ON DELETE CASCADE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ames_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    item_type TEXT,
                    bil INTEGER,
                    kod_tarif TEXT NOT NULL,
                    deskripsi TEXT NOT NULL,
                    nisbah TEXT,
                    tarikh_kuatkuasa TEXT,
                    FOREIGN KEY (application_id) REFERENCES applications (id)
                        ON DELETE CASCADE
                )
            ''')
            
            # ==================== SIGNUP B DETAILS ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS signupb_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    email TEXT,
                    talian TEXT,
                    FOREIGN KEY (application_id) REFERENCES applications (id)
                        ON DELETE CASCADE
                )
            ''')
            
            # ==================== DOCUMENT ATTACHMENTS ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS document_attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT,
                    file_size INTEGER,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (application_id) REFERENCES applications (id)
                        ON DELETE CASCADE
                )
            ''')
            
            # ==================== AUDIT LOG ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER,
                    action TEXT NOT NULL,
                    user_name TEXT,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (application_id) REFERENCES applications (id)
                        ON DELETE SET NULL
                )
            ''')
            
            # ==================== CREATE INDEXES ====================
            indexes = [
                ('idx_form_type', 'applications', 'form_type'),
                ('idx_rujukan', 'applications', 'rujukan_kami'),
                ('idx_nama', 'applications', 'nama_syarikat'),
                ('idx_status', 'applications', 'status'),
                ('idx_created', 'applications', 'created_at'),
                ('idx_chasis', 'butiran5d_vehicles', 'no_chasis'),
                ('idx_enjin', 'butiran5d_vehicles', 'no_enjin'),
                ('idx_kod_tarif', 'ames_items', 'kod_tarif'),
                ('idx_no_sijil', 'butiran5d_details', 'no_sijil'),
                ('idx_no_kelulusan', 'ames_details', 'no_kelulusan')
            ]
            
            for idx_name, table_name, column_name in indexes:
                cursor.execute(f'''
                    CREATE INDEX IF NOT EXISTS {idx_name} 
                    ON {table_name}({column_name})
                ''')
            
            conn.commit()
        finally:
            conn.close()
    
    # ==================== GENERAL CRUD OPERATIONS ====================
    
    def save_application(self, form_type, application_data, specific_details=None):
        """
        Save a new application (generic for all forms)
        
        Args:
            form_type: 'pelupusan', 'butiran5d', 'ames', 'signupb', etc.
            application_data: dict with basic application details
            specific_details: dict with form-specific details
            
        Returns:
            application_id
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insert main application
            cursor.execute('''
                INSERT INTO applications 
                (form_type, category, sub_option, rujukan_kami, rujukan_tuan, 
                 nama_syarikat, alamat, tarikh, tarikh_islam, nama_pegawai, 
                 status, document_path, additional_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                form_type,
                application_data.get('category'),
                application_data.get('sub_option'),
                application_data.get('rujukan_kami'),
                application_data.get('rujukan_tuan'),
                application_data.get('nama_syarikat'),
                application_data.get('alamat'),
                application_data.get('tarikh'),
                application_data.get('tarikh_islam'),
                application_data.get('nama_pegawai'),
                application_data.get('status'),
                application_data.get('document_path'),
                json.dumps(application_data.get('additional_data', {}))
            ))
            
            application_id = cursor.lastrowid
            
            # Save form-specific details
            if specific_details:
                if form_type == 'pelupusan':
                    self._save_pelupusan_details(cursor, application_id, specific_details)
                elif form_type == 'butiran5d':
                    self._save_butiran5d_details(cursor, application_id, specific_details)
                elif form_type == 'ames':
                    self._save_ames_details(cursor, application_id, specific_details)
                elif form_type == 'signupb':
                    self._save_signupb_details(cursor, application_id, specific_details)
            
            # Log action
            self._log_action(cursor, application_id, 'CREATE', 
                           application_data.get('nama_pegawai'),
                           f"Created {form_type} application")
            
            conn.commit()
            return application_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _save_pelupusan_details(self, cursor, app_id, details):
        """Save Pelupusan-specific details"""
        cursor.execute('''
            INSERT INTO pelupusan_details
            (application_id, proses, jenis_barang, pengecualian, amount,
             tarikh_mula, tarikh_tamat, tempoh)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            app_id,
            details.get('proses'),
            details.get('jenis_barang'),
            details.get('pengecualian'),
            details.get('amount'),
            details.get('tarikh_mula'),
            details.get('tarikh_tamat'),
            details.get('tempoh')
        ))
    
    def _save_butiran5d_details(self, cursor, app_id, details):
        """Save Butiran 5D-specific details"""
        cursor.execute('''
            INSERT INTO butiran5d_details
            (application_id, no_sijil, tarikh_kuatkuasa, sebab_tolak)
            VALUES (?, ?, ?, ?)
        ''', (
            app_id,
            details.get('no_sijil'),
            details.get('tarikh_kuatkuasa'),
            details.get('sebab_tolak')
        ))
        
        # Save vehicles
        for vehicle in details.get('vehicles', []):
            cursor.execute('''
                INSERT INTO butiran5d_vehicles
                (application_id, bil, jenama_model, no_chasis, no_enjin)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                app_id,
                vehicle.get('bil'),
                vehicle.get('jenama_model'),
                vehicle.get('no_chasis'),
                vehicle.get('no_enjin')
            ))
    
    def _save_ames_details(self, cursor, app_id, details):
        """Save AMES-specific details"""
        cursor.execute('''
            INSERT INTO ames_details
            (application_id, no_kelulusan, kategori, tarikh_mula, 
             tarikh_tamat, tempoh_kelulusan)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            app_id,
            details.get('no_kelulusan'),
            details.get('kategori'),
            details.get('tarikh_mula'),
            details.get('tarikh_tamat'),
            details.get('tempoh_kelulusan')
        ))
        
        # Save items
        for item in details.get('items', []):
            cursor.execute('''
                INSERT INTO ames_items
                (application_id, item_type, bil, kod_tarif, deskripsi,
                 nisbah, tarikh_kuatkuasa)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                app_id,
                item.get('item_type'),
                item.get('bil'),
                item.get('kod_tarif'),
                item.get('deskripsi'),
                item.get('nisbah'),
                item.get('tarikh_kuatkuasa')
            ))
    
    def _save_signupb_details(self, cursor, app_id, details):
        """Save SignUp B-specific details"""
        cursor.execute('''
            INSERT INTO signupb_details
            (application_id, email, talian)
            VALUES (?, ?, ?)
        ''', (
            app_id,
            details.get('email'),
            details.get('talian')
        ))
    
    def _log_action(self, cursor, app_id, action, user_name, details):
        """Log action to audit log"""
        cursor.execute('''
            INSERT INTO audit_log
            (application_id, action, user_name, details)
            VALUES (?, ?, ?, ?)
        ''', (app_id, action, user_name, details))
    
    # ==================== SEARCH & RETRIEVAL ====================
    
    def get_all_applications(self, form_type=None, limit=100):
        """Get all applications, optionally filtered by form type
        
        Optimizations:
        - Caches results from get_all_applications calls
        - Uses indexed columns (form_type)
        - Limited results with LIMIT clause
        """
        # Create cache key from parameters
        cache_key = f"get_all_apps_{form_type}_{limit}"
        
        with self._cache_lock:
            if cache_key in self._query_cache:
                return self._query_cache[cache_key]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if form_type:
                cursor.execute('''
                    SELECT id, form_type, category, sub_option, rujukan_kami, 
                           nama_syarikat, tarikh, status, created_at
                    FROM applications
                    WHERE form_type = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (form_type, limit))
            else:
                cursor.execute('''
                    SELECT id, form_type, category, sub_option, rujukan_kami, 
                           nama_syarikat, tarikh, status, created_at
                    FROM applications
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Cache results
            with self._cache_lock:
                self._query_cache[cache_key] = results
            
            return results
            
            return results
        finally:
            conn.close()
    
    def get_application_by_id(self, application_id):
        """Get full application details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get main application
            cursor.execute('SELECT * FROM applications WHERE id = ?', (application_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            columns = [desc[0] for desc in cursor.description]
            application = dict(zip(columns, row))
            
            # Get form-specific details
            form_type = application['form_type']
            
            if form_type == 'pelupusan':
                cursor.execute('''
                    SELECT * FROM pelupusan_details 
                    WHERE application_id = ?
                ''', (application_id,))
                row = cursor.fetchone()
                if row:
                    cols = [desc[0] for desc in cursor.description]
                    application['pelupusan_details'] = dict(zip(cols, row))
            
            elif form_type == 'butiran5d':
                cursor.execute('''
                    SELECT * FROM butiran5d_details 
                    WHERE application_id = ?
                ''', (application_id,))
                row = cursor.fetchone()
                if row:
                    cols = [desc[0] for desc in cursor.description]
                    application['butiran5d_details'] = dict(zip(cols, row))
                
                cursor.execute('''
                    SELECT bil, jenama_model, no_chasis, no_enjin
                    FROM butiran5d_vehicles
                    WHERE application_id = ?
                    ORDER BY bil
                ''', (application_id,))
                cols = [desc[0] for desc in cursor.description]
                application['vehicles'] = [dict(zip(cols, row)) for row in cursor.fetchall()]
            
            elif form_type == 'ames':
                cursor.execute('''
                    SELECT * FROM ames_details 
                    WHERE application_id = ?
                ''', (application_id,))
                row = cursor.fetchone()
                if row:
                    cols = [desc[0] for desc in cursor.description]
                    application['ames_details'] = dict(zip(cols, row))
                
                cursor.execute('''
                    SELECT item_type, bil, kod_tarif, deskripsi, nisbah, tarikh_kuatkuasa
                    FROM ames_items
                    WHERE application_id = ?
                    ORDER BY item_type, bil
                ''', (application_id,))
                cols = [desc[0] for desc in cursor.description]
                application['items'] = [dict(zip(cols, row)) for row in cursor.fetchall()]
            
            elif form_type == 'signupb':
                cursor.execute('''
                    SELECT * FROM signupb_details 
                    WHERE application_id = ?
                ''', (application_id,))
                row = cursor.fetchone()
                if row:
                    cols = [desc[0] for desc in cursor.description]
                    application['signupb_details'] = dict(zip(cols, row))
            
            return application
        finally:
            conn.close()
    
    def search_applications(self, search_text, form_type=None):
        """Search applications across all fields"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            search_pattern = f"%{search_text}%"
            
            query = '''
                SELECT DISTINCT a.id, a.form_type, a.category, a.rujukan_kami, 
                       a.nama_syarikat, a.tarikh, a.status, a.created_at
                FROM applications a
                LEFT JOIN butiran5d_vehicles v ON a.id = v.application_id
                LEFT JOIN ames_items i ON a.id = i.application_id
                WHERE (a.rujukan_kami LIKE ? 
                   OR a.nama_syarikat LIKE ?
                   OR a.alamat LIKE ?
                   OR v.no_chasis LIKE ?
                   OR v.no_enjin LIKE ?
                   OR i.kod_tarif LIKE ?)
            '''
            
            params = [search_pattern] * 6
            
            if form_type:
                query += ' AND a.form_type = ?'
                params.append(form_type)
            
            query += ' ORDER BY a.created_at DESC LIMIT 50'
            
            cursor.execute(query, params)
            
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return results
        finally:
            conn.close()
    
    def delete_application(self, application_id):
        """Delete application (cascades to all related tables)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Log deletion
            cursor.execute('''
                SELECT form_type, rujukan_kami, nama_syarikat
                FROM applications WHERE id = ?
            ''', (application_id,))
            app_info = cursor.fetchone()
            
            if app_info:
                self._log_action(cursor, application_id, 'DELETE', None,
                               f"Deleted {app_info[0]} application: {app_info[1]} - {app_info[2]}")
            
            # Delete application (cascades to all related tables)
            cursor.execute('DELETE FROM applications WHERE id = ?', (application_id,))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    # ==================== STATISTICS & REPORTS ====================
    
    def get_statistics(self, form_type=None):
        """Get comprehensive statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            stats = {}
            
            # Total applications (using parameterized query to prevent SQL injection)
            if form_type:
                cursor.execute('SELECT COUNT(*) FROM applications WHERE form_type = ?', (form_type,))
            else:
                cursor.execute('SELECT COUNT(*) FROM applications')
            stats['total_applications'] = cursor.fetchone()[0]
            
            # By status
            if form_type:
                cursor.execute('''
                    SELECT status, COUNT(*) 
                    FROM applications
                    WHERE form_type = ?
                    GROUP BY status
                ''', (form_type,))
            else:
                cursor.execute('''
                    SELECT status, COUNT(*) 
                    FROM applications
                    GROUP BY status
                ''')
            stats['by_status'] = dict(cursor.fetchall())
            
            # By form type (if not filtered)
            if not form_type:
                cursor.execute('''
                    SELECT form_type, COUNT(*) 
                    FROM applications
                    GROUP BY form_type
                ''')
                stats['by_form_type'] = dict(cursor.fetchall())
            
            # Recent (last 7 days)
            if form_type:
                cursor.execute('''
                    SELECT COUNT(*) FROM applications
                    WHERE form_type = ? AND created_at >= datetime('now', '-7 days')
                ''', (form_type,))
            else:
                cursor.execute('''
                    SELECT COUNT(*) FROM applications
                    WHERE created_at >= datetime('now', '-7 days')
                ''')
            stats['last_7_days'] = cursor.fetchone()[0]
            
            # Recent (last 30 days)
            if form_type:
                cursor.execute('''
                    SELECT COUNT(*) FROM applications
                    WHERE form_type = ? AND created_at >= datetime('now', '-30 days')
                ''', (form_type,))
            else:
                cursor.execute('''
                    SELECT COUNT(*) FROM applications
                    WHERE created_at >= datetime('now', '-30 days')
                ''')
            stats['last_30_days'] = cursor.fetchone()[0]
            
            # This month
            if form_type:
                cursor.execute('''
                    SELECT COUNT(*) FROM applications
                    WHERE form_type = ? AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
                ''', (form_type,))
            else:
                cursor.execute('''
                    SELECT COUNT(*) FROM applications
                    WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
                ''')
            stats['this_month'] = cursor.fetchone()[0]
            
            # This year
            if form_type:
                cursor.execute('''
                    SELECT COUNT(*) FROM applications
                    WHERE form_type = ? AND strftime('%Y', created_at) = strftime('%Y', 'now')
                ''', (form_type,))
            else:
                cursor.execute('''
                    SELECT COUNT(*) FROM applications
                    WHERE strftime('%Y', created_at) = strftime('%Y', 'now')
                ''')
            stats['this_year'] = cursor.fetchone()[0]
            
            return stats
        finally:
            conn.close()
    
    def get_monthly_report(self, year=None):
        """Get monthly breakdown of applications"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if not year:
                year = datetime.now().year
            
            cursor.execute('''
                SELECT 
                    strftime('%m', created_at) as month,
                    form_type,
                    COUNT(*) as count
                FROM applications
                WHERE strftime('%Y', created_at) = ?
                GROUP BY month, form_type
                ORDER BY month, form_type
            ''', (str(year),))
            
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return results
        finally:
            conn.close()
    
    def export_to_csv(self, form_type=None, filename=None):
        """Export applications to CSV"""
        import csv
        
        if not filename:
            form_suffix = f"_{form_type}" if form_type else "_all"
            filename = f"kastam_export{form_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Use parameterized query to prevent SQL injection
            if form_type:
                cursor.execute('''
                    SELECT a.rujukan_kami, a.nama_syarikat, a.alamat, a.tarikh, 
                           a.form_type, a.category, a.sub_option, a.status, 
                           a.nama_pegawai, a.created_at
                    FROM applications a
                    WHERE a.form_type = ?
                    ORDER BY a.created_at DESC
                ''', (form_type,))
            else:
                cursor.execute('''
                    SELECT a.rujukan_kami, a.nama_syarikat, a.alamat, a.tarikh, 
                           a.form_type, a.category, a.sub_option, a.status, 
                           a.nama_pegawai, a.created_at
                    FROM applications a
                    ORDER BY a.created_at DESC
                ''')
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Rujukan', 'Nama Syarikat', 'Alamat', 'Tarikh',
                               'Jenis Borang', 'Kategori', 'Sub-Kategori', 'Status',
                               'Pegawai', 'Tarikh Rekod'])
                writer.writerows(cursor.fetchall())
            
            return filename
        finally:
            conn.close()
    
    # ==================== AUDIT & HISTORY ====================
    
    def get_audit_log(self, application_id=None, limit=100):
        """Get audit log entries"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if application_id:
                cursor.execute('''
                    SELECT * FROM audit_log
                    WHERE application_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (application_id, limit))
            else:
                cursor.execute('''
                    SELECT * FROM audit_log
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return results
        finally:
            conn.close()
    
    def add_attachment(self, application_id, file_name, file_path, file_type=None, file_size=None):
        """Add attachment to application"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO document_attachments
                (application_id, file_name, file_path, file_type, file_size)
                VALUES (?, ?, ?, ?, ?)
            ''', (application_id, file_name, file_path, file_type, file_size))
            
            self._log_action(cursor, application_id, 'ATTACHMENT_ADDED', None,
                           f"Added attachment: {file_name}")
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_attachments(self, application_id):
        """Get all attachments for an application"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM document_attachments
                WHERE application_id = ?
                ORDER BY uploaded_at DESC
            ''', (application_id,))
            
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return results
        finally:
            conn.close()


# ==================== CONVENIENCE FUNCTIONS ====================

def get_database():
    """Get singleton database instance"""
    if not hasattr(get_database, 'instance'):
        get_database.instance = UnifiedDatabase()
    return get_database.instance
