import { Component, OnInit } from '@angular/core';
import { HttpClientService } from '../service/http-client.service';
import {Router} from '@angular/router';
import { User } from '../user';

const  maxsize=30*1024*1024; //in MegaBytes
var totalsize=0;


@Component({
  selector: 'app-addleaf',
  templateUrl: './addleaf.component.html',
  styleUrls: ['./addleaf.component.scss']
})
export class AddleafComponent implements OnInit {
  sendres:any
  srcData:any
  fileToUpload: any=[]
  plantName:any
  userModel=new User('','','')
  login_flag:any
  smt=true
  startIndex:any

  constructor(private httpClient:HttpClientService, private router:Router) { 
    
  }

  ngOnInit(): void {
  }

  onChange(event: any) {
    console.log(event);
    for(var i=0; i<event.target.files.length; i++){
      console.log(typeof event.target.files[i].type)
      console.log(event.target.files[i].type)
      if(event.target.files[i].type=='image/jpeg'||event.target.files[i].type=='image/png'||event.target.files[i].type=='image/jpg')
        this.fileToUpload.push(event.target.files[i]);
    }
    console.log(this.fileToUpload);
  }
    
  onsubmit()
  {
    if(this.smt)
    { 
      this.smt=false
      this.httpClient.checksignin().subscribe(
        res=>{
          this.login_flag=res
          console.log(this.login_flag);
          this.check()
          
      })
    }
  }
 
  check()
  {
    if(this.login_flag)
      this.upload();
    else
    this.router.navigate(['login']);
  }

  func1()
  {
    this.httpClient.sendfiledata(this.userModel).subscribe(
        res=>{
          this.func2()
        })
  }
  async func2()
  {
    for(var i=0;i<this.fileToUpload.length;i++)
    {
      this.httpClient.sendimagedata(this.fileToUpload[i]).subscribe(
      res=>{
        this.sendres=res; 
      })
      await new Promise(resolve=>setTimeout(resolve,500));
      console.log(i);
    }
    console.log('sendres');
    alert(this.sendres);
    this.smt=true
    window.location.reload();
  }

  upload()
  {
    for(var i=0;i<this.fileToUpload.length;i++)
    {
     totalsize+=this.fileToUpload[i].size;
    }

    if(this.fileToUpload.length>0 && this.fileToUpload.length<=5 && totalsize<=maxsize){
      this.httpClient.sendimgname([this.plantName, this.fileToUpload.length]).subscribe(
        res=>{
          this.startIndex=res
          this.func1()
        }) 
  }
  else{
    window.location.reload();
    alert("Check image size,type and quantity");
    console.log(totalsize);

    }
  }
  
}


