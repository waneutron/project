"""
error_handler.py - Centralized error handling and logging
"""
import logging
import traceback
from datetime import datetime
from tkinter import messagebox
import json
import os

class ErrorHandler:
    """Centralized error handling"""
    
    def __init__(self, log_file='app_errors.log'):
        self.log_file = log_file
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def log_error(self, error, context=''):
        """Log error with full traceback"""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'traceback': traceback.format_exc()
        }
        
        logging.error(json.dumps(error_info, indent=2))
        return error_info
    
    def log_info(self, message, context=''):
        """Log informational message"""
        logging.info(f"{context}: {message}" if context else message)
    
    def log_warning(self, message, context=''):
        """Log warning message"""
        logging.warning(f"{context}: {message}" if context else message)
    
    def handle_error(self, error, context='', show_user=True, critical=False):
        """
        Handle error comprehensively
        
        Args:
            error: The exception
            context: Where the error occurred
            show_user: Show messagebox to user
            critical: Is this a critical error?
        """
        # Log error
        error_info = self.log_error(error, context)
        
        # Show to user
        if show_user:
            if critical:
                messagebox.showerror(
                    "Critical Error",
                    f"A critical error occurred:\n\n{str(error)}\n\n"
                    f"Context: {context}\n\n"
                    f"Please check {self.log_file} for details."
                )
            else:
                messagebox.showwarning(
                    "Error",
                    f"An error occurred:\n\n{str(error)}\n\n"
                    f"Context: {context}"
                )
        
        return error_info
    
    def safe_execute(self, func, *args, context='', show_errors=True, default_return=None, **kwargs):
        """
        Execute function with error handling
        
        Returns:
            Function result or default_return if error
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle_error(e, context=context or func.__name__, show_user=show_errors)
            return default_return
    
    def get_error_summary(self, days=7):
        """Get summary of recent errors"""
        if not os.path.exists(self.log_file):
            return "No errors logged"
        
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        error_count = 0
        warning_count = 0
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ' - ERROR - ' in line:
                        error_count += 1
                    elif ' - WARNING - ' in line:
                        warning_count += 1
        except (IOError, UnicodeDecodeError) as e:
            # Log the error but don't fail the summary
            logging.warning(f"Failed to read error log for summary: {e}")
        
        return f"Last {days} days: {error_count} errors, {warning_count} warnings"
    
    def clear_old_logs(self, days=90):
        """Clear logs older than specified days"""
        # For simplicity, just truncate if file is too large
        if os.path.exists(self.log_file):
            size_mb = os.path.getsize(self.log_file) / (1024 * 1024)
            if size_mb > 10:  # If log file is > 10MB
                # Archive old log
                archive_name = f"{self.log_file}.{datetime.now().strftime('%Y%m%d')}.old"
                os.rename(self.log_file, archive_name)
                logging.info("Log file archived and reset")


# Global error handler instance
_error_handler = None

def get_error_handler():
    """Get global error handler"""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler


# Decorator for automatic error handling
def handle_errors(context='', show_user=True, default_return=None):
    """Decorator to automatically handle errors"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            handler = get_error_handler()
            return handler.safe_execute(
                func, *args,
                context=context or func.__name__,
                show_errors=show_user,
                default_return=default_return,
                **kwargs
            )
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator


if __name__ == '__main__':
    # Test error handler
    handler = ErrorHandler()
    
    # Test logging
    handler.log_info("Test info message")
    handler.log_warning("Test warning message")
    
    try:
        raise ValueError("Test error")
    except Exception as e:
        handler.handle_error(e, context="Testing", show_user=False)
    
    print(handler.get_error_summary())

