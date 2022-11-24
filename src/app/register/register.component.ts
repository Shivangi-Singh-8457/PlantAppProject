import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClientService } from '../service/http-client.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  email:string=""
  phone:string=""
  password:string=""
  msg:any
  otp:any
  otp_msg:any
  flag=true;
  email_flag=false
  resend_flag=false

  constructor(private httpClient:HttpClientService, private router:Router) { }

  ngOnInit(): void {
  }
  onsubmit(userForm:NgForm){
    this.httpClient.signup(this.email).subscribe(res=>{
      this.msg=res
      if(this.msg=="true")
      {
          this.email_flag=true
          this.flag=false
      }
      else
      {
        alert(this.msg)
        userForm.reset()
      }
    })
  }
  otpsubmit(otpForm:NgForm)
  {
    this.httpClient.registration_otp([this.phone,this.password,this.otp]).subscribe(res=>{
      if(res=="wrong otp")
      {
        if(!this.resend_flag)
          this.otp_msg=res
        otpForm.reset();
      }
      else
      {
        alert(res)
        this.goToPage('index');
      }
    });
  }
  resend()
  {
    this.otp_msg=""
    this.resend_flag=true
    this.httpClient.resend().subscribe(res=>{this.resend_flag=false})
  }
  goToPage(this:any, pageName:string){
    this.router.navigate([`${pageName}`]);
  }
}
