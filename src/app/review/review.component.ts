import { Component, OnInit, Output, Input, Inject } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClientService } from '../service/http-client.service';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.scss'],
})

export class ReviewComponent implements OnInit {

  folderlist:any=[];
  imagelist:any={};
  comments:any={};
  arr: any=[];
  folderResult:any={};
  login_flag:any;
  msg:any;
  report_reason: any;
  imgResult:any={};
  x:any={};
  y:any={};
  z:any={}  
  feature: any;
  corrected: any;
  corrections:any={}
  correction_result:any={}

  constructor(private httpClient:HttpClientService, private router:Router, public dialog: MatDialog){
    this.httpClient.checksignin().subscribe(
      res=>{
        this.login_flag=res
        console.log(this.login_flag);
        this.start();
        this.needhelp();
    });
  }

  ngOnInit(): void {
    
  }
  needhelp()
  {
     Swal.fire("Here you will find some options like Upvote, Downvote , Report and Correction \n if you think Plant name and its Characteristics is correct then kindly Upvote it \n if you think folder name is not correct then Downvote it \n if you think folder name is violating some rules or not valid then Report it with suitable given option otherwise select other if option not available \n If you want to give some specific correction then you can choose correction option \n Same will be applied for images also ");
  }
  start(){
    this.httpClient.getfolders().subscribe(
      res=>{
        this.folderlist=res[0]
        this.imagelist=res[1]
        this.x=res[2]
        this.y=res[3]
        this.z=res[4]
        this.folderResult=res[5]
        this.imgResult=res[6]
        this.corrections=res[7]
        this.correction_result=res[8]
      })
  }
  async wait()
  {
    await new Promise(resolve=>setTimeout(resolve,1000));
  }
  
  correctionList(id:any, ch:any){
    var key=id.toString()+"_"+ch;
    if(key in this.corrections)
      return this.corrections[key];
    else
      return []; 
  }

  folderVote(id:any, ch:any)
  {
    if(this.login_flag)
    { 
      if(ch=='r' && this.report_reason!=undefined)
      {
        this.httpClient.folder_vote([id,ch,this.report_reason]).subscribe(
          res=>{
            this.x[id]=res[0];
            if(!(id in this.folderResult))
            {
              this.folderResult[id]=[res[1],res[2]];
            }
            else
            {
              this.folderResult[id][0]=res[1];
              this.folderResult[id][1]=res[2];
            }
            this.ngOnInit();
          });
        
      }
      else if(ch=='ur')
      {
        this.httpClient.folder_vote([id,'r']).subscribe(res=>{
          this.x[id]=res[0];
          this.folderResult[id][0]=res[1];
          this.folderResult[id][1]=res[2];
          this.ngOnInit();
        });
      }
      else if((!(id in this.folderResult) || this.folderResult[id][1]==0) && (ch=='u' || ch=='d'))
      { 
        this.httpClient.folder_vote([id,ch]).subscribe(res=>{
          this.x[id]=res[0];
          if(!(id in this.folderResult))
          {
            this.folderResult[id]=[res[1],res[2]];
          }
          else
          {
            this.folderResult[id][0]=res[1];
            this.folderResult[id][1]=res[2];
          }
          this.ngOnInit();
        });
      }
    }
    else
    this.router.navigate(['login']);
  }
  imgVote(id:any, ind:any, ch:any){
    if(this.login_flag)
    {
      var key=id.toString()+"_"+ind.toString();
      if(ch=='r' && this.report_reason!=undefined)
      {
        this.httpClient.image_vote([id,ind,ch,this.report_reason]).subscribe(res=>{
          this.y[key]=res[0];
          if(!(key in this.imgResult))
          {
            this.imgResult[key]=[res[1],res[2]];
          }
          else
          {
            this.imgResult[key][0]=res[1];
            this.imgResult[key][1]=res[2];
          }
          this.ngOnInit();
        });
      }
      else if(ch=='ur') 
      {
        this.httpClient.image_vote([id,ind,'r']).subscribe(res=>{
          this.y[key]=res[0];
          this.imgResult[key][0]=res[1];
          this.imgResult[key][1]=res[2];
          this.ngOnInit();
        }); 
      }
      else if((!(key in this.imgResult) || this.imgResult[key][1]==0) && (ch=='u' || ch=='d'))
      {  
        this.httpClient.image_vote([id,ind,ch]).subscribe(res=>{
          console.log(res);
          this.y[key]=res[0];
          if(!(key in this.imgResult))
          {
            this.imgResult[key]=[res[1],res[2]];
          }
          else
          {
            this.imgResult[key][0]=res[1];
            this.imgResult[key][1]=res[2];
          }
          console.log( this.y[key]=res[0],this.imgResult[key][0]=res[1], this.imgResult[key][1]=res[2])
          this.ngOnInit();});
      }
    }
    else
      this.router.navigate(['login']);
 }
 fetchComments(id:any)
 {
    this.httpClient.get_comments(id).subscribe(res=>{this.comments[id]=res});
 }
 saveComment(commentform:NgForm, id:any)
 {
  if(this.login_flag)
  {
    this.httpClient.save_comment([id,this.msg]).subscribe(res=>{});
    commentform.reset();
  }
  else
    this.router.navigate(['login']);
 }
 check_imgVote(id:any, ind:any, ch:any)
 {
    var key=id.toString()+"_"+ind.toString();
    if(ch=='r')
    {
      if(key in this.imgResult && this.imgResult[key][1]==1)
        return false;
      else 
        return true;
    }
    if(ch=='u')
    {
      if(key in this.imgResult && this.imgResult[key][0]==1)
        return false;
      else 
        return true;
    } 
    if(ch=='d')
    {
      if(key in this.imgResult && this.imgResult[key][0]==-1)
        return false;
      else 
        return true;
    } 
    return false;      
 } 

