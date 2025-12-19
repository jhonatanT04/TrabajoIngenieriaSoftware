import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ExportCsvService {

  export(data: any[]) {
    console.log('Exportando CSV', data);
  }
}
