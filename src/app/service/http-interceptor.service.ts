import { HttpErrorResponse, HttpHandler, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class HttpInterceptorService {

  constructor() { }

  
  intercept(req: HttpRequest<any>, next: HttpHandler) {
/*
    if (this.authService.getToken() !== null) {
      req = req.clone({
        setHeaders: {
          Authorization: this.authService.getToken()
        }
      })
    }*/
    return next.handle(req).pipe(tap(() => { },
      (err: any) => {
        if (err instanceof HttpErrorResponse) {
          if (err.status !== 401) {
            return;
          }
         // this.authService.logOutClient();
        }
      }));
  }
}
