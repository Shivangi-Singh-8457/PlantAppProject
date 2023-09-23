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
  msg:any={}
  otp:any
  otp_msg:any
  flag=true;
  email_flag=false
  resend_flag=false

  constructor(private httpClient:HttpClientService, private router:Router) { }

  ngOnInit(): void {
  }
  onsubmit(userForm:NgForm){
    this.httpClient.signup({email:this.email}).subscribe(res=>{
      this.msg=res
      if(this.msg.flag)
      {
          this.email_flag=true
          this.flag=false
      }
      else
      {
        alert(this.msg.value)
        userForm.reset()
      }
    })
  }
  otpsubmit(otpForm:NgForm)
  {
    if(this.msg.otp==this.otp)
    {
      this.httpClient.registration_otp({username:this.email, phone:this.phone, password:this.password}).subscribe(res=>
      {
        alert(res.msg)
        this.goToPage('index');
      })
    }
    else
    {
      if(!this.resend_flag)
          this.otp_msg="wrong otp"
      otpForm.reset();
    }
    // this.httpClient.registration_otp([this.phone,this.password]).subscribe(res=>{
    //   if(res=="wrong otp")
    //   {
    //     if(!this.resend_flag)
    //       this.otp_msg=res
    //     otpForm.reset();
    //   }
    //   else
    //   {
    //     alert(res)
    //     this.goToPage('index');
    //   }
    // });
  }
  resend()
  {
    this.otp_msg=""
    this.resend_flag=true
    this.httpClient.resend({email:this.email}).subscribe(res=>{this.msg=res; this.resend_flag=false})
  }
  goToPage(this:any, pageName:string){
    this.router.navigate([`${pageName}`]);
  }
}
