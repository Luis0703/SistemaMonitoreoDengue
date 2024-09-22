import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { HeatMapComponent } from './heat-map/heat-map.component';
import { RouterOutlet } from '@angular/router';
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, LoginComponent, HeatMapComponent, RouterOutlet],
  templateUrl: './app.component.html', 
  styleUrls: ['./app.component.scss']
  
})
export class AppComponent {
  title = 'SistemaMonitoreoDengue';
  isLoggedIn = false;

   onLoginSuccess(){
    this.isLoggedIn=true
   }
}