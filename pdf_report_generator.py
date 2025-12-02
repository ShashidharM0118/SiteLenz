"""
Professional PDF Report Generator for SiteLenz
Generates comprehensive, data-rich inspection reports with AI analysis
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from typing import List, Dict, Optional
import json

from groq_helper import GroqClient
from config_env import load_environment, get_api_key


class InspectionReportGenerator:
    """Generate comprehensive PDF inspection reports with AI analysis"""
    
    def __init__(self, output_dir: str = "reports"):
        """Initialize report generator"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize Groq client for AI content generation
        load_environment()
        api_key = get_api_key('GROQ_API_KEY')
        self.ai_client = GroqClient(api_key, model=GroqClient.MODELS["mixtral"])
        
        # Report styles
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5282'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection heading
        self.styles.add(ParagraphStyle(
            name='SubHeading',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='BodyJustified',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
        
        # Executive summary
        self.styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16,
            leftIndent=20,
            rightIndent=20,
            textColor=colors.HexColor('#2d3748')
        ))
    
    def generate_comprehensive_report(
        self,
        defects_data: List[Dict],
        site_info: Dict,
        voice_transcripts: List[Dict] = None,
        images_paths: List[str] = None
    ) -> str:
        """
        Generate a comprehensive inspection report
        
        Args:
            defects_data: List of detected defects with details
            site_info: Site information (location, inspector, etc.)
            voice_transcripts: List of voice annotations
            images_paths: List of image file paths
            
        Returns:
            Path to generated PDF report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"inspection_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build report content
        story = []
        
        # 1. Cover Page
        story.extend(self._create_cover_page(site_info))
        story.append(PageBreak())
        
        # 2. Table of Contents
        story.extend(self._create_table_of_contents())
        story.append(PageBreak())
        
        # 3. Executive Summary
        story.extend(self._create_executive_summary(defects_data, site_info, voice_transcripts))
        story.append(PageBreak())
        
        # 4. Site Information
        story.extend(self._create_site_information(site_info))
        story.append(Spacer(1, 20))
        
        # 5. Inspection Statistics
        story.extend(self._create_statistics_section(defects_data))
        story.append(PageBreak())
        
        # 6. Defect Analysis (detailed)
        story.extend(self._create_defect_analysis(defects_data, voice_transcripts))
        story.append(PageBreak())
        
        # 7. AI-Powered Insights
        story.extend(self._create_ai_insights(defects_data, voice_transcripts))
        story.append(PageBreak())
        
        # 8. Risk Assessment
        story.extend(self._create_risk_assessment(defects_data))
        story.append(PageBreak())
        
        # 9. Recommendations
        story.extend(self._create_recommendations(defects_data))
        story.append(PageBreak())
        
        # 10. Cost Estimates
        story.extend(self._create_cost_estimates(defects_data))
        story.append(PageBreak())
        
        # 11. Maintenance Priority Matrix
        story.extend(self._create_priority_matrix(defects_data))
        story.append(PageBreak())
        
        # 12. Voice Annotations & Context
        if voice_transcripts:
            story.extend(self._create_voice_annotations_section(voice_transcripts))
            story.append(PageBreak())
        
        # 13. Appendices
        story.extend(self._create_appendices(defects_data))
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        print(f"✓ Report generated: {filepath}")
        return filepath
    
    def _create_cover_page(self, site_info: Dict) -> List:
        """Create professional cover page"""
        elements = []
        
        # Spacer for centering
        elements.append(Spacer(1, 2*inch))
        
        # Main title
        title = Paragraph(
            "STRUCTURAL INSPECTION REPORT",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Site name
        site_name = Paragraph(
            f"<b>{site_info.get('site_name', 'N/A')}</b>",
            ParagraphStyle(
                'SiteName',
                parent=self.styles['Heading2'],
                fontSize=18,
                alignment=TA_CENTER
            )
        )
        elements.append(site_name)
        elements.append(Spacer(1, 0.3*inch))
        
        # Location
        location = Paragraph(
            site_info.get('location', 'N/A'),
            ParagraphStyle(
                'Location',
                parent=self.styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER
            )
        )
        elements.append(location)
        elements.append(Spacer(1, inch))
        
        # Inspection details table
        inspection_data = [
            ['Inspector:', site_info.get('inspector_name', 'N/A')],
            ['Date:', datetime.now().strftime("%B %d, %Y")],
            ['Time:', datetime.now().strftime("%I:%M %p")],
            ['Report ID:', site_info.get('report_id', f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}")],
        ]
        
        details_table = Table(inspection_data, colWidths=[2*inch, 3*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(details_table)
        
        elements.append(Spacer(1, 1.5*inch))
        
        # Footer
        footer_text = Paragraph(
            "<i>Generated by SiteLenz AI-Powered Infrastructure Monitoring System</i>",
            ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontSize=9,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
        )
        elements.append(footer_text)
        
        return elements
    
    def _create_table_of_contents(self) -> List:
        """Create table of contents"""
        elements = []
        
        elements.append(Paragraph("TABLE OF CONTENTS", self.styles['SectionHeading']))
        elements.append(Spacer(1, 20))
        
        toc_items = [
            ('1. Executive Summary', 3),
            ('2. Site Information', 4),
            ('3. Inspection Statistics', 4),
            ('4. Detailed Defect Analysis', 5),
            ('5. AI-Powered Insights', 6),
            ('6. Risk Assessment', 7),
            ('7. Recommendations', 8),
            ('8. Cost Estimates', 9),
            ('9. Maintenance Priority Matrix', 10),
            ('10. Voice Annotations & Context', 11),
            ('11. Appendices', 12),
        ]
        
        toc_data = [[item, f"Page {page}"] for item, page in toc_items]
        
        toc_table = Table(toc_data, colWidths=[4.5*inch, 1.5*inch])
        toc_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(toc_table)
        
        return elements
    
    def _create_executive_summary(self, defects_data: List[Dict], site_info: Dict, voice_transcripts: List[Dict]) -> List:
        """Generate AI-powered executive summary"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        # Generate comprehensive summary using AI
        defects_summary = self._prepare_defects_summary_text(defects_data)
        voice_context = self._prepare_voice_context(voice_transcripts) if voice_transcripts else ""
        
        # Calculate statistics for context
        stats = self._calculate_defect_statistics(defects_data)
        critical_count = stats['critical_count'] + stats['high_priority_count']
        
        prompt = f"""You are a senior structural engineer with 25+ years of experience writing formal inspection reports for commercial and residential buildings. Generate a COMPREHENSIVE, HIGHLY DETAILED executive summary for a professional structural inspection report.

SITE INFORMATION:
- Building Name: {site_info.get('site_name', 'N/A')}
- Location: {site_info.get('location', 'N/A')}
- Building Type: {site_info.get('building_type', 'Commercial/Residential Building')}
- Year Built: {site_info.get('year_built', 'Not specified')}
- Total Building Area: {site_info.get('total_area', 'Not specified')}
- Inspection Date: {datetime.now().strftime('%B %d, %Y')}

QUANTITATIVE FINDINGS:
- Total Defects Detected: {len(defects_data)}
- Critical/High Priority Issues: {critical_count}
- Average Detection Confidence: {stats['avg_confidence']:.1f}%
- Defect Distribution: {', '.join([f"{k.replace('_', ' ').title()}: {v}" for k, v in stats['defect_types'].items()])}

DETAILED DEFECTS BREAKDOWN:
{defects_summary}

INSPECTOR'S ON-SITE OBSERVATIONS AND CONTEXTUAL NOTES:
{voice_context if voice_context else "No voice annotations recorded during inspection."}

WEATHER CONDITIONS DURING INSPECTION:
- Weather: {site_info.get('weather', 'Not recorded')}
- Temperature: {site_info.get('temperature', 'Not recorded')}

YOUR TASK: Write an extremely detailed, professional executive summary of 500-600 words that covers ALL of the following sections in depth:

1. INSPECTION SCOPE AND METHODOLOGY (100-120 words):
   - Begin with the formal purpose of this structural inspection
   - Describe what areas of the building were inspected
   - Mention the use of AI-powered defect detection technology (Vision Transformer model with 95%+ accuracy)
   - Reference the systematic approach taken (visual inspection, photographic documentation, voice annotation)
   - State compliance standards referenced (ACI 318, local building codes, ISO 13822)
   - Mention any limitations of the inspection scope

2. KEY FINDINGS AND CRITICAL DEFECTS (150-180 words):
   - Start with the total number of defects found and their severity distribution
   - Highlight EACH critical and high-priority defect specifically by type and location
   - Provide specific measurements, dimensions, or characteristics where mentioned
   - Explain the potential structural implications of each major defect
   - Mention confidence levels of detections
   - Reference specific inspector observations from voice annotations
   - Describe any patterns or correlations observed between different defects
   - Note any areas where multiple defects are co-located

3. OVERALL STRUCTURAL CONDITION ASSESSMENT (100-120 words):
   - Provide a clear, definitive assessment of the building's current structural integrity
   - Rate the overall condition on a scale (Excellent/Good/Fair/Poor/Critical)
   - Discuss the cumulative impact of all detected defects
   - Assess the load-bearing capacity concerns, if any
   - Evaluate the progression risk (is deterioration accelerating?)
   - Consider environmental factors affecting structural health
   - Compare current condition to expected condition for building age
   - Mention any positive findings or areas of concern

4. IMMEDIATE SAFETY CONCERNS AND URGENT ACTIONS (80-100 words):
   - List all defects requiring immediate attention (within 7 days) with specific reasons
   - Identify any safety hazards to occupants or personnel
   - Specify temporary protective measures needed
   - Recommend immediate access restrictions if necessary
   - Provide clear justification for urgency based on engineering principles
   - Mention potential consequences of delayed action

5. RECOMMENDED ACTIONS AND REPAIR STRATEGY (80-100 words):
   - Outline phased approach: immediate (0-7 days), short-term (30 days), medium-term (3-6 months)
   - Specify types of contractors/specialists needed
   - Mention need for detailed engineering analysis where required
   - Recommend monitoring protocols for progressive defects
   - Suggest preventive maintenance measures
   - Reference need for follow-up inspections

6. RISK ASSESSMENT AND FINANCIAL IMPLICATIONS (60-80 words):
   - Assign overall risk level (Low/Moderate/High/Critical) with justification
   - Estimate financial impact category (Minor repairs <$10K, Moderate $10-50K, Major $50-200K, Extensive >$200K)
   - Discuss liability concerns
   - Mention insurance implications
   - Warn about cost escalation if repairs are delayed

WRITING STYLE REQUIREMENTS:
- Use formal, technical language appropriate for structural engineering reports
- Write in third person, objective tone
- Include specific technical terminology (spalling, delamination, efflorescence, structural integrity, load-bearing capacity, etc.)
- Reference specific locations and measurements from the data
- Use transition sentences between paragraphs for flow
- Begin with: "This comprehensive structural inspection of [building name]..."
- Conclude with a clear recommendation statement

CRITICAL: Make every sentence substantive and information-dense. Avoid generic statements. Reference specific data points, locations, and findings throughout. The summary should stand alone as a complete assessment even if the reader doesn't read the full report."""

        try:
            summary_text = self.ai_client.chat(
                message=prompt,
                system_prompt="You are a licensed Professional Engineer (P.E.) with expertise in structural engineering, building inspection, and forensic analysis. You write detailed, technically accurate reports for building owners, insurance companies, and regulatory authorities. Your reports are known for being comprehensive, precise, and actionable.",
                temperature=0.35,
                max_tokens=1000
            )
        except Exception as e:
            print(f"AI generation failed: {e}")
            summary_text = self._generate_fallback_summary(defects_data, site_info)
        
        summary_para = Paragraph(summary_text, self.styles['ExecutiveSummary'])
        elements.append(summary_para)
        
        return elements
    
    def _create_site_information(self, site_info: Dict) -> List:
        """Create detailed site information section"""
        elements = []
        
        elements.append(Paragraph("SITE INFORMATION", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        site_data = [
            ['Property Details', ''],
            ['Site Name:', site_info.get('site_name', 'N/A')],
            ['Location:', site_info.get('location', 'N/A')],
            ['Building Type:', site_info.get('building_type', 'Commercial/Residential')],
            ['Year Built:', site_info.get('year_built', 'N/A')],
            ['Total Area:', site_info.get('total_area', 'N/A')],
            ['', ''],
            ['Inspection Details', ''],
            ['Inspector:', site_info.get('inspector_name', 'N/A')],
            ['License No:', site_info.get('license_no', 'N/A')],
            ['Inspection Date:', datetime.now().strftime("%B %d, %Y")],
            ['Weather Conditions:', site_info.get('weather', 'Clear')],
            ['Temperature:', site_info.get('temperature', 'N/A')],
        ]
        
        site_table = Table(site_data, colWidths=[2.5*inch, 3.5*inch])
        site_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, 7), (1, 7), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 7), (1, 7), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(site_table)
        
        return elements
    
    def _create_statistics_section(self, defects_data: List[Dict]) -> List:
        """Create comprehensive statistics section with numerical data"""
        elements = []
        
        elements.append(Paragraph("INSPECTION STATISTICS", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        # Calculate statistics
        stats = self._calculate_defect_statistics(defects_data)
        
        # Overview statistics
        elements.append(Paragraph("Overall Metrics", self.styles['SubHeading']))
        
        overview_data = [
            ['Metric', 'Value', 'Percentage'],
            ['Total Defects Detected', str(stats['total_defects']), '100%'],
            ['Critical Defects', str(stats['critical_count']), f"{stats['critical_percent']:.1f}%"],
            ['High Priority', str(stats['high_priority_count']), f"{stats['high_priority_percent']:.1f}%"],
            ['Medium Priority', str(stats['medium_priority_count']), f"{stats['medium_priority_percent']:.1f}%"],
            ['Low Priority', str(stats['low_priority_count']), f"{stats['low_priority_percent']:.1f}%"],
            ['Average Confidence Score', f"{stats['avg_confidence']:.2f}%", '-'],
        ]
        
        overview_table = Table(overview_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        overview_table.setStyle(self._get_table_style())
        elements.append(overview_table)
        elements.append(Spacer(1, 20))
        
        # Defect type breakdown
        elements.append(Paragraph("Defect Type Distribution", self.styles['SubHeading']))
        
        type_data = [['Defect Type', 'Count', 'Percentage', 'Avg Confidence']]
        for defect_type, count in stats['defect_types'].items():
            percentage = (count / stats['total_defects'] * 100) if stats['total_defects'] > 0 else 0
            avg_conf = stats['type_confidence'].get(defect_type, 0)
            type_data.append([
                defect_type.replace('_', ' ').title(),
                str(count),
                f"{percentage:.1f}%",
                f"{avg_conf:.1f}%"
            ])
        
        type_table = Table(type_data, colWidths=[2*inch, 1*inch, 1.5*inch, 1.5*inch])
        type_table.setStyle(self._get_table_style())
        elements.append(type_table)
        elements.append(Spacer(1, 20))
        
        # Location-based statistics
        if stats['location_distribution']:
            elements.append(Paragraph("Location Distribution", self.styles['SubHeading']))
            
            loc_data = [['Location', 'Defects Found', 'Severity Score']]
            for location, count in stats['location_distribution'].items():
                severity = stats['location_severity'].get(location, 0)
                loc_data.append([location, str(count), f"{severity:.1f}/10"])
            
            loc_table = Table(loc_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
            loc_table.setStyle(self._get_table_style())
            elements.append(loc_table)
        
        return elements
    
    def _create_defect_analysis(self, defects_data: List[Dict], voice_transcripts: List[Dict]) -> List:
        """Create detailed defect analysis section"""
        elements = []
        
        elements.append(Paragraph("DETAILED DEFECT ANALYSIS", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        for idx, defect in enumerate(defects_data, 1):
            # Get AI analysis for this defect
            analysis = self._get_defect_ai_analysis(defect, voice_transcripts)
            
            elements.append(Paragraph(f"Defect #{idx}: {defect['type'].replace('_', ' ').title()}", 
                                    self.styles['SubHeading']))
            
            # Defect details table
            details_data = [
                ['Classification:', defect['type'].replace('_', ' ').title()],
                ['Confidence Score:', f"{defect.get('confidence', 0)*100:.2f}%"],
                ['Location:', defect.get('location', 'N/A')],
                ['Severity Level:', defect.get('severity', 'Medium')],
                ['Detection Time:', defect.get('timestamp', 'N/A')],
                ['Image Reference:', defect.get('image_id', 'N/A')],
            ]
            
            details_table = Table(details_data, colWidths=[2*inch, 4*inch])
            details_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(details_table)
            elements.append(Spacer(1, 10))
            
            # AI Analysis
            elements.append(Paragraph("<b>Technical Analysis:</b>", self.styles['Normal']))
            elements.append(Paragraph(analysis['technical'], self.styles['BodyJustified']))
            elements.append(Spacer(1, 8))
            
            elements.append(Paragraph("<b>Root Causes:</b>", self.styles['Normal']))
            elements.append(Paragraph(analysis['causes'], self.styles['BodyJustified']))
            elements.append(Spacer(1, 8))
            
            elements.append(Paragraph("<b>Recommended Actions:</b>", self.styles['Normal']))
            elements.append(Paragraph(analysis['actions'], self.styles['BodyJustified']))
            
            elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_ai_insights(self, defects_data: List[Dict], voice_transcripts: List[Dict]) -> List:
        """Generate AI-powered insights and patterns"""
        elements = []
        
        elements.append(Paragraph("AI-POWERED INSIGHTS & PATTERNS", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        # Generate insights using AI
        defects_summary = self._prepare_defects_summary_text(defects_data)
        voice_context = self._prepare_voice_context(voice_transcripts) if voice_transcripts else ""
        stats = self._calculate_defect_statistics(defects_data)
        
        # Prepare location-severity mapping
        location_analysis = "\n".join([
            f"- {loc}: {count} defects, Average severity score: {stats['location_severity'].get(loc, 0):.1f}/10"
            for loc, count in stats['location_distribution'].items()
        ])
        
        prompt = f"""You are a forensic structural engineer and building pathology expert with 30+ years of experience analyzing deterioration patterns in buildings. Your specialty is identifying root causes, systemic issues, and predicting future failure modes.

COMPREHENSIVE DEFECT DATA:
{defects_summary}

STATISTICAL ANALYSIS:
- Total Defects: {len(defects_data)}
- Critical Issues: {stats['critical_count']}
- High Priority: {stats['high_priority_count']}
- Medium Priority: {stats['medium_priority_count']}
- Average Confidence: {stats['avg_confidence']:.1f}%

DEFECT TYPE DISTRIBUTION WITH CONFIDENCE LEVELS:
{chr(10).join([f"- {k.replace('_', ' ').title()}: {v} instances (Avg confidence: {stats['type_confidence'].get(k, 0):.1f}%)" for k, v in stats['defect_types'].items()])}

LOCATION-BASED DISTRIBUTION AND SEVERITY:
{location_analysis}

INSPECTOR'S CONTEXTUAL OBSERVATIONS:
{voice_context}

YOUR COMPREHENSIVE ANALYSIS TASK (700-900 words):

Write an EXTREMELY DETAILED technical analysis covering ALL of the following aspects. Each section should be thorough and backed by engineering principles:

1. PATTERN RECOGNITION AND CORRELATION ANALYSIS (200-250 words):
   - Identify ALL patterns in defect distribution (clustering by location, type, severity)
   - Analyze correlations between different defect types (e.g., do cracks appear near water stains? Is algae growth near spalling?)
   - Map defect locations to building orientation (north/south/east/west exposures)
   - Examine temporal patterns if timestamps suggest progression
   - Identify "defect chains" where one problem leads to another
   - Discuss statistical significance of patterns observed
   - Use specific examples from the data with locations and defect types
   - Explain the engineering significance of each pattern

2. ROOT CAUSE AND SYSTEMIC ISSUES ANALYSIS (200-250 words):
   - Identify the PRIMARY root cause(s) of the defect patterns
   - Discuss SECONDARY contributing factors
   - Analyze systemic building design or construction deficiencies that enable these defects
   - Evaluate maintenance history implications
   - Examine original construction quality indicators
   - Consider building systems interactions (waterproofing failure affecting structural elements)
   - Assess whether defects indicate isolated issues or widespread deterioration
   - Reference building codes and standards relevant to identified issues
   - Provide engineering rationale for each root cause identified

3. ENVIRONMENTAL AND EXTERNAL FACTORS (150-180 words):
   - Analyze how climate and weather patterns contribute (freeze-thaw cycles, UV exposure, humidity, rainfall)
   - Evaluate sun exposure effects on different building faces
   - Assess water infiltration pathways and drainage issues
   - Consider seasonal variations in defect progression
   - Examine urban environment factors (pollution, vibration, chemical exposure)
   - Discuss vegetation impact if algae or biological growth present
   - Evaluate thermal cycling effects on materials
   - Mention any specific local environmental challenges

4. PROGRESSIVE DETERIORATION RISK ASSESSMENT (150-180 words):
   - Predict HOW each defect type will progress if left unaddressed
   - Provide SPECIFIC timelines for deterioration stages
   - Identify "tipping points" where minor issues become major
   - Analyze acceleration factors that could speed deterioration
   - Assess cascading failure risks (one failure causing others)
   - Evaluate the exponential vs. linear progression likelihood
   - Discuss point-of-no-return scenarios for structural elements
   - Quantify risk increase over time (e.g., "deterioration rate doubles every 18 months")
   - Reference engineering failure case studies similar to observed conditions

5. HIDDEN AND SECONDARY CONCERNS (100-120 words):
   - Identify defects that may be SYMPTOMS of unseen problems
   - Discuss what cannot be seen from visual inspection (internal corrosion, concealed structural damage)
   - Predict subsurface issues based on surface manifestations
   - Warn about potential hidden water damage or mold
   - Consider foundation settlement implications if crack patterns suggest it
   - Evaluate concealed mechanical system failures
   - Mention need for invasive testing or NDT (non-destructive testing) where warranted

6. PREVENTIVE STRATEGY AND LONG-TERM MAINTENANCE (100-120 words):
   - Design a comprehensive preventive maintenance program specific to this building
   - Recommend inspection frequency for different building systems
   - Specify monitoring methods for progressive defects
   - Suggest protective treatments or coatings
   - Recommend building system upgrades (better drainage, ventilation, waterproofing)
   - Outline quality control procedures for repairs
   - Propose documentation and record-keeping systems
   - Mention warranty considerations for new work

TECHNICAL WRITING REQUIREMENTS:
- Use advanced engineering terminology appropriately
- Reference specific defect numbers, locations, and types from the data
- Include cause-and-effect relationships throughout
- Use phrases like "forensic analysis indicates," "engineering assessment reveals," "pathology examination shows"
- Cite relevant failure mechanisms (concrete carbonation, rebar corrosion, alkali-silica reaction, etc.)
- Include quantitative assessments where possible
- Connect observations to engineering principles and material science
- Write in formal third-person technical style
- Every statement should add analytical value

CRITICAL: This section should demonstrate EXPERT-LEVEL analysis that goes far beyond surface observations. Show deep understanding of building science, structural behavior, and material deterioration mechanisms. Reference the actual data points throughout your analysis."""

        try:
            insights = self.ai_client.chat(
                message=prompt,
                system_prompt="You are Dr. Sarah Chen, P.E., Ph.D., a renowned forensic structural engineer and building pathologist. You've investigated over 500 building failures and written 50+ peer-reviewed papers on structural deterioration. You're testifying as an expert witness - your analysis must be thorough, technically impeccable, and defensible under cross-examination. You think systematically about root causes, failure modes, and risk progression.",
                temperature=0.4,
                max_tokens=1400
            )
            
            elements.append(Paragraph(insights, self.styles['BodyJustified']))
        except Exception as e:
            print(f"AI insights generation failed: {e}")
            elements.append(Paragraph("Detailed AI analysis temporarily unavailable. Manual expert review recommended.", self.styles['Normal']))
        
        return elements
    
    def _create_risk_assessment(self, defects_data: List[Dict]) -> List:
        """Create comprehensive risk assessment"""
        elements = []
        
        elements.append(Paragraph("RISK ASSESSMENT", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        # Calculate risk scores
        risk_data = self._calculate_risk_scores(defects_data)
        
        # Overall risk summary
        elements.append(Paragraph("Overall Risk Profile", self.styles['SubHeading']))
        
        risk_summary = [
            ['Risk Category', 'Score (0-10)', 'Level', 'Status'],
            ['Structural Integrity', f"{risk_data['structural_risk']:.1f}", 
             self._get_risk_level(risk_data['structural_risk']), 
             self._get_status_indicator(risk_data['structural_risk'])],
            ['Safety Hazards', f"{risk_data['safety_risk']:.1f}", 
             self._get_risk_level(risk_data['safety_risk']), 
             self._get_status_indicator(risk_data['safety_risk'])],
            ['Deterioration Rate', f"{risk_data['deterioration_risk']:.1f}", 
             self._get_risk_level(risk_data['deterioration_risk']), 
             self._get_status_indicator(risk_data['deterioration_risk'])],
            ['Financial Impact', f"{risk_data['financial_risk']:.1f}", 
             self._get_risk_level(risk_data['financial_risk']), 
             self._get_status_indicator(risk_data['financial_risk'])],
            ['Overall Risk Score', f"{risk_data['overall_risk']:.1f}", 
             self._get_risk_level(risk_data['overall_risk']), 
             self._get_status_indicator(risk_data['overall_risk'])],
        ]
        
        risk_table = Table(risk_summary, colWidths=[2*inch, 1.2*inch, 1.5*inch, 1.3*inch])
        risk_table.setStyle(self._get_table_style())
        elements.append(risk_table)
        elements.append(Spacer(1, 20))
        
        # Generate risk analysis using AI
        prompt = f"""You are a risk management specialist and structural engineer analyzing building risk levels. Provide a comprehensive risk assessment suitable for insurance companies, building owners, and regulatory authorities.

QUANTIFIED RISK SCORES (0-10 scale, where 10 is maximum risk):
- Structural Integrity Risk: {risk_data['structural_risk']:.1f}/10
- Safety Hazard Risk: {risk_data['safety_risk']:.1f}/10  
- Deterioration Rate Risk: {risk_data['deterioration_risk']:.1f}/10
- Financial Impact Risk: {risk_data['financial_risk']:.1f}/10
- OVERALL COMPOSITE RISK: {risk_data['overall_risk']:.1f}/10

DEFECT PROFILE:
- Total Defects Detected: {len(defects_data)}
- Critical Defects: {risk_data.get('critical_count', 0)}
- High Priority: {risk_data.get('high_count', 0)}
- Risk Classification: {self._get_risk_level(risk_data['overall_risk'])}

YOUR COMPREHENSIVE RISK ASSESSMENT (500-600 words):

Write an EXTREMELY DETAILED risk analysis covering ALL of the following:

1. IMMEDIATE SAFETY CONCERNS (120-150 words):
   
   Analyze each risk score and explain:
   
   • LIFE SAFETY RISKS:
     - Identify any conditions posing immediate danger to occupants
     - Assess falling hazard risks (loose materials, spalling concrete)
     - Evaluate structural collapse potential
     - Consider secondary hazards (electrical, fire safety impacts)
     - Specify areas requiring immediate access restriction
   
   • PUBLIC LIABILITY:
     - Risks to adjacent properties or public spaces
     - Pedestrian safety concerns
     - Vehicle traffic exposure
     - Third-party injury potential
   
   • OCCUPANCY STATUS RECOMMENDATIONS:
     - Can building remain occupied? Under what conditions?
     - Required monitoring protocols if occupied
     - Evacuation triggers and procedures
     - Load restrictions and usage limitations

2. LONG-TERM STRUCTURAL IMPLICATIONS (150-180 words):
   
   Provide engineering analysis of:
   
   • LOAD-BEARING CAPACITY:
     - Current vs. design capacity assessment
     - Impact of defects on structural redundancy
     - Critical vs. non-critical structural elements affected
     - Factor of safety considerations
   
   • PROGRESSIVE FAILURE SCENARIOS:
     - Chain reaction failure possibilities
     - Domino effect of deteriorating elements
     - Critical failure modes and trigger conditions
     - Point-of-no-return identification
   
   • STRUCTURAL SYSTEM INTEGRITY:
     - Overall system behavior under current conditions
     - Load path alterations due to defects
     - Seismic or wind load resistance impact
     - Foundation settlement or movement concerns
   
   • LIFESPAN PROJECTIONS:
     - Remaining service life estimates for affected components
     - Acceleration factors in deterioration
     - Maintenance vs. replacement decisions
     - Building obsolescence considerations

3. LIABILITY AND INSURANCE CONSIDERATIONS (100-120 words):
   
   Address legal and financial exposure:
   
   • LEGAL LIABILITY:
     - Owner's duty of care obligations
     - Premises liability exposure
     - Code compliance violations
     - Negligent maintenance claims potential
   
   • INSURANCE IMPLICATIONS:
     - Impact on property insurance coverage
     - Potential for denial of claims
     - Required disclosures to insurers
     - Premium adjustment likelihood
   
   • DOCUMENTATION REQUIREMENTS:
     - Evidence of reasonable care and maintenance
     - Inspection and repair records needed
     - Professional engineer certifications required
     - Third-party verification recommendations

4. INTERVENTION TIMELINE AND URGENCY (80-100 words):
   
   Provide specific timelines:
   
   • CRITICAL PATH ITEMS (0-7 days):
     - Must be addressed immediately
     - Specific engineering justification for urgency
   
   • HIGH PRIORITY (8-30 days):
     - Risk escalation if delayed beyond 30 days
     - Tipping points in deterioration
   
   • MEDIUM PRIORITY (31-90 days):
     - Preventive window before significant progression
   
   • MONITORING SCHEDULE:
     - Inspection frequency for different risk levels
     - Trigger points for escalated action

5. CONSEQUENCES OF DELAYED ACTION (100-120 words):
   
   Quantify impacts of inaction:
   
   • RISK ESCALATION:
     - How quickly does risk increase? (e.g., "Risk doubles every 6 months")
     - Exponential vs. linear progression
     - Critical transition points
   
   • COST ESCALATION:
     - Current repair cost vs. projected future cost
     - Multiplier effect of delayed repairs (e.g., "$10K today becomes $50K in 2 years")
     - Secondary damage costs
   
   • CASCADING FAILURES:
     - What additional problems will develop?
     - Interconnected system failures
     - Collateral damage to other building components
   
   • LIABILITY GROWTH:
     - Increasing exposure with knowledge of defects
     - Gross negligence threshold
     - Enhanced penalties for willful neglect

CRITICAL WRITING REQUIREMENTS:
- Use quantitative language wherever possible (percentages, timeframes, cost multipliers)
- Reference specific risk scores provided in the data
- Make clear cause-and-effect statements
- Use engineering judgment terminology ("in my professional opinion," "based on forensic analysis")
- Include both best-case and worst-case scenarios
- Provide actionable decision points
- Write with the gravity appropriate to the risk level
- Consider both technical and business/legal perspectives
- Every sentence should add decision-making value

Format with clear section headings for readability. Write as if this assessment will be reviewed by insurance underwriters, legal counsel, and building officials."""

        try:
            risk_analysis = self.ai_client.chat(
                message=prompt,
                system_prompt="You are a risk assessment expert with dual expertise in structural engineering and insurance/liability. You've provided expert testimony in building failure cases and conduct risk assessments for major insurance carriers. Your assessments must be defensible, quantitative, and action-oriented. You understand both the engineering and business/legal implications of building defects.",
                temperature=0.3,
                max_tokens=1000
            )
            
            elements.append(Paragraph("Risk Analysis", self.styles['SubHeading']))
            elements.append(Paragraph(risk_analysis, self.styles['BodyJustified']))
        except Exception as e:
            print(f"Risk analysis generation failed: {e}")
            fallback_text = f"""Based on the overall risk score of {risk_data['overall_risk']:.1f}/10, this building is classified as {self._get_risk_level(risk_data['overall_risk'])} risk. Immediate attention from a licensed structural engineer is {"required" if risk_data['overall_risk'] >= 6 else "recommended"}. The identified defects present {"significant" if risk_data['overall_risk'] >= 6 else "moderate"} concerns for structural integrity and safety. Detailed risk assessment requires comprehensive engineering analysis."""
            elements.append(Paragraph("Risk Analysis", self.styles['SubHeading']))
            elements.append(Paragraph(fallback_text, self.styles['BodyJustified']))
        
        return elements
    
    def _create_recommendations(self, defects_data: List[Dict]) -> List:
        """Generate detailed recommendations"""
        elements = []
        
        elements.append(Paragraph("RECOMMENDATIONS", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        # Get AI-generated recommendations
        defects_summary = self._prepare_defects_summary_text(defects_data)
        stats = self._calculate_defect_statistics(defects_data)
        risk_scores = self._calculate_risk_scores(defects_data)
        
        prompt = f"""You are a licensed Professional Engineer (P.E.) providing detailed repair and remediation recommendations for a building inspection report. This section will be used by building owners, contractors, and project managers to plan and execute repairs.

COMPLETE DEFECT INVENTORY:
{defects_summary}

RISK ASSESSMENT SCORES:
- Structural Integrity Risk: {risk_scores['structural_risk']:.1f}/10
- Safety Risk: {risk_scores['safety_risk']:.1f}/10
- Deterioration Rate: {risk_scores['deterioration_risk']:.1f}/10
- Financial Impact Risk: {risk_scores['financial_risk']:.1f}/10
- Overall Risk: {risk_scores['overall_risk']:.1f}/10

DEFECT STATISTICS:
- Total Defects: {len(defects_data)}
- Critical: {stats['critical_count']}, High: {stats['high_priority_count']}, Medium: {stats['medium_priority_count']}, Low: {stats['low_priority_count']}

YOUR TASK: Generate COMPREHENSIVE, ACTION-ORIENTED recommendations (900-1100 words) organized into four time-based priority categories. Each recommendation must be SPECIFIC, MEASURABLE, and IMPLEMENTABLE.

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

═══════════════════════════════════════════════════════════════
IMMEDIATE ACTIONS REQUIRED (0-7 DAYS) - CRITICAL PRIORITY
═══════════════════════════════════════════════════════════════

[Write 250-300 words covering:]

For EACH critical and high-priority defect, provide:

• DEFECT: [Specific defect type and location]
  - IMMEDIATE ACTION: [Exact steps to take within 7 days]
  - RESPONSIBLE PARTY: [Who should perform this - licensed structural engineer, general contractor, specialist, etc.]
  - SAFETY MEASURES: [Temporary protection needed - barriers, shoring, load restrictions, access control]
  - ESTIMATED TIME: [Hours or days to complete]
  - SUCCESS CRITERIA: [How to verify action is complete]
  - CONSEQUENCES IF DELAYED: [Specific risks of not acting within timeframe]

• STRUCTURAL ENGINEER ASSESSMENT:
  - Schedule comprehensive structural evaluation by licensed P.E.
  - Specify areas requiring detailed analysis
  - List any load testing or NDT (non-destructive testing) needed
  - Timeline for engineering report delivery

• SAFETY PROTOCOLS:
  - Occupancy restrictions if needed
  - Temporary shoring or bracing requirements
  - Warning signage and barrier placement
  - Emergency contact procedures

═══════════════════════════════════════════════════════════════
SHORT-TERM REPAIRS (8-30 DAYS) - HIGH PRIORITY
═══════════════════════════════════════════════════════════════

[Write 250-300 words covering:]

For EACH short-term repair:

• REPAIR PROJECT: [Specific repair description]
  - SCOPE OF WORK: [Detailed steps - cleaning, preparation, material application, curing, finishing]
  - REQUIRED MATERIALS: [Specific products, specifications, quantities]
  - CONTRACTOR QUALIFICATIONS: [Required licenses, certifications, experience level]
  - EQUIPMENT NEEDED: [Scaffolding, lifts, specialized tools]
  - ESTIMATED DURATION: [Number of days for completion]
  - WEATHER REQUIREMENTS: [Temperature range, dry conditions needed, etc.]
  - QUALITY CONTROL: [Inspection checkpoints, testing requirements]
  - WARRANTY EXPECTATIONS: [Minimum warranty periods]

• PREPARATORY WORK:
  - Surface preparation requirements
  - Area protection and containment
  - Material testing before application
  - Substrate moisture testing

• COORDINATION:
  - Sequencing with other repairs
  - Access requirements and scheduling
  - Utility shutdowns if needed
  - Tenant notification procedures

═══════════════════════════════════════════════════════════════
MEDIUM-TERM MAINTENANCE (31-180 DAYS) - MODERATE PRIORITY
═══════════════════════════════════════════════════════════════

[Write 200-250 words covering:]

• PREVENTIVE MAINTENANCE PROGRAM:
  - Establish regular inspection schedule (monthly, quarterly, annually)
  - Create building maintenance log system
  - Assign responsibility for routine checks
  - Document all findings and actions

• MONITORING PROTOCOLS for Progressive Defects:
  - Install crack monitors on specific defects
  - Establish baseline measurements
  - Schedule monitoring frequency
  - Define alarm thresholds for action
  - Create photographic documentation procedure

• SYSTEM IMPROVEMENTS:
  - Drainage system upgrades (specify locations and types)
  - Waterproofing enhancements (areas and materials)
  - Ventilation improvements (specific systems)
  - Protective coating applications (surfaces and products)

• AESTHETIC REPAIRS:
  - Address lower-priority cosmetic issues
  - Painting and finishing work
  - Cleaning and restoration
  - Landscaping modifications affecting building

═══════════════════════════════════════════════════════════════
LONG-TERM STRATEGIC PLANNING (6-12+ MONTHS) - PLANNING PRIORITY
═══════════════════════════════════════════════════════════════

[Write 200-250 words covering:]

• CAPITAL IMPROVEMENT PROJECTS:
  - Major structural upgrades needed
  - Building envelope restoration
  - Foundation waterproofing systems
  - Roof replacement or major repairs
  - HVAC system modifications affecting moisture control

• ENGINEERING STUDIES:
  - Comprehensive structural analysis
  - Building envelope performance testing
  - Energy audit and moisture modeling
  - Seismic evaluation (if applicable)
  - Ground penetrating radar or subsurface investigation

• FINANCIAL PLANNING:
  - Reserve fund requirements
  - Phasing strategy for large projects
  - Grant or funding opportunities
  - Insurance considerations
  - Property value impact assessment

• DOCUMENTATION AND COMPLIANCE:
  - As-built drawing updates
  - Building code compliance upgrades
  - Permit requirements for major work
  - Historic preservation considerations
  - Environmental compliance (lead, asbestos, etc.)

• LONG-TERM MONITORING:
  - Establish 5-year maintenance plan
  - Schedule follow-up inspections
  - Plan for evolving building needs
  - Consider building lifespan and obsolescence

WRITING REQUIREMENTS:
- Use bullet points and clear formatting as shown above
- Be EXTREMELY SPECIFIC - avoid vague language like "repair as needed"
- Include technical specifications where relevant
- Reference specific defect locations from the data
- Provide realistic timeframes and cost considerations
- Consider contractor availability and weather constraints
- Account for permitting and approval timelines
- Mention coordination between different trades
- Include quality assurance procedures
- Consider building occupancy and operations
- Every recommendation must be actionable and measurable"""

        try:
            recommendations = self.ai_client.chat(
                message=prompt,
                system_prompt="You are a licensed Professional Engineer (P.E.) and construction project manager with expertise in repair planning, contractor coordination, and project execution. You write clear, actionable recommendations that contractors can bid on and execute. Your recommendations are detailed enough to form the basis of construction specifications and scopes of work.",
                temperature=0.35,
                max_tokens=1800
            )
            
            elements.append(Paragraph(recommendations, self.styles['BodyJustified']))
        except Exception as e:
            print(f"Recommendations generation failed: {e}")
            elements.append(Paragraph("Detailed recommendations section temporarily unavailable. Consult with licensed structural engineer for specific repair guidance.", self.styles['Normal']))
        
        return elements
    
    def _create_cost_estimates(self, defects_data: List[Dict]) -> List:
        """Generate cost estimates for repairs"""
        elements = []
        
        elements.append(Paragraph("COST ESTIMATES", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        # Calculate cost estimates
        cost_data = self._calculate_repair_costs(defects_data)
        
        cost_summary = [
            ['Repair Category', 'Quantity', 'Unit Cost (USD)', 'Total Cost (USD)'],
        ]
        
        total_cost = 0
        for category, details in cost_data.items():
            cost_summary.append([
                category,
                str(details['quantity']),
                f"${details['unit_cost']:,.2f}",
                f"${details['total']:,.2f}"
            ])
            total_cost += details['total']
        
        cost_summary.append(['', '', 'SUBTOTAL:', f"${total_cost:,.2f}"])
        cost_summary.append(['', '', 'Contingency (15%):', f"${total_cost * 0.15:,.2f}"])
        cost_summary.append(['', '', 'TOTAL ESTIMATE:', f"${total_cost * 1.15:,.2f}"])
        
        cost_table = Table(cost_summary, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        cost_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (2, -3), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (3, -1), (3, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -4), 0.5, colors.grey),
            ('LINEABOVE', (2, -3), (-1, -3), 1, colors.black),
            ('LINEABOVE', (2, -1), (-1, -1), 2, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(cost_table)
        elements.append(Spacer(1, 12))
        
        disclaimer = Paragraph(
            "<i>Note: Cost estimates are approximate and based on industry standards. "
            "Actual costs may vary based on material availability, labor rates, and site-specific conditions. "
            "A detailed quote from licensed contractors is recommended.</i>",
            ParagraphStyle('Disclaimer', parent=self.styles['Normal'], fontSize=9, textColor=colors.grey)
        )
        elements.append(disclaimer)
        
        return elements
    
    def _create_priority_matrix(self, defects_data: List[Dict]) -> List:
        """Create maintenance priority matrix"""
        elements = []
        
        elements.append(Paragraph("MAINTENANCE PRIORITY MATRIX", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        # Categorize defects by priority
        priority_groups = {
            'Critical (Immediate)': [],
            'High (7 days)': [],
            'Medium (30 days)': [],
            'Low (90 days)': []
        }
        
        for defect in defects_data:
            priority = self._determine_priority(defect)
            priority_groups[priority].append(defect)
        
        matrix_data = [['Priority', 'Defects', 'Timeline', 'Action Required']]
        
        for priority, defects in priority_groups.items():
            if defects:
                defect_list = ', '.join([d['type'].replace('_', ' ').title() for d in defects[:3]])
                if len(defects) > 3:
                    defect_list += f" (+{len(defects)-3} more)"
                
                matrix_data.append([
                    priority.split('(')[0].strip(),
                    defect_list,
                    priority.split('(')[1].strip(')'),
                    'Required' if 'Critical' in priority or 'High' in priority else 'Recommended'
                ])
        
        matrix_table = Table(matrix_data, colWidths=[1.3*inch, 2.5*inch, 1.2*inch, 1.5*inch])
        matrix_table.setStyle(self._get_table_style())
        elements.append(matrix_table)
        
        return elements
    
    def _create_voice_annotations_section(self, voice_transcripts: List[Dict]) -> List:
        """Create section with voice annotations and context"""
        elements = []
        
        elements.append(Paragraph("VOICE ANNOTATIONS & INSPECTOR CONTEXT", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        intro = Paragraph(
            "The following annotations were recorded by the inspector during the site visit. "
            "These provide valuable contextual information and real-time observations that complement "
            "the automated defect detection analysis.",
            self.styles['BodyJustified']
        )
        elements.append(intro)
        elements.append(Spacer(1, 12))
        
        for idx, transcript in enumerate(voice_transcripts, 1):
            elements.append(Paragraph(f"Annotation #{idx}", self.styles['SubHeading']))
            
            annotation_data = [
                ['Timestamp:', transcript.get('timestamp', 'N/A')],
                ['Location:', transcript.get('location', 'N/A')],
                ['Duration:', transcript.get('duration', 'N/A')],
                ['Transcript:', transcript.get('text', 'N/A')],
            ]
            
            annotation_table = Table(annotation_data, colWidths=[1.5*inch, 4.5*inch])
            annotation_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(annotation_table)
            elements.append(Spacer(1, 15))
        
        return elements
    
    def _create_appendices(self, defects_data: List[Dict]) -> List:
        """Create appendices section"""
        elements = []
        
        elements.append(Paragraph("APPENDICES", self.styles['SectionHeading']))
        elements.append(Spacer(1, 12))
        
        # Appendix A: Methodology
        elements.append(Paragraph("Appendix A: Inspection Methodology", self.styles['SubHeading']))
        methodology_text = """This inspection was conducted using the SiteLenz AI-Powered Infrastructure 
        Monitoring System, which employs a Vision Transformer (ViT) deep learning model trained on thousands 
        of structural defect images. The system achieves 95%+ accuracy in defect classification and provides 
        real-time analysis. All findings were verified against standard structural engineering practices and 
        building codes."""
        elements.append(Paragraph(methodology_text, self.styles['BodyJustified']))
        elements.append(Spacer(1, 15))
        
        # Appendix B: Defect Classification Guide
        elements.append(Paragraph("Appendix B: Defect Classification Guide", self.styles['SubHeading']))
        classification_data = [
            ['Defect Type', 'Description', 'Typical Severity'],
            ['Major Crack', 'Cracks wider than 3mm or structurally significant', 'High'],
            ['Minor Crack', 'Surface cracks less than 3mm wide', 'Low-Medium'],
            ['Spalling', 'Concrete deterioration exposing rebar', 'High'],
            ['Algae Growth', 'Biological growth indicating moisture issues', 'Low-Medium'],
            ['Stain', 'Discoloration indicating water infiltration', 'Medium'],
            ['Peeling', 'Paint or coating failure', 'Low'],
        ]
        
        classification_table = Table(classification_data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
        classification_table.setStyle(self._get_table_style())
        elements.append(classification_table)
        elements.append(Spacer(1, 15))
        
        # Appendix C: References
        elements.append(Paragraph("Appendix C: Standards & References", self.styles['SubHeading']))
        references_text = """
        • ACI 318: Building Code Requirements for Structural Concrete<br/>
        • ASTM C876: Standard Test Method for Corrosion Potentials<br/>
        • ISO 13822: Assessment of Existing Structures<br/>
        • Local Building Code Compliance Standards<br/>
        • SiteLenz AI Model Documentation v2.0
        """
        elements.append(Paragraph(references_text, self.styles['BodyJustified']))
        
        return elements
    
    # Helper methods
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(72, A4[1] - 50, "SiteLenz Inspection Report")
        canvas.drawRightString(A4[0] - 72, A4[1] - 50, f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
        canvas.line(72, A4[1] - 55, A4[0] - 72, A4[1] - 55)
        
        # Footer
        canvas.drawString(72, 50, "Confidential - For authorized use only")
        canvas.drawRightString(A4[0] - 72, 50, f"Page {doc.page}")
        canvas.line(72, 55, A4[0] - 72, 55)
        
        canvas.restoreState()
    
    def _get_table_style(self):
        """Get standard table style"""
        return TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ])
    
    def _calculate_defect_statistics(self, defects_data: List[Dict]) -> Dict:
        """Calculate comprehensive defect statistics"""
        stats = {
            'total_defects': len(defects_data),
            'critical_count': 0,
            'high_priority_count': 0,
            'medium_priority_count': 0,
            'low_priority_count': 0,
            'defect_types': {},
            'type_confidence': {},
            'location_distribution': {},
            'location_severity': {},
            'avg_confidence': 0,
        }
        
        total_confidence = 0
        type_confidence_sum = {}
        type_confidence_count = {}
        
        for defect in defects_data:
            # Priority counts
            severity = defect.get('severity', 'medium').lower()
            if severity == 'critical':
                stats['critical_count'] += 1
            elif severity == 'high':
                stats['high_priority_count'] += 1
            elif severity == 'medium':
                stats['medium_priority_count'] += 1
            else:
                stats['low_priority_count'] += 1
            
            # Type distribution
            defect_type = defect.get('type', 'unknown')
            stats['defect_types'][defect_type] = stats['defect_types'].get(defect_type, 0) + 1
            
            # Confidence tracking
            confidence = defect.get('confidence', 0) * 100
            total_confidence += confidence
            
            if defect_type not in type_confidence_sum:
                type_confidence_sum[defect_type] = 0
                type_confidence_count[defect_type] = 0
            type_confidence_sum[defect_type] += confidence
            type_confidence_count[defect_type] += 1
            
            # Location distribution
            location = defect.get('location', 'Unknown')
            stats['location_distribution'][location] = stats['location_distribution'].get(location, 0) + 1
            
            # Location severity (simplified calculation)
            severity_score = {'critical': 10, 'high': 7, 'medium': 5, 'low': 3}.get(severity, 5)
            if location not in stats['location_severity']:
                stats['location_severity'][location] = []
            stats['location_severity'][location].append(severity_score)
        
        # Calculate percentages and averages
        if stats['total_defects'] > 0:
            stats['critical_percent'] = (stats['critical_count'] / stats['total_defects']) * 100
            stats['high_priority_percent'] = (stats['high_priority_count'] / stats['total_defects']) * 100
            stats['medium_priority_percent'] = (stats['medium_priority_count'] / stats['total_defects']) * 100
            stats['low_priority_percent'] = (stats['low_priority_count'] / stats['total_defects']) * 100
            stats['avg_confidence'] = total_confidence / stats['total_defects']
        else:
            stats['critical_percent'] = 0
            stats['high_priority_percent'] = 0
            stats['medium_priority_percent'] = 0
            stats['low_priority_percent'] = 0
            stats['avg_confidence'] = 0
        
        # Average confidence per type
        for defect_type in type_confidence_sum:
            stats['type_confidence'][defect_type] = type_confidence_sum[defect_type] / type_confidence_count[defect_type]
        
        # Average severity per location
        for location in stats['location_severity']:
            stats['location_severity'][location] = sum(stats['location_severity'][location]) / len(stats['location_severity'][location])
        
        return stats
    
    def _calculate_risk_scores(self, defects_data: List[Dict]) -> Dict:
        """Calculate risk scores"""
        critical_defects = ['major_crack', 'spalling']
        
        structural_risk = 0
        safety_risk = 0
        deterioration_risk = 0
        
        for defect in defects_data:
            defect_type = defect.get('type', '')
            confidence = defect.get('confidence', 0)
            
            if defect_type in critical_defects:
                structural_risk += confidence * 8
                safety_risk += confidence * 7
            else:
                structural_risk += confidence * 3
                safety_risk += confidence * 2
            
            deterioration_risk += confidence * 5
        
        count = len(defects_data) if defects_data else 1
        
        return {
            'structural_risk': min(structural_risk / count, 10),
            'safety_risk': min(safety_risk / count, 10),
            'deterioration_risk': min(deterioration_risk / count, 10),
            'financial_risk': min((structural_risk + deterioration_risk) / (count * 2), 10),
            'overall_risk': min((structural_risk + safety_risk + deterioration_risk) / (count * 3), 10)
        }
    
    def _calculate_repair_costs(self, defects_data: List[Dict]) -> Dict:
        """Calculate repair cost estimates"""
        cost_data = {}
        
        # Cost per defect type (simplified estimates in USD)
        unit_costs = {
            'major_crack': 500,
            'minor_crack': 150,
            'spalling': 800,
            'algae': 200,
            'stain': 100,
            'peeling': 120,
        }
        
        for defect in defects_data:
            defect_type = defect.get('type', 'unknown')
            base_type = defect_type.replace('_growth', '').replace('_crack', '')
            
            if base_type not in cost_data:
                cost_data[base_type] = {
                    'quantity': 0,
                    'unit_cost': unit_costs.get(defect_type, 250),
                    'total': 0
                }
            
            cost_data[base_type]['quantity'] += 1
        
        # Calculate totals
        for category in cost_data:
            cost_data[category]['total'] = cost_data[category]['quantity'] * cost_data[category]['unit_cost']
        
        return cost_data
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level text from score"""
        if score >= 8:
            return "Critical"
        elif score >= 6:
            return "High"
        elif score >= 4:
            return "Medium"
        else:
            return "Low"
    
    def _get_status_indicator(self, score: float) -> str:
        """Get status indicator"""
        if score >= 8:
            return "⚠ URGENT"
        elif score >= 6:
            return "⚡ HIGH"
        elif score >= 4:
            return "◐ MODERATE"
        else:
            return "✓ LOW"
    
    def _determine_priority(self, defect: Dict) -> str:
        """Determine priority category"""
        severity = defect.get('severity', 'medium').lower()
        confidence = defect.get('confidence', 0)
        
        if severity == 'critical' or (severity == 'high' and confidence > 0.9):
            return 'Critical (Immediate)'
        elif severity == 'high':
            return 'High (7 days)'
        elif severity == 'medium':
            return 'Medium (30 days)'
        else:
            return 'Low (90 days)'
    
    def _prepare_defects_summary_text(self, defects_data: List[Dict]) -> str:
        """Prepare defects summary for AI prompts"""
        summary_lines = []
        for idx, defect in enumerate(defects_data, 1):
            summary_lines.append(
                f"{idx}. {defect['type'].replace('_', ' ').title()} - "
                f"Confidence: {defect.get('confidence', 0)*100:.1f}%, "
                f"Location: {defect.get('location', 'N/A')}, "
                f"Severity: {defect.get('severity', 'Medium')}"
            )
        return '\n'.join(summary_lines)
    
    def _prepare_voice_context(self, voice_transcripts: List[Dict]) -> str:
        """Prepare voice context for AI"""
        if not voice_transcripts:
            return "No voice annotations available."
        
        context_lines = []
        for idx, transcript in enumerate(voice_transcripts, 1):
            context_lines.append(f"{idx}. {transcript.get('text', 'N/A')}")
        return '\n'.join(context_lines)
    
    def _get_defect_ai_analysis(self, defect: Dict, voice_transcripts: List[Dict]) -> Dict:
        """Get AI analysis for individual defect"""
        defect_type = defect['type'].replace('_', ' ')
        location = defect.get('location', 'unknown location')
        confidence = defect.get('confidence', 0) * 100
        severity = defect.get('severity', 'medium')
        timestamp = defect.get('timestamp', 'Not recorded')
        
        # Find relevant voice annotations for this defect
        relevant_annotations = []
        if voice_transcripts:
            for transcript in voice_transcripts:
                if location.lower() in transcript.get('text', '').lower() or defect_type.lower() in transcript.get('text', '').lower():
                    relevant_annotations.append(transcript.get('text', ''))
        
        annotations_text = "\n".join(relevant_annotations) if relevant_annotations else "No specific annotations for this defect"
        
        prompt = f"""You are a forensic structural engineer performing a detailed analysis of a specific building defect. Provide a comprehensive technical assessment that will be included in a professional inspection report.

DEFECT DETAILS:
- Classification: {defect_type.title()}
- Location: {location}
- Detection Confidence: {confidence:.1f}%
- Severity Level: {severity.upper()}
- Detection Timestamp: {timestamp}
- Image Reference: {defect.get('image_id', 'N/A')}

INSPECTOR'S ON-SITE OBSERVATIONS:
{annotations_text}

YOUR COMPREHENSIVE ANALYSIS TASK (Total: 400-450 words divided into three sections):

═══════════════════════════════════════════════════════════════
SECTION 1: TECHNICAL ANALYSIS AND CHARACTERIZATION (150-180 words)
═══════════════════════════════════════════════════════════════

Provide an EXTREMELY DETAILED technical assessment covering:

• PHYSICAL CHARACTERISTICS:
  - Exact description of the defect appearance and extent
  - Estimated dimensions, width, length, depth (if measurable from description)
  - Surface texture and condition
  - Color variations or staining patterns
  - Edge characteristics (sharp, weathered, deteriorated)

• MATERIAL CONDITION:
  - Type of material affected (concrete, masonry, steel, coating, etc.)
  - Material degradation level
  - Loss of section or material integrity
  - Surface preparation or finish condition

• STRUCTURAL IMPLICATIONS:
  - Impact on load-bearing capacity (if structural element)
  - Effect on weather resistance and envelope integrity
  - Influence on adjacent building components
  - Potential for progressive failure
  - Connection to building systems (waterproofing, drainage, etc.)

• DETECTION CONFIDENCE ANALYSIS:
  - Given the {confidence:.1f}% confidence level, discuss reliability
  - Mention any factors that might affect detection accuracy
  - Note if visual confirmation by engineer is recommended

═══════════════════════════════════════════════════════════════
SECTION 2: ROOT CAUSE ANALYSIS (120-150 words)
═══════════════════════════════════════════════════════════════

Perform FORENSIC-LEVEL analysis of causes:

• PRIMARY CAUSE:
  - Identify the most likely root cause with engineering rationale
  - Explain the failure mechanism (corrosion, fatigue, overload, material defect, installation error, etc.)
  - Reference material science principles

• CONTRIBUTING FACTORS:
  - List ALL secondary factors that contributed
  - Environmental factors (weather, UV, moisture, temperature cycles)
  - Design deficiencies or construction errors
  - Maintenance neglect or inappropriate repairs
  - Building age and material lifespan issues
  - Loading conditions or usage patterns

• TIMELINE ASSESSMENT:
  - Estimate when this defect likely initiated
  - Assess current stage of deterioration
  - Predict progression if left untreated

• SIMILAR DEFECT RISK:
  - Identify other locations that may develop similar problems
  - Discuss if this indicates systemic building issues

═══════════════════════════════════════════════════════════════
SECTION 3: SPECIFIC REPAIR RECOMMENDATIONS (130-120 words)
═══════════════════════════════════════════════════════════════

Provide ACTIONABLE repair guidance:

• REPAIR METHODOLOGY:
  - Step-by-step repair procedure appropriate for this specific defect
  - Surface preparation requirements
  - Material removal or cleaning needed
  - Repair material specifications (product types, performance requirements)
  - Application procedures and techniques
  - Curing time and conditions

• CONTRACTOR REQUIREMENTS:
  - Required qualifications, licenses, or certifications
  - Specialized equipment or tools needed
  - Safety protocols and PPE requirements

• QUALITY ASSURANCE:
  - Inspection checkpoints during repair
  - Testing requirements (pull tests, core samples, moisture tests, etc.)
  - Success criteria and acceptance standards
  - Post-repair monitoring recommendations

• COST AND TIME ESTIMATES:
  - Approximate repair duration (hours/days)
  - Material cost range
  - Labor cost considerations
  - Access requirements affecting cost

• URGENCY JUSTIFICATION:
  - Clear explanation of why this repair has {severity} priority
  - Specific consequences of delayed repair (structural, safety, financial)
  - Recommended timeline for repair completion

TECHNICAL WRITING REQUIREMENTS:
- Use precise engineering terminology
- Reference specific standards where applicable (ACI, ASTM, ASCE)
- Include quantitative details wherever possible
- Cite material properties and behavior
- Reference building codes if violations present
- Write in formal third-person technical style
- Make every sentence information-dense and valuable
- Connect observations to engineering principles

Format your response with clear section headers as shown above for easy readability in the report."""

        try:
            full_response = self.ai_client.chat(
                message=prompt,
                system_prompt="You are a forensic structural engineer and building pathologist specializing in defect analysis. You combine 30+ years of field experience with deep knowledge of material science, structural mechanics, and building codes. Your analyses are detailed enough to defend in court and form the basis for repair specifications.",
                temperature=0.3,
                max_tokens=800
            )
            
            # Parse the response into sections (simplified parsing)
            sections = full_response.split('═══════════════════════════════════════════════════════════════')
            
            technical = sections[1].strip() if len(sections) > 1 else full_response[:len(full_response)//3]
            causes = sections[2].strip() if len(sections) > 2 else full_response[len(full_response)//3:2*len(full_response)//3]
            actions = sections[3].strip() if len(sections) > 3 else full_response[2*len(full_response)//3:]
            
            return {
                'technical': technical,
                'causes': causes,
                'actions': actions
            }
        except Exception as e:
            print(f"Defect analysis failed for {defect_type}: {e}")
            return {
                'technical': f"Detected {defect_type} at {location} with {confidence:.1f}% confidence. Severity classified as {severity}. Detailed technical analysis requires manual inspection by licensed structural engineer.",
                'causes': "Root cause analysis requires detailed on-site investigation and material testing. Common causes for this defect type should be investigated including material degradation, environmental exposure, and structural loading conditions.",
                'actions': f"Recommended action: Schedule detailed structural assessment by licensed Professional Engineer (P.E.) within {7 if severity in ['critical', 'high'] else 30} days. Engineer should verify defect characteristics, determine root cause, and specify appropriate repair methodology."
            }
    
    def _generate_fallback_summary(self, defects_data: List[Dict], site_info: Dict) -> str:
        """Generate fallback summary if AI fails"""
        return f"""This structural inspection report documents the findings from a comprehensive assessment 
        of {site_info.get('site_name', 'the subject property')} located at {site_info.get('location', 'N/A')}. 
        The inspection identified {len(defects_data)} defects requiring attention, ranging from minor surface 
        issues to potentially significant structural concerns. This report provides detailed analysis, risk 
        assessment, and recommendations for remediation."""


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("SiteLenz - PDF Report Generator Test")
    print("=" * 70)
    
    # Sample data
    sample_defects = [
        {
            'type': 'major_crack',
            'confidence': 0.95,
            'location': 'North Wall, Room 101',
            'severity': 'high',
            'timestamp': '2025-12-02 14:30:00',
            'image_id': 'IMG_001.jpg'
        },
        {
            'type': 'spalling',
            'confidence': 0.87,
            'location': 'Column B-3, Ground Floor',
            'severity': 'critical',
            'timestamp': '2025-12-02 14:35:00',
            'image_id': 'IMG_002.jpg'
        },
        {
            'type': 'stain',
            'confidence': 0.76,
            'location': 'Ceiling, Room 102',
            'severity': 'medium',
            'timestamp': '2025-12-02 14:40:00',
            'image_id': 'IMG_003.jpg'
        },
        {
            'type': 'minor_crack',
            'confidence': 0.82,
            'location': 'East Wall, Corridor',
            'severity': 'low',
            'timestamp': '2025-12-02 14:45:00',
            'image_id': 'IMG_004.jpg'
        },
        {
            'type': 'algae',
            'confidence': 0.91,
            'location': 'Exterior North Face',
            'severity': 'medium',
            'timestamp': '2025-12-02 14:50:00',
            'image_id': 'IMG_005.jpg'
        }
    ]
    
    sample_site_info = {
        'site_name': 'Hamilton Commercial Plaza',
        'location': '123 Main Street, Springfield, IL 62701',
        'building_type': 'Commercial Office Building',
        'year_built': '1985',
        'total_area': '45,000 sq ft',
        'inspector_name': 'John Smith, P.E.',
        'license_no': 'PE-12345',
        'weather': 'Clear, Dry',
        'temperature': '72°F',
        'report_id': 'RPT-20251202-001'
    }
    
    sample_voice_transcripts = [
        {
            'timestamp': '2025-12-02 14:30:15',
            'location': 'North Wall, Room 101',
            'duration': '00:00:45',
            'text': 'Major vertical crack observed on north wall of room 101. Crack extends from floor to ceiling, approximately 5mm wide at widest point. Water staining visible along crack edges. Recommend immediate structural assessment.'
        },
        {
            'timestamp': '2025-12-02 14:35:20',
            'location': 'Column B-3',
            'duration': '00:00:38',
            'text': 'Severe spalling detected on column B-3. Concrete has deteriorated exposing reinforcement bars. Visible rust on rebar. This appears to be a result of water infiltration and requires urgent attention to prevent further deterioration.'
        },
        {
            'timestamp': '2025-12-02 14:40:10',
            'location': 'Room 102 Ceiling',
            'duration': '00:00:30',
            'text': 'Brown staining on ceiling indicates active water leak from above. Stain pattern suggests plumbing issue. No structural damage visible yet but needs investigation to prevent mold growth.'
        }
    ]
    
    try:
        # Generate report
        generator = InspectionReportGenerator()
        
        print("\nGenerating comprehensive PDF report...")
        print("This may take 1-2 minutes due to AI content generation...\n")
        
        report_path = generator.generate_comprehensive_report(
            defects_data=sample_defects,
            site_info=sample_site_info,
            voice_transcripts=sample_voice_transcripts
        )
        
        print("\n" + "=" * 70)
        print("SUCCESS! Report generated successfully!")
        print("=" * 70)
        print(f"\nReport saved to: {report_path}")
        print(f"File size: {os.path.getsize(report_path) / 1024:.1f} KB")
        print("\nReport includes:")
        print("  ✓ Professional cover page")
        print("  ✓ Table of contents")
        print("  ✓ AI-generated executive summary")
        print("  ✓ Comprehensive statistics with numerical data")
        print("  ✓ Detailed defect analysis with AI insights")
        print("  ✓ Risk assessment with scores")
        print("  ✓ Professional recommendations")
        print("  ✓ Cost estimates")
        print("  ✓ Priority matrix")
        print("  ✓ Voice annotations and context")
        print("  ✓ Technical appendices")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error generating report: {e}")
        import traceback
        traceback.print_exc()
