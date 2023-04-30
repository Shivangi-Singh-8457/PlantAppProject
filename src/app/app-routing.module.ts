import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IndexComponent } from './index/index.component';
import { DetectComponent } from './detect/detect.component';
import { LearningModuleComponent } from './learning-module/learning-module.component';
import { AddleafComponent } from './addleaf/addleaf.component';
import { LearnComponent } from './learn/learn.component';
import { ReviewComponent } from './review/review.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { LogoutComponent } from './logout/logout.component';
import { ForgotPswdComponent } from './forgot-pswd/forgot-pswd.component';
import { AboutusComponent } from './aboutus/aboutus.component';

const routes: Routes = [
  {path:'index',component:IndexComponent},
  {path:'detect',component:DetectComponent},
  {path:'LearningModule',component:LearningModuleComponent},
  {path:'addleaf',component:AddleafComponent},
  {path:'learn',component:LearnComponent},
  {path:'review',component:ReviewComponent},
  {path:'register',component:RegisterComponent},
  {path:'login',component:LoginComponent},
  {path:'logout',component:LogoutComponent},
  {path:'forgotPswd',component:ForgotPswdComponent},
  {path:'aboutus',component:AboutusComponent},
  {path:'**',redirectTo:'index'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
