# PDF Report Generation Feature

## Overview
Professional building inspection reports are now automatically generated as downloadable PDF documents with SiteLenz branding.

## Features Implemented

### 1. **Professional PDF Report Generator** (`lib/services/pdf_report_generator.dart`)
   - A4 format professional documents
   - SiteLenz branding with blue gradient cover page
   - Multi-page layout with proper pagination

### 2. **Report Sections**
   - **Cover Page**: SiteLenz branding, inspection ID, and date
   - **Executive Summary**: Location, building type, and overview
   - **Inspection Findings**: Categorized by severity (Critical, High, Medium, Low)
   - **Visual Documentation**: Embedded images from inspection
   - **Cost Estimation**: Repair cost estimates in table format
   - **Building Condition Statistics**: Overall condition, safety rating, urgency level
   - **Recommendations**: Priority-ordered action items
   - **Safety Considerations**: Critical safety concerns

### 3. **AI-Enhanced Analysis**
   - Enhanced Gemini AI prompt for professional report generation
   - Extracts location details from observations
   - Categorizes findings by severity
   - Provides cost estimates
   - Generates actionable recommendations
   - NO MENTION of "transcript" - uses professional terminology:
     * "Site observations"
     * "Inspection findings"
     * "Visual documentation"
     * "Field notes"

### 4. **User Interface Updates**
   - Analyze button changed to PDF icon (`Icons.picture_as_pdf`)
   - Tooltip updated to "Generate PDF Report"
   - Loading indicators during report generation
   - Success/error notifications

## How to Use

1. **Capture Inspection Data**:
   - Go to "Record" tab
   - Use speech-to-text to document observations
   - Capture images during inspection
   - Save session

2. **Generate PDF Report**:
   - Go to "Logs" tab
   - View your saved sessions
   - Click the **PDF icon** in the app bar
   - Wait for AI analysis (may take 10-30 seconds)
   - PDF will automatically open in preview/print dialog

3. **Download/Share PDF**:
   - From the PDF preview, you can:
     * Save to device storage
     * Print the report
     * Share via email/messaging apps

## Technical Details

### Dependencies Added
```yaml
pdf: ^3.11.1          # PDF document generation
printing: ^5.13.2     # PDF preview, print, and save functionality
```

### Key Files Modified
- `lib/logs_screen.dart`: Updated analyze function to generate PDF
- `lib/services/pdf_report_generator.dart`: New PDF generation service
- `pubspec.yaml`: Added PDF packages

### AI Prompt Enhancement
The Gemini AI prompt now includes:
- Location extraction requirements
- Building type classification
- Severity categorization (Critical/High/Medium/Low)
- Cost estimation guidelines
- Statistics generation
- Professional language requirements
- Explicit instruction to avoid "transcript" terminology

## PDF Report Structure

```
┌─────────────────────────────────────┐
│ Cover Page                          │
│ - SiteLenz Logo/Branding           │
│ - Inspection ID                     │
│ - Date                              │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Executive Summary                   │
│ - Location                          │
│ - Building Type                     │
│ - Overview                          │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Inspection Findings                 │
│ - Severity-coded issues            │
│ - Detailed descriptions            │
│ - Visual Documentation (images)    │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Cost Estimation                     │
│ - Item-by-item breakdown           │
│ - Price ranges                     │
│ - Notes and disclaimers            │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Building Condition Statistics       │
│ - Overall Condition                │
│ - Safety Rating                    │
│ - Urgency Level                    │
│ - Estimated Timeframe              │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Recommendations & Safety            │
│ - Priority recommendations         │
│ - Safety considerations            │
│ - Footer with date/branding        │
└─────────────────────────────────────┘
```

## Color Scheme
- **Primary**: Blue (600-700) - Professional, trustworthy
- **Critical Issues**: Red (700)
- **High Issues**: Orange (700)
- **Medium Issues**: Amber (700)
- **Low Issues**: Blue (700)

## Future Enhancements (Optional)
- [ ] Add SiteLenz logo image to cover page
- [ ] Company contact information in footer
- [ ] Customizable report templates
- [ ] Report history/archive
- [ ] Export to different formats (Word, Excel)
- [ ] Email report directly from app
- [ ] Digital signature support
- [ ] Multi-language support

## Testing Checklist
- [x] PDF packages installed
- [x] Code compiles without errors
- [ ] Test PDF generation with real session data
- [ ] Verify images embed correctly
- [ ] Check PDF opens in preview
- [ ] Test save/share functionality
- [ ] Verify AI analysis quality
- [ ] Check cost estimation accuracy
- [ ] Test with multiple sessions

## Notes
- PDF generation requires internet connection for AI analysis
- Images are limited to 20 per report to prevent token overflow
- Cost estimates are preliminary and require professional validation
- Report generation may take 10-30 seconds depending on data volume
