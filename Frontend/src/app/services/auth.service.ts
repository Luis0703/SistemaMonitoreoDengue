import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() { }

  loginWithGoogle(): void {
    window.location.href = 'http://localhost:5000/auth/google';  // La URL del backend
  }
}
