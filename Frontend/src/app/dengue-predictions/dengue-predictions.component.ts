import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgApexchartsModule } from 'ng-apexcharts';
import {
  ChartComponent,
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexDataLabels,
  ApexStroke,
  ApexMarkers,
  ApexYAxis,
  ApexGrid,
  ApexTitleSubtitle,
  ApexLegend
} from "ng-apexcharts";

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  stroke: ApexStroke;
  dataLabels: ApexDataLabels;
  markers: ApexMarkers;
  colors: string[];
  yaxis: ApexYAxis;
  grid: ApexGrid;
  legend: ApexLegend;
  title: ApexTitleSubtitle;
};

@Component({
  selector: 'app-dengue-predictions',
  standalone: true,
  imports: [CommonModule, FormsModule, NgApexchartsModule],
  templateUrl: './dengue-predictions.component.html',
  styleUrls: ['./dengue-predictions.component.scss']
})
export class DenguePredictionsComponent implements OnInit {
  @ViewChild("chart") chart!: ChartComponent;
  public chartOptions: Partial<ChartOptions>;

  // Model metrics
  modelPrecision: number = 87;
  meanSquaredError: number = 0.23;
  
  // Alert data
  alert = {
    region: 'Región Norte',
    message: 'Aumento proyectado'
  };

  constructor() {
    this.chartOptions = {
      series: [
        {
          name: "Casos Reales",
          data: [130, 150, 195, 180, 190, 250]
        },
        {
          name: "Predicción",
          data: [130, 160, 195, 185, 200, 260]
        }
      ],
      chart: {
        height: 350,
        type: "line",
        dropShadow: {
          enabled: true,
          color: "#000",
          top: 18,
          left: 7,
          blur: 10,
          opacity: 0.2
        },
        toolbar: {
          show: false
        },
        fontFamily: 'Arial, sans-serif'
      },
      colors: ["#4CAF50", "#2196F3"],
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: "smooth",
        width: 3
      },
      grid: {
        borderColor: "#e7e7e7",
        row: {
          colors: ["#f3f3f3", "transparent"],
          opacity: 0.5
        }
      },
      markers: {
        size: 6,
        hover: {
          size: 8
        }
      },
      xaxis: {
        categories: ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
        title: {
          text: "Mes"
        }
      },
      yaxis: {
        title: {
          text: "Número de casos"
        },
        min: 0,
        max: 300
      },
      legend: {
        position: "top",
        horizontalAlign: "center",
        floating: true,
        offsetY: -25,
        offsetX: -5
      }
    };
  }

  ngOnInit(): void {
    // Any additional initialization logic
  }
}
