import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { GoogleMapsModule } from '@angular/google-maps';

@Component({
  selector: 'app-heat-map',
  standalone: true,
  imports: [FormsModule, GoogleMapsModule], // Añade GoogleMapsModule
  templateUrl: './heat-map.component.html',
  styleUrls: ['./heat-map.component.scss']
})
export class HeatMapComponent {
  title = 'MAPA DE CALOR';
  
// Configuración del mapa
center: google.maps.LatLngLiteral = {
  lat: -12.046374,
  lng: -77.042793,
};
zoom = 5;
options: google.maps.MapOptions = {
  // Puedes añadir opciones adicionales si lo deseas
};
// Propiedades para los menús desplegables

  timePeriod: string = '';
  department: string = '';
  province: string = '';
  district: string = '';

// Método que se ejecuta cuando el mapa está listo
onMapReady(map: google.maps.Map) {
  console.log('Mapa cargado con éxito:', map);
}
// Método de búsqueda
  onSearch() {
    console.log('Searching with:', {
      timePeriod: this.timePeriod,
      department: this.department,
      province: this.province,
      district: this.district
    });
  }
}