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

@mcp.tool(description="Get 1-day active users metric for a date range with supported dimensions.")
async def get_1_day_active_users(
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None
) -> List[TextContent]:
    """
    Fetches the 1-day active users metric (active1DayUsers) for the specified date range,
    optionally grouped by supported dimensions.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        dimensions (Optional[List[str]]): List of dimensions to group by.

    Returns:
        List[TextContent]: Formatted analytics response or error message.
    """
    # Comprehensive list of officially supported dimensions for active1DayUsers
    supported_dimensions = {
        # Date & Time
        "date", "dayOfWeek", "week", "month", "year",
        # Geography
        "country", "region", "city", "continent",
        # Device/Platform
        "platform", "deviceCategory", "operatingSystem", "browser", "screenResolution",
        # User
        "language", "newVsReturning", "userType",
        # Traffic Source
        "source", "medium", "campaignName", "defaultChannelGroup",
        "sessionSource", "sessionMedium", "sessionCampaignName",
        # App-specific
        "appVersion", "screenName", "screenClass"
    }

    try:
        # Filter only valid dimensions
        valid_dimensions = [d for d in (dimensions or []) if d in supported_dimensions]

        response = analytics.run_report(
            request={
                "property": f"properties/{PROPERTY_ID}",
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "metrics": [{"name": "active1DayUsers"}],
                "dimensions": [{"name": d} for d in valid_dimensions] if valid_dimensions else [],
            }
        )

        return format_ga_response(response)

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    
@mcp.tool(description="Get 28-day active users metric for a date range with supported dimensions.")
async def get_28_day_active_users(
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None
) -> List[TextContent]:
    """
    Fetches the 28-day active users metric (active28DayUsers) for the specified date range,
    optionally grouped by supported dimensions.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        dimensions (Optional[List[str]]): List of dimensions to group by.

    Returns:
        List[TextContent]: Formatted analytics response or error message.
    """
    global analytics

    # Comprehensive list of officially supported dimensions for active28DayUsers
    supported_dimensions = {
        # Date & Time
        "date", "dayOfWeek", "week", "month", "year",
        # Geography
        "country", "region", "city", "continent",
        "countryId", "regionId", "cityId",
        # Device/Platform
        "platform", "deviceCategory", "operatingSystem", "operatingSystemVersion",
        "browser", "browserVersion", "screenResolution",
        "deviceBrand", "deviceModel",
        # User
        "language", "newVsReturning", "userType",
        # Traffic Source
        "source", "medium", "campaignName", "defaultChannelGroup",
        "sessionSource", "sessionMedium", "sessionCampaignName",
        # App-specific
        "appVersion", "screenName", "screenClass",
        # Audience
        "audienceName",
        # Web content
        "pagePath", "pageTitle",
        # Event
        "eventName"
    }

    try:
        # Filter only valid dimensions
        valid_dimensions = [d for d in (dimensions or []) if d in supported_dimensions]

        response = analytics.run_report(
            request={
                "property": f"properties/{PROPERTY_ID}",
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "metrics": [{"name": "active28DayUsers"}],
                "dimensions": [{"name": d} for d in valid_dimensions] if valid_dimensions else [],
            }
        )

        # Handle empty response gracefully
        if not getattr(response, "rows", None):
            return [TextContent(type="text", text="No data found for the given parameters.")]

        return format_ga_response(response)

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    
@mcp.tool(description="Get 7-day active users metric for a date range with supported dimensions.")
async def get_7_day_active_users(
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None
) -> List[TextContent]:
    """
    Fetches the 7-day active users metric (active7DayUsers) for the specified date range,
    optionally grouped by supported dimensions.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        dimensions (Optional[List[str]]): List of dimensions to group by.

    Returns:
        List[TextContent]: Formatted analytics response or error message.
    """
    global analytics

    # Comprehensive list of officially supported dimensions for active7DayUsers
    supported_dimensions = {
        # Date & Time
        "date", "dayOfWeek", "week", "month", "year",

        # Geography
        "continent", "country", "region", "city",

        # Device/Platform
        "platform", "deviceCategory", "mobileDeviceBranding", "mobileDeviceMarketingName",
        "operatingSystem", "operatingSystemVersion", "browser", "screenResolution",

        # App/Screen
        "appVersion", "unifiedScreenName", "unifiedScreenClass", "streamId", "streamName",

        # User properties
        "language", "newVsReturning", "signedInWithUserId", "userId",

        # Acquisition
        "firstUserSource", "firstUserMedium", "firstUserCampaignName",
        "firstUserDefaultChannelGroup", "firstUserGoogleAdsAccountName",
        "source", "medium", "campaignName", "defaultChannelGroup",

        # Session acquisition
        "sessionSource", "sessionMedium", "sessionCampaignName"
    }

    try:
        # Filter only valid dimensions
        valid_dimensions = [d for d in (dimensions or []) if d in supported_dimensions]

        response = analytics.run_report(
            request={
                "property": f"properties/{PROPERTY_ID}",
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "metrics": [{"name": "active7DayUsers"}],
                "dimensions": [{"name": d} for d in valid_dimensions] if valid_dimensions else [],
            }
        )

        # Handle empty response gracefully
        if not getattr(response, "rows", None):
            return [TextContent(type="text", text="No data found for the given parameters.")]

        return format_ga_response(response)

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

