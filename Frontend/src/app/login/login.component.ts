// src/app/login/login.component.ts

import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';  // Importa el servicio de autenticación
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  @Output() loginSuccess = new EventEmitter<void>();  // Añade el Output para el evento
  loginForm: FormGroup;
  errorMessage: string = '';

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const { username, password } = this.loginForm.value;

      this.authService.login(username, password).subscribe(
        (response) => {
          // Guarda el token
          this.authService.setToken(response.access_token);
          // Emitir el evento loginSuccess
          this.loginSuccess.emit();
          // Navegar a la ruta heat-map
          this.router.navigate(['/heat-map']);
        },
        (error) => {
          // Manejo de errores
          this.errorMessage = error.error.message || 'Error al iniciar sesión';
        }
      );
    }
  }

  // Función para manejar el login con Google
  loginWithGoogle(): void {
    this.authService.loginWithGoogle();
  }
}
