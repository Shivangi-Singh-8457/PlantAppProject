import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { EventEmitter, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { map, catchError, switchMap } from 'rxjs/operators';
import { Observable, of, timer } from 'rxjs';

// @Injectable({
//   providedIn: 'root'
// })
// export class AuthenticationService {

//   constructor() { }
// }

const TOKEN = 'token';
const USERNAME = 'username';
const USERID = 'userId';
const MIN15 = 1000 * 60 * 15;

var headers = new HttpHeaders({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${localStorage.getItem('access_token')}` // Include the JWT token here
});

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private isAuthenticated = false;
  // private privileges: Array<string>;
  // private roles: Array<string>;
  private userId: any;
  // private type;
  getLoggedInUserInfo = new EventEmitter<string>();

  constructor(private httpClient: HttpClient, private router: Router) { }

  private resetFields() {
    this.isAuthenticated = false;
    // this.privileges = null;
  }
  
  authenticate(email: string, password: string) {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/login`, {email, password}).pipe(
      map(
        data => {
          this.saveUserAuthInfo(data,true);
          return data;
        }
      )
    );
  }

  refreshTokenSubs = timer(MIN15, MIN15).subscribe(val => {
    this.httpClient.get<any>(`${environment.apiBaseUrl}/refreshToken`, {headers}).subscribe(
      data => {
        this.saveUserAuthInfo(data,false);
      },
      error => {
        if (error.status === 401) {
          this.logOutClient();
        }
      });
  });

  private handleError(err: HttpErrorResponse): Observable<any> {
    console.error(`Status code ${err.status}`);
    //FIXME - check how can we call this.logOutClient();
    localStorage.removeItem(TOKEN);
    localStorage.removeItem(USERNAME);
    return of(false);
  }

  private autehticated(): boolean {
    return this.isAuthenticated;
  }

  autehticatedOrValidToken(): Observable<boolean> | boolean {
    if (this.autehticated()) {
      return true;
    }
    const token = this.getToken();
    if (token !== null) {
      return this.httpClient.get<any>(`${environment.apiBaseUrl}/validateToken`).pipe(
        map(
          data => {
            this.saveUserAuthInfo(data,false);
            return true;
          }
        ),
        catchError(this.handleError)
      );
    }
    return false;
  }

  getToken() {
    return localStorage.getItem(TOKEN);
  }

  getName() {
    return localStorage.getItem(USERNAME);
  }
  getLoggedInUserId() {
    return localStorage.getItem(USERID);
  }
  // getPrivileges() {
  //   return this.privileges;
  // }
  // getRoles() {
  //   return this.roles;
  // }
  // getUserType() {
  //   return this.type;
  // }
  logOut() {
    this.httpClient.get(`${environment.apiBaseUrl}/logout`)
      .subscribe(
        data => {
          this.logOutClient();
        },
        error => {
          this.logOutClient();
        });
  }
  logOutClient() {
    localStorage.removeItem(TOKEN);
    localStorage.removeItem(USERNAME);
    localStorage.removeItem(USERID);
    this.resetFields();
    this.getLoggedInUserInfo.emit("");
    // this.router.navigate(['/login']);
  }

  // hasPrivilege(privilege: string) {
  //   return this.privileges && this.privileges.indexOf(privilege) !== -1;
  // }

  // hashRole(role: string) {
  //   return this.roles && this.roles.indexOf(role) !== -1;
  // }
  // parseRolesAndPrivileges(privileges) {
  //   let R = []
  //   let P = []
  //   privileges.forEach(priv => {
  //     R.push(priv.role);
  //     priv.privileges.forEach(pr => {
  //       P.push(pr.privilege);
  //     });
  //   });
  //   this.roles = R;
  //   this.privileges = P;
  // }

  private saveUserAuthInfo(data: any , flag: boolean) {
    // localStorage.setItem(USERNAME, data.userName);
    let tokenStr = `Bearer ${data.access_token}`;
    localStorage.setItem(TOKEN, tokenStr);
    // localStorage.setItem(USERID, data.userId);
    this.isAuthenticated = true;
    // this.userId = data.userId;
    // this.type = data.userType;
    // this.parseRolesAndPrivileges(data.roles);
    // this.getLoggedInUserInfo.emit(data.userName);
    if(flag){
      this.router.navigate(['/dashboard']);
    }
  }

  ngOnDestroy() {
    this.refreshTokenSubs.unsubscribe();
  }

}