@mcp.tool(description="Get active users metric for a date range.")
async def get_active_users(
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None
) -> List[TextContent]:
    """
    Fetches the active users metric (activeUsers) for the specified date range,
    optionally grouped by supported dimensions.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        dimensions (Optional[List[str]]): List of dimensions to group by.

    Returns:
        List[TextContent]: Formatted analytics response or error message.
    """
    global analytics

    # ✅ Officially compatible dimensions with 'activeUsers'
    supported_dimensions = {
        # Time-based
        "date", "dayOfWeek", "week", "month", "year",

        # Geo
        "continent", "country", "region", "city",

        # Device/Platform
        "platform", "deviceCategory", "mobileDeviceBranding", "mobileDeviceMarketingName",
        "operatingSystem", "browser", "screenResolution",

        # App/Screen
        "appVersion", "unifiedScreenName", "unifiedScreenClass", "streamId", "streamName",

        # User properties
        "language", "newVsReturning", "signedInWithUserId", "userId",

        # Acquisition
        "firstUserSource", "firstUserMedium", "firstUserCampaignName",
        "firstUserDefaultChannelGroup", "firstUserGoogleAdsAccountName",
        "source", "medium", "campaignName", "defaultChannelGroup",

        # Session acquisition
        "sessionSource", "sessionMedium", "sessionCampaignName"
    }

    try:
        valid_dimensions = [d for d in (dimensions or []) if d in supported_dimensions]

        response = analytics.run_report(
            request={
                "property": f"properties/{PROPERTY_ID}",
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "metrics": [{"name": "activeUsers"}],
                "dimensions": [{"name": d} for d in valid_dimensions] if valid_dimensions else [],
            }
        )

        return format_ga_response(response)

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

@mcp.tool(description="Get ad unit exposure metric for a date range.")
async def get_ad_unit_exposure(
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None
) -> List[TextContent]:
    """
    Fetches the ad unit exposure metric (adUnitExposure) for the specified date range,
    optionally grouped by supported dimensions.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        dimensions (Optional[List[str]]): List of dimensions to group by.

    Returns:
        List[TextContent]: Formatted analytics response or error message.
    """
    global analytics

    # ✅ Officially supported dimensions for 'adUnitExposure'
    supported_dimensions = {
        # Ad-related
        "adUnitName", "adFormat", "adSourceName",

        # Platform/Device/App
        "platform", "appVersion", "deviceCategory", "operatingSystem",
        "mobileDeviceBranding", "mobileDeviceMarketingName",

        # Geo/User
        "country", "region", "city", "language",

        # Time-based
        "date"
    }

    try:
        valid_dimensions = [d for d in (dimensions or []) if d in supported_dimensions]

        response = analytics.run_report(
            request={
                "property": f"properties/{PROPERTY_ID}",
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "metrics": [{"name": "adUnitExposure"}],
                "dimensions": [{"name": d} for d in valid_dimensions] if valid_dimensions else [],
            }
        )

        return format_ga_response(response)

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

if __name__ == "__main__":
    # Initialize Google Analytics client with service account credentials
    ga_credentials = service_account.Credentials.from_service_account_info(GA_CREDENTIALS)
    analytics = BetaAnalyticsDataClient(credentials=ga_credentials)
    asyncio.run(mcp.run_sse_async(host="0.0.0.0", port=8080))