from fastmcp import FastMCP
from typing import List, Optional, Any
from mcp.types import TextContent
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
import asyncio

# Initialize MCP (no API key required)
mcp = FastMCP("GoogleAnalyticsMCP", require_api_key=False)

# Google Analytics credentials and property ID
GA_CREDENTIALS = {
    "client_email": "",
    "private_key": "",
    "token_uri": ""
}
PROPERTY_ID = ""
analytics = None  # Will be initialized in main
valid_dimension_names = set()  # To be fetched dynamically

def format_ga_response(response: Any) -> List[TextContent]:
    """Format GA API response to a list of TextContent."""
    if not hasattr(response, "rows") or not response.rows:
        return [TextContent(type="text", text="No data found")]
    headers = [d.name for d in response.dimension_headers] + [m.name for m in response.metric_headers]
    results = []
    for row in response.rows:
        dims = [v.value for v in row.dimension_values]
        mets = [v.value for v in row.metric_values]
        results.append(TextContent(
            type="text",
            text=", ".join(f"{k}: {v}" for k, v in zip(headers, dims + mets))
        ))
    return results

def build_filter_expression(filters: Optional[Dict[str, str]]) -> Optional[FilterExpression]:
    """
    Build a GA4 FilterExpression from a dict of filters.
    Each filter is a dimension name and value (string equality).
    """
    if not filters:
        return None
    filter_list = [
        Filter(
            field_name=k,
            string_filter=Filter.StringFilter(value=str(v))
        )
        for k, v in filters.items()
        if k in valid_dimension_names
    ]
    if not filter_list:
        return None
    if len(filter_list) == 1:
        return FilterExpression(filter=filter_list[0])
    else:
        return FilterExpression(
            and_group=FilterExpression.AndGroup(
                expressions=[FilterExpression(filter=f) for f in filter_list]
            )
        )

@mcp.tool(description="Get 1-day active users metric for a date range with dynamic dimensions and filters.")
async def get_1_day_active_users(
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None,
    filters: Optional[Dict[str, str]] = None
) -> List[TextContent]:
    try:
        valid_dimensions = [d for d in (dimensions or []) if d in valid_dimension_names]
        filter_expr = build_filter_expression(filters) if filters else None

        response = analytics.run_report(
            request={
                "property": f"properties/{PROPERTY_ID}",
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "metrics": [{"name": "active1DayUsers"}],
                "dimensions": [{"name": d} for d in valid_dimensions] if valid_dimensions else [],
                "dimension_filter": filter_expr,
            }
        )

        return format_ga_response(response)
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

@mcp.tool(description="Get 7-day active users metric for a date range with dynamic dimensions and filters.")
async def get_7_day_active_users(
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None,
    filters: Optional[Dict[str, str]] = None
) -> List[TextContent]:
    try:
        valid_dimensions = [d for d in (dimensions or []) if d in valid_dimension_names]
        filter_expr = build_filter_expression(filters) if filters else None

        response = analytics.run_report(
            request={
                "property": f"properties/{PROPERTY_ID}",
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "metrics": [{"name": "active7DayUsers"}],
                "dimensions": [{"name": d} for d in valid_dimensions] if valid_dimensions else [],
                "dimension_filter": filter_expr,
            }
        )

        return format_ga_response(response)
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

@mcp.tool(description="Get 28-day active users metric for a date range with dynamic dimensions and filters.")
async def get_28_day_active_users(
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None,
    filters: Optional[Dict[str, str]] = None
) -> List[TextContent]:
    try:
        valid_dimensions = [d for d in (dimensions or []) if d in valid_dimension_names]
        filter_expr = build_filter_expression(filters) if filters else None

        response = analytics.run_report(
            request={
                "property": f"properties/{PROPERTY_ID}",
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "metrics": [{"name": "active28DayUsers"}],
                "dimensions": [{"name": d} for d in valid_dimensions] if valid_dimensions else [],
                "dimension_filter": filter_expr,
            }
        )

        return format_ga_response(response)
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

if __name__ == "__main__":
    # Initialize Google Analytics client with service account credentials
    ga_credentials = service_account.Credentials.from_service_account_info(GA_CREDENTIALS)
    analytics = BetaAnalyticsDataClient(credentials=ga_credentials)

    # Fetch and cache valid dimension names dynamically from GA metadata
    metadata = analytics.get_metadata(name=f"properties/{PROPERTY_ID}/metadata")
    valid_dimension_names = {d.api_name for d in metadata.dimensions}

    print(f"Valid dimensions fetched: {valid_dimension_names}")

    asyncio.run(mcp.run_sse_async(host="0.0.0.0", port=8080))
