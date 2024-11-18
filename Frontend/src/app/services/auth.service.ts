// src/app/services/auth.service.ts
import { jwtDecode } from 'jwt-decode';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';  // Importa HttpClient

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000'; // URL de tu backend

  constructor(private http: HttpClient) {}  // Inyecta HttpClient
  
  loginWithGoogle(): void {
    window.location.href = 'http://localhost:5000/auth/google';  // La URL del backend
  }

  // Nuevo método de inicio de sesión
  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, { username: username, password: password },{
      headers: { 'Content-Type': 'application/json' }});
  }

  // Método para guardar el token
  setToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  // Método para obtener el token
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  // Método para verificar si el usuario está autenticado
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }

  // Método para cerrar sesión
  logout(): void {
    localStorage.removeItem('access_token');
  }


  getUserData(): any {
    const token = this.getToken();
    if (!token) {
      return null;
    }
    const decodedToken: any = jwtDecode(token);
    return decodedToken.sub;
  }

  getDepartamentos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/departamentos`);
  }

  getProvincias(departamento: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/provincias?departamento=${departamento}`);
  }

  getDistritos(provincia: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/distritos?provincia=${provincia}`);
  }
  getResumen(): Observable<any> {
    return this.http.get(`${this.apiUrl}/resumen`);
  }

  getTendenciaCasos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/casos/tendencia`);
  }

  obtenerNoticias(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/api/noticias`);
  }

  getConsejos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/consejos`);
  }

  getNotificaciones(limit: number = 5): Observable<any> {
    return this.http.get(`${this.apiUrl}/notificaciones/recientes?limit=${limit}`);
  }
  getUserNotificaciones(): Observable<any> {
    const headers = {
      'Authorization': `Bearer ${this.getToken()}`,
      'Content-Type': 'application/json'
    };
    return this.http.get(`${this.apiUrl}/notificaciones/usuario`, { headers });
  }
}