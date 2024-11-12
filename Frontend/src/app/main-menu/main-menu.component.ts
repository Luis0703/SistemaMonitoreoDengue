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
  totalCasos: number = 0;
  alertasActivas: number = 0;
  zonasControladas: string = '0%';
  noticias: any[] = [];
  consejos: any[] = [];
  indiceNoticiaActual: number = 0;

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

  cargarResumen(): void {
    this.dataService.getResumen().subscribe(data => {
      this.totalCasos = data.totalCasos;
      this.alertasActivas = data.alertasActivas;
      this.zonasControladas = `${data.zonasControladas}%`;
    });
  }

  cargarTendenciaCasos(): void {
    this.dataService.getTendenciaCasos().subscribe(data => {
      // Asignar los años como etiquetas y los casos como datos
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
  // Método para ir a la siguiente noticia
  siguienteNoticia(): void {
    this.indiceNoticiaActual = (this.indiceNoticiaActual + 1) % this.noticias.length;
  }
  // Método para ir a la noticia anterior
  noticiaAnterior(): void {
    this.indiceNoticiaActual =
      (this.indiceNoticiaActual - 1 + this.noticias.length) % this.noticias.length;
  }

  cargarConsejos(): void {
    this.dataService.getConsejos().subscribe(data => {
      this.consejos = data;
    });
  }
}
