import os
import logging
import io
import markdown
from fastmcp import FastMCP
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google-workspace-mcp")

mcp = FastMCP("Google Workspace")

# Scopes required for Drive and Docs
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/presentations.readonly'
]

def get_credentials():
    """Gets credentials from service account file or environment."""
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_path and os.path.exists(creds_path):
        return service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    # Fallback or alternative auth methods can be added here
    return None

@mcp.tool()
def list_folder_files(folder_id: str):
    """Lists files in a specific Google Drive folder."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

@mcp.tool()
def read_google_doc(file_id: str):
    """Reads the content of a Google Doc."""
    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)
    
    doc = service.documents().get(documentId=file_id).execute()
    
    # Simple extraction of text
    content = doc.get('body').get('content')
    text = ""
    for element in content:
        if 'paragraph' in element:
            for part in element.get('paragraph').get('elements'):
                text += part.get('textRun', {}).get('content', "")
    return text

@mcp.tool()
def read_google_slides(file_id: str):
    """Reads the content of a Google Slides deck."""
    creds = get_credentials()
    service = build('slides', 'v1', credentials=creds)
    
    presentation = service.presentations().get(presentationId=file_id).execute()
    slides = presentation.get('slides', [])
    
    text = ""
    for i, slide in enumerate(slides):
        text += f"\n--- Slide {i+1} ---\n"
        for element in slide.get('pageElements', []):
            if 'shape' in element and 'text' in element['shape']:
                for part in element['shape']['text'].get('textElements', []):
                    text += part.get('textRun', {}).get('content', "")
    return text

@mcp.tool()
def write_report_doc(folder_id: str, filename: str, content: str):
    """Creates a new Google Doc in a folder by converting Markdown to HTML and then to Google Doc format."""
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)
    
    # 1. Convert Markdown to HTML
    # We use 'extra' to support tables, lists, and other markdown extensions
    html_content = markdown.markdown(content, extensions=['extra'])
    
    # 2. Wrap in basic HTML structure
    full_html = f"<html><body>{html_content}</body></html>"
    
    # 3. Prepare the file metadata for Drive
    file_metadata = {
        'name': filename,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [folder_id]
    }
    
    # 4. Prepare the media upload (uploading HTML but converting to Doc)
    media = MediaIoBaseUpload(
        io.BytesIO(full_html.encode('utf-8')),
        mimetype='text/html',
        resumable=True
    )
    
    # 5. Create the file (this triggers the automatic conversion)
    try:
        doc_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        doc_id = doc_file.get('id')
        return {
            "status": "success", 
            "file_id": doc_id, 
            "url": f"https://docs.google.com/document/d/{doc_id}/edit"
        }
    except Exception as e:
        logger.error(f"Error creating report: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run(transport="http")
