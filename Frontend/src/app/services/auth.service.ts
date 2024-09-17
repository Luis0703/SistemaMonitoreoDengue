import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor() {}
/*
  login(credentials: { username: string; password: string }): Observable<boolean> {
    // Aquí iría la lógica real de autenticación con el backend
    // Por ahora, simulamos un login exitoso
    console.log('Logging in with:', credentials);
    return of(true);
  }
*/
  loginWithGoogle(): void {
    window.location.href = 'http://localhost:5000/auth/google';  // La URL del backend
   
  }
}