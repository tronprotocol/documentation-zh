import os
import shutil
import re
import time
import requests
from git import Repo
import frontmatter

# --- Configuration ---
TIPS_REPO_URL = "https://github.com/tronprotocol/tips.git"
TMP_DIR = "./.tmp_tips_repo"
DEST_DIR = "docs/developers/tips"

# 1. Hardcoded Manual Map for known contributors
MANUAL_AUTHOR_MAP = {
    "getty.io": "dbuarque([@dbuarque](https://github.com/dbuarque))",
    "jiangyangyang@tron.network": "jiangyy0824([@jiangyy0824](https://github.com/jiangyy0824))",
    "nanfengpo@hotmail.com": "nanfengpo([@nanfengpo](https://github.com/nanfengpo))",
    "zhaohong2292@gmail.com": "zhaohong([@zhaohong](https://github.com/zhaohong))",
    "liangzhiyan@tron.network": "lvs007([@lvs007](https://github.com/lvs007))",
    "@ithinker1991": "yinshucheng([@yinshucheng](https://github.com/yinshucheng))",
    "jiangxinjian@tron.network": "BlueHoopor([@BlueHoopor](https://github.com/BlueHoopor))",
    "xing@tron.network": "billtron([@billtron](https://github.com/billtron))",
    "federico.zhen@tron.network": "Federico2014([@Federico2014](https://github.com/Federico2014))",
    "leo.hou@tron.network": "Federico2014([@Federico2014](https://github.com/Federico2014))",
    "liu.sean@tron.network": "renchenchang([@renchenchang](http://github.com/renchenchang))",
    "neo.hong@tron.network": "Lredhdx([@Lredhdx](https://github.com/Lredhdx))",
    "kiven.liang@tron.network": "lvs007([@lvs007](https://github.com/lvs007))",
    "andy.zhang@tron.network": "zhang0125([@zhang0125](https://github.com/zhang0125))",
    "wb_bupt@163.com": "xxo1shine([@xxo1shine](https://github.com/xxo1shine))",
    "lucas.wu@tron.network": "xxo1shine([@xxo1shine](https://github.com/xxo1shine))",
    "lxcmyf@gmail.com": "lxcmyf([@lxcmyf](https://github.com/lxcmyf))",
    "raymondliu0711": "raymondliu0711([@raymondliu0711](https://github.com/raymondliu0711))",
    "cooperdepp90@outlook.com": "CooperDepp([@CooperDepp](https://github.com/CooperDepp))",
    "allen.cheng@tron.network": "jwrct([@jwrct](https://github.com/jwrct))",
    "lei19942016@hotmail.com": "raymondliu0711([@raymondliu0711](https://github.com/raymondliu0711))",
    "aaronluotron@gmail.com": "EllenWhitmore([@EllenWhitmore](https://github.com/EllenWhitmore))",
    "lopeed_prcy": "lopeed([@lopeed](https://github.com/lopeed))",
    "liang3885@hotmail.com": "raymondliu0711([@raymondliu0711](https://github.com/raymondliu0711))"
}

# 2. In-memory cache to prevent hitting GitHub API rate limits
GITHUB_CACHE = {}

def fetch_github_profile(email):
    """Fetch GitHub name, login, and html_url using the commit search API."""
    if email in GITHUB_CACHE:
        return GITHUB_CACHE[email]
        
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    try:
        search_url = f"https://api.github.com/search/commits?q=author-email:{email}"
        resp = requests.get(search_url, headers=headers, timeout=5)
        
        if resp.status_code == 403:
            print(f"--> GitHub API rate limit hit for {email}. Falling back to raw string.")
            GITHUB_CACHE[email] = None
            return None
            
        if resp.status_code == 200:
            data = resp.json()
            if data.get("total_count", 0) > 0 and data["items"][0].get("author"):
                login = data["items"][0]["author"]["login"]
                html_url = data["items"][0]["author"]["html_url"]
                
                user_url = data["items"][0]["author"]["url"]
                user_resp = requests.get(user_url, headers=headers, timeout=5)
                
                if user_resp.status_code == 200:
                    user_data = user_resp.json()
                    name = user_data.get("name") or login
                else:
                    name = login
                    
                formatted_str = f"{name}([@{login}]({html_url}))"
                GITHUB_CACHE[email] = formatted_str
                time.sleep(2) # Respect GitHub limits
                return formatted_str
                
    except Exception as e:
        print(f"--> Error fetching GitHub info for {email}: {e}")
        
    GITHUB_CACHE[email] = None
    return None

