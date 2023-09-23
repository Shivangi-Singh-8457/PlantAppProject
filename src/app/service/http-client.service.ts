import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';


// Retrieve the token from localStorage
// Prepare the headers with the Authorization token
var headers = new HttpHeaders({
  'Content-Type': 'multipart/form-data',
  // 'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Include the JWT token here
});

@Injectable({
  providedIn: 'root'
})

export class HttpClientService {
  
  constructor(private httpClient : HttpClient) { }
   
    

  getfilename(query: any) {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/predict`, query);
  }
  // sendfiledata(query: any)
  // {
  //   return this.httpClient.post<any>(`${environment.apiBaseUrl}/adddata`, query);
  // }
  // sendimagedata(query:any)
  // {
  //   return this.httpClient.post<any>(`${environment.apiBaseUrl}/imagedata`, query);
  // }
  // sendimgname(query:any)
  // {
  //   return this.httpClient.post<any>(`${environment.apiBaseUrl}/imagename`, query);
  // }
  addleaf(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/addleaf`, query);
  }
  signup(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/register`, query);
  }
  registration_otp(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/registration_otp`, query);
  }
  checkemail(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/checkemail`, query);
  }
  checkotp(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/checkotp`, query);
  }
  chngpswd(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/chngpswd`, query);
  }
  resend(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/resend`,query);
  }
  signout()
  {
    return this.httpClient.get<any>(`${environment.apiBaseUrl}/logout`);
  }
  checksignin()
  {
    return this.httpClient.get<any>(`${environment.apiBaseUrl}/checklogin`);
  }
  getfolders()
  {
    return this.httpClient.get<any>(`${environment.apiBaseUrl}/folderlist`);
  }
  folder_vote(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/folder_vote`, query);
  }
  image_vote(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/image_vote`, query);
  }
  get_comments(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/get_comments`,query);
  }
  save_comment(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/save_comment`,query);
  }
  save_corrections(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/save_corrections`,query);
  }
  correction_vote(query:any)
  {
    return this.httpClient.post<any>(`${environment.apiBaseUrl}/correction_vote`, query);
  }
}
