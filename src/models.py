"""
FerreRAP — Modelos del dominio
Patrones implementados: Observer, Strategy
IS2 · UCP · 2026
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ─────────────────────────────────────────────────────────────
#  PATRÓN OBSERVER
#  Sujeto: Producto (tabla en Supabase)
#  Observadores: Alerta, OrdenReposicion
#  Los observadores reaccionan automáticamente cuando el stock
#  de un producto cae por debajo del mínimo configurado.
# ─────────────────────────────────────────────────────────────

class Observador(ABC):
    """Interfaz base para todos los observadores del sistema."""

    @abstractmethod
    def actualizar(self, producto):
        """Llamado cuando el stock cae por debajo del mínimo."""
        pass

    def resolver(self, producto):
        """Llamado cuando el stock es repuesto y supera el mínimo.
        Implementar en subclases si aplica; por defecto no hace nada."""
        return None


class Alerta(Observador):
    """
    Observador concreto.
    Se activa cuando el stock de un Producto cae bajo el mínimo.
    Persiste las alertas en la tabla 'alertas' de Supabase.
    """
    def __init__(self, db):
        self.db = db

    def actualizar(self, producto):
        entrada = {
            "producto_nombre": producto["nombre"],
            "mensaje": f"Stock bajo en '{producto['nombre']}'",
            "tipo": "alerta",
            "stock_actual": producto["stock_actual"],
            "stock_minimo": producto["stock_minimo"],
            "leida": False,
        }
        self.db.table("alertas").insert(entrada).execute()
        return entrada

    def resolver(self, producto):
        """Registra en la base de datos que el stock fue normalizado."""
        entrada = {
            "producto_nombre": producto["nombre"],
            "mensaje": f"Stock normalizado en '{producto['nombre']}'",
            "tipo": "reposicion_ok",
            "stock_actual": producto["stock_actual"],
            "stock_minimo": producto["stock_minimo"],
            "leida": False,
        }
        self.db.table("alertas").insert(entrada).execute()
        return entrada


class OrdenReposicion(Observador):
    """
    Observador concreto.
    Genera una orden de reposición automática ante stock bajo.
    Persiste las órdenes en la tabla 'ordenes_reposicion' de Supabase.
    """
    def __init__(self, db):
        self.db = db

    def actualizar(self, producto):
        entrada = {
            "producto_nombre": producto["nombre"],
            "mensaje": f"Reponer '{producto['nombre']}'",
            "cantidad_sugerida": producto["stock_minimo"] * 2,
            "estado": "pendiente",
        }
        self.db.table("ordenes_reposicion").insert(entrada).execute()
        return entrada

    def resolver(self, producto):
        """Cierra automáticamente todas las órdenes pendientes del producto repuesto."""
        ahora = datetime.now().isoformat()
        result = self.db.table("ordenes_reposicion") \
            .update({"estado": "resuelta", "fecha_resolucion": ahora}) \
            .eq("producto_nombre", producto["nombre"]) \
            .eq("estado", "pendiente") \
            .execute()
        return result.data if result.data else None


# ─────────────────────────────────────────────────────────────
#  PATRÓN STRATEGY
#  Contexto: GeneradorReporte
#  Estrategias: ReporteReposicion, ReporteStockActual
#  Permite intercambiar el algoritmo de generación de reportes
#  en tiempo de ejecución sin modificar GeneradorReporte.
# ─────────────────────────────────────────────────────────────

class EstrategiaReporte(ABC):
    """Interfaz base para todas las estrategias de reporte."""
    @abstractmethod
    def generar(self, productos):
        pass


class ReporteReposicion(EstrategiaReporte):
    """Estrategia: devuelve solo productos con stock bajo mínimo."""
    def generar(self, productos):
        return [
            {
                "nombre": p["nombre"],
                "descripcion": p.get("descripcion", ""),
                "categoria": p["categoria"],
                "stock_actual": p["stock_actual"],
                "stock_minimo": p["stock_minimo"],
                "precio_costo": float(p["precio_costo"]),
                "precio_venta": float(p["precio_venta"]),
            }
            for p in productos if p["stock_actual"] < p["stock_minimo"]
        ]


class ReporteStockActual(EstrategiaReporte):
    """Estrategia: devuelve todos los productos con su estado completo."""
    def generar(self, productos):
        return [
            {
                "nombre": p["nombre"],
                "descripcion": p.get("descripcion", ""),
                "categoria": p["categoria"],
                "stock_actual": p["stock_actual"],
                "stock_minimo": p["stock_minimo"],
                "precio_costo": float(p["precio_costo"]),
                "precio_venta": float(p["precio_venta"]),
                "bajo_stock": p["stock_actual"] < p["stock_minimo"],
            }
            for p in productos
        ]


class GeneradorReporte:
    """
    Contexto del patrón Strategy.
    Delega la generación del reporte en la estrategia configurada.
    Se puede cambiar la estrategia en tiempo de ejecución.
    """
    def __init__(self, estrategia: EstrategiaReporte):
        self._estrategia = estrategia

    def cambiar_estrategia(self, estrategia: EstrategiaReporte):
        self._estrategia = estrategia

    def ejecutar(self, productos):
        return self._estrategia.generar(productos)
