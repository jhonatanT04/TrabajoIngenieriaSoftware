import { HttpInterceptorFn } from '@angular/common/http';
import { finalize } from 'rxjs';



let activeRequests = 0;

export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  activeRequests++;

  if (activeRequests === 1) {
    dispatchLoadingEvent(true);
  }

  return next(req).pipe(
    finalize(() => {
      activeRequests--;

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
