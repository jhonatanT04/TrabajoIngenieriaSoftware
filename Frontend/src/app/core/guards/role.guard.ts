import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {

    const roles = route.data['roles'] as string[] | undefined;

    if (!roles || roles.length === 0) {
      return true;
    }

    const userRole = this.auth.getRole();

    if (userRole && roles.includes(userRole)) {
      return true;
    }

    this.router.navigate(['/auth/login']);
    return false;
  }
}
