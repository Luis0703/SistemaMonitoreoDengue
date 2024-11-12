import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { MainMenuComponent } from './main-menu/main-menu.component';
import { HeatMapComponent } from './heat-map/heat-map.component';
import { DenguePredictionsComponent } from './dengue-predictions/dengue-predictions.component';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [
        CommonModule,
        RouterModule,
        LoginComponent,
        MainMenuComponent,
        HeatMapComponent,
        DenguePredictionsComponent,
    ],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'SistemaMonitoreoDengue';
    isLoggedIn = false;

    onLoginSuccess() {
        this.isLoggedIn = true;
    }
}