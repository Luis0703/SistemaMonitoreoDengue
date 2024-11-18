import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Routes } from '@angular/router';
import { MainMenuComponent } from './main-menu/main-menu.component';
import { LoginComponent } from './login/login.component';

// Definir las rutas
const routes: Routes = [
  { path: '', redirectTo: '/main-menu', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'main-menu', component: MainMenuComponent },
  // Agrega más rutas según sea necesario
];

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule, MainMenuComponent, LoginComponent],  // Importa componentes necesarios
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'SistemaMonitoreoDengue';
}
