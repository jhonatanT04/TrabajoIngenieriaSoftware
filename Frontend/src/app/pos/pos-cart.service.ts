import { Injectable } from '@angular/core';

export interface PosCartItem {
  id: string;
  nombre: string;
  precio: number;
  stock: number;
  cantidad: number;
}

@Injectable({ providedIn: 'root' })
export class PosCartService {
  private storageKey = 'pos_cart_items';
  private items: PosCartItem[] = [];

  constructor() {
    this.items = this.readFromStorage();
  }

  getItems(): PosCartItem[] {
    return [...this.items];
  }

  setItems(items: PosCartItem[]): void {
    this.items = [...items];
    this.persist();
  }

  clear(): void {
    this.items = [];
    this.persist();
  }

  upsert(product: { id: string; nombre: string; precio: number; stock: number }): void {
    const idx = this.items.findIndex(i => i.id === product.id);
    if (idx >= 0) {
      if (this.items[idx].cantidad < product.stock) {
        this.items[idx].cantidad += 1;
      }
    } else {
      this.items.push({ ...product, cantidad: 1 });
    }
    this.persist();
  }

  updateQuantity(id: string, cantidad: number): void {
    this.items = this.items.map(i =>
      i.id === id ? { ...i, cantidad: Math.max(1, Math.min(i.stock, cantidad)) } : i
    );
    this.persist();
  }

  remove(id: string): void {
    this.items = this.items.filter(i => i.id !== id);
    this.persist();
  }

  total(): number {
    return this.items.reduce((acc, p) => acc + p.precio * p.cantidad, 0);
  }

  private persist(): void {
    sessionStorage.setItem(this.storageKey, JSON.stringify(this.items));
  }

  private readFromStorage(): PosCartItem[] {
    try {
      const raw = sessionStorage.getItem(this.storageKey);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }
}
