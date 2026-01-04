import os
import datetime
import random

# 설정: 프로젝트 루트에서 실행한다고 가정
OUTPUT_DIR = "content/thought"
INPUT_FILES = ["data_business.txt", "data_mindset.txt", "data_life.txt"]

def create_hugo_post(index, title, category, body, source_refs):
    # 날짜 분산 (최근 60일 내 랜덤 배정 효과)
    days_ago = index % 60 
    dt = datetime.datetime.now() - datetime.timedelta(days=days_ago, hours=index%24)
    date_str = dt.strftime("%Y-%m-%dT%H:%M:%S-07:00")
    
    # [수정 핵심] title이 문자열인지 확실히 확인 후 공백 제거
    clean_title = str(title).strip()
    
    # 파일명 생성 (특수문자 제거 및 길이 제한)
    safe_title = "".join([c if c.isalnum() or c.isspace() else "" for c in clean_title]).strip().replace(" ", "-")
    safe_title = safe_title[:50]
    filename = f"{OUTPUT_DIR}/{index:03d}-{safe_title}.md"
    
    # 태그 자동 매핑
    tags = ["Insight", "BookNote"]
    cat_lower = str(category).lower().strip()
    
    if "business" in cat_lower or "trend" in cat_lower or "sales" in cat_lower:
        tags.extend(["Business", "Trend"])
    elif "mindset" in cat_lower or "philosophy" in cat_lower:
        tags.extend(["Mindset", "Wisdom"])
    elif "health" in cat_lower or "bio" in cat_lower:
        tags.extend(["Health", "Biohacking"])
    elif "parenting" in cat_lower:
        tags.append("Parenting")
    
    # 중복 태그 제거
    tags = list(set(tags))
    tag_str = ", ".join([f'"{t}"' for t in tags])

    # MD 내용 작성
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
    # 출력 폴더가 없으면 생성
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
        except FileExistsError:
            pass

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
                # 안전장치: 3덩어리 이상일 때만 처리
                if len(parts) >= 3:
                    # [여기입니다!] 인덱스 번호를 명확히 지정
                    title = parts      # 첫 번째 칸: 제목
                    category = parts[1]   # 두 번째 칸: 카테고리
                    body_part = parts[2]  # 세 번째 칸: 본문
                    
                    # 본문 내에 출처 표기([...])가 있는지 확인하여 분리
                    if "[" in body_part:
                        temp = body_part.split("[", 1) 
                        body_text = temp
                        source_refs = "[" + temp[1]
                    else:
                        body_text = body_part
                        source_refs = "BookNote Archive"
                        
                    create_hugo_post(total_count, title, category, body_text, source_refs.strip())
                    total_count += 1

    print(f"\nSuccessfully generated {total_count-1} posts!")

if __name__ == "__main__":
    main()
