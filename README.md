# Everest InSAR Autonomous Pipeline (珠峰 InSAR 全自动解算流水线)

[English](#english) | [中文说明](#chinese)

---

<a name="english"></a>
## English

An autonomous, cloud-native Sentinel-1 InSAR processing and Line-Of-Sight (LOS) displacement screening pipeline for Mount Everest glacier monitoring.

### Architecture: How Full Automation Works

```text
[ Daily Cron Trigger (UTC 02:00) ]
               │
               ▼
[ 1. Query CDSE STAC / OData API ] ──> Detects latest Sentinel-1D Track 12 Ascending overpass (every 12 days)
               │
               ▼
[ 2. Submit openEO Cloud InSAR Job ] ──> Serverless execution on ESA cloud (Burst 23790 IW1/VV)
               │
               ▼
[ 3. Adaptive Inversion Algorithm ] ──> Auto-locks bedrock anchor (Coherence > 0.96) & computes LOS mm displacement
               │
               ▼
[ 4. Automated Delivery & Sync ] ──> Automatically commits data and triggers the Windy plugin build
```

### Zero Local Environment Dependency
Anyone can fork this repository and run it out-of-the-box without setting up local GDAL/SNAP/Jupyter environments.
The entire workflow runs in GitHub Actions using official Copernicus openEO Python SDK.


### Connected Ecosystem Repositories (多仓联动架构)
This automated pipeline is part of the dual-engine Everest Glacier Monitoring System:
1. **[everest-insar-pipeline](https://github.com/Yizebaba/everest-insar-pipeline)** (Backend Engine): Autonomous overpass sensing, openEO InSAR processing, adaptive bedrock zero-displacement calibration, and LOS inversion.
2. **[hqmw-cryosphere-windy](https://github.com/Yizebaba/hqmw-cryosphere-windy)** (Frontend Visualization): Windy.com map plugin rendering verified bedrock anchor markers, displacement baselines, and candidate popups.

### Configuration (Repository Secrets)
To enable live autonomous processing, set the following secrets in GitHub Settings:
- `CDSE_USERNAME`: Your Copernicus Data Space Ecosystem username/email.
- `CDSE_PASSWORD`: Your Copernicus Data Space Ecosystem password.
- `GH_PAT`: GitHub Personal Access Token (for cross-repo dispatch to the Windy plugin).

---

<a name="chinese"></a>
## 中文说明

**珠穆朗玛峰 Sentinel-1 InSAR 与视线向（LOS）毫米级位移自动化处理流水线**。

### 为什么能做到“别人拿去填上账号就能全自动运行”？

1. **摆脱对本地和 JupyterLab 界面的硬依赖**：
   - 传统方案依赖云端 JupyterLab 手动点击，以及本地复杂的 C++ 遥感库；
   - 本项目将算法封装为轻量级无状态脚本 `pipeline.py`，全部利用欧空局官方 `openeo-python-client` 直接以 API 形式驱动云端超算。
2. **每天定时自动侦听新卫星数据（零人工干预）**：
   - GitHub Actions 每天 UTC 02:00（北京时间 10:00）自动启动；
   - 自动通过 STAC 接口检测过去 12 天内哨兵 1 号是否刚刚飞过珠峰；
   - 一旦发现新过境数据，自动向欧空局集群下发 InSAR 批处理任务并拉回解缠相位。
3. **自适应基岩锚点与位移闭环**：
   - 自动在网格中搜寻相干性最高的坚硬基底作为零形变锚点；
   - 自动换算毫米级位移并生成 JSON 摘要与矢量成果。


### 多仓全自动联动架构说明
本自动化流水线与前端展示插件已实现 100% 自动跨仓闭环：
1. **[everest-insar-pipeline](https://github.com/Yizebaba/everest-insar-pipeline)**（后端算力仓）：在卫星过境窗口期自动侦听、自动调用 openEO 集群干涉、自动完成基岩零形变平差与毫米位移解算；
2. **[hqmw-cryosphere-windy](https://github.com/Yizebaba/hqmw-cryosphere-windy)**（前端展示仓）：接收后端推送的最新位移数据，自动递增版本并打包发布到 Windy 官方节点，直接在地图上动态呈现基岩不动点与形变连线！

### 部署与使用方法
任何人只需 Fork 本仓库，并在 **Settings ➔ Secrets and variables ➔ Actions** 中填入：
- `CDSE_USERNAME`：欧空局 Copernicus 账号
- `CDSE_PASSWORD`：欧空局 Copernicus 密码
即可享受每天自动无人值守解算！

## 📦 Package Release & Agent Integration (软件包发布与 Agent 调用指南)

This project is officially packaged and published as a standard Python Wheel package (`everest-glacier-engine`), ready to be called directly by AI Agents, LangGraph, or custom CLI scripts.

### 1. Installation (安装)
Install directly from GitHub Release via `pip`:
```bash
pip install https://github.com/Yizebaba/everest-insar-pipeline/releases/download/v1.0.0/everest_glacier_engine-1.0.0-py3-none-any.whl
```
Or install via git repository:
```bash
pip install git+https://github.com/Yizebaba/everest-insar-pipeline.git
```

### 2. CLI Execution (命令行直接运行)
```bash
everest-glacier
```

### 3. Agent & Python Invocation (Agent 代码直接调用)
```python
from pipeline import run_displacement_inversion
from models.glavitu_rgi_bridge import GlaViTURGIBridge
from models.cloud_services_adapter import CloudGlacierVelocityService, CloudInSARSAMAdapter

# 1. Verify RGI 7.0 boundary
bridge = GlaViTURGIBridge()
in_glacier, name, debris_frac = bridge.verify_point_in_glacier(86.8585, 27.9868)
print(f"Glacier Name: {name}, Debris Fraction: {debris_frac}")

# 2. Query NASA ITS_LIVE baseline flow speed
its_service = CloudGlacierVelocityService()
its_meta = its_service.fetch_latest_itslive_metadata()
print(f"Khumbu baseline flow speed: {its_meta.get('benchmark_velocity_khumbu_m_yr')} m/yr")

# 3. Generate InSAR + SAM deformation region
sam = CloudInSARSAMAdapter()
feature = sam.generate_deformation_polygon_from_point(86.8585, 27.9868, disp_mm=0.66)
print(f"SAM Polygon Area: {feature['properties']['area_approx_km2']} km2")
```