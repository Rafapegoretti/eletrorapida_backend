import traceback
from .models import ErrorLog


def log_internal_error(request, exception):
    ErrorLog.objects.create(
        path=request.path,
        method=request.method,
        status_code=500,
        error_message=str(exception),
        traceback=traceback.format_exc(),
    )
