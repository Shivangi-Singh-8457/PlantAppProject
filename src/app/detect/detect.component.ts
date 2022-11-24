import { HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
//import { DetectService } from '../service/detect.service';
import {Router} from '@angular/router';
import { HttpClientService } from '../service/http-client.service';

@Component({
  selector: 'app-detect',
  templateUrl: './detect.component.html',
  styleUrls: ['./detect.component.scss']
})
export class DetectComponent implements OnInit {
  sendreq:any=[]
  leafApicesValue:string=""
  leafBaceisValue:string=""
  leafMarginValue:string=""
  postdata=new Map <string,string>()
  jsonObject:any= {};
  jsonString:string=""
  datalist:any
  key:any
  flag:boolean=false

  constructor(private httpClient:HttpClientService,private router: Router) { 
    
  }

  ngOnInit(): void {
  }
    
  goToPage(this:any, pageName:string){
    this.router.navigate([`${pageName}`]);
  }
   display(name:string,value:any) {
     console.log(name)
     if(name=='leaf_apicies')
     {
      this.leafApicesValue=value;
      console.log(this.leafApicesValue);
      }
     if(name=='leaf_margin')
     {
      this.leafMarginValue=value;
      console.log(this.leafMarginValue);
     }
     if(name=='leaf_bases')
       {
        this.leafBaceisValue=value;
        console.log(this.leafBaceisValue);
       }
      this.submit()
   }
   submit()
   {
       if(this.leafApicesValue!="")
       {
         this.postdata.set('leaf_apices',this.leafApicesValue)
         console.log(this.postdata)
       }
       if(this.leafBaceisValue!="")
       {
         this.postdata.set('leaf_bases',this.leafBaceisValue)
         console.log(this.postdata)
       }
       if(this.leafMarginValue!="")
       {
         this.postdata.set('leaf_margin',this.leafMarginValue)
         console.log(this.postdata)
       }
         
      this.postdata.forEach((value, key) => {  
       this.jsonObject[key] = value  
       });  

       this.jsonString=JSON.stringify(this.jsonObject);
      //  no use of send request
      //  console.log(this.jsonString)
      //  this.sendreq.push(this.jsonString)
      //  console.log("send req:"+this.sendreq)
       
    
       this.httpClient.getfilename(this.jsonObject).subscribe(
         res=>{
           //console.log(res)
           this.datalist=res;
           this.key=Object.keys(this.datalist);
           console.log(this.key)
           console.log("after key")
         }
        )
        this.flag=true
    }
    
  }