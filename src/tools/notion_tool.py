import requests
from langchain_core.tools import tool
from src.config import settings


class NotionService:
    def __init__(self):
        self.api_key = settings.NOTION_API_KEY
        self.database_id = settings.NOTION_DATABASE_ID
        self.base_url = "https://api.notion.com/v1"

    def query_database(self) -> list[dict]:
        """Consulta a base de dados do Notion e retorna os metadados formatados de forma limpa."""
        url = f"{self.base_url}/databases/{self.database_id}/query"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, headers=headers, json={})
            response.raise_for_status()
            data = response.json()
            
            pages = data.get("results", [])
            formatted_results = []

            for page in pages:
                properties = page.get("properties", {})
                row_data = {}
                
                for prop_name, prop_value in properties.items():
                    prop_type = prop_value.get("type")
                    
                    if prop_type == "title":
                        title_array = prop_value.get("title", [])
                        row_data[prop_name] = title_array[0].get("plain_text", "") if title_array else ""
                    elif prop_type == "rich_text":
                        text_array = prop_value.get("rich_text", [])
                        row_data[prop_name] = text_array[0].get("plain_text", "") if text_array else ""
                    elif prop_type == "select":
                        select_obj = prop_value.get("select")
                        row_data[prop_name] = select_obj.get("name") if select_obj else None
                    elif prop_type == "status":
                        status_obj = prop_value.get("status")
                        row_data[prop_name] = status_obj.get("name") if status_obj else None
                    elif prop_type == "number":
                        row_data[prop_name] = prop_value.get("number")
                    elif prop_type == "date":
                        date_obj = prop_value.get("date")
                        row_data[prop_name] = date_obj.get("start") if date_obj else None
                        
                formatted_results.append(row_data)
                
            return formatted_results
        except Exception as e:
            return [{"error": str(e)}]


notion_service = NotionService()


@tool
def query_notion_database() -> list[dict]:
    """Consulta a base de dados estruturada no Notion para recuperar informações e metadados das páginas."""
    return notion_service.query_database()