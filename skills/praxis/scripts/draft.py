import json
import os

def main():
    print("Running Praxis Drafter Pipeline...")
    try:
        with open('.praxis/data/knowledge_base.json', 'r') as f:
            kb = json.load(f)
    except FileNotFoundError:
        print("Error: knowledge_base.json not found. Run ingest pipeline first.")
        return

    # Extract dynamic data
    skills = list(kb.get('RelationalSkillsDatabase', {}).keys())
    top_skills = ", ".join(skills[:30]) if skills else "Python, Distributed Systems, Kubernetes, RAG, AI Agents, Node.js"

    # Generate Resume.md
    with open('Resume.md', 'w') as f:
        f.write("# Kenton Smeltzer\n")
        f.write("Phone: 786-933-0944 | Email: ksmeltzer@gmail.com | LinkedIn: http://www.linkedin.com/in/kentonsmeltzer | GitHub: https://github.com/ksmeltzer\n\n")
        
        f.write("## Summary\n")
        f.write("Principal Systems Engineer and AI Solutions Architect with over two decades of experience designing high-scale, secure, and distributed enterprise platforms. Proven track record of architecting systems that handle high-volume global reservations, complex federal investigations, and secure healthcare data. Expertise spans RAG pipelines, agentic workflows, distributed event-based data platforms, and adversarial modeling.\n\n")
        
        f.write("## Skills\n")
        f.write(f"**Core Competencies:** {top_skills}\n\n")
        
        f.write("## Patents & Projects\n")
        f.write("- **US Patent Pending (US20250103405A1):** Distributed Event-Based Data Platform. Designed and authored core architecture for secure, high-throughput healthcare data event streaming.\n")
        f.write("- **OpenCode AI Orchestration:** Engineered a custom 7-persona AI Architecture Review Panel, AI-driven PR analyzer, and intelligent technical interview scribe.\n")
        f.write("- **Patient Matching Algorithm:** Authored best-in-class algorithm at DexCare to reduce duplicate patient records while maintaining strict HIPAA compliance.\n\n")

        f.write("## Experience\n\n")
        
        for role in kb.get('CareerCatalog', []):
            f.write(f"### {role['title']}\n")
            f.write(f"#### {role['company']} | {role['dates']}\n")
            for b in role['bullets']:
                f.write(f"- {b}\n")
            f.write("\n")

    # Generate LinkedIn_Profile.md
    with open('LinkedIn_Profile.md', 'w') as f:
        f.write("# LinkedIn Profile Draft\n\n")
        f.write("**Headline:** Principal Systems Engineer & AI Solutions Architect | RAG pipelines, Agentic Workflows, and High-Scale Enterprise Systems\n\n")
        f.write("## About\n")
        f.write("Principal Systems Engineer and AI Solutions Architect with over two decades of experience designing high-scale, secure, and distributed enterprise platforms. I have built systems that handle high volume, global reservations (Marriott, Orlando.com), complex federal investigations (Joint Interagency Task Force), and secure healthcare data (DexCare). My roots in adversarial modeling and spatial intelligence algorithms trace back to DoD simulators in 1998. Expert in RAG pipelines, agentic workflows, distributed event-based data platforms, and bridging rapid innovation with strict financial and healthcare compliance.\n\n")
        f.write("## Patents & Publications\n")
        f.write("- **US Patent Pending (US20250103405A1):** Distributed Event-Based Data Platform\n\n")
        f.write("## Skills to Add (Top Endorsements)\n")
        f.write(f"{top_skills}\n\n")
        f.write("## Experience\n\n")
        for role in kb.get('CareerCatalog', []):
            f.write(f"### {role['title']}\n")
            f.write(f"#### {role['company']} | {role['dates']}\n")
            for b in role['bullets']:
                f.write(f"- {b}\n")
            f.write("\n")

    print("Drafting complete. Resume.md and LinkedIn_Profile.md generated successfully.")

if __name__ == "__main__":
    main()
