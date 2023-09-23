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
  result:any;
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
    this.httpClient.checkemail({email:this.email}).subscribe(res=>{ 
        this.result=res
        this.email_flag=this.result.flag
        console.log(res)
        console.log(typeof res)
        console.log(this.email_flag)
        console.log(typeof this.email_flag)
        this.func1()
      });
      // userForm.reset();
  }
  otpsubmit(otpForm:NgForm)
  {
    if(this.result.otp==this.otp)
    {
      this.otp_flag=true;
    }
    else{
      this.otp_flag=false;
    }
    this.func2()
    otpForm.reset();
  }
  pswdsubmit(pswdForm:NgForm){
    this.httpClient.chngpswd({email: this.email, password:this.password}).subscribe(res=>{ 
        this.msg=res
        alert(this.msg);
        this.location.back();
      });
      pswdForm.reset();
  }
  resend()
  {
    console.log(this.email)
    this.resend_flag=true;
    this.httpClient.resend({email:this.email}).subscribe(res=>{})
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
