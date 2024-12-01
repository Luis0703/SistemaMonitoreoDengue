import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  @Input() isAuthenticated: boolean = false; // Recibe el estado de autenticación
  @Input() user: any = null; // Recibe los datos del usuario
  notificaciones: any[] = [];
  showNotifications: boolean = false;

  constructor(private dataService: AuthService) {}

  ngOnInit(): void {
    // Si el usuario está autenticado, cargamos sus notificaciones
    if (this.isAuthenticated) {
      console.log('Usuario autenticado:', this.user); // Debug
      this.cargarNotificacionesUsuario(); // Cargar notificaciones específicas
    } else {
      console.log('Usuario no autenticado: no se cargan notificaciones');
      this.notificaciones = []; // No cargar notificaciones si no está autenticado
    }
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
    // Si no está autenticado, no cargar notificaciones generales
    if (!this.isAuthenticated) {
      this.notificaciones = []; // No cargamos notificaciones generales
      return;
    }

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
    this.notificaciones = [];  // Limpiar las notificaciones al cerrar sesión
  }
}