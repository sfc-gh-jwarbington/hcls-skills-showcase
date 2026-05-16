#!/usr/bin/env python3
"""
Reads skill directories from the source repo's skills/ folder and regenerates index.html.
Each skill folder is expected to have a prompt.md with a description line.
"""
import os
import re
import json
import subprocess

SKILLS_DIR = "source-skills"

CATEGORIES = {
    "cross": {"label": "Cross-Domain", "badge_class": "badge-cross", "icon_map": {
        "aiml-industrymodels": "&#129302;",
        "cke-clinical-trials": "&#128300;",
        "cke-pubmed": "&#128218;",
        "platform-multitenancy": "&#127970;",
        "research-problem-selection": "&#127919;",
        "skill-development": "&#128736;",
    }},
    "pharma": {"label": "Pharma &amp; Life Sciences", "badge_class": "badge-pharma", "icon_map": {
        "dsafety-clinical-trial-protocol": "&#128203;",
        "dsafety-pharmacovigilance": "&#9888;&#65039;",
        "genomics-nextflow": "&#129516;",
        "genomics-scvi-tools": "&#129504;",
        "genomics-single-cell-qc": "&#128172;",
        "genomics-survival-analysis": "&#128200;",
        "genomics-variant-annotation": "&#129516;",
        "lab-allotrope": "&#129514;",
        "lab-ml-optimization": "&#9881;&#65039;",
    }},
    "provider": {"label": "Healthcare Provider", "badge_class": "badge-provider", "icon_map": {
        "cdata-clinical-docs": "&#128196;",
        "cdata-clinical-nlp": "&#128221;",
        "cdata-fhir": "&#128257;",
        "cdata-omop": "&#128202;",
        "claims-data-analysis": "&#128176;",
        "imaging": "&#128444;&#65039;",
    }},
}

DEFAULT_ICONS = ["&#128300;", "&#129302;", "&#128218;", "&#128200;", "&#128196;"]


def get_skill_description(skill_path):
    prompt_file = os.path.join(skill_path, "prompt.md")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r") as f:
            content = f.read()
        lines = content.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("---"):
                clean = re.sub(r'["\']', '', line)
                if len(clean) > 20:
                    return clean[:200]
    config_file = os.path.join(skill_path, "config.yaml")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            for line in f:
                if "description:" in line.lower():
                    desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if desc:
                        return desc[:200]
    return "AI-powered skill for healthcare and life sciences workflows on Snowflake."


def classify_skill(skill_name):
    if skill_name.startswith("hcls-cross-"):
        suffix = skill_name.replace("hcls-cross-", "")
        return "cross", suffix
    elif skill_name.startswith("hcls-pharma-"):
        suffix = skill_name.replace("hcls-pharma-", "")
        return "pharma", suffix
    elif skill_name.startswith("hcls-provider-"):
        suffix = skill_name.replace("hcls-provider-", "")
        return "provider", suffix
    return None, skill_name


def format_skill_name(suffix):
    words = suffix.replace("-", " ").split()
    return " ".join(w.capitalize() for w in words)


def get_icon(category, suffix):
    cat_info = CATEGORIES.get(category, {})
    icon_map = cat_info.get("icon_map", {})
    if suffix in icon_map:
        return icon_map[suffix]
    idx = hash(suffix) % len(DEFAULT_ICONS)
    return DEFAULT_ICONS[idx]


def discover_skills():
    skills = {"cross": [], "pharma": [], "provider": []}
    if not os.path.exists(SKILLS_DIR):
        print(f"Warning: {SKILLS_DIR} not found")
        return skills

    for entry in sorted(os.listdir(SKILLS_DIR)):
        skill_path = os.path.join(SKILLS_DIR, entry)
        if not os.path.isdir(skill_path):
            continue
        if not entry.startswith("hcls-"):
            continue
        category, suffix = classify_skill(entry)
        if category is None:
            continue
        desc = get_skill_description(skill_path)
        skills[category].append({
            "name": entry,
            "display_name": format_skill_name(suffix),
            "description": desc,
            "icon": get_icon(category, suffix),
        })
    return skills


