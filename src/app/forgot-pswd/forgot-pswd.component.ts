import { Component, OnInit } from '@angular/core';
import { HttpClientService } from '../service/http-client.service';
import { Location } from '@angular/common';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-forgot-pswd',
  templateUrl: './forgot-pswd.component.html',
  styleUrls: ['./forgot-pswd.component.scss']
})
export class ForgotPswdComponent implements OnInit {

  email:string=""
  password:string=""
  otp:any;
  msg:any;
  flag:boolean=true;
  email_flag:any;
  otp_flag:any;
  resend_flag:any;
  email_msg:string="";
  otp_msg:string="";

  constructor(private httpClient:HttpClientService, private location:Location) { }

  ngOnInit(): void {
  }

  onsubmit(userForm:NgForm){
    this.httpClient.checkemail(this.email).subscribe(res=>{ 
        this.email_flag=res
        console.log(res)
        console.log(typeof res)
        console.log(this.email_flag)
        console.log(typeof this.email_flag)
        this.func1()
      });
      userForm.reset();
  }
  otpsubmit(otpForm:NgForm)
  {
    this.httpClient.checkotp(this.otp).subscribe(res=>{ 
        this.otp_flag=res
        this.func2()
      });
      otpForm.reset();
  }
  pswdsubmit(pswdForm:NgForm){
    this.httpClient.chngpswd(this.password).subscribe(res=>{ 
        this.msg=res
        alert(this.msg);
        this.location.back();
      });
      pswdForm.reset();
  }
  resend()
  {
    this.resend_flag=true;
    this.httpClient.resend().subscribe(res=>{})
  }
  func1(){
    if(this.email_flag)
      this.flag=false;
    else if(!this.email_flag)
      this.email_msg="You are not our user.";
  }
  func2(){
    if(this.otp_flag)
      this.email_flag=false;
    else if(!this.otp_flag && !this.resend_flag)
      this.otp_msg="Wrong OTP";
  }
}