 save_corrections(id:any){
  if(this.login_flag)
  {
      var key=id.toString()+"_"+this.feature;
      console.log(key)
      this.httpClient.save_corrections([id,this.feature,this.corrected]).subscribe(res=>{
      console.log(res); 
      alert(res[0]);
      if(res[1]!="")
      {
        if(!(key in this.corrections))
        {
          this.corrections[key]=[res[1]];
          console.log(1,this.corrections[key])
        }
        else
        {
          this.corrections[key].push(res[1]);
          console.log(2,this.corrections[key])
        }
        this.z[key+"_"+this.corrected]=res[2];
      }
      console.log(3,this.z[key+"_"+this.corrected])
      this.ngOnInit();
    });
  }
  else
    this.router.navigate(['login']);
 }

 correctionsVote(id: any, characteristics: any, suggestion:any, ch:any){
  if(this.login_flag)
    {
      var key=id.toString()+"_"+characteristics+"_"+suggestion;
          this.httpClient.correction_vote([id,characteristics,suggestion,ch]).subscribe(res=>{
          this.z[key]=res[0];
          this.correction_result[key]=res[1];
          this.ngOnInit();
        });
    }
    else
      this.router.navigate(['login']);
 }

 check_correctionVote(id:any, characteristics: any, suggestion:any, ch:any)
 {
    var key=id.toString()+"_"+characteristics+"_"+suggestion;
    if(ch=='u')
    {
      if(key in this.correction_result && this.correction_result[key]==1)
        return false;
      else 
        return true;
    } 
    if(ch=='d')
    {
      if(key in this.correction_result && this.correction_result[key]==-1)
        return false;
      else 
        return true;
    } 
    return false;      
 } 

 openDialog(id:any,ind:any,ch:any): void {
    console.log("dialog box opened");
    const dialogRef = this.dialog.open(ReportDialogComponent, {
      width: '300px',
      data: {report_reason: this.report_reason},
    });
    console.log("dialog box1");
    dialogRef.afterClosed().subscribe(res => {
      console.log('The dialog was closed');
      this.report_reason = res;
      console.log(this.report_reason);
      if(this.report_reason){
        if(ch=='f')
          this.folderVote(id,'r');
        else
          this.imgVote(id,ind,'r');
      }
    });
    console.log("dialog box2");
  }

  openCorrectionDialog(id:any): void {
    console.log("dialog box opened");
    const dialogRef = this.dialog.open(CorrectionDialogComponent, {
      width: '300px',
      data: {feature: this.feature, corrected: this.corrected},
    });
   // console.log("dialog box1");
    dialogRef.afterClosed().subscribe(res => {
      console.log('The dialog was closed');
      console.log(typeof(res));
      this.feature=res[0];
      this.corrected=res[1];
      console.log(this.feature, this.corrected);
      if(this.feature && this.corrected)
      {
        this.save_corrections(id);
      }
    });
    //console.log("dialog box2");
  }
}

@Component({
  selector: 'app-review',
  templateUrl: './reportDialog.html',
  styleUrls: ['./review.component.scss'],
})
export class ReportDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<ReportDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data:{report_reason: any},
  ) {console.log('report_dialog')}

  onNoClick(): void {
    this.dialogRef.close();
  }
}

@Component({
  selector: 'app-review',
  templateUrl: './correctionDialog.html',
  styleUrls: ['./review.component.scss'],
})
export class CorrectionDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<CorrectionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data:{feature: any, corrected: any},
  ) {console.log('correction_dialog')}

  onNoClick(): void {
    this.dialogRef.close();
  }
}