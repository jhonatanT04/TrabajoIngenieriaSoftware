import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ExportExcelService {

  export(data: any[]) {
    console.log('Exportando Excel', data);
  }
}
