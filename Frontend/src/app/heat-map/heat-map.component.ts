import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { GoogleMapsModule } from '@angular/google-maps';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';


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
  private apiUrl = environment.apiUrl; // Usar apiUrl del entorno

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

  // Propiedades para el filtro de semanas
  anioInicio: number | null = null;
  semanaInicio: number | null = null;
  anioFin: number | null = null;
  semanaFin: number | null = null;
  
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
    this.loadHeatMapData();  // Cargar los datos globales del mapa de calor al inicio
  }

  // Función para cargar todos los datos del mapa de calor
  loadHeatMapData() {
    const url = `${this.apiUrl}/casos/mapa-calor`;

    this.http.get<{data: HeatMapData[]}>(url).subscribe({
      next: (response) => {
        console.log('Datos recibidos para el mapa de calor:', response.data);
        this.updateHeatMap(response.data);  // Actualizar el mapa con todos los puntos
      },
      error: (error) => {
        console.error('Error al cargar los datos del mapa de calor:', error);
      }
    });
  }

  heatmap: google.maps.visualization.HeatmapLayer | null = null;
  map: google.maps.Map | null = null;

  // Actualizar los datos del mapa de calor
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

  // Inicializar el mapa cuando esté listo
  onMapReady(map: google.maps.Map) {
    this.map = map;
    console.log('El mapa está listo y centrado en:', this.center.lat, this.center.lng);
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
        },
        error: (error) => {
          console.error('Error al cargar distritos:', error);
        }
      });
    }
  }

  // Función para aplicar el zoom al área seleccionada sin filtrar los datos
  onSearch() {
    let url = `${this.apiUrl}/casos/mapa-calor?`;
    const params = new URLSearchParams();
  
    // Solo incluir filtros de tiempo si se seleccionan semanas
    if (this.timePeriod === 'rango-personalizado' && this.anioInicio && this.semanaInicio && this.anioFin && this.semanaFin) {
      params.append('anio_inicio', this.anioInicio.toString());
      params.append('semana_inicio', this.semanaInicio.toString());
      params.append('anio_fin', this.anioFin.toString());
      params.append('semana_fin', this.semanaFin.toString());
    }
    
  
    url += params.toString();
  
    // Solicitar datos del mapa de calor (sin filtrar por lugar)
    this.http.get<{data: HeatMapData[]}>(url).subscribe({
      next: (response) => {
        console.log('Datos recibidos:', response.data);
        this.updateHeatMap(response.data);  // Actualiza los datos solo con el filtro de tiempo
      },
      error: (error) => {
        console.error('Error al cargar los datos del mapa de calor:', error);
      }
    });
  
    // Solo hacer zoom si se selecciona un lugar
    if (this.department || this.province || this.district) {
      this.centerMapOnSelectedRegion();
    }
  }
  
  centerMapOnSelectedRegion() {
    let url = `${this.apiUrl}/regiones/coords?`;
    const params = new URLSearchParams();
  
    if (this.district) {
      params.append('distrito', this.district);
    } else if (this.province) {
      params.append('provincia', this.province);
    } else if (this.department) {
      params.append('departamento', this.department);
    }
  
    url += params.toString();
  
    // Obtener coordenadas para hacer zoom en la región seleccionada
    this.http.get<{ lat: number, lng: number }>(url).subscribe({
      next: (response) => {
        this.center = { lat: response.lat, lng: response.lng };
        this.zoom = 12;  // Ajustar el nivel de zoom según sea necesario
        this.map?.setCenter(this.center);
        this.map?.setZoom(this.zoom);
      },
      error: (error) => {
        console.error('Error al obtener las coordenadas para el zoom:', error);
      }
    });
  }
}
