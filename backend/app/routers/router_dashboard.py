from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlmodel import select, func

from app.deps import DBSession
from app.models.models import (
    Sale,
    Product,
    User,
    Supplier,
    Customer,
    InventoryMovement,
    Inventory,
)
from app.models.enums import SaleStatus
from app.auth.auth import RoleChecker, get_current_user

router = APIRouter()

@router.get("/dashboard/metrics", tags=["Dashboard"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero", "Contador"]))])
async def get_dashboard_metrics(
    db: DBSession,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtener métricas principales para el dashboard
    """
    # Ventas de hoy
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
    
    ventas_hoy_query = select(func.sum(Sale.total_amount)).where(
        Sale.sale_date >= today_start,
        Sale.sale_date <= today_end,
        Sale.status == SaleStatus.completada
    )
    ventas_hoy = db.exec(ventas_hoy_query).first() or 0.0
    
    # Total productos
    total_productos = db.exec(select(func.count(Product.id))).first() or 0
    
    # Total usuarios
    total_usuarios = db.exec(select(func.count(User.id)).where(User.is_active == True)).first() or 0
    
    # Total proveedores
    total_proveedores = db.exec(select(func.count(Supplier.id)).where(Supplier.is_active == True)).first() or 0
    
    # Total clientes
    total_clientes = db.exec(select(func.count(Customer.id)).where(Customer.is_active == True)).first() or 0
    
    # Stock bajo (productos con cantidad menor o igual al mínimo)
    # Productos con stock por debajo del mínimo configurado
    stock_bajo_query = (
        select(func.count(Product.id))
        .select_from(Product)
        .join(Inventory, Inventory.product_id == Product.id, isouter=True)
        .group_by(Product.id, Product.stock_min)
        .having(func.coalesce(func.sum(Inventory.quantity), 0) <= Product.stock_min)
    )
    stock_bajo_result = db.exec(stock_bajo_query).all() or []
    stock_bajo = len(stock_bajo_result)
    
    return {
        "ventas_hoy": float(ventas_hoy),
        "total_productos": total_productos,
        "total_usuarios": total_usuarios,
        "total_proveedores": total_proveedores,
        "total_clientes": total_clientes,
        "stock_bajo": stock_bajo
    }


@router.get("/dashboard/recent-activity", tags=["Dashboard"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero", "Contador"]))])
async def get_recent_activity(
    db: DBSession,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtener actividad reciente del sistema
    """
    activities = []
    
    # Últimas ventas
    recent_sales = db.exec(
        select(Sale)
        .where(Sale.status == SaleStatus.completada)
        .order_by(Sale.sale_date.desc())
        .limit(5)
    ).all()
    
    for sale in recent_sales:
        time_diff = datetime.utcnow() - sale.sale_date
        activities.append({
            "title": "Venta completada",
            "description": f"Total: ${sale.total_amount:.2f}",
            "time": format_time_ago(time_diff),
            "type": "venta",
            "timestamp": sale.sale_date.isoformat()
        })
    
    # Últimos productos agregados
    recent_products = db.exec(
        select(Product)
        .order_by(Product.created_at.desc())
        .limit(3)
    ).all()
    
    for product in recent_products:
        time_diff = datetime.utcnow() - product.created_at
        activities.append({
            "title": "Nuevo producto agregado",
            "description": product.name,
            "time": format_time_ago(time_diff),
            "type": "producto",
            "timestamp": product.created_at.isoformat()
        })
    
    # Últimos movimientos de inventario
    recent_movements = db.exec(
        select(InventoryMovement)
        .order_by(InventoryMovement.created_at.desc())
        .limit(2)
    ).all()
    
    for movement in recent_movements:
        time_diff = datetime.utcnow() - movement.created_at
        # movement_type puede ser string o enum, manejar ambos casos
        movement_type_str = movement.movement_type.value if hasattr(movement.movement_type, 'value') else movement.movement_type
        activities.append({
            "title": "Movimiento de inventario",
            "description": f"{movement_type_str}: {movement.quantity} unidades",
            "time": format_time_ago(time_diff),
            "type": "inventario",
            "timestamp": movement.created_at.isoformat()
        })
    
    # Ordenar por timestamp descendente
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return activities[:limit]


@router.get("/dashboard/sales-summary", tags=["Dashboard"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Contador"]))])
async def get_sales_summary(
    db: DBSession,
    days: int = 7
) -> Dict[str, Any]:
    """
    Obtener resumen de ventas de los últimos días
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Total de ventas en el periodo
    total_sales_query = select(func.sum(Sale.total_amount)).where(
        Sale.sale_date >= start_date,
        Sale.status == SaleStatus.completada
    )
    total_sales = db.exec(total_sales_query).first() or 0.0
    
    # Cantidad de ventas
    count_sales_query = select(func.count(Sale.id)).where(
        Sale.sale_date >= start_date,
        Sale.status == SaleStatus.completada
    )
    count_sales = db.exec(count_sales_query).first() or 0
    
    # Promedio de venta
    avg_sale = float(total_sales) / count_sales if count_sales > 0 else 0.0
    
    return {
        "period_days": days,
        "total_sales": float(total_sales),
        "count_sales": count_sales,
        "average_sale": avg_sale,
        "start_date": start_date.isoformat(),
        "end_date": datetime.utcnow().isoformat()
    }


def format_time_ago(time_diff: timedelta) -> str:
    """Formatear diferencia de tiempo en texto legible"""
    seconds = time_diff.total_seconds()
    
    if seconds < 60:
        return "Hace unos segundos"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"Hace {minutes} min" if minutes == 1 else f"Hace {minutes} min"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"Hace {hours} hora" if hours == 1 else f"Hace {hours} horas"
    else:
        days = int(seconds / 86400)
        return f"Hace {days} día" if days == 1 else f"Hace {days} días"
