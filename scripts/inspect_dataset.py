"""Inspect NYC DOT Traffic Speeds dataset availability and coverage."""

import json
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://data.cityofnewyork.us/resource/i4gi-tjb9.json"

QUERIES = {
    "Sample records": (
        "SELECT link_id, data_as_of, speed, travel_time, status, borough "
        "ORDER BY data_as_of DESC LIMIT 5"
    ),
    "Recent daily coverage": (
        "SELECT date_trunc_ymd(data_as_of) AS day, "
        "count(*) AS records, "
        "count(distinct link_id) AS road_segments "
        "WHERE data_as_of >= '2026-10-01T00:00:00' "
        "GROUP BY day ORDER BY day"
    ),
    "Historical sample": (
        "SELECT link_id, data_as_of, speed "
        "WHERE data_as_of >= '2025-10-01T00:00:00' "
        "AND data_as_of < '2025-10-02T00:00:00' "
        "LIMIT 5"
    ),
        "Historical daily coverage": (
        "SELECT date_trunc_ymd(data_as_of) AS day, "
        "count(*) AS records, "
        "count(distinct link_id) AS road_segments "
        "WHERE data_as_of >= '2025-10-01T00:00:00' "
        "AND data_as_of < '2025-10-08T00:00:00' "
        "GROUP BY day ORDER BY day"
    ),
    "Recent status distribution": (
        "SELECT status, count(*) AS records "
        "WHERE data_as_of >= '2026-10-01T00:00:00' "
        "AND data_as_of < '2026-10-08T00:00:00' "
        "GROUP BY status ORDER BY records DESC"
    ),
}


def execute_query(query):
    params = urllib.parse.urlencode({"$query": query})
    request = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={"User-Agent": "FlowCast-Research/1.0"},
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def main():
    print("FlowCast — NYC DOT Dataset Inspection")
    print("=" * 45)

    for name, query in QUERIES.items():
        print(f"\n{name}")
        print("-" * 45)

        try:
            result = execute_query(query)
            print(json.dumps(result, indent=2))
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"Request failed: {error}")
        except Exception as error:
            print(f"Unexpected error: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
