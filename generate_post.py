import os
import datetime
import random

# 설정: Hugo 콘텐츠 경로 (사용자 환경에 맞게 수정)
OUTPUT_DIR = "content/thought"
INPUT_FILES = ["data_business.txt", "data_mindset.txt", "data_life.txt"]

def create_hugo_post(index, title, category, body, source_refs):
    # 날짜를 분산시켜서 포스팅이 한꺼번에 몰리지 않은 것처럼 보이게 함
    # 최근 60일간의 날짜 중 하나를 랜덤 배정 (혹은 순차적으로 하려면 수정 가능)
    days_ago = index % 60 
    dt = datetime.datetime.now() - datetime.timedelta(days=days_ago, hours=index%24)
    date_str = dt.strftime("%Y-%m-%dT%H:%M:%S-07:00")
    
    # URL 친화적인 파일명 (영문, 숫자, 하이픈만)
    safe_title = "".join([c if c.isalnum() or c.isspace() else "" for c in title]).strip().replace(" ", "-")
    filename = f"{OUTPUT_DIR}/{index:03d}-{safe_title}.md"
    
    # 카테고리에 따른 태그 자동 매핑
    tags = ["Insight", "BookNote"]
    cat_lower = category.lower()
    
    if "business" in cat_lower or "marketing" in cat_lower or "sales" in cat_lower:
        tags.extend(["Business", "Strategy"])
    if "mindset" in cat_lower or "philosophy" in cat_lower:
        tags.extend(["Mindset", "Wisdom"])
    if "health" in cat_lower or "biohacking" in cat_lower:
        tags.extend(["Health", "Biohacking"])
    if "parenting" in cat_lower:
        tags.append("Parenting")
    
    # 중복 태그 제거 및 포맷팅
    tags = list(set(tags))
    tag_str = ", ".join([f'"{t}"' for t in tags])

    # MD 내용 작성
    md_content = f"""---
title: "{title.strip()}"
date: {date_str}
draft: false
categories: ["Intellectual Archive"]
tags: [{tag_str}]
---

{body.strip()}

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
            print(f"Warning: {input_file} not found. Skipping.")
            continue
            
        print(f"Processing {input_file}...")
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            if "|||" in line:
                parts = line.split("|||")
                if len(parts) >= 3:
                    title = parts
                    category = parts[11]
                    body_part = parts[23]
                    
                    # 소스 인용구 분리 (예: [1], [2])
                    if "[" in body_part:
                        body_text = body_part.split("[")
                        source_refs = "[" + body_part.split("[", 1)[11]
                    else:
                        body_text = body_part
                        source_refs = "BookNote Archive"
                        
                    create_hugo_post(total_count, title, category, body_text, source_refs.strip())
                    total_count += 1

    print(f"\nSuccessfully generated {total_count-1} posts!")

if __name__ == "__main__":
    main()
