"""Cloud-only Sentinel-1 discovery through Copernicus Data Space OData."""
import datetime as _dt
import requests

CDSE_PRODUCTS = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
EVEREST_BBOX = "POLYGON ((86.55 27.72, 87.05 27.72, 87.05 28.10, 86.55 28.10, 86.55 27.72))"


def discover_sentinel1_slc_pair(days_back=60):
    """Return the newest two AOI-intersecting Sentinel-1 SLC products.

    This only discovers remote products; it never downloads SAFE archives.
    Downstream processing must provide a matching cloud InSAR result.
    """
    since = (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%SZ")
    area = f"geography'SRID=4326;{EVEREST_BBOX}'"
    filt = (
        "Collection/Name eq 'SENTINEL-1' and "
        f"OData.CSC.Intersects(area={area}) and "
        "(startswith(Name,'S1A_IW_SLC') or startswith(Name,'S1B_IW_SLC') "
        "or startswith(Name,'S1C_IW_SLC') or startswith(Name,'S1D_IW_SLC')) and "
        f"ContentDate/Start ge {since}"
    )
    params = {"$filter": filt, "$orderby": "ContentDate/Start desc", "$top": "50"}
    response = requests.get(CDSE_PRODUCTS, params=params, headers={"User-Agent": "Everest-Pipeline/5.1", "Accept": "application/json"}, timeout=45)
    response.raise_for_status()
    products = response.json().get("value", [])
    if len(products) < 2:
        raise RuntimeError(f"CDSE returned only {len(products)} AOI Sentinel-1 SLC product(s); refusing stale fallback")
    unique = {}
    for p in products:
        start = p.get("ContentDate", {}).get("Start")
        if start and start[:10] not in unique:
            unique[start[:10]] = {
                "id": p.get("Id"), "name": p.get("Name"), "date": start[:10],
                "content_start": start, "s3_path": p.get("S3Path"),
                "online": p.get("Online"), "footprint": p.get("GeoFootprint")
            }
    if len(unique) < 2:
        raise RuntimeError("CDSE returned fewer than two distinct acquisition dates; refusing stale fallback")
    pair = list(unique.values())[:2]
    return {"latest": pair[0], "previous": pair[1], "source": "Copernicus Data Space OData Products", "query_type": "AOI_INTERSECTING_SENTINEL1_SLC"}