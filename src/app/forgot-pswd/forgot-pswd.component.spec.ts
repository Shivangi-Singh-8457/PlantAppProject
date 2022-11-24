import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ForgotPswdComponent } from './forgot-pswd.component';

describe('ForgotPswdComponent', () => {
  let component: ForgotPswdComponent;
  let fixture: ComponentFixture<ForgotPswdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ForgotPswdComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ForgotPswdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
