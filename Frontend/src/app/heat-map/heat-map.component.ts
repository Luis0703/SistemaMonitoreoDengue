import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { GoogleMapsModule } from '@angular/google-maps';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface HeatMapData {
  lat: number;
  lng: number;
  cantidad_casos: number;
}

@Component({
  selector: 'app-heat-map',
  standalone: true,
  imports: [FormsModule, GoogleMapsModule, CommonModule],
  templateUrl: './heat-map.component.html',
  styleUrls: ['./heat-map.component.scss']
})
export class HeatMapComponent implements OnInit {
  title = 'Mapa de Calor';
  
  // Configuración del mapa
  center: google.maps.LatLngLiteral = {
    lat: -9.189967,  // Centrando en Perú
    lng: -75.015152
  };
  zoom = 5;
  options: google.maps.MapOptions = {
    mapTypeId: 'terrain',
    zoomControl: true,
    scrollwheel: true,
    disableDoubleClickZoom: true,
    maxZoom: 15,
    minZoom: 4,
  };

  // Propiedades para los filtros
  timePeriod: string = '';
  department: string = '';
  province: string = '';
  district: string = '';
  
  fechaInicio: string = '';
  fechaFin: string = '';
  
  departamentos: string[] = [];
  provincias: string[] = [];
  distritos: string[] = [];

  periodosTiempo = [
    { value: 'ultima-semana', label: 'Última semana' },
    { value: 'ultimo-mes', label: 'Último mes' },
    { value: 'ultimo-año', label: 'Último año' },
    { value: 'rango-personalizado', label: 'Rango personalizado' }
  ];

  constructor(
    private regionService: AuthService,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.cargarDepartamentos();
    this.loadHeatMapData();
  }

  loadHeatMapData() {
    let url = 'http://localhost:5000/casos/mapa-calor?';
    const params = new URLSearchParams();

    if (this.timePeriod === 'rango-personalizado' && this.fechaInicio && this.fechaFin) {
      params.append('fecha_inicio', this.fechaInicio);
      params.append('fecha_fin', this.fechaFin);
    }
    if (this.department) params.append('departamento', this.department);
    if (this.province) params.append('provincia', this.province);
    if (this.district) params.append('distrito', this.district);

    url += params.toString();

    this.http.get<{data: HeatMapData[]}>(url).subscribe({
      next: (response) => {
        console.log('Datos recibidos para el mapa de calor:', response.data);
        this.updateHeatMap(response.data);
      },
      error: (error) => {
        console.error('Error al cargar los datos del mapa de calor:', error);
      }
    });
  }

  heatmap: google.maps.visualization.HeatmapLayer | null = null;
  map: google.maps.Map | null = null;

  updateHeatMap(data: HeatMapData[]) {
    if (!this.map) {
      console.error('Mapa no inicializado');
      return;
    }

    if (!google.maps.visualization) {
      console.error('Biblioteca de visualización de Google Maps no está cargada');
      return;
    }

    const heatmapData = data.map(point => ({
      location: new google.maps.LatLng(point.lat, point.lng),
      weight: point.cantidad_casos
    }));

    if (this.heatmap) {
      this.heatmap.setData(heatmapData);
    } else {
      this.heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        map: this.map,
        radius: 30,
        opacity: 0.6
      });
    }
  }

  onMapReady(map: google.maps.Map) {
    this.map = map;
    console.log('El mapa está listo');
  }

  cargarDepartamentos() {
    this.regionService.getDepartamentos().subscribe({
      next: (response) => {
        this.departamentos = response.departamentos;
      },
      error: (error) => {
        console.error('Error al cargar departamentos:', error);
      }
    });
  }

  onDepartamentoChange() {
    if (this.department) {
      this.regionService.getProvincias(this.department).subscribe({
        next: (response) => {
          this.provincias = response.provincias;
          this.province = '';
          this.district = '';
          this.distritos = [];
          this.loadHeatMapData();
        },
        error: (error) => {
          console.error('Error al cargar provincias:', error);
        }
      });
    }
  }

  onProvinciaChange() {
    if (this.province) {
      this.regionService.getDistritos(this.province).subscribe({
        next: (response) => {
          this.distritos = response.distritos;
          this.district = '';
          this.loadHeatMapData();
        },
        error: (error) => {
          console.error('Error al cargar distritos:', error);
        }
      });
    }
  }

  onSearch() {
    this.loadHeatMapData();
  }
}
