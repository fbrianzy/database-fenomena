"""
Error handlers untuk Flask app dengan security protection
File: error_handlers.py
"""
from flask import render_template, request, jsonify
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Suspicious patterns yang mengindikasikan serangan
SUSPICIOUS_PATTERNS = [
    "' OR '1'='1",
    "OR 1=1--",
    "'admin' OR 1=1--",
    "' OR 1=1",
    "admin'--",
    "1' UNION SELECT",
    "<script>",
    "javascript:",
    "../",
    "..\\",
    "SELECT * FROM",
    "DROP TABLE",
    "INSERT INTO",
    "UPDATE SET",
    "DELETE FROM",
    "EXEC(",
    "EXECUTE",
]

def log_suspicious_request(error_type="Unknown"):
    """Log suspicious requests untuk monitoring"""
    try:
        suspicious_indicators = []
        
        # Check URL parameters
        for key, value in request.args.items():
            value_str = str(value).upper()
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern.upper() in value_str:
                    suspicious_indicators.append(f"Query param '{key}': {pattern}")
        
        # Check form data
        if request.form:
            for key, value in request.form.items():
                value_str = str(value).upper()
                for pattern in SUSPICIOUS_PATTERNS:
                    if pattern.upper() in value_str:
                        suspicious_indicators.append(f"Form field '{key}': {pattern}")
        
        # Check JSON body
        if request.is_json:
            try:
                json_data = request.get_json(silent=True)
                if json_data:
                    json_str = str(json_data).upper()
                    for pattern in SUSPICIOUS_PATTERNS:
                        if pattern.upper() in json_str:
                            suspicious_indicators.append(f"JSON body: {pattern}")
            except:
                pass
        
        if suspicious_indicators:
            logger.warning(
                f"SUSPICIOUS REQUEST DETECTED\n"
                f"Error Type: {error_type}\n"
                f"IP: {request.remote_addr}\n"
                f"Method: {request.method}\n"
                f"URL: {request.url}\n"
                f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}\n"
                f"Indicators: {', '.join(suspicious_indicators)}\n"
                f"Timestamp: {datetime.now().isoformat()}"
            )
            return True
        return False
    except Exception as e:
        logger.error(f"Error in log_suspicious_request: {e}")
        return False

def register_error_handlers(app):
    """Register all error handlers to Flask app"""
    
    @app.errorhandler(400)
    def bad_request(e):
        """Handle 400 Bad Request"""
        log_suspicious_request("400 Bad Request")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Bad Request',
                'message': 'Permintaan tidak valid',
                'status': 400
            }), 400
        
        return render_template('errors/400.html', error=e), 400
    
    @app.errorhandler(403)
    def forbidden(e):
        """Handle 403 Forbidden"""
        log_suspicious_request("403 Forbidden")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Forbidden',
                'message': 'Akses ditolak',
                'status': 403
            }), 403
        
        return render_template('errors/403.html', error=e), 403
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 Not Found"""
        # Log jika ada suspicious pattern di URL
        url_str = str(request.url).upper()
        for pattern in SUSPICIOUS_PATTERNS:
            if pattern.upper() in url_str:
                log_suspicious_request("404 Not Found - Suspicious URL")
                break
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Not Found',
                'message': 'Endpoint tidak ditemukan',
                'status': 404
            }), 404
        
        return render_template('errors/404.html', error=e), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        """Handle 405 Method Not Allowed"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Method Not Allowed',
                'message': f'Method {request.method} tidak diizinkan',
                'status': 405
            }), 405
        
        return render_template('errors/405.html', error=e), 405
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 Internal Server Error"""
        logger.error(f"Internal Server Error: {str(e)}", exc_info=True)
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'Terjadi kesalahan server',
                'status': 500
            }), 500
        
        return render_template('errors/500.html', error=e), 500
    
    @app.errorhandler(503)
    def service_unavailable(e):
        """Handle 503 Service Unavailable"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Service Unavailable',
                'message': 'Layanan sedang tidak tersedia',
                'status': 503
            }), 503
        
        return render_template('errors/503.html', error=e), 503
    
    @app.before_request
    def check_suspicious_requests():
        """Check untuk suspicious patterns sebelum request diproses"""
        try:
            # Skip untuk static files
            if request.path.startswith('/static/'):
                return None
            
            # Check query parameters
            for key, value in request.args.items():
                value_str = str(value).upper()
                for pattern in SUSPICIOUS_PATTERNS:
                    if pattern.upper() in value_str:
                        log_suspicious_request("Blocked - Suspicious Query Parameter")
                        return render_template('errors/403.html', 
                            error="Permintaan ditolak: Terdeteksi pola yang mencurigakan"), 403
            
            # Check form data
            if request.form:
                for key, value in request.form.items():
                    value_str = str(value).upper()
                    for pattern in SUSPICIOUS_PATTERNS:
                        if pattern.upper() in value_str:
                            log_suspicious_request("Blocked - Suspicious Form Data")
                            return render_template('errors/403.html',
                                error="Permintaan ditolak: Terdeteksi pola yang mencurigakan"), 403
            
            return None
        except Exception as e:
            logger.error(f"Error in check_suspicious_requests: {e}")
            return None