def generate_cards_html(skills_list):
    cards = []
    for skill in skills_list:
        card = f'''                <div class="skill-card">
                    <div class="skill-card-header">
                        <div class="skill-icon">{skill["icon"]}</div>
                        <div>
                            <div class="skill-name">{skill["display_name"]}</div>
                            <div class="skill-command">${skill["name"]}</div>
                        </div>
                    </div>
                    <div class="skill-desc">{skill["description"]}</div>
                </div>'''
        cards.append(card)
    return "\n".join(cards)


def generate_section(category_key, skills_list):
    cat = CATEGORIES[category_key]
    cards_html = generate_cards_html(skills_list)
    return f'''        <section class="category-section">
            <div class="category-header">
                <span class="category-badge {cat["badge_class"]}">&#9672; {cat["label"]}</span>
            </div>
            <div class="skills-grid">
{cards_html}
            </div>
        </section>'''


def count_genomics(skills):
    return sum(1 for s in skills.get("pharma", []) if "genomics" in s["name"])


def count_clinical(skills):
    count = sum(1 for s in skills.get("provider", []) if "cdata" in s["name"])
    count += sum(1 for s in skills.get("provider", []) if "claims" in s["name"])
    return count


def generate_html(skills):
    total = sum(len(v) for v in skills.values())
    genomics_count = count_genomics(skills)
    clinical_count = count_clinical(skills)

    sections = []
    for cat_key in ["cross", "pharma", "provider"]:
        if skills[cat_key]:
            sections.append(generate_section(cat_key, skills[cat_key]))

    sections_html = "\n\n".join(sections)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cortex Code | HCLS Skills Showcase</title>
    <style>
        :root {{
            --sf-blue: #29B5E8;
            --sf-dark-blue: #11567F;
            --sf-navy: #0D2B3E;
            --sf-light-blue: #E8F7FC;
            --sf-gradient-start: #29B5E8;
            --sf-gradient-end: #1D9BD1;
            --sf-white: #FFFFFF;
            --sf-gray-100: #F8FAFC;
            --sf-gray-200: #E2E8F0;
            --sf-gray-600: #475569;
            --sf-gray-800: #1E293B;
            --pharma-color: #7C3AED;
            --provider-color: #059669;
            --cross-color: #D97706;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--sf-navy);
            color: var(--sf-gray-800);
            min-height: 100vh;
        }}

        .hero {{
            background: linear-gradient(135deg, var(--sf-navy) 0%, #163B52 50%, var(--sf-dark-blue) 100%);
            padding: 60px 40px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 50%, rgba(41,181,232,0.08) 0%, transparent 50%),
                        radial-gradient(circle at 70% 80%, rgba(41,181,232,0.05) 0%, transparent 40%);
            animation: pulse 8s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.05); opacity: 1; }}
        }}

        .hero-content {{ position: relative; z-index: 1; }}

        .logo-row {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            margin-bottom: 20px;
        }}

        .snowflake-icon {{
            width: 56px;
            height: auto;
            object-fit: contain;
        }}

        .hero h1 {{
            font-size: 2.8rem;
            font-weight: 700;
            color: var(--sf-white);
            letter-spacing: -0.5px;
        }}

        .hero h1 span {{ color: var(--sf-blue); }}

        .hero-subtitle {{
            font-size: 1.1rem;
            color: rgba(255,255,255,0.7);
            margin-top: 12px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }}

        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 48px;
            margin-top: 32px;
            flex-wrap: wrap;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--sf-blue);
        }}

        .stat-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: rgba(255,255,255,0.5);
            margin-top: 4px;
        }}

        .main-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 24px 60px;
        }}

        .category-section {{
            margin-bottom: 40px;
        }}

        .category-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }}

        .category-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .badge-pharma {{ background: rgba(124,58,237,0.15); color: #A78BFA; border: 1px solid rgba(124,58,237,0.3); }}
        .badge-provider {{ background: rgba(5,150,105,0.15); color: #6EE7B7; border: 1px solid rgba(5,150,105,0.3); }}
        .badge-cross {{ background: rgba(217,119,6,0.15); color: #FCD34D; border: 1px solid rgba(217,119,6,0.3); }}

        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 16px;
        }}

        .skill-card {{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.2s ease;
            backdrop-filter: blur(10px);
        }}

        .skill-card:hover {{
            background: rgba(255,255,255,0.06);
            border-color: rgba(41,181,232,0.3);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }}

        .skill-card-header {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 10px;
        }}

        .skill-icon {{
            font-size: 1.4rem;
            flex-shrink: 0;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            background: rgba(41,181,232,0.1);
        }}

        .skill-name {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--sf-white);
            line-height: 1.3;
        }}

        .skill-command {{
            font-size: 0.7rem;
            font-family: 'SF Mono', 'Fira Code', monospace;
            color: var(--sf-blue);
            opacity: 0.8;
            margin-top: 2px;
        }}

        .skill-desc {{
            font-size: 0.82rem;
            color: rgba(255,255,255,0.55);
            line-height: 1.5;
        }}

        .footer {{
            text-align: center;
            padding: 32px;
            border-top: 1px solid rgba(255,255,255,0.06);
        }}

        .footer-text {{
            font-size: 0.8rem;
            color: rgba(255,255,255,0.35);
        }}

        .footer-text a {{
            color: var(--sf-blue);
            text-decoration: none;
        }}

        .invoke-hint {{
            display: inline-block;
            background: rgba(41,181,232,0.1);
            border: 1px solid rgba(41,181,232,0.2);
            border-radius: 6px;
            padding: 8px 16px;
            margin-top: 20px;
            font-family: 'SF Mono', 'Fira Code', monospace;
            font-size: 0.8rem;
            color: var(--sf-blue);
        }}

        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2rem; }}
            .skills-grid {{ grid-template-columns: 1fr; }}
            .stats-bar {{ gap: 24px; }}
        }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <div class="logo-row">
                <img class="snowflake-icon" src="https://www.snowflake-store.com/wp-content/uploads/2021/05/bug-sno-R-blue.png" alt="Snowflake Logo">
            </div>
            <h1>Health &amp; Life Sciences <span>Skills</span></h1>
            <p class="hero-subtitle">Purpose-built AI skills for Cortex Code &mdash; accelerating healthcare providers, pharma R&amp;D, and life sciences workflows on Snowflake.</p>
            <div class="stats-bar">
                <div class="stat">
                    <div class="stat-value">{total}</div>
                    <div class="stat-label">Industry Skills</div>
                </div>
                <div class="stat">
                    <div class="stat-value">3</div>
                    <div class="stat-label">Domains</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{genomics_count}</div>
                    <div class="stat-label">Genomics Pipelines</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{clinical_count}</div>
                    <div class="stat-label">Clinical Data Skills</div>
                </div>
            </div>
            <div class="invoke-hint">$ cortex skill invoke hcls-&lt;domain&gt;-&lt;skill&gt;</div>
        </div>
    </section>

    <div class="main-content">

{sections_html}

    </div>

    <footer class="footer">
        <p class="footer-text">Built with <a href="https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code">Cortex Code</a> &mdash; Snowflake\'s AI-Powered IDE &mdash; Auto-generated from <a href="https://github.com/Snowflake-Solutions/health-sciences-coco-skills-incubator">source</a></p>
    </footer>
</body>
</html>'''
    return html


def main():
    skills = discover_skills()
    total = sum(len(v) for v in skills.values())
    if total == 0:
        print("No skills found in source-skills/. Skipping regeneration.")
        return
    html = generate_html(skills)
    with open("index.html", "w") as f:
        f.write(html)
    print(f"Generated index.html with {total} skills")


if __name__ == "__main__":
    main()
