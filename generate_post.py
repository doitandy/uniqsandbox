import os
import datetime
import random

# 설정
OUTPUT_DIR = "content/thought"
INPUT_FILES = ["data_business.txt", "data_mindset.txt", "data_life.txt"]

def create_hugo_post(index, title, category, body, source_refs):
    days_ago = index % 60 
    dt = datetime.datetime.now() - datetime.timedelta(days=days_ago, hours=index%24)
    date_str = dt.strftime("%Y-%m-%dT%H:%M:%S-07:00")
    
    # [핵심] 제목이 문자열인지 확실히 하고 따옴표(")가 겹치지 않게 처리
    clean_title = str(title).strip().replace('"', "'")
    
    safe_title = "".join([c if c.isalnum() or c.isspace() else "" for c in clean_title]).strip().replace(" ", "-")
    safe_title = safe_title[:50]
    filename = f"{OUTPUT_DIR}/{index:03d}-{safe_title}.md"
    
    tags = ["Insight", "BookNote"]
    cat_lower = str(category).lower().strip()
    
    if "business" in cat_lower or "trend" in cat_lower: tags.extend(["Business", "Trend"])
    elif "mindset" in cat_lower: tags.extend(["Mindset", "Wisdom"])
    elif "health" in cat_lower: tags.extend(["Health", "Biohacking"])
    
    tags = list(set(tags))
    tag_str = ", ".join([f'"{t}"' for t in tags])

    md_content = f"""---
title: "{clean_title}"
date: {date_str}
draft: false
categories: ["Intellectual Archive"]
tags: [{tag_str}]
---

{str(body).strip()}

<!-- Source References: {source_refs} -->
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Created: {filename}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    total_count = 1
    
    for input_file in INPUT_FILES:
        if not os.path.exists(input_file):
            continue
            
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            if "|||" in line:
                parts = line.split("|||")
                if len(parts) >= 3:
                    # [여기] 인덱스를 명확히 지정해서 문자열만 뽑아냄
                    title = parts      
                    category = parts[1]   
                    body_part = parts[2]  
                    
                    if "[" in body_part:
                        temp = body_part.split("[", 1)
                        body_text = temp
                        source_refs = "[" + temp[1]
                    else:
                        body_text = body_part
                        source_refs = "BookNote Archive"
                        
                    create_hugo_post(total_count, title, category, body_text, source_refs.strip())
                    total_count += 1

if __name__ == "__main__":
    main()
