import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  styles: [`
    .login-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem;
    }

    .login-card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
      padding: 3rem;
      max-width: 500px;
      width: 100%;
    }

    .login-header {
      text-align: center;
      margin-bottom: 2rem;
    }

    .logo-container {
      margin-bottom: 1rem;
    }

    .logo-icon {
      font-size: 4rem;
      color: #667eea;
    }

    h1 {
      color: #333;
      font-size: 1.75rem;
      margin-bottom: 0.25rem;
      font-weight: 600;
    }

    h2 {
      color: #667eea;
      font-size: 1.125rem;
      margin-bottom: 0.5rem;
      font-weight: 500;
    }

    .subtitle {
      color: #666;
      font-size: 0.875rem;
    }

    .form-box {
      background: #1a202c;
      border-radius: 16px;
      padding: 2.5rem 2rem;
      margin-bottom: 1.5rem;
      box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
    }

    .form-title {
      color: #cbd5e1;
      font-size: 1.125rem;
      font-weight: 600;
      margin: 0 0 2rem 0;
      text-align: center;
    }

    .login-form {
      margin: 0;
    }

    .form-group {
      margin-bottom: 1.75rem;
    }

    .form-group:last-of-type {
      margin-bottom: 1.5rem;
    }

    label {
      display: block;
      color: #94a3b8;
      font-weight: 500;
      margin-bottom: 0.625rem;
      font-size: 0.9rem;
    }

    .input-group {
      position: relative;
      margin-bottom: 0.25rem;
    }

    .input-icon {
      position: absolute;
      left: 1rem;
      top: 50%;
      transform: translateY(-50%);
      color: #64748b;
      font-size: 1.25rem;
      z-index: 1;
    }

    .input-group input {
      width: 100%;
      padding: 0.9rem 3rem 0.9rem 3rem;
      background: #0f172a;
      border: 2px solid #2d3748;
      border-radius: 10px;
      font-size: 1rem;
      color: #e2e8f0;
      transition: all 0.3s;
      box-sizing: border-box;
    }

    .input-group input::placeholder {
      color: #4a5568;
      font-size: 0.95rem;
    }

    .input-group input:focus {
      outline: none;
      border-color: #667eea;
      background: #1e293b;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .input-group input.error {
      border-color: #dc3545;
    }

    .toggle-password {
      position: absolute;
      right: 1rem;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: #64748b;
      cursor: pointer;
      padding: 0.25rem;
      z-index: 1;
    }

    .toggle-password:hover {
      color: #94a3b8;
    }

    .error-message {
      color: #dc3545;
      font-size: 0.875rem;
      margin-top: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }

    .error-message .material-icons {
      font-size: 1rem;
    }

    .forgot-password {
      display: block;
      text-align: right;
      margin-top: 0.5rem;
      color: #667eea;
      font-size: 0.875rem;
      text-decoration: none;
    }

    .forgot-password:hover {
      text-decoration: underline;
    }

    .alert {
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .alert-danger {
      background-color: #f8d7da;
      color: #721c24;
      border: 1px solid #f5c6cb;
    }

    .btn-login {
      width: 100%;
      padding: 1rem;
      background: #475569;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 0.875rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      cursor: pointer;
      transition: all 0.3s;
      text-transform: uppercase;
    }

    .btn-login:hover:not(:disabled) {
      background: #334155;
    }

    .btn-login:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .login-footer {
      text-align: center;
      color: #666;
      font-size: 0.875rem;
    }

    .login-footer p {
      margin: 0.5rem 0;
    }

    .login-footer a {
      color: #667eea;
      font-weight: 600;
      text-decoration: none;
    }

    .login-footer a:hover {
      text-decoration: underline;
    }

    .demo-credentials {
      margin-top: 1rem;
      padding: 1rem;
      background-color: #f8f9fa;
      border-radius: 8px;
      border-left: 4px solid #667eea;
    }

    .demo-credentials code {
      background-color: #e9ecef;
      padding: 0.2rem 0.4rem;
      border-radius: 4px;
      font-family: monospace;
      font-size: 0.875rem;
    }

    @media (max-width: 768px) {
      .login-card {
        padding: 2rem;
      }

      .form-box {
        padding: 1.5rem;
      }
    }
  `]
})
export class LoginComponent {

  loginForm: FormGroup;
  loading = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  showPassword = false;

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  login() {
    if (this.loginForm.invalid) return;

    this.loading = true;
    this.errorMessage = '';

    const { username, password } = this.loginForm.value;

    this.authService.login(username, password).subscribe({
      next: (user: any) => {
        this.loading = false;

        if (user.role === 'CAJERO') {
          this.router.navigate(['/pos']);
        } else if (user.role === 'ADMIN') {
          this.router.navigate(['/dashboard/admin']);
        } else {
          this.router.navigate(['/dashboard']);
        }
      },
      error: () => {
        this.loading = false;
        this.errorMessage = 'Usuario o contraseña incorrectos';
      }
    });
  }
}
