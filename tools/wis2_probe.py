#!/usr/bin/env python3
"""WIS2 探测：珠峰周边有哪些气象站在实时推送（中国气象局 + 尼泊尔水文气象局）。

做什么：连上世界气象组织 WIS2 的全球代理（公开账号 everyone/everyone），订阅两国的地面天气观测（SYNOP），
跑一段时间；对每条通知，若带坐标且在范围内、或者没带坐标，就下载数据文件（BUFR），解码出站号、坐标、海拔、时间、气温，
只保留在范围内的站。结束时打印一张表，并写出 probe_result.json。只读，不发送任何东西。

安装：  pip install eccodes paho-mqtt
运行：  python wis2_probe.py                 （默认 190 分钟：中国每小时一次、尼泊尔每 3 小时一次，跑够一轮）
        python wis2_probe.py --minutes 20    （先试试能不能连上）
可选：  --bbox 西 南 东 北（默认 85.5 27.3 88.0 29.3，珠峰周边约 250 km）
        --broker gb.wis.cma.cn               （默认按顺序尝试：中国、法国、美国、巴西的全球代理）
        --max-downloads 400                  （没带坐标的通知要下载文件才知道是哪个站，这里限个总数，礼貌一点）

格式依据：WIS2 通知消息标准（geometry 可为 null；数据链接 rel=canonical；integrity 为 sha256 等）；
主题来自 WIS2 发现目录：cn-cma 每小时、np-nepalmet 每 3 小时，数据政策都是 core（免费、不限制）。
未实测：写脚本的环境连不上 WIS2，所以连接和真实文件都没跑过；解码部分用自己生成的 SYNOP BUFR 测过。
"""
import argparse, base64, hashlib, json, os, queue, ssl, sys, threading, time, urllib.request
from datetime import datetime, timezone

TOPICS = {"cn-cma": "cache/a/wis2/cn-cma/data/core/weather/surface-based-observations/synop",
          "np-nepalmet": "cache/a/wis2/np-nepalmet/data/core/weather/surface-based-observations/synop"}
BROKERS = ["gb.wis.cma.cn", "globalbroker.meteo.fr", "wis2globalbroker.nws.noaa.gov", "globalbroker.inmet.gov.br"]
MISSING = 1e30


def in_bbox(lon, lat, b):
    return lon is not None and lat is not None and b[0] <= lon <= b[2] and b[1] <= lat <= b[3]


def centre_of(topic):
    for k, t in TOPICS.items():
        if topic.startswith(t[: t.index("/data/")]):
            return k
    return "?"


def wanted(msg, bbox):
    """通知 -> (要不要下载, 原因)。带点坐标且在范围内：要；带坐标但不在：不要；没坐标：要（只能下载后看）。"""
    g = msg.get("geometry")
    if g and g.get("type") == "Point":
        lon, lat = g["coordinates"][:2]
        return (in_bbox(lon, lat, bbox), "point")
    if g and g.get("type") == "Polygon":
        xs = [c[0] for c in g["coordinates"][0]]; ys = [c[1] for c in g["coordinates"][0]]
        hit = not (max(xs) < bbox[0] or min(xs) > bbox[2] or max(ys) < bbox[1] or min(ys) > bbox[3])
        return (hit, "polygon")
    return (True, "null")


def canonical(msg):
    for l in msg.get("links", []):
        if l.get("rel") == "canonical":
            return l.get("href")


def check_integrity(data, msg):
    it = (msg.get("properties") or {}).get("integrity")
    if not it:
        return None
    m = it.get("method", "").replace("-", "_")
    if m not in hashlib.algorithms_available:
        return None
    return base64.b64encode(hashlib.new(m, data).digest()).decode() == it.get("value")


def _arr(h, key):
    import eccodes
    try:
        v = eccodes.codes_get_array(h, key)
        return list(v)
    except Exception:
        return []


def decode_synop(data):
    """BUFR 字节 -> 观测列表（每个子集一条）。缺测值（eccodes 用 CODES_MISSING_*）记为 None。"""
    import eccodes
    out = []
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".bufr", delete=False) as f:
        f.write(data); path = f.name
    try:
        with open(path, "rb") as fh:
            while True:
                h = eccodes.codes_bufr_new_from_file(fh)
                if h is None:
                    break
                try:
                    eccodes.codes_set(h, "unpack", 1)
                    n = eccodes.codes_get(h, "numberOfSubsets")
                    def col(key, cast=float):
                        a = _arr(h, key)
                        if len(a) == 1 and n > 1:
                            a = a * n
                        a = (a + [None] * n)[:n]
                        return [None if (x is None or (isinstance(x, (int, float)) and abs(x) >= 1e9) or x == eccodes.CODES_MISSING_LONG) else cast(x) for x in a]
                    blk, sta = col("blockNumber", int), col("stationNumber", int)
                    lat, lon = col("latitude"), col("longitude")
                    z = col("heightOfStationGroundAboveMeanSeaLevel")
                    t = col("airTemperature")
                    yy, mo, dd, hh, mi = (col(k, int) for k in ("year", "month", "day", "hour", "minute"))
                    try:
                        names = list(eccodes.codes_get_string_array(h, "stationOrSiteName"))
                    except Exception:
                        names = []
                    names = (names + [""] * n)[:n]
                    for i in range(n):
                        wmo = "%02d%03d" % (blk[i], sta[i]) if blk[i] is not None and sta[i] is not None else None
                        ts = "%04d-%02d-%02dT%02d:%02d:00Z" % (yy[i], mo[i], dd[i], hh[i], mi[i] or 0) if None not in (yy[i], mo[i], dd[i], hh[i]) else None
                        out.append(dict(wmo=wmo, name=(names[i] or "").strip(), lat=lat[i], lon=lon[i], z=z[i], time=ts,
                                        t_c=None if t[i] is None else round(t[i] - 273.15, 1)))
                finally:
                    eccodes.codes_release(h)
    finally:
        os.unlink(path)
    return out


