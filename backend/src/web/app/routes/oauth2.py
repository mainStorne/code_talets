from fastapi import Request, APIRouter
from starlette.responses import HTMLResponse

oauth2_router = APIRouter(prefix='/oauth2')


@oauth2_router.get('/yandex/code')
async def oauth2_yandex_signup(request: Request, code: str, cid: str):
    html_content = f"""
     <html>
     <body>
         <script type="text/javascript">
             // Отправляем токен в родительское окно через postMessage
             window.opener.postMessage({{code: "{code}"}}, "https://musical-pheasant-major.ngrok-free.app");
             // Закрываем текущее окно
             window.close();
         </script>
     </body>
     </html>
     """
    return HTMLResponse(content=html_content)
