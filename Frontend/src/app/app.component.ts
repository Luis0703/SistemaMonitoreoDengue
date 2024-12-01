import { Component } from '@angular/core';
import { Router } from '@angular/router';  // Necesitamos Router para escuchar cambios de ruta
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header/header.component'; // Importación del HeaderComponent
import { AuthService } from './services/auth.service';  // Servicio de autenticación

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule, HeaderComponent],  // El HeaderComponent está importado aquí
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'SistemaMonitoreoDengue';
  isAuthenticated: boolean = false;
  user: any = null;
  showHeader: boolean = true;  // Controla si el encabezado se muestra

  constructor(private authService: AuthService, private router: Router) {
    // Verificar estado de autenticación en la inicialización
    this.isAuthenticated = this.authService.isAuthenticated();
    this.user = this.authService.getUserData();

    // Escuchar los cambios de ruta
    this.router.events.subscribe(() => {
      // Mostrar el encabezado solo si no estamos en la página de login
      this.showHeader = this.router.url !== '/login';
    });
  }

  loginSuccess() {
    this.isAuthenticated = true;
    this.user = this.authService.getUserData();
  }

  logout() {
    this.authService.logout();
    this.isAuthenticated = false;
    this.user = null;
  }
}