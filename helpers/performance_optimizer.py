"""
performance_optimizer.py - Performance optimizations for template loading
"""
import functools
import time
from collections import OrderedDict

class LRUCache:
    """Least Recently Used cache for templates"""
    
    def __init__(self, max_size=20):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        """Get item from cache"""
        if key in self.cache:
            self.hits += 1
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        self.misses += 1
        return None
    
    def put(self, key, value):
        """Add item to cache"""
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            self.cache[key] = value
            # Remove oldest if over limit
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self):
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1f}%"
        }


class OptimizedTemplateStorage:
    """Optimized template storage with caching and lazy loading"""
    
    def __init__(self):
        self.document_cache = LRUCache(max_size=20)
        self.metadata_cache = {}
        self.load_times = {}  # Track load times
        
        try:
            from helpers.template_storage import get_template_storage
            self.storage = get_template_storage()
        except ImportError:
            self.storage = None
    
    def get_template_fast(self, filename):
        """Get template with caching"""
        # Check cache first
        cached_doc = self.document_cache.get(filename)
        if cached_doc:
            return cached_doc
        
        # Load from storage
        start_time = time.time()
        
        if self.storage:
            from helpers.template_storage import get_template_document
            doc = get_template_document(filename)
        else:
            from docx import Document
            from helpers.resource_path import get_template_path
            doc = Document(get_template_path(filename))
        
        load_time = time.time() - start_time
        
        # Track performance
        self.load_times[filename] = load_time
        
        # Cache it
        if doc:
            self.document_cache.put(filename, doc)
        
        return doc
    
    def preload_common_templates(self):
        """Preload frequently used templates"""
        common_templates = [
            'pelupusan_penjualan.docx',
            'pelupusan_pemusnahan.docx',
            'ames_pedagang.docx',
            'signUpB.docx'
        ]
        
        for template in common_templates:
            try:
                self.get_template_fast(template)
            except:
                pass  # Skip if template doesn't exist
    
    def get_performance_report(self):
        """Get performance statistics"""
        cache_stats = self.document_cache.get_stats()
        
        report = {
            'cache': cache_stats,
            'load_times': {}
        }
        
        if self.load_times:
            avg_load = sum(self.load_times.values()) / len(self.load_times)
            max_load = max(self.load_times.values())
            min_load = min(self.load_times.values())
            
            report['load_times'] = {
                'average': f"{avg_load*1000:.1f} ms",
                'max': f"{max_load*1000:.1f} ms",
                'min': f"{min_load*1000:.1f} ms",
                'count': len(self.load_times)
            }
        
        return report
    
    def clear_cache(self):
        """Clear all caches"""
        self.document_cache.clear()
        self.metadata_cache.clear()
        self.load_times.clear()


# Decorator for performance monitoring
def monitor_performance(func):
    """Decorator to monitor function performance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        
        if elapsed > 1.0:  # Log slow operations
            print(f"Slow operation: {func.__name__} took {elapsed:.2f}s")
        
        return result
    return wrapper


# Batch processing for multiple documents
class BatchProcessor:
    """Process multiple documents efficiently"""
    
    def __init__(self):
        self.template_storage = OptimizedTemplateStorage()
    
    @monitor_performance
    def generate_multiple_documents(self, document_configs):
        """
        Generate multiple documents in batch
        
        Args:
            document_configs: List of {template, replacements, output_path}
        """
        results = []
        
        # Preload unique templates
        unique_templates = set(config['template'] for config in document_configs)
        for template in unique_templates:
            try:
                self.template_storage.get_template_fast(template)
            except:
                pass
        
        # Process each document
        for config in document_configs:
            try:
                doc = self.template_storage.get_template_fast(config['template'])
                
                # Apply replacements
                from docx_helper import replace_in_document
                replace_in_document(doc, config['replacements'])
                
                # Save
                doc.save(config['output_path'])
                results.append({'success': True, 'path': config['output_path']})
                
            except Exception as e:
                results.append({'success': False, 'error': str(e)})
        
        return results


# Global instance
_optimizer = None

def get_optimizer():
    """Get global optimizer instance"""
    global _optimizer
    if _optimizer is None:
        _optimizer = OptimizedTemplateStorage()
    return _optimizer


if __name__ == '__main__':
    # Test performance optimizer
    optimizer = OptimizedTemplateStorage()
    
    print("Preloading common templates...")
    optimizer.preload_common_templates()
    
    print("\nPerformance Report:")
    report = optimizer.get_performance_report()
    print(f"Cache: {report['cache']}")
    if report['load_times']:
        print(f"Load Times: {report['load_times']}")

