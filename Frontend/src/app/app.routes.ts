import { Routes } from '@angular/router';
import { MainMenuComponent } from './main-menu/main-menu.component';
import { LoginComponent } from './login/login.component';
import { DenguePredictionsComponent } from './dengue-predictions/dengue-predictions.component';
import { HeatMapComponent } from './heat-map/heat-map.component';

export const routes: Routes = [
  { path: '', redirectTo: '/main-menu', pathMatch: 'full' },
  { path: 'main-menu', component: MainMenuComponent },
  { path: 'heat-map', component: HeatMapComponent },
  { path: 'dengue-predictions', component: DenguePredictionsComponent },
  { path: 'login', component: LoginComponent },
];
