import copy
import inspect
import json
from datetime import datetime
from typing import Tuple

from app.databases.errors import DeleteFailed, ExecuteQueryFailed, InsertFailed, UpdateFailed
from app.databases.mysql import MySQLConnection
from app.utils.logger import Logger


class Model:  # pragma: no cover
    """Classe de interface dos modelos."""

    _table = ""
    _suffix = ""
    _pk = ""

    def __init__(self, db: MySQLConnection, **kwargs):
        """Construtor da modelo."""
        self._database = db
        Model.__fill(instance=self, attributes=kwargs)

    def populate_from_dict(self, data: dict):
        """Método auxiliar que vai popular os atributos do objeto à partir de uma dict.

        Args:
            data(dict): Dict com os atributos preenchidos da classe alvo.
        """
        obj_attrs = list(filter(lambda x: not x.startswith("_"), dir(self)))
        for key in obj_attrs:
            if data.get(key):
                self.__dict__[key] = data.get(key)

    def _insert(self, data: dict):
        """Insere os dados na tabela.

        Args:
            data (dict): dados que devem ser inseridos na tabela.

        Returns:
            resultado ou raise InsertFailed exceção
        """
        Logger().debug("[Model] Trying to insert record.")
        try:
            values = {
                str(key).upper(): data[key] for key in data if key not in ["_table", "_database"]
            }
            result = self._database.insert(table=self._table, data=values)
        except InsertFailed as error:
            raise error

        return result

    def _insert_fields(self, columns: tuple, values: list):
        """
        Insere os dados das colunas e valores na tabela.

        Args:
            columns (tuple): e.g ("column1", "column2", "column2", ...)
            values (list): e.g.  [(value1, value2, value3), (value1, value2, value3), ...]
        Returns:
            resultado ou raise InsertFailed exceção
        """
        Logger().debug("[Model] Trying to insert fields.")
        try:
            result = self._database.insert_fields(
                table=self._table, columns_insert=columns, values_insert=values
            )
        except InsertFailed as error:
            raise error

        self._database.commit()
        return result

    def _update(self, data: dict, where: str):
        """
        Atualiza os dados da tabela.

        Args:
            data (dict): e.g {"column1": "value1", "column2": "value2", "color": "red"}
            where (str): e.g ("id=%s AND year=%s", [id, year]) or ["id=1"]
        Returns:
            Bool ou raise UpdateFailed exceção
        """
        Logger().debug("[Model] Trying to update record.")
        if where is None:
            return False

        try:
            values = {
                str(key).upper(): data[key] for key in data if key not in ["_table", "_database"]
            }
            self._database.update(table=self._table, data=values, where=where)
        except UpdateFailed as error:
            raise error

        return True

    def _delete(self, where: tuple):
        """
        Deletar um registro da tabela.

        Args:
            where (tuple): e.g ("id=%s AND year=%s", [id, year])
        Returns:
            Bool ou raise DeleteFailed exceção
        """
        Logger().debug("[Model] Trying to delete record.")
        if where is None:
            return False

        try:
            self._database.delete(table=self._table, where=where)

        except DeleteFailed as error:
            raise error

        self._database.commit()

        # Clean values from fields into a instance
        values = {
            str(key).lower(): None for key in self.__dict__ if key not in ["_table", "_database"]
        }
        self.__dict__.update(values)
        return True

    def _columns(self):
        """Retorna as colunas do modelo."""
        columns = self._columns_with_value()
        return [column[0] for column in columns]

    def _columns_with_value(self):
        """Retorna as colunas e o valor atribuido."""
        columns = []
        for model_attributes in inspect.getmembers(self):
            # remove funções privadas e protegidas
            # remove outros métodos que não começam com underscore '_'
            if (
                not model_attributes[0].startswith("_")
                and not callable(model_attributes[1])
                and not isinstance(inspect.getattr_static(self, model_attributes[0]), staticmethod)
            ):
                columns.append(model_attributes)
        return columns

    def save(self):
        """
        Altera ou Atualiza um registro da tabela.

        Caso a pk esteja preenchida irá executar um update, caso
        não ira realizar um insert
        """
        index = self.__dict__.get(self._pk)
        columns = list(filter(lambda x: x is not self._pk, self._columns()))
        data_value = {str(key).upper(): self.__getattr(key) for key in columns}
        if index:
            return self._update(data_value, (self._pk + "=%s", [index]))
        insert_id = self._insert(data_value)
        if self._pk:
            self.__dict__[self._pk] = insert_id
        return insert_id

    def __getattr(self, key: str):
        """Retorna o valor de um atributo do objeto.

        Args:
            key (str): nome do atributo

        Returns:
            [Any]: Valor do atributo
        """
        value = getattr(self, key)
        return json.dumps(value) if isinstance(value, dict) else value

    def create_table(self, suffix: str = None) -> Tuple[bool, str]:
        """
        Cria uma nova tabela  no banco à partir do modelo da classe.

        Args:
            suffix (str): Sufixo para nova tabela.  Valor default é None.
        Returns:
            Tuple[bool, str].
        """
        temp_suffix = "" if not suffix else f"_{suffix}"
        table_name = f"{self._table}{str(temp_suffix).upper()}"
        sql_columns = ""

        for col_type in self._columns():
            if col_type != self._pk:
                if isinstance(getattr(self, col_type), int):
                    sql_columns += f"`{col_type}` INT,"
                elif isinstance(getattr(self, col_type), dict):
                    sql_columns += f"`{col_type}` JSON,"
                else:
                    sql_columns += f"`{col_type}` VARCHAR(250),"

        if self._pk:
            sql_script = f"""CREATE TABLE {table_name} (`{self._pk}` INT NOT NULL AUTO_INCREMENT,
                        {sql_columns} PRIMARY KEY (`{self._pk}`));"""
        else:
            sql_script = f"CREATE TABLE {table_name} ({sql_columns[:-1]}); "

        try:
            self._database.query(sql_script)
        except ExecuteQueryFailed as error:
            return False, f"Tabela {self._table} não foi criada{error}"

        return True, f"Tabela {self._table} Criada"

    def remove(self, ignore_columns=None):
        """Delete o registro do banco."""
        if ignore_columns is None:
            ignore_columns = []
        pk_value = self.__dict__.get(self._pk)
        if pk_value:
            where = "%s = %s" % (self._pk, pk_value)
        else:
            where = self.build_where(ignore_columns=ignore_columns)
        try:
            self._database.delete(table=self._table, where=[where])
        except DeleteFailed as error:
            raise error

    def drop_table(self):
        """Deletar a tabela do banco."""
        try:
            self._database.drop_table(table=self._table)

        except DeleteFailed as error:
            raise error

    def filter_in(
        self,
        field_in: str,
        values: list,
        fields="*",
    ) -> list:
        """
        Procura registros filtrando pelo campo no qual contem valores em uma lista (IN).

        Args:
            fields (str):. Columns to show
            field_in (str): Name of field / column filtered
            values (list): Param filters
        Returns:
            resultado ou raise ExecuteQueryFailed exceção
        """
        Logger().debug("[Model] Trying to filter in.")
        if not values:
            msg = "Cannot select without values %s of %s " % (values, self)
            Logger().error("[Model] ExecuteQueryFailed - %s" % msg)
            raise ExecuteQueryFailed(msg)

        values_str = ",".join(str(x) for x in values)
        where = ["%s IN (%s)" % (field_in, values_str)]
        return self.fetch_all(where=where, fields=fields)

    def like_in(self, field_like: str, value_like: str, fields="*"):
        """
        Procura registros filtrando o campo por string usando LIKE db comando.

        Args:
            field_like (str): field to search for
            value_like (str): value or word to looking for
            fields (str): fields to select return
        Returns:
            resultado ou raise ExecuteQueryFailed exceção
        """
        Logger().debug("[Model] Trying to like in.")
        if not (field_like and value_like):
            msg = "Cannot select like without field or values %s of %s " % (
                field_like,
                value_like,
            )
            Logger().error("[Model] ExecuteQueryFailed - %s" % msg)
            raise ExecuteQueryFailed(msg)

        value_like = "%" + value_like + "%"
        where = [" %s LIKE '%s' " % (field_like, value_like)]
        return self.fetch_all(where=where, fields=fields)

    def filter(self, where: tuple, limit=None, order=None):
        """
        Filtro baseado em uma tuple como WHERE db command.

            where (tuple): e.g ("ID_FORNECEDOR_API_FAES=%s", [id])
            limit (list): numero de resultados da busca.
            order: ordenação da busca DESC ou ASC
        Returns:
            resultado
        """
        if limit is None:
            limit = [1000]
        Logger().debug("[Model] Trying to filter.")
        return self.fetch_all(order=order, limit=limit, where=where)

    def count(self, count="*", where=None):
        """
        Retorna a quantidade de registros de uma determinada tabela.

        :param count:
        :param where:
        :return:
        """
        Logger().debug("[Model] Trying to count.")
        sql = "SELECT count(%s) as counter from %s " % (count, self._table)

        if where:
            sql += "WHERE %s" % where

        cur = self._database.query(sql=sql)
        rows = cur.fetchone()
        return rows.get("counter", 0)

    def build_where(self, columns_and_values=None, ignore_columns=None) -> str:
        """Retorna um Sql where a partir dos atributos da modelo ou \
            transforma uma Tuple[coluna, valor] caso passado como argumento em um Sql where.

        Args:
            columns_and_values (Tuple[coluna, valor], opcional): Tuple com as colunas e os valores. Defaults é None.

        Returns:
            str: Sql where
        """
        if ignore_columns is None:
            ignore_columns = []
        if columns_and_values:
            columns = columns_and_values
        else:
            columns = self.columns_and_values()
        where_conditions = "1=1 "
        for column, value in columns:
            if column not in ignore_columns:
                if value:
                    if isinstance(value, datetime):
                        date = value.strftime("%Y-%m-%d %H:%M:%S")
                        where_conditions += f" AND {column}='{date}'"
                    elif isinstance(value, str):
                        where_conditions += f" AND {column}='{value}'"
                    else:
                        where_conditions += f" AND {column}={value}"

        return where_conditions

    def columns_and_values(self) -> list:
        """
        Retorna as colunas e o valores contidos na classe.

        Returns:
            (list[tuple]): Lista de Coluna e Valor da propria classe.
        """
        columns = []
        for model_attributes in inspect.getmembers(self):
            # remove funções privadas e protegidas
            # remove outros métodos que não começam com underscore '_'
            if not model_attributes[0].startswith("_") and not callable(model_attributes[1]):
                columns.append(model_attributes)
        return columns

    def fetch_one(self, fields="*", where=None, order=None, limit=(0, 1)):
        """
        Retorna apenas um registro.

        :param fields:
        :param where:
        :param order:
        :param limit:
        :return:
        """
        Logger().debug("[Model] Trying to fetch one.")
        if not where:
            where_conditions = "1=1 "
            columns = self._columns_with_value()
            for key, value in columns:
                if value is not None:
                    if isinstance(value, datetime):
                        date = value.strftime("%Y-%m-%d %H:%M:%S")
                        where_conditions += f" AND {key}='{date}'"
                    elif isinstance(value, str):
                        where_conditions += f" AND {key}='{value}'"
                    else:
                        where_conditions += f" AND {key}={value}"

            where = (where_conditions,)

        row = self._database.fetch_one(
            table=self._table, fields=fields, where=where, order=order, limit=limit
        )
        if row:
            keys = {attr.lower(): row.get(attr.upper()) for attr in self._columns()}
            self.__dict__.update(keys)

        return self

    def fetch_all(
        self,
        fields="*",
        where=None,
        group=None,
        order=None,
        limit=None,
        distinct=False,
    ):
        """
        Retorna todos registros que atendem a clausula where.

                :param fields: str
                :param where:
                :param group:
                :param order:
                :param limit: list. [from, to] or [to]. Default is 1000
                            eg: [0, 1000] or [1000]
                :param distinct: bool. Default is False
                :return: instance: list of instances with data from database
        """
        Logger().debug("[Model] Trying to fetch all.")
        if limit is None:
            limit = [1000]

        if not where:
            where_conditions = "1=1 "
            columns = self._columns_with_value()
            for key, value in columns:
                if value:
                    if isinstance(value, datetime):
                        date = value.strftime("%Y-%m-%d %H:%M:%S")
                        where_conditions += f" AND {key}='{date}'"
                    elif isinstance(value, str):
                        where_conditions += f" AND {key}='{value}'"
                    else:
                        where_conditions += f" AND {key}={value}"

            where = (where_conditions,)

        rows = self._database.fetch_all(
            table=self._table,
            fields=fields,
            where=where,
            group=group,
            order=order,
            limit=limit,
            distinct=distinct,
        )
        instances = []
        for row in rows:
            new_instance = copy.copy(self)
            Model.__fill(instance=new_instance, attributes=row)
            instances.append(new_instance)

        return instances

    @staticmethod
    def __fill(instance, attributes):
        """Preenche a instancia com a dict de atributos."""
        keys = {k.lower(): v for k, v in attributes.items()}
        instance.__dict__.update(keys)
        return instance

    def select_join_raw(self, fields, main_table, join_fields, where, order=None, limit=100):
        """
        Monta uma instrução sql, conforme os campos enviados, e executa a busca.

        :param fields:
        :param main_table:
        :param join_fields:
        :param where:
        :param order:
        :param limit:
        :return:
        """
        Logger().debug("[Model] Trying to select join raw query.")
        return self._database.select_join_raw(
            fields=fields,
            main_table=main_table,
            join_fields=join_fields,
            where=where,
            order=order,
            limit=limit,
        )

    def query_raw(self, sql: str, params=None):
        """
        Executa uma consulta conforme a instrução sql e os parametros enviados.

                :param sql:
                :param params:
                :return:
        """
        Logger().debug("[Model] Trying to query raw.")
        return self._database.query_raw(sql=sql, params=params)

    def rollback(self):
        """
        Executa rollback na sessão.

        :return:
        """
        Logger().debug("[Model] Trying to rollback.")
        return self._database.rollback()

    def commit(self):
        """
        Executa commit na sessão.

        :return:
        """
        Logger().debug("[Model] Trying to commit.")
        return self._database.commit()

    def _max(self, column: str, table: str):
        """
        Executa a instrução MAX em uma determinada tabela/coluna.

        :param column:
        :param table:
        :return:
        """
        Logger().debug("[Model] Trying to get max from table %s." % table)
        max_id = self._database.max(column=column, table=table)
        if max_id is None:
            max_id = 0
        return max_id

    def add_suffix(self, suffix: str):
        """
        Função add_suffix.

        Adiciona sufixo temporário ao nome da tabela do modelo.

        Args:
            suffix (str): Sufixo para nova tabela.
        Returns:
            self._table (str): Nome da tabela.
        """
        self._table = f"{self._table}_{str(suffix).upper()}"
        return self._table

    def get_table_name(self):
        """Retorna o nome da tabela."""
        return self._table

    def bulk_update(self, fields, values, where_in, where_field="", chunks_size=0):
        """Método para atualizar (update) em bulk.

        Args:
            fields (list|tuple): Colunas da tabela
            values (list|tuple): Valores
            where_in (list|tuple): valores para procurar
            where_field (str): Coluna para incidir a atualização
            chunks_size (limite)
        """
        if not where_field:
            where_field = self._pk
        values = [f"'{value}'" if isinstance(value, str) else value for value in values]
        set_values = ",".join(f"{field}={value}" for field, value in list(zip(fields, values)))
        chunks = self._chunks(iterable_list=list(where_in), chunks_size=chunks_size)
        for chunk in chunks:
            in_values = ",".join(f"'{value}'" for value in chunk)
            query = f"""UPDATE {self._table}
                        SET {set_values}
                        WHERE {where_field} IN ({in_values});"""
            try:
                return self._database.query_raw(sql=query)
            except ExecuteQueryFailed as error:
                raise error

    def bulk_insert(self, fields, values: list, table: str = None, chunks_size=0, ignore=False):
        """Método para atualizar (update) em bulk.

        Args:
            fields (list|tuple): Colunas da tabela
            values (list[Tuple(valores das colunas)]): Valores das colunas
            table (str) Nome da tabela (Não obrigatório)
            chunks_size (limite) Quantidade de registros inseridos em partes
        """
        columns = ", ".join(fields)
        table_name = self._table if not table else table
        chunks = self._chunks(iterable_list=list(values), chunks_size=chunks_size)
        try:
            for chunk in chunks:
                insert_values = ", ".join(str(value) for value in chunk)
                query = f"INSERT {'IGNORE' if ignore else ''} INTO {table_name} ({columns}) VALUES {insert_values};"
                self._database.query(sql=query)
        except ExecuteQueryFailed as error:
            raise error

    def bulk_delete(self, where_in, where_field="", chunks_size=0, where_option="1=1"):
        """Método para atualizar (update) em bulk.

        Args:
            where_in (list|tuple): Valores para procurar
            where_field (str): Coluna para incidir a atualização
            chunks_size (limite)
        """
        if not where_field:
            where_field = self._pk

        chunks = self._chunks(iterable_list=list(where_in), chunks_size=chunks_size)
        for chunk in chunks:
            in_values = ",".join(f"'{value}'" for value in chunk)
            query = f"""DELETE FROM {self._table}
                        WHERE {where_option} AND {where_field} IN ({in_values});"""
            try:
                return self._database.query(sql=query)
            except ExecuteQueryFailed as error:
                raise error

    @staticmethod
    def _chunks(iterable_list: list, chunks_size: int):
        """Segura(Yield) pedaços de tamanho(chunks_size) da lista.

        Args:
            iterable_list(list): Lista a ser partida em pedaços(chunks)
            chunks_size(int): Tamanho dos 'pedaços(chunks) da lista
        """
        if chunks_size:
            for position in range(0, len(iterable_list), chunks_size):
                yield iterable_list[position : position + chunks_size]
        else:
            yield iterable_list

    def parser_row(self, row):  # pylint: disable=R0201
        """Faz o parser da row que são retornadas como dict."""
        if row:
            return {k.lower(): v for k, v in row.items()}
        return None

    def primary_key(self):
        """Retorna a 'primary key' da tabela."""
        return self._pk