def process_authors(author_string):
    """Extract emails, check manual map, fetch GitHub profiles, and return formatted string."""
    if not author_string or author_string.lower() == "unknown":
        return "Unknown"
        
    parts = [p.strip() for p in author_string.split(',')]
    new_parts = []
    
    for part in parts:
        matched_manual = False
        
        for key, formatted_author in MANUAL_AUTHOR_MAP.items():
            if key.lower() in part.lower():
                new_parts.append(formatted_author)
                matched_manual = True
                break
                
        if matched_manual:
            continue
            
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', part)
        if email_match:
            email = email_match.group(0)
            gh_info = fetch_github_profile(email)
            if gh_info:
                new_parts.append(gh_info)
            else:
                new_parts.append(part)
        else:
            new_parts.append(part)
            
    return ", ".join(new_parts)

def sync_and_build():
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    print(f"Cloning repository: {TIPS_REPO_URL}...")
    Repo.clone_from(TIPS_REPO_URL, TMP_DIR, depth=1)

    # Safe cleanup mode
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
    else:
        for f in os.listdir(DEST_DIR):
            if f.startswith("tip-") or f.startswith("category-") or f == "index.md":
                file_path = os.path.join(DEST_DIR, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    source_tips_path = os.path.join(TMP_DIR, "tips")
    if not os.path.exists(source_tips_path):
        for alt_name in ["TIPs", "Tips"]:
            if os.path.exists(os.path.join(TMP_DIR, alt_name)):
                source_tips_path = os.path.join(TMP_DIR, alt_name)
                break
        else:
            source_tips_path = TMP_DIR
            
    print(f"Successfully located TIPs directory: {source_tips_path}")

    all_tips_data = []
    ignored_files = {"readme.md", "license.md", "template.md"}

    # Dynamically extract the relative folder path for GitHub URLs
    rel_folder = os.path.relpath(source_tips_path, TMP_DIR).replace("\\", "/")

    for filename in os.listdir(source_tips_path):
        if filename.endswith(".md") and filename.lower() not in ignored_files:
            src_path = os.path.join(source_tips_path, filename)
            
            with open(src_path, 'r', encoding='utf-8') as f:
                content_str = f.read()
            
            post = frontmatter.loads(content_str)
            metadata = post.metadata
            content = post.content

            if not metadata:
                for line in content.split('\n')[:20]:
                    if ':' in line and not line.startswith('#'):
                        k, v = line.split(':', 1)
                        metadata[k.strip().lower()] = v.strip().replace('"', '').replace("'", "")

            status = str(metadata.get("status", "Unknown")).strip()
            title = str(metadata.get("title", "Untitled")).strip()
            
            raw_author = str(metadata.get("author", "Unknown")).strip()
            processed_author = process_authors(raw_author)
            
            raw_type = str(metadata.get("type", "")).strip()
            raw_category = str(metadata.get("category", "")).strip()
            
            if raw_category and raw_category.lower() != "none":
                tip_category = raw_category
            elif raw_type and raw_type.lower() != "none":
                tip_category = raw_type
            else:
                tip_category = "Unknown"
            
            tip_id_raw = metadata.get("tip", filename)
            nums = re.findall(r'\d+', str(tip_id_raw))
            tip_id = nums[0] if nums else str(tip_id_raw)

            # Rebuild standardized Markdown for local search index
            new_post = frontmatter.Post(content, **metadata)
            new_post.metadata["tags"] = [status, tip_category]

            with open(os.path.join(DEST_DIR, filename), 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(new_post))

            # --- Modification: Change local link to GitHub repository link ---
            if rel_folder == ".":
                github_link = f"https://github.com/tronprotocol/tips/blob/master/{filename}"
            else:
                github_link = f"https://github.com/tronprotocol/tips/blob/master/{rel_folder}/{filename}"

            all_tips_data.append({
                "id": tip_id,
                "title": title,
                "author": processed_author,
                "status": status,
                "category": tip_category,
                "link": github_link  # Use GitHub URL here
            })

    generate_category_pages(all_tips_data)
    print("TIP pages and categories processing completed!")

def generate_category_pages(tips_data):
    preferred_category_order = ["Core", "Networking", "Interface", "TRC", "VM", "Informational"]
    all_categories = set(item['category'] for item in tips_data)
    
    categories = ["All"]
    for pref_cat in preferred_category_order:
        matched_cat = next((c for c in all_categories if c.lower() == pref_cat.lower()), None)
        if matched_cat:
            categories.append(matched_cat)
            all_categories.remove(matched_cat)
    
    categories.extend(sorted(list(all_categories)))
    print(f"--> Sorted TIP Categories: {categories}")

    for current_cat in categories:
        if current_cat == "All":
            filename = "index.md"
            filtered_tips = tips_data
        else:
            safe_cat_name = re.sub(r'[^a-zA-Z0-9]+', '-', current_cat.lower()).strip('-')
            filename = f"category-{safe_cat_name}.md"
            filtered_tips = [t for t in tips_data if t['category'] == current_cat]

        filepath = os.path.join(DEST_DIR, filename)

        status_dict = {}
        for item in filtered_tips:
            s = item['status']
            if s not in status_dict:
                status_dict[s] = []
            status_dict[s].append(item)

        preferred_status_order = ["Draft", "Last Call", "Accepted", "Final", "Deferred"]
        actual_statuses = list(status_dict.keys())
        ordered_statuses = []
        
        for pref_status in preferred_status_order:
            matched_status = next((s for s in actual_statuses if s.lower() == pref_status.lower()), None)
            if matched_status:
                ordered_statuses.append(matched_status)
                actual_statuses.remove(matched_status)
        
        ordered_statuses.extend(sorted(actual_statuses))

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("search:\n  boost: 2\n")
            f.write("---\n\n")
            f.write("# TRON Improvement Proposals (TIPs)\n\n")

            f.write("**类别:**\n\n")
            cat_links = []
            for cat in categories:
                if cat == "All":
                    cat_filename = "index.md"
                else:
                    safe_name = re.sub(r'[^a-zA-Z0-9]+', '-', cat.lower()).strip('-')
                    cat_filename = f"category-{safe_name}.md"
                
                btn_class = "{: .md-button .md-button--primary }" if cat == current_cat else "{: .md-button }"
                cat_links.append(f"[{cat}](./{cat_filename}){btn_class}")

            f.write(" ".join(cat_links) + "\n\n")

            if ordered_statuses:
                f.write("**快速跳转至状态:**\n\n")
                status_links = []
                for status in ordered_statuses:
                    anchor = status.lower().replace(" ", "-")
                    status_links.append(f"[{status}](#{anchor}){{: .md-button }}")
                f.write(" ".join(status_links) + "\n\n")

            f.write("---\n\n")

            for status in ordered_statuses:
                f.write(f"## {status}\n\n")
                f.write("| TIP | Title | Author | Category |\n")
                f.write("| :--- | :--- | :--- | :--- |\n")
                
                # --- Modification: Sort in Descending Order ---
                def sort_key(x):
                    nums = re.findall(r'\d+', str(x['id']))
                    # Return -1 for items without numbers so they stay at the bottom when reversed
                    return int(nums[0]) if nums else -1
                        
                # Added reverse=True to sort newest first
                sorted_items = sorted(status_dict[status], key=sort_key, reverse=True)
                
                for item in sorted_items:
                    f.write(f"| {item['id']} | [{item['title']}]({item['link']}) | {item['author']} | {item['category']} |\n")
                f.write("\n")

if __name__ == "__main__":
    sync_and_build()