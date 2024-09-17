import { Routes } from '@angular/router';
import { HeatMapComponent } from './heat-map/heat-map.component';

export const routes: Routes = [
  { path: 'heat-map', component: HeatMapComponent },
  { path: '', redirectTo: '/heat-map', pathMatch: 'full' },
  // Agrega más rutas aquí para futuros componentes
];