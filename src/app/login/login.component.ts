import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import {Router} from '@angular/router';
import { HttpClientService } from '../service/http-client.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  email:string=""
  password:string=""
  msg:any 
  
  constructor(private httpClient:HttpClientService, private router: Router, private location:Location) { }

  ngOnInit(): void {
  }
  onsubmit(userForm:NgForm)
  {
    this.httpClient.signin([this.email,this.password]).subscribe(res=>
    { 
      this.msg=res
      console.log(typeof this.msg[1])
      alert(this.msg[0])
      this.func()
    })
    userForm.reset();
  }
  func()
  {
    if(this.msg[1]=='true')
    this.location.back();
    else
    window.location.reload();
  }
  goToPage(this:any, pageName:string){
    this.router.navigate([`${pageName}`]);
  }
}
