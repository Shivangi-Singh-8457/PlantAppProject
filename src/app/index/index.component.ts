import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import { HttpClientService } from '../service/http-client.service';
var menulist:any;
var menulist1:any;
@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {
  
  login_flag:any;
  //iscollapse=false;
  
  constructor(private httpClient:HttpClientService, private router: Router){
 
  }

  ngOnInit(): void {
    this.httpClient.checksignin().subscribe(
      res=>{
        this.login_flag=res
        console.log(this.login_flag);
        console.log(typeof this.login_flag); 
    });
    
  }
  
  togglemenu(){
    menulist=document.getElementById("menulist");
    menulist1=document.getElementById("menubar1");
    menulist1.style.display="block";
    if(menulist.style.maxHeight=="0px"){
    menulist.style.maxHeight="130px"
    }
    else
    {
      menulist.style.maxHeight="0px"
    }
  
  }
  goToPage(this:any, pageName:string){
    this.router.navigate([`${pageName}`]);
  }    
  
}
 

