import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';


export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      let errorMessage = 'Ha ocurrido un error';

      if (error.error instanceof ErrorEvent) {

        errorMessage = `Error: ${error.error.message}`;
      } else {

        switch (error.status) {
          case 400:
            errorMessage = error.error?.message || 'Solicitud incorrecta';
            break;
          case 401:
            errorMessage = 'No autorizado. Por favor inicie sesión';
            break;
          case 403:
            errorMessage = 'No tiene permisos para realizar esta acción';
            break;
          case 404:
            errorMessage = 'Recurso no encontrado';
            break;
          case 500:
            errorMessage = 'Error interno del servidor';
            break;
          default:
            errorMessage = error.error?.message || `Error del servidor: ${error.status}`;
        }
      }

      console.error('Error HTTP:', errorMessage, error);


      return throwError(() => ({
        message: errorMessage,
        status: error.status,
        error: error.error
      }));
    })
  );
};
