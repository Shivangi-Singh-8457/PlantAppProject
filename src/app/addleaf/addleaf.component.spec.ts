import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddleafComponent } from './addleaf.component';

describe('AddleafComponent', () => {
  let component: AddleafComponent;
  let fixture: ComponentFixture<AddleafComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddleafComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddleafComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
