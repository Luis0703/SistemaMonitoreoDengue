import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { BaseChartDirective } from 'ng2-charts';
import { Chart, ChartData, ChartOptions, registerables } from 'chart.js';
import { AuthService } from '../services/auth.service';
import { RouterModule } from '@angular/router';

Chart.register(...registerables);

@Component({
  selector: 'app-main-menu',
  standalone: true,
  imports: [CommonModule, HttpClientModule, BaseChartDirective, RouterModule],
  templateUrl: './main-menu.component.html',
  styleUrls: ['./main-menu.component.scss'],
  providers: [AuthService]
})
export class MainMenuComponent implements OnInit {
  isAuthenticated: boolean = false;
  user: any = null;
  totalCasos: number = 0;
  alertasActivas: number = 0;
  zonasControladas: string = '0%';
  noticias: any[] = [];
  consejos: any[] = [];
  indiceNoticiaActual: number = 0;
  notificaciones: any[] = [];
  showNotifications: boolean = false;

  public barChartData: ChartData<'bar'> = {
    labels: [],
    datasets: [
      {
        label: 'Casos',
        data: [],
        backgroundColor: '#42A5F5',
      },
    ],
  };

  public barChartOptions: ChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
    },
  };

  constructor(private dataService: AuthService) {}

  ngOnInit(): void {
    this.cargarResumen();
    this.cargarTendenciaCasos();
    this.cargarNoticias();
    this.cargarConsejos();
  }
  


  cargarNotificacionesUsuario(): void {
    this.dataService.getUserNotificaciones().subscribe({
      next: (data) => {
        this.notificaciones = data.data; // Ajusta según el formato del backend
      },
      error: (err) => {
        console.error('Error al cargar notificaciones del usuario:', err);
      }
    });
  }

  cargarNotificaciones(): void {
    this.dataService.getNotificaciones(5).subscribe({
      next: (data) => {
        this.notificaciones = data.data; // Ajusta según el formato del backend
      },
      error: (err) => {
        console.error('Error al cargar notificaciones generales:', err);
      }
    });
  }

  toggleNotifications(): void {
    this.showNotifications = !this.showNotifications;
  }

  logout(): void {
    this.dataService.logout();
    this.isAuthenticated = false;
    this.user = null;
  }

  cargarResumen(): void {
    this.dataService.getResumen().subscribe(data => {
      this.totalCasos = data.totalCasos;
      this.alertasActivas = data.alertasActivas;
      this.zonasControladas = `${data.zonasControladas}%`;
    });
  }

  cargarTendenciaCasos(): void {
    this.dataService.getTendenciaCasos().subscribe(data => {
      this.barChartData.labels = data.map((item: any) => item.anio.toString());
      this.barChartData.datasets[0].data = data.map((item: any) => item.casos);
    });
  }

  cargarNoticias(): void {
    this.dataService.obtenerNoticias().subscribe(
      (data) => {
        this.noticias = data;
      },
      (error) => {
        console.error('Error al cargar las noticias:', error);
      }
    );
  }

  irANoticia(indice: number): void {
    this.indiceNoticiaActual = indice;
  }

  cargarConsejos(): void {
    this.dataService.getConsejos().subscribe(data => {
      this.consejos = data;
    });
  }
}
