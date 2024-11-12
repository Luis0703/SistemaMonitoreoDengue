import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DenguePredictionsComponent } from './dengue-predictions.component';

describe('DenguePredictionsComponent', () => {
  let component: DenguePredictionsComponent;
  let fixture: ComponentFixture<DenguePredictionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DenguePredictionsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DenguePredictionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});