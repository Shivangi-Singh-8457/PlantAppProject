import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClientService } from '../service/http-client.service';
import { AuthenticationService } from '../service/authentication.service';
import Swal, { SweetAlertOptions } from 'sweetalert2';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.scss']
})
export class LogoutComponent implements OnInit {

  msg:any;
  
  constructor(private httpClient:HttpClientService, private router: Router, private authService: AuthenticationService) {
    
   }

  ngOnInit(): void {
    // this.httpClient.signout().subscribe(
    //   res=>{
    //     this.msg=res
    //     Swal.fire(this.msg);
    //     //alert(this.msg);
    //     this.goToPage('index'); 
    // })
    this.logout()
  }
  
  logout()
  {
    this.authService.logOutClient()
      {
        Swal.fire("You are logged out.");
        this.goToPage('index'); 
      }
  }
  goToPage(this:any, pageName:string){
    this.router.navigate([`${pageName}`]);
  }
}
