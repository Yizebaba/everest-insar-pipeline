#!/usr/bin/env python3
"""从 Zenodo 取南坡气象站数据（Khadka 等，ESSD 2026，doi:10.5281/zenodo.18849098）。
先保存记录元数据（文件清单、许可、版本），再下载不超过 --max-mb 的文件并按记录里的 checksum 校验；
超过上限的只记在清单里不下载（GitHub 单文件上限 100 MB）。在 GitHub Actions 里跑。"""
import argparse, hashlib, json, os, sys, urllib.request

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "everest-zenodo-fetch/0.1"}), timeout=300) as r:
        return r.read()

ap = argparse.ArgumentParser()
ap.add_argument("--record", default="18849098")
ap.add_argument("--out", default="data/south_slope")
ap.add_argument("--max-mb", type=float, default=90)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
rec = json.loads(get("https://zenodo.org/api/records/%s" % a.record))
json.dump(rec, open(os.path.join(a.out, "zenodo_record.json"), "w"), ensure_ascii=False, indent=1)
files = rec.get("files") or []
print("记录：%s；许可：%s；文件 %d 个" % ((rec.get("metadata") or {}).get("title"), (rec.get("metadata") or {}).get("license"), len(files)))
log = []
for f in files:
    key, size = f.get("key"), f.get("size", 0)
    url = (f.get("links") or {}).get("self") or (f.get("links") or {}).get("content")
    ent = dict(key=key, size=size, checksum=f.get("checksum"), url=url)
    if size > a.max_mb * 1e6:
        ent["status"] = "SKIPPED_TOO_LARGE"; log.append(ent); print("跳过（太大）", key, size); continue
    data = get(url)
    algo, _, want = (f.get("checksum") or "").partition(":")
    ok = (hashlib.new(algo, data).hexdigest() == want) if want and algo in hashlib.algorithms_available else None
    if ok is False:
        ent["status"] = "CHECKSUM_FAIL"; log.append(ent); print("校验失败，丢弃", key); continue
    open(os.path.join(a.out, key), "wb").write(data)
    ent.update(status="OK", sha256=hashlib.sha256(data).hexdigest(), checksum_ok=ok); log.append(ent); print("已下载", key, size)
json.dump(log, open(os.path.join(a.out, "fetch_log.json"), "w"), ensure_ascii=False, indent=1)
