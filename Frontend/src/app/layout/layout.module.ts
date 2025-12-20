import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AdminLayoutComponent } from './admin-layout/admin-layout.component';
import { PosLayoutComponent } from './pos-layout/pos-layout.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    AdminLayoutComponent,
    PosLayoutComponent
  ],
  exports: [
    AdminLayoutComponent,
    PosLayoutComponent
  ]
})
export class LayoutModule { }
