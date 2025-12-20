import { HttpInterceptorFn } from '@angular/common/http';
import { finalize } from 'rxjs';

/**
 * Interceptor de carga
 * Controla el estado de carga global de las peticiones HTTP
 */

// Variable global para controlar el estado de carga
let activeRequests = 0;

export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  activeRequests++;

  // Emitir evento de inicio de carga
  if (activeRequests === 1) {
    dispatchLoadingEvent(true);
  }

  return next(req).pipe(
    finalize(() => {
      activeRequests--;

      // Emitir evento de fin de carga cuando no hay peticiones activas
      if (activeRequests === 0) {
        dispatchLoadingEvent(false);
      }
    })
  );
};

function dispatchLoadingEvent(isLoading: boolean) {
  const event = new CustomEvent('loading', { detail: isLoading });
  window.dispatchEvent(event);
}

export function getActiveRequests(): number {
  return activeRequests;
}
