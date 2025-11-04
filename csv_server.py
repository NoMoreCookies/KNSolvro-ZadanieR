"""
CSV Reader MCP Server

Example usage:
- 'What droinks should i try?'
- 'What drinks contain ..."'
"""


from fastmcp import FastMCP
import pandas as pd
from pathlib import Path

mcp = FastMCP("drink_reader_server")

@mcp.tool()
def read_drinks() -> list:
    """Reads a CSV file and returns its contents as a dictionary."""
    file_path_resolved = Path(__file__).parent / "cocktails.csv"
    if not file_path_resolved.is_file():
        return {"error": f"File not found: {file_path_resolved} "}
    
    df = pd.read_csv(file_path_resolved)
    return df.columns.tolist()

@mcp.tool()
def get_column(column_name: str) -> list:
    """Returns the specified column from the CSV as a list."""
    file_path_resolved = Path(__file__).parent / "cocktails.csv"
    if not file_path_resolved.is_file():
       return {"error": f"File not found: {file_path_resolved} "}
    
    df = pd.read_csv(file_path_resolved)
    if column_name not in df.columns:
        return {"error": f"Column '{column_name}' not found in CSV."}
    
    return df[column_name].tolist()

@mcp.tool()
def filter_drinks_by_indgredient(ingredient: str) -> list:
    """Filters drinks by ingredient and returns matching rows."""
    file_path_resolved = Path(__file__).parent / "cocktails.csv"
    if not file_path_resolved.is_file():
        return {"error": f"Column '{column_name}' not found in CSV."}
    
    df = pd.read_csv(file_path_resolved)
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(ingredient, case=False).any(), axis=1)]
    return filtered_df.to_dict(orient="records")

if __name__ == "__main__":
    mcp.run()  # stdio transport
    