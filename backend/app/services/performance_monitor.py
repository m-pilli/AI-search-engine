import time
import psutil
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Performance monitoring service for tracking system metrics."""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history = defaultdict(lambda: deque(maxlen=max_history))
        self.lock = threading.Lock()
        
        # Performance thresholds
        self.thresholds = {
            'response_time_ms': 200,
            'cpu_percent': 80,
            'memory_percent': 80,
            'disk_percent': 90
        }
    
    def record_metric(self, metric_name: str, value: float, timestamp: Optional[datetime] = None):
        """Record a performance metric."""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        with self.lock:
            self.metrics_history[metric_name].append({
                'value': value,
                'timestamp': timestamp
            })
    
    def get_metric_history(self, metric_name: str, minutes: int = 60) -> List[Dict]:
        """Get metric history for the last N minutes."""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        
        with self.lock:
            history = list(self.metrics_history[metric_name])
            return [
                point for point in history 
                if point['timestamp'] >= cutoff_time
            ]
    
    def get_current_metrics(self) -> Dict:
        """Get current system metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            
            # Process info
            process = psutil.Process()
            process_memory = process.memory_info()
            
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_used_mb': memory.used / (1024 * 1024),
                'memory_available_mb': memory.available / (1024 * 1024),
                'disk_percent': disk_percent,
                'disk_used_gb': disk.used / (1024 * 1024 * 1024),
                'disk_free_gb': disk.free / (1024 * 1024 * 1024),
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'process_memory_mb': process_memory.rss / (1024 * 1024),
                'process_cpu_percent': process.cpu_percent(),
                'load_average': psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
            }
            
            # Record metrics
            self.record_metric('cpu_percent', cpu_percent)
            self.record_metric('memory_percent', memory_percent)
            self.record_metric('disk_percent', disk_percent)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting current metrics: {e}")
            return {}
    
    def get_performance_summary(self, minutes: int = 60) -> Dict:
        """Get performance summary for the last N minutes."""
        summary = {
            'period_minutes': minutes,
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': {}
        }
        
        for metric_name in ['cpu_percent', 'memory_percent', 'disk_percent', 'response_time_ms']:
            history = self.get_metric_history(metric_name, minutes)
            
            if history:
                values = [point['value'] for point in history]
                summary['metrics'][metric_name] = {
                    'current': values[-1] if values else 0,
                    'average': sum(values) / len(values) if values else 0,
                    'min': min(values) if values else 0,
                    'max': max(values) if values else 0,
                    'count': len(values),
                    'threshold': self.thresholds.get(metric_name, 0),
                    'status': self._get_status(values[-1] if values else 0, metric_name)
                }
        
        return summary
    
    def _get_status(self, value: float, metric_name: str) -> str:
        """Get status based on metric value and threshold."""
        threshold = self.thresholds.get(metric_name, 0)
        
        if value <= threshold * 0.7:
            return 'good'
        elif value <= threshold:
            return 'warning'
        else:
            return 'critical'
    
    def get_alerts(self) -> List[Dict]:
        """Get performance alerts based on thresholds."""
        alerts = []
        current_metrics = self.get_current_metrics()
        
        for metric_name, threshold in self.thresholds.items():
            if metric_name in current_metrics:
                value = current_metrics[metric_name]
                if value > threshold:
                    alerts.append({
                        'metric': metric_name,
                        'value': value,
                        'threshold': threshold,
                        'severity': 'critical',
                        'message': f'{metric_name} is {value:.1f}%, exceeding threshold of {threshold}%',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                elif value > threshold * 0.8:
                    alerts.append({
                        'metric': metric_name,
                        'value': value,
                        'threshold': threshold,
                        'severity': 'warning',
                        'message': f'{metric_name} is {value:.1f}%, approaching threshold of {threshold}%',
                        'timestamp': datetime.utcnow().isoformat()
                    })
        
        return alerts
    
    def record_search_performance(self, query: str, response_time_ms: float, 
                                result_count: int, search_type: str):
        """Record search performance metrics."""
        self.record_metric('response_time_ms', response_time_ms)
        self.record_metric('result_count', result_count)
        
        # Record per-search-type metrics
        self.record_metric(f'response_time_{search_type}', response_time_ms)
        self.record_metric(f'result_count_{search_type}', result_count)
    
    def get_search_performance_stats(self, minutes: int = 60) -> Dict:
        """Get search performance statistics."""
        response_times = self.get_metric_history('response_time_ms', minutes)
        result_counts = self.get_metric_history('result_count', minutes)
        
        if not response_times:
            return {}
        
        rt_values = [point['value'] for point in response_times]
        rc_values = [point['value'] for point in result_counts]
        
        return {
            'period_minutes': minutes,
            'total_searches': len(response_times),
            'response_time': {
                'average': sum(rt_values) / len(rt_values),
                'min': min(rt_values),
                'max': max(rt_values),
                'p95': self._percentile(rt_values, 95),
                'p99': self._percentile(rt_values, 99)
            },
            'result_count': {
                'average': sum(rc_values) / len(rc_values) if rc_values else 0,
                'min': min(rc_values) if rc_values else 0,
                'max': max(rc_values) if rc_values else 0
            },
            'performance_target': {
                'target_response_time_ms': 200,
                'target_throughput_qps': 1000,
                'meeting_target': sum(1 for rt in rt_values if rt <= 200) / len(rt_values) * 100
            }
        }
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of values."""
        if not values:
            return 0
        
        sorted_values = sorted(values)
        index = int((percentile / 100) * len(sorted_values))
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def get_health_status(self) -> Dict:
        """Get overall health status."""
        alerts = self.get_alerts()
        critical_alerts = [a for a in alerts if a['severity'] == 'critical']
        warning_alerts = [a for a in alerts if a['severity'] == 'warning']
        
        if critical_alerts:
            status = 'critical'
        elif warning_alerts:
            status = 'warning'
        else:
            status = 'healthy'
        
        return {
            'status': status,
            'timestamp': datetime.utcnow().isoformat(),
            'critical_alerts': len(critical_alerts),
            'warning_alerts': len(warning_alerts),
            'alerts': alerts
        }
    
    def clear_history(self):
        """Clear all metric history."""
        with self.lock:
            for metric_name in self.metrics_history:
                self.metrics_history[metric_name].clear()
        logger.info("Performance metrics history cleared")
    
    def set_threshold(self, metric_name: str, threshold: float):
        """Set threshold for a metric."""
        self.thresholds[metric_name] = threshold
        logger.info(f"Set threshold for {metric_name}: {threshold}")
    
    def get_thresholds(self) -> Dict:
        """Get all thresholds."""
        return self.thresholds.copy()

