import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HeatMapComponent } from './heat-map/heat-map.component';
import { MainMenuComponent } from './main-menu/main-menu.component';
import { DenguePredictionsComponent } from './dengue-predictions/dengue-predictions.component';

export const routes: Routes = [
    { path: '', redirectTo: '/main-menu', pathMatch: 'full' },  // Redirige a la página principal por defecto
    { path: 'login', component: LoginComponent },  // Solo se accede aquí cuando el usuario quiere iniciar sesión
    { path: 'main-menu', component: MainMenuComponent },
    { path: 'heat-map', component: HeatMapComponent },
    { path: 'dengue-predictions', component: DenguePredictionsComponent },
    { path: '**', redirectTo: '/main-menu' }  // Redirige si la ruta no existe
];


export const appConfig = {
    providers: []
};
