import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-heat-map',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './heat-map.component.html',
  styleUrls: ['./heat-map.component.scss']
})
export class HeatMapComponent {
  title = 'MAPA DE CALOR';
  
  // Properties for dropdown menus
  timePeriod: string = '';
  department: string = '';
  province: string = '';
  district: string = '';

  // Method to handle search
  onSearch() {
    console.log('Searching with:', { timePeriod: this.timePeriod, department: this.department, province: this.province, district: this.district });
    // Implement search logic here
  }
}