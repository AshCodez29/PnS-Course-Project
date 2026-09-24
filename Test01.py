# pip install pystac-client planetary-computer stackstac rioxarray
import pystac_client, planetary_computer as pc

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=pc.sign_inplace,
)
search = catalog.search(
    collections=["landsat-c2-l2"],
    bbox=[73.75, 18.40, 73.98, 18.63],      # rough Pune box
    datetime="2026-03-01/2026-04-30",
    query={"eo:cloud_cover": {"lt": 10},
           "platform": {"in": ["landsat-8", "landsat-9"]}},
)
items = list(search.items())
for i in items:
    print(i.id, i.properties["eo:cloud_cover"])