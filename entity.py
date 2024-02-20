from typing import Optional

from pydantic import BaseModel

class InfoNit(BaseModel):
    numero_identificacion: Optional[str] = ""


class InfoGeneral(BaseModel):
    camara: Optional[str] = ""
    razon_social: Optional[str] = ""
    tipo_identificacion: Optional[str] = ""
    dv: Optional[str] = ""
    tipo_sociedad: Optional[str] = ""
    tipo_organizacion: Optional[str] = ""
    categoria_matricula: Optional[str] = ""
    direccion_comercial: Optional[str] = ""
    departamento: Optional[str] = ""
    municipio: Optional[str] = ""
    tel_comercial: Optional[str] = ""
    tel_com_2: Optional[str] = "" # No viene
    tel_com_3: Optional[str] = "" # No viene
    correo_comercial: Optional[str] = ""
    dirweb: Optional[str] = "" # No viene
    ciiu: Optional[str] = ""
    actividad_economica: Optional[str] = ""
    ciiu_2: Optional[str] = ""
    actividad_economica_2: Optional[str] = ""
    ciiu_3: Optional[str] = ""
    actividad_economica_3: Optional[str] = ""
    ciiu_4: Optional[str] = ""
    actividad_economica_4: Optional[str] = ""
    clasificacion_imp_exp: Optional[str] = "0" # No viene
    empresa_familiar: Optional[str] = "" # No Viene
    proceso_innovacion: Optional[str] = "" # No viene
    numero_matricula: Optional[str] = ""
    fecha_matricula: Optional[str] = ""
    fecha_constitucion: Optional[str] = ""
    fecha_renovacion: Optional[str] = ""
    ultimo_ano_renovado: Optional[str] = ""
    estado: Optional[str] = ""
    fecha_vigencia: Optional[str] = "" # No viene
    fecha_cancelacion: Optional[str] = ""
    inscripcion_proponente: Optional[str] = ""
    empleados: Optional[str] = 0
    porcentaje_empleados_temporales: Optional[int] = 0 # No viene
    tamano_empresa: Optional[str]= ""  # No viene
    grupo_niif:  Optional[str]= ""  # No viene
    cantidad_establecimientos: Optional[int] = 0
    fecha_actualizacion: Optional[str]= ""


class InfoFinacienciera(BaseModel):
    ano_informacion_financiera: Optional[str] = ""
    activo_corriente: Optional[int] = 0
    activo_no_corriente: Optional[int] = 0
    activo_total: Optional[int] = 0
    pasivo_corriente: Optional[int] = 0
    pasivo_no_corriente: Optional[int] = 0
    pasivo_total: Optional[int] = 0
    patrimonio_neto: Optional[int] = 0
    ingresos_actividad_ordinaria: Optional[int] = 0
    otros_ingresos: Optional[int] = 0
    costo_ventas: Optional[int] = 0
    gastos_operacionales: Optional[int] = 0
    otros_gastos: Optional[int] = 0
    gastos_impuestos: Optional[int] = 0
    utilidad_perdida_operacional: Optional[int] = 0
    resultado_del_periodo: Optional[int] = 0

class InfoRepLegal(BaseModel):
    rep_legal: Optional[str] = ""
    rep_legal_tipo_vinculo: Optional[str] = ""
    rep_legal_tipo_id: Optional[str] = ""
    rep_legal_numero_id: Optional[str] = ""