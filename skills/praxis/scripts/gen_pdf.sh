#!/bin/bash
set -e

# Usage: gen_pdf.sh <input.md> <output.pdf>
# Converts markdown to PDF using md-to-pdf with sandbox disabled (required for non-root).

if [ $# -lt 2 ]; then
    echo "Usage: $0 <input.md> <output.pdf>"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

if [ ! -f "$INPUT" ]; then
    echo "Input file not found: $INPUT"
    exit 1
fi

# Create temporary config to disable Chrome sandbox (required in containerized/non-root envs)
CONFIG_FILE=".md-to-pdf.js"
cat > "$CONFIG_FILE" <<'EOF'
module.exports = {
  launch_options: {
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  },
  stylesheet: [],
  css: `
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 11pt; line-height: 1.4; color: #333; margin: 0.5in 0.6in; }
    h1 { font-size: 18pt; margin-bottom: 2pt; color: #1a1a1a; }
    h2 { font-size: 13pt; border-bottom: 1px solid #ccc; padding-bottom: 2pt; margin-top: 12pt; color: #1a1a1a; }
    h3 { font-size: 11pt; margin-bottom: 0; margin-top: 8pt; }
    ul { margin-top: 2pt; margin-bottom: 4pt; padding-left: 18pt; }
    li { margin-bottom: 2pt; }
    p { margin: 2pt 0; }
    strong { color: #1a1a1a; }
    a { color: #0066cc; text-decoration: none; }
  `,
  pdf_options: {
    format: 'Letter',
    margin: { top: '0.5in', bottom: '0.5in', left: '0.6in', right: '0.6in' },
    printBackground: true
  }
};
EOF

# Generate PDF
npx -y md-to-pdf "$INPUT" --config-file "$CONFIG_FILE" 2>/dev/null

# md-to-pdf outputs alongside the input file with .pdf extension
GENERATED="${INPUT%.md}.pdf"
if [ -f "$GENERATED" ] && [ "$GENERATED" != "$OUTPUT" ]; then
    mv -f "$GENERATED" "$OUTPUT"
fi

# Clean up config
rm -f "$CONFIG_FILE"

echo "PDF generated: $OUTPUT"