class Probe:
    def __init__(self, bbox, max_dl, out):
        self.bbox, self.max_dl, self.out = bbox, max_dl, out
        self.q = queue.Queue()
        self.stats = {k: dict(notifications=0, with_point=0, null_geometry=0, downloaded=0, decode_errors=0, integrity_fail=0) for k in TOPICS}
        self.stations = {}
        self.dl = 0
        self.lock = threading.Lock()

    def on_notification(self, topic, payload):
        try:
            msg = json.loads(payload)
        except ValueError:
            return
        c = centre_of(topic)
        if c not in self.stats:
            return
        s = self.stats[c]; s["notifications"] += 1
        want, why = wanted(msg, self.bbox)
        s["with_point" if why == "point" else "null_geometry" if why == "null" else "with_point"] += 0 if why == "polygon" else 1
        if not want:
            return
        with self.lock:
            if self.dl >= self.max_dl:
                return
            self.dl += 1
        self.q.put((c, msg))

    def worker(self):
        while True:
            c, msg = self.q.get()
            url = canonical(msg)
            if not url:
                continue
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "everest-wis2-probe/0.1"}), timeout=60) as r:
                    data = r.read()
            except Exception as e:
                print("  下载失败 %s: %s" % (url[:80], e), flush=True); continue
            s = self.stats[c]; s["downloaded"] += 1
            if check_integrity(data, msg) is False:
                s["integrity_fail"] += 1; continue           # 校验不过的文件不用
            try:
                obs = decode_synop(data)
            except Exception:
                s["decode_errors"] += 1; continue
            for o in obs:
                if not in_bbox(o["lon"], o["lat"], self.bbox):
                    continue
                k = o["wmo"] or "%s,%s" % (o["lat"], o["lon"])
                with self.lock:
                    st = self.stations.setdefault(k, dict(centre=c, wmo=o["wmo"], name=o["name"], lat=o["lat"], lon=o["lon"], z=o["z"], reports=0, last_time=None, last_t_c=None,
                                                          wigos=(msg.get("properties") or {}).get("wigos_station_identifier")))
                    st["reports"] += 1
                    if o["time"] and (st["last_time"] is None or o["time"] > st["last_time"]):
                        st["last_time"], st["last_t_c"] = o["time"], o["t_c"]
                print("  ✓ %s %s %s  %.3f,%.3f  %sm  %s  %s°C" % (c, o["wmo"], o["name"], o["lat"], o["lon"], o["z"], o["time"], o["t_c"]), flush=True)

    def report(self):
        res = dict(generated_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"), bbox=self.bbox, stats=self.stats,
                   stations=sorted(self.stations.values(), key=lambda x: (x["centre"], -(x["z"] or 0))))
        json.dump(res, open(self.out, "w"), ensure_ascii=False, indent=1)
        print("\n=== 结果 ===")
        for c, s in self.stats.items():
            print("%-12s 通知 %d（带坐标 %d / 无坐标 %d），下载 %d，解码失败 %d，校验失败 %d" % (c, s["notifications"], s["with_point"], s["null_geometry"], s["downloaded"], s["decode_errors"], s["integrity_fail"]))
        if not self.stations:
            print("范围内没有收到任何站。可能：跑的时间不够、该国没有在这个范围内的站、或下载上限太低。")
        for st in res["stations"]:
            print("%-12s %-6s %-20s %8.3f %8.3f %6sm  %3d 条  最新 %s  %s°C" % (st["centre"], st["wmo"], st["name"][:20], st["lat"], st["lon"], st["z"], st["reports"], st["last_time"], st["last_t_c"]))
        print("已写出 %s —— 把这个文件发给我。" % self.out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=190)
    ap.add_argument("--bbox", nargs=4, type=float, default=[85.5, 27.3, 88.0, 29.3])
    ap.add_argument("--broker")
    ap.add_argument("--max-downloads", type=int, default=400)
    ap.add_argument("--out", default="probe_result.json")
    a = ap.parse_args(argv)
    import paho.mqtt.client as mqtt
    p = Probe(a.bbox, a.max_downloads, a.out)
    for _ in range(3):
        threading.Thread(target=p.worker, daemon=True).start()
    brokers = [a.broker] if a.broker else BROKERS
    cli = None
    for b in brokers:
        c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="everest-probe-%d" % os.getpid(), clean_session=True)
        c.username_pw_set("everyone", "everyone")
        c.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        c.on_connect = lambda cl, u, f, rc, pr: [cl.subscribe(t, qos=0) for t in TOPICS.values()] and print("已连接，已订阅：%s" % ", ".join(TOPICS), flush=True)
        c.on_message = lambda cl, u, m: p.on_notification(m.topic, m.payload)
        try:
            print("连接 %s:8883 …" % b, flush=True)
            c.connect(b, 8883, keepalive=60)
            cli = c; break
        except Exception as e:
            print("  连不上 %s：%s" % (b, e), flush=True)
    if not cli:
        sys.exit("所有全球代理都连不上：检查网络/防火墙是否放行 8883 端口。")
    cli.loop_start()
    end = time.time() + a.minutes * 60
    try:
        while time.time() < end:
            time.sleep(30)
            print("[%s] 收到通知：%s；范围内站 %d" % (datetime.now().strftime("%H:%M"), {k: v["notifications"] for k, v in p.stats.items()}, len(p.stations)), flush=True)
    except KeyboardInterrupt:
        print("\n提前结束。")
    cli.loop_stop(); cli.disconnect()
    time.sleep(2)
    p.report()


if __name__ == "__main__":
    main()
