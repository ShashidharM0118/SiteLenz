"""
Flask API Extension for PDF Report Generation
Add these endpoints to your existing Flask app (app.py)
"""

from flask import Flask, request, jsonify, send_file
from datetime import datetime
import os
import json

from pdf_report_generator import InspectionReportGenerator


# Add these endpoints to your existing app.py
# Initialize the report generator
report_generator = InspectionReportGenerator(output_dir="reports")


# Endpoint 1: Generate comprehensive report
@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """
    Generate a comprehensive PDF inspection report
    
    Expected JSON body:
    {
        "defects": [
            {
                "type": "major_crack",
                "confidence": 0.95,
                "location": "North Wall",
                "severity": "high",
                "timestamp": "2025-12-02 14:30:00",
                "image_id": "IMG_001.jpg"
            },
            ...
        ],
        "site_info": {
            "site_name": "Building Name",
            "location": "Address",
            "inspector_name": "Inspector Name",
            "building_type": "Commercial",
            ...
        },
        "voice_transcripts": [
            {
                "timestamp": "2025-12-02 14:30:00",
                "location": "Room 101",
                "duration": "00:00:45",
                "text": "Transcript text here"
            },
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'defects' not in data or 'site_info' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: defects and site_info'
            }), 400
        
        # Extract data
        defects_data = data['defects']
        site_info = data['site_info']
        voice_transcripts = data.get('voice_transcripts', [])
        
        # Validate defects
        if not isinstance(defects_data, list) or len(defects_data) == 0:
            return jsonify({
                'success': False,
                'error': 'Defects must be a non-empty array'
            }), 400
        
        # Generate report
        report_path = report_generator.generate_comprehensive_report(
            defects_data=defects_data,
            site_info=site_info,
            voice_transcripts=voice_transcripts
        )
        
        # Get file info
        file_size = os.path.getsize(report_path)
        filename = os.path.basename(report_path)
        
        return jsonify({
            'success': True,
            'message': 'Report generated successfully',
            'report_path': report_path,
            'filename': filename,
            'file_size_kb': round(file_size / 1024, 2),
            'download_url': f'/api/download-report/{filename}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint 2: Download generated report
@app.route('/api/download-report/<filename>', methods=['GET'])
def download_report(filename):
    """
    Download a generated PDF report
    """
    try:
        report_path = os.path.join('reports', filename)
        
        if not os.path.exists(report_path):
            return jsonify({
                'success': False,
                'error': 'Report not found'
            }), 404
        
        return send_file(
            report_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint 3: List all generated reports
@app.route('/api/reports', methods=['GET'])
def list_reports():
    """
    List all generated PDF reports
    """
    try:
        reports_dir = 'reports'
        if not os.path.exists(reports_dir):
            return jsonify({
                'success': True,
                'reports': []
            }), 200
        
        reports = []
        for filename in os.listdir(reports_dir):
            if filename.endswith('.pdf'):
                filepath = os.path.join(reports_dir, filename)
                file_stat = os.stat(filepath)
                
                reports.append({
                    'filename': filename,
                    'size_kb': round(file_stat.st_size / 1024, 2),
                    'created': datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                    'download_url': f'/api/download-report/{filename}'
                })
        
        # Sort by creation time (newest first)
        reports.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'reports': reports,
            'total_count': len(reports)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint 4: Delete a report
@app.route('/api/delete-report/<filename>', methods=['DELETE'])
def delete_report(filename):
    """
    Delete a generated PDF report
    """
    try:
        report_path = os.path.join('reports', filename)
        
        if not os.path.exists(report_path):
            return jsonify({
                'success': False,
                'error': 'Report not found'
            }), 404
        
        os.remove(report_path)
        
        return jsonify({
            'success': True,
            'message': f'Report {filename} deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint 5: Generate quick report (simplified version)
@app.route('/api/generate-quick-report', methods=['POST'])
def generate_quick_report():
    """
    Generate a quick report with minimal information
    Useful for real-time report generation during inspection
    """
    try:
        data = request.get_json()
        
        # Create minimal site info if not provided
        site_info = data.get('site_info', {})
        if 'site_name' not in site_info:
            site_info['site_name'] = f"Inspection {datetime.now().strftime('%Y-%m-%d')}"
        if 'inspector_name' not in site_info:
            site_info['inspector_name'] = 'Inspector'
        if 'location' not in site_info:
            site_info['location'] = 'N/A'
        
        # Get defects
        defects_data = data.get('defects', [])
        if not defects_data:
            return jsonify({
                'success': False,
                'error': 'No defects provided'
            }), 400
        
        # Generate report
        report_path = report_generator.generate_comprehensive_report(
            defects_data=defects_data,
            site_info=site_info,
            voice_transcripts=data.get('voice_transcripts', [])
        )
        
        filename = os.path.basename(report_path)
        
        return jsonify({
            'success': True,
            'message': 'Quick report generated',
            'filename': filename,
            'download_url': f'/api/download-report/{filename}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


"""
INTEGRATION INSTRUCTIONS:

1. Add these imports to your app.py:
   from pdf_report_generator import InspectionReportGenerator

2. Initialize the generator after creating your Flask app:
   report_generator = InspectionReportGenerator(output_dir="reports")

3. Add the route handlers above to your app.py

4. Install dependencies:
   pip install reportlab

5. Test the API:
   
   # Generate report
   curl -X POST http://localhost:5000/api/generate-report \\
     -H "Content-Type: application/json" \\
     -d '{
       "defects": [{
         "type": "major_crack",
         "confidence": 0.95,
         "location": "North Wall",
         "severity": "high",
         "timestamp": "2025-12-02 14:30:00",
         "image_id": "IMG_001.jpg"
       }],
       "site_info": {
         "site_name": "Test Building",
         "location": "123 Main St",
         "inspector_name": "John Doe"
       }
     }'
   
   # List reports
   curl http://localhost:5000/api/reports
   
   # Download report
   curl http://localhost:5000/api/download-report/inspection_report_20251202_143000.pdf -o report.pdf

6. Mobile App Integration:
   - Call /api/generate-report when user taps "Generate Report"
   - Display list using /api/reports
   - Download using /api/download-report/<filename>
   - Share PDF file with native sharing dialog
"""


# Example client code for mobile app (Flutter/Dart)
"""
// Flutter service method
Future<Map<String, dynamic>> generateReport({
  required List<Map<String, dynamic>> defects,
  required Map<String, dynamic> siteInfo,
  List<Map<String, dynamic>>? voiceTranscripts,
}) async {
  final response = await http.post(
    Uri.parse('$baseUrl/api/generate-report'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'defects': defects,
      'site_info': siteInfo,
      'voice_transcripts': voiceTranscripts ?? [],
    }),
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to generate report');
  }
}

// Download and share report
Future<void> downloadAndShareReport(String filename) async {
  final response = await http.get(
    Uri.parse('$baseUrl/api/download-report/$filename'),
  );
  
  if (response.statusCode == 200) {
    final bytes = response.bodyBytes;
    final dir = await getTemporaryDirectory();
    final file = File('${dir.path}/$filename');
    await file.writeAsBytes(bytes);
    
    // Share the file
    await Share.shareXFiles([XFile(file.path)]);
  }
}
"""
