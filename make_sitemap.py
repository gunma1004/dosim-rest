import os

base_url = "https://golmokrest.netlify.app"

# (url, changefreq, priority) 튜플을 담는 리스트
sitemap_entries = [
    (f"{base_url}/", "daily", "1.0")
]

area_dir = "area"
if os.path.exists(area_dir):
    for root, dirs, files in os.walk(area_dir):
        if "index.html" in files:
            # 윈도우 역슬래시(\)를 슬래시(/)로 변환
            rel_path = os.path.relpath(root, ".").replace("\\", "/").strip("/")
            
            # depth에 따른 우선순위 및 수집 주기 차등 부여
            path_parts = rel_path.split("/")
            
            if rel_path == "area":
                # /area/ (수도권 전체보기)
                changefreq = "daily"
                priority = "0.9"
            elif len(path_parts) == 3:
                # /area/{city}/{gu}/ (구 단위 페이지)
                changefreq = "weekly"
                priority = "0.8"
            else:
                # /area/{city}/{gu}/{dong}/ (동 단위 상세 페이지)
                changefreq = "monthly"
                priority = "0.6"

            url = f"{base_url}/{rel_path}/"
            sitemap_entries.append((url, changefreq, priority))

# 중복 제거 (URL 기준 고유값 유지)
seen_urls = set()
unique_entries = []
for entry in sitemap_entries:
    if entry[0] not in seen_urls:
        seen_urls.add(entry[0])
        unique_entries.append(entry)

# XML 문서 조합
xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for url, freq, prio in unique_entries:
    xml_lines.append("    <url>")
    xml_lines.append(f"        <loc>{url}</loc>")
    xml_lines.append(f"        <changefreq>{freq}</changefreq>")
    xml_lines.append(f"        <priority>{prio}</priority>")
    xml_lines.append("    </url>")

xml_lines.append('</urlset>')

# sitemap.xml 파일 저장
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines))

print(f"총 {len(unique_entries)}개의 정돈된 URL이 sitemap.xml에 성공적으로 생성되었습니다!")