import traceback
from .models import ErrorLog

# Registra um erro interno (HTTP 500) no banco de dados.
# Captura o caminho, método HTTP, mensagem de erro e traceback completo.
# Essa função deve ser chamada dentro de blocos try/except para rastreamento de falhas.


def log_internal_error(request, exception):
    ErrorLog.objects.create(
        path=request.path,
        method=request.method,
        status_code=500,
        error_message=str(exception),
        traceback=traceback.format_exc(),
    )
