from scholarly import scholarly
import json
import os
from datetime import datetime


def main():
    # 从环境变量里读你的 Google Scholar ID
    scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID")
    if not scholar_id:
        raise RuntimeError("Environment variable GOOGLE_SCHOLAR_ID is not set.")

    # 用 ID 直接获取作者
    # 你的 workflow 里已经设置了 GOOGLE_SCHOLAR_ID: ${{ secrets.GOOGLE_SCHOLAR_ID }}
    author = scholarly.search_author_id(scholar_id)

    # 填充作者的详细信息
    scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

    # 加一个更新时间字段
    author["updated"] = datetime.utcnow().isoformat()

    # 把 publications 改成 {author_pub_id: publication} 这种字典结构（跟模板一致）
    author["publications"] = {
        pub["author_pub_id"]: pub for pub in author.get("publications", [])
    }

    # 输出到 results/gs_data.json
    os.makedirs("results", exist_ok=True)
    with open("results/gs_data.json", "w", encoding="utf-8") as f:
        json.dump(author, f, ensure_ascii=False, indent=2)

    # 顺便再生成一个给 badge 用的简化版（可有可无，看你需不需要）
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": f"{author.get('citedby', '0')}",
    }
    with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
        json.dump(shieldio_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
