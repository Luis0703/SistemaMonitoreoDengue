import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { HeatMapComponent } from './heat-map/heat-map.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, LoginComponent, HeatMapComponent],
  templateUrl: './app.component.html', 
  styleUrls: ['./app.component.scss']
  
})
export class AppComponent {
  title = 'SistemaMonitoreoDengue';
}