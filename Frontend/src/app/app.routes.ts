import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HeatMapComponent } from './heat-map/heat-map.component';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'heat-map', component: HeatMapComponent },
  //{ path: '', redirectTo: '/heat-map', pathMatch: 'full' },
  
  // Agrega más rutas aquí para futuros componentes
];