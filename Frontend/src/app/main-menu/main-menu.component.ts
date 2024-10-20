import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
interface ChartData {
  name: string;
  casos: number;
}

@Component({
  selector: 'main-menu',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './main-menu.component.html',
  styleUrls: ['./main-menu.component.scss']
})
export class MainMenuComponent implements OnInit {
  chartData: ChartData[] = [
    { name: 'Ene', casos: 4000 },
    { name: 'Feb', casos: 3000 },
    { name: 'Mar', casos: 2000 },
    { name: 'Abr', casos: 2780 },
    { name: 'May', casos: 1890 },
    { name: 'Jun', casos: 2390 },
  ];

  constructor() { }

  ngOnInit(): void {
  }
}