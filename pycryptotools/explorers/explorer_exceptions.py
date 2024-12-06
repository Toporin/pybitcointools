

class DataFetcherError(Exception):
    """Custom exception for data fetching errors"""
    INVALID_URL = "Invalid URL"
    MISSING_DATA = "Missing Data"