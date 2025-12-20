import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import {
  NavbarComponent,
  SidebarComponent,
  FooterComponent,
  ModalComponent,
  ConfirmDialogComponent,
  TableComponent
} from './components';


@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    NavbarComponent,
    SidebarComponent,
    FooterComponent,
    ModalComponent,
    ConfirmDialogComponent,
    TableComponent
  ],
  exports: [
    CommonModule,
    NavbarComponent,
    SidebarComponent,
    FooterComponent,
    ModalComponent,
    ConfirmDialogComponent,
    TableComponent
  ]
})
export class SharedModule { }
