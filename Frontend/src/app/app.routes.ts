import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HeatMapComponent } from './heat-map/heat-map.component';
import { MainMenuComponent } from './main-menu/main-menu.component';

export const routes: Routes = [
    { path: 'main-menu', component: MainMenuComponent },
    { path: 'heat-map', component: HeatMapComponent }
   
];

export const appConfig = {
    providers: []
};