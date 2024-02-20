from typing import Dict

from entity import InfoNit, InfoGeneral, InfoFinacienciera, InfoRepLegal


class Builder:
    def __init__(self, data):
        self.__data = data
        self._result = {}

    def __get_data_info_financiera(self):
        if  "informacionFinanciera" in self.__data["registros"][0].keys():
            return self.__data["registros"][0]["informacionFinanciera"][0]
        else:
            return None

    def __get_data_info_rep_legal(self):
        if "vinculos" in self.__data["registros"][0].keys():
            rep_legal =[]
            for rep in self.__data["registros"][0]["vinculos"]:
                if rep["tipo_vinculo"]== 'Representante Legal - Principal':
                    rep_legal.append(rep)
                    return rep_legal[0]
        else:
            return None


    def __get_data_nit(self) -> str:
        return self.__data["nit"]

    def __build_nit(self):
        data = self.__get_data_nit()
        data = InfoNit(
            numero_identificacion=data
        ).model_dump()
        self._result.update(data)

    def __cantidad_establecimientos(self):
        if  "establecimientos" in self.__data["registros"][0].keydeactcd:
            return len(self.__data["registros"][0]["establecimientos"])
        else:
            return 0
    def __get_data_info_general(self):
        return self.__data["registros"][0]

    def __build_info_general(self):
        data = self.__get_data_info_general()
        data = InfoGeneral(
            camara=data.get("camara", ""),
            razon_social=data.get("razon_social", ""),
            tipo_identificacion=data.get("tipo_identificacion", ""),
            dv=data.get("digito_verificacion", ""),
            tipo_sociedad=data.get("tipo_sociedad", ""),
            tipo_organizacion=data.get("organizacion_juridica", ""),
            categoria_matricula=data.get("categoria_matricula", ""),
            direccion_comercial=data.get("direccion_comercial", ""),
            departamento=data.get("dpto_comercial", ""),
            municipio=data.get("municipio_comercial", ""),
            tel_comercial=data.get("telefono_comercial_1", ""),
            tel_com_2=data.get("telefono_comercial_2", ""),
            tel_com_3=data.get("telefono_comercial_3", ""),
            correo_comercial=data.get("correo_electronico_comercial", ""),
            ciiu=data.get("cod_ciiu_act_econ_pri", ""),
            actividad_economica=data.get("desc_ciiu_act_econ_pri", ""),
            ciiu_2=data.get("cod_ciiu_act_econ_sec", ""),
            actividad_economica_2=data.get("desc_ciiu_act_econ_sec", ""),
            ciiu_3=data.get("ciiu3", ""),
            actividad_economica_3=data.get("desc_ciiu3", ""),
            ciiu_4=data.get("ciiu4", ""),
            actividad_economica_4=data.get("desc_ciiu4", ""),
            numero_matricula="00000"+ data.get("matricula", "") if data.get("matricula") else "",
            fecha_matricula=data.get("fecha_matricula", ""),
            fecha_constitucion=data.get("fecha_constitucion", ""),
            fecha_renovacion=data.get("fecha_renovacion", ""),
            ultimo_ano_renovado=data.get("ultimo_ano_renovado", ""),
            estado=data.get("estado_matricula", ""),
            fecha_vigencia=data.get("fecha_vigencia", ""),
            fecha_cancelacion=data.get("fecha_cancelacion", ""),
            inscripcion_proponente=data.get("inscripcion_proponente", ""),
            empleados=data.get("numero_empleados", ""),
            cantidad_establecimientos=self.__cantidad_establecimientos(),
            fecha_actualizacion=data.get("fecha_actualizacion_rues", "")


        ).model_dump()
        self._result.update(data)

    def __build_info_financiera(self):
        data = self.__get_data_info_financiera()
        if data:
            data = InfoFinacienciera(
                ano_informacion_financiera=data["ano_informacion_financiera"],
                activo_corriente=data["activo_corriente"],
                activo_no_corriente=data["activo_no_corriente"],
                activo_total=data["activo_total"],
                pasivo_corriente=data["pasivo_corriente"],
                pasivo_no_corriente=data["pasivo_no_corriente"],
                pasivo_total=data["pasivo_total"],
                patrimonio_neto=data["patrimonio_neto"],
                ingresos_actividad_ordinaria=data["ingresos_actividad_ordinaria"],
                otros_ingresos=data["otros_ingresos"],
                costo_ventas=data["costo_ventas"],
                gastos_operacionales=data["gastos_operacionales"],
                otros_gastos=data["otros_gastos"],
                gastos_impuestos=data["gastos_impuestos"],
                utilidad_perdida_operacional=data["utilidad_perdida_operacional"],
                resultado_del_periodo=data["resultado_del_periodo"]

            ).model_dump()
            self._result.update(data)
        else:
            data = InfoFinacienciera().model_dump()
            self._result.update(data)

    def __build_rep_legal_info(self):
        data = self.__get_data_info_rep_legal()
        if data:
            data =InfoRepLegal(
                rep_legal=data["nombre"],
                rep_legal_tipo_vinculo=data["tipo_vinculo"],
                rep_legal_tipo_id=data["clase_identificacion"],
                rep_legal_numero_id=data["numero_identificacion"]
            ).model_dump()
            self._result.update(data)
        else:
            data = InfoRepLegal().model_dump()
            self._result.update(data)

    @property
    def get_data(self):
        self.__build_rep_legal_info()
        self.__build_nit()
        self.__build_info_financiera()
        self.__build_info_general()
        return self._result