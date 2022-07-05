"""
Mysql Database Module.

Documentation:
https://mysqlclient.readthedocs.io/

Repo:https://github.com/PyMySQL/mysqlclient-python

Benchmark - Python MySQLdb vs mysql-connector query performance:
https://charlesnagy.info/it/python/python-mysqldb-vs-mysql-connector-query-performance

FAQ:
https://stackoverflow.com/questions/43102442/whats-the-difference-between-mysqldb-mysqlclient-and-mysql-connector-python

You probably are better off using MySQLdb instead of using this module
directly. In general, renaming goes from mysql_* to _mysql.*. _mysql.connect()
returns a connection object (MYSQL).
Functions which expect MYSQL * as an argument are now methods of the connection
object. A number of things return result objects (MYSQL_RES).
Functions which expect MYSQL_RES * as an argument are now methods of the result
object. Deprecated functions (as of 3.23) are NOT implemented.
"""
import os
from datetime import datetime
from typing import Any, Union

import MySQLdb  # type: ignore
import MySQLdb.cursors  # type: ignore

from app.utils.logger import Logger

from .errors import (
    ConnectionFailed,
    DeleteFailed,
    ExecuteQueryFailed,
    InsertFailed,
    ProgrammingError,
    UpdateFailed,
)


class SerializeData:
    """Converte atributos Dict em formatos para facilitar o trabalho com queries no banco."""

    @staticmethod
    def _serialize_insert(data: dict):
        """
        Formatar valores de dicionário do insert em strings.

        :param data: dict e.g {"column1": "value1", "column2": "value2", "color": "red"}
        :return: columns, values
        """
        columns = ",".join(data.keys())
        values = ",".join("%s" for k in data)

        return columns, values

    @staticmethod
    def _serialize_insert_fields(columns: tuple, values: list):
        """
        Formatar valores de dicionário do insert em strings.

        :return: columns, values
        """
        columns_str = ", ".join(columns)
        values_str = ", ".join("%s" for v in values)
        return columns_str, values_str

    @staticmethod
    def _serialize_update(data: dict):
        """
        Formatar valores de dicionário do update em strings.

        :param data: dict e.g {"column1": "value1", "column2": "value2", "color": "red"}
        :return: str
        """
        return "=%s,".join(data.keys()) + "=%s"


class MySQLConnection(SerializeData):  # pragma: no cover
    """MySql Connection Class."""

    _table: Union[str, None] = None

    def __init__(self, **kwargs):
        """
        Construtor de classe.

        :param str host:     host para conectar
        :param str user:     usuário para conectar como
        :param str password: senha para usar
        :param str database: banco de dados a ser usado
        :param str port:     porta TCP / IP para conectar
        """
        self.logger = Logger()

        self.__auth = {
            "password": os.environ.get("MYSQL_PASSWORD", "mypass"),
            "user": os.environ.get("MYSQL_USER", "root"),
        }

        self.config = {
            "host": os.environ.get("MYSQL_HOST", "db-dev.apirest_default"),
            "port": int(os.environ.get("MYSQL_PORT", 3306)),
            "database": os.environ.get("MYSQL_DATABASE", "mybd"),
            "autocommit": False,
            "attempts": kwargs.get("attempts", 3),
            "connect_timeout": kwargs.get("connect_timeout", 30),
            "charset": kwargs.get("charset", "utf8"),
        }

        self.conn = None
        self.cursor = None
        self.connected = False
        self._retries = 0

        self.connect()

    def __enter__(self):
        """Entrar no objeto mysql."""
        self.logger.debug("[MYSQL] Entrando no database!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Saindo do objeto mysql."""
        self.logger.debug("[MYSQL] Saindo do database!")
        self.close()

    def reconnect(self):
        """
        Reconexão.

        :return:
        """
        self.logger.warning("[MYSQL] Re-conectando no database!")
        return self.connect()

    def commit(self) -> Union[Any, None]:
        """Commitar uma transação.

        Return:
            (None|Any)
        """
        if self.conn is not None:
            try:
                return self.conn.commit()
            except MySQLdb.OperationalError:
                self.reconnect()
                self.commit()
        return None

    def is_open(self) -> bool:
        """Checar se a conexão está aberta."""
        if self.conn is None:
            return False

        return bool(self.conn.open)

    def close(self) -> None:
        """Fechar conexão."""
        self.logger.debug("[MYSQL] Closing connection...")
        self.cursor.close()
        self.conn.close()

    def rollback(self):
        """
        Rollback na transação.

        :return:
        """
        self.logger.warning("[MYSQL] Applying rollback...")
        self.conn.rollback()

    def has_cursor(self):
        """Verificar se cursor está aberto."""
        self.logger.debug("Verify if has cursor")
        return self.cursor is not None

    def connect(self):
        """Conexão no mysql."""
        message_attempts = f"Tentativas máximas: {self.config.get('attempts')}"
        self.logger.debug(
            f"[MYSQL] Conectando no banco de dados: {self.config['host']}. {message_attempts}"
        )
        attempts = 0
        connected = False

        if self.__auth.get("user") is None or self.__auth.get("password") is None:
            raise ConnectionFailed("credentials is None.")

        while attempts < self.config.get("attempts") and not connected:

            try:
                self.logger.debug("Trying to connect. %s attempts" % attempts)

                self.conn = MySQLdb.connect(
                    host=self.config.get("host"),
                    port=self.config.get("port"),
                    user=self.__auth.get("user"),
                    password=self.__auth.get("password"),
                    db=self.config.get("database"),
                    cursorclass=MySQLdb.cursors.DictCursor,
                    charset=self.config.get("charset"),
                    use_unicode=True,
                    autocommit=self.config.get("autocommit"),
                )
                self.conn.autocommit = self.config.get("autocommit")
                self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                connected = True

            except MySQLdb.OperationalError as error:
                # Exception raised for errors that are related to the
                # database's operation and not necessarily under the
                # control of the programmer, e.g. an unexpected disconnect
                # occurs, the data source name is not found, a transaction
                # could not be processed, a memory allocation error occurred
                # during processing, etc.

                attempts += 1
                self.logger.critical("Try it again")
                self.logger.critical(">>Attempt %s %s" % (attempts, self.config.get("attempts")))
                self.logger.critical(
                    ">>MySQLdb.OperationalError - " "Exception raised for error %s" % error
                )
                raise ConnectionFailed(error) from error

            except (TypeError, ValueError) as error:
                attempts = self.config.get("attempts") + 1
                self.logger.critical(">>Attempt %s %s" % (attempts, self.config.get("attempts")))
                self.logger.critical(
                    ">>TypeError/ValueError Exception " "raised for error %s" % error
                )
                raise ConnectionFailed(error) from error

        self._retries = attempts
        self.connected = connected
        self.logger.debug("Connected?! %s" % connected)
        return connected

    def last_id(self):
        """Obter a última consulta executada."""
        try:

            last_id = self.conn.lastrowid

        except AttributeError as error:
            raise error

        return last_id

    def now(self) -> datetime:
        """Retrieve date now from database.

        Returns:
            (datetime): Data atual.
        """
        cursor = self.query("SELECT SYSDATE() AS NOW")
        query_result = cursor.fetchone()
        return query_result["NOW"]

    def query(self, sql: str, params=tuple()):
        """
        Execute a consulta com base em uma string sql e um parâmetro do tipo tuple.

        Se for bem-sucedido, retorne o cursor, caso contrário ExecuteQueryFailed
        ou exceções ProgrammingError serão levantadas.

        ExecuteQueryFailed:
            Exceção levantada para erros relacionados ao banco de dados
            operação e não necessariamente sob o controle do programador,
            por exemplo. ocorre uma desconexão inesperada, o nome da fonte de dados não é
            encontrado, uma transação não pôde ser processada, uma alocação de memória
            ocorreu um erro durante o processamento, etc.

        ProgrammingError:
            Exceção levantada para erros relacionados a
            as operações de sintaxe como uma tabela não existem,
            formato inválido de string sql, etc.

        :param sql:
        :param params:
        :return:
        """
        self.logger.debug("Trying to run query: %s with params: %s" % (sql, params))
        if not self.is_open():
            details = {
                "cursor": self.cursor,
                "connection": self.cursor,
                "is_open": False,
            }
            self.logger.error("Connection was close. Details: %s" % details)
            raise ConnectionFailed({"message": "Connection was gone", "details": details})

        try:
            self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.cursor.execute(sql, params)

        except MySQLdb.OperationalError as error:
            self.rollback()
            self.logger.error("ExecuteQueryFailed was raised: %s" % error)
            raise ExecuteQueryFailed from error

        except MySQLdb.ProgrammingError as error:
            self.rollback()
            self.logger.error("ProgrammingError was raised: %s" % error)
            raise ProgrammingError from error

        return self.cursor

    def _select(
        self,
        table: str,
        fields=(),
        distinct=False,
        where=None,
        group=None,
        order=None,
        limit=None,
    ):
        """
        Executa um select baseado nos parametros enviados.

        :param table: str
        :param fields: tuple, str
        :param distinct: bool. Default is False
        :param where: tuple
        :param group:
        :param order:
        :param limit:
        :return:
        """
        if limit is None:
            limit = [1000]
        sql = f"""{MySQLConnection._sql_select(distinct, fields, table)} {MySQLConnection._sql_where(where)}
                {MySQLConnection._sql_group(group)} {MySQLConnection._sql_order(order)}
                {MySQLConnection._sql_limit(limit)}"""
        return self.query(sql)

    @staticmethod
    def _sql_select(distinct: bool, fields: Union[str, tuple, list], table: str):
        """Gera o sql para select.

        Args:
            distinct (bool): Flag indicando o uso de distinct ou não.
            fields (Union[str,list,tuple]): Colunas do Select.
                Exemplo: "*", "ID, NOME", ["ID, NOME"], ["%s, %s", ["ID", "NOME"]]
            table (str): Nome da tabela do FROM.

        Returns:
            str: Query select. Exemplo "SELECT ID, NOME"
        """
        query_select = ""
        query_distinct = ""
        if distinct:
            query_distinct = "DISTINCT"
        if isinstance(fields, (tuple, list)):
            query_select += f"SELECT {query_distinct} {','.join(fields)} FROM {table} "
        else:
            query_select += f"SELECT {query_distinct} {fields} FROM {table} "
        return query_select

    @staticmethod
    def _sql_where(where):
        """Gera o sql para where.

        Args:
            where (Union[str,list,tuple]): Where. Exemplo "WHERE ID = 1", ["WHERE ID = 1"], ["WHERE ID = %s", "1"]

        Returns:
            str: Query where. Exemplo "WHERE ID = 1"
        """
        query_where = ""
        if isinstance(where, str):
            query_where += " WHERE %s" % where
        elif where:
            query_where += " WHERE %s" % where[0]
            if len(where) > 1:
                if isinstance(where[1], (list, tuple)):
                    query_where = query_where % tuple(f"'{w}'" for w in where[1])
                    query_where = query_where.replace("%", "%%")
                else:
                    query_where = query_where % where[1]
        return query_where

    @staticmethod
    def _sql_group(group: Union[str, list, tuple]) -> str:
        """Gera o sql para group.

        Args:
            group (Union[str,list,tuple]): Group by. Exemplo "GROUP BY ID", ["GROUP BY ID"], ["GROUP BY %s", "ID"]

        Returns:
            str: Query group. Exemplo "GROUP BY ID"
        """
        query_group = ""
        if isinstance(group, str):
            query_group += " GROUP BY %s" % group
        elif group:
            query_group += " GROUP BY %s" % group[0]
            if len(group) > 1:
                query_group += " %s" % group[1]
        return query_group

    @staticmethod
    def _sql_order(order: Union[str, list, tuple]) -> str:
        """Gera o sql para order.

        Args:
            order (Union[str,list,tuple]): Order by.
                Exemplo "ORDER BY ID DESC", ["ORDER BY ID DESC"], ["ORDER BY %s DESC", "ID"]

        Returns:
            str: Query order. Exemplo "ORDER BY ID DESC" ou "ORDER BY NAME ASC"
        """
        query_order = ""
        if isinstance(order, str):
            query_order += " ORDER BY %s" % order
        elif order:
            query_order += " ORDER BY %s" % order[0]
            if len(order) > 1:
                query_order += " %s" % order[1]
        return query_order

    @staticmethod
    def _sql_limit(limit: list) -> str:
        """Gera o sql para limite.

        Args:
            limit (list): Lista de inteiros para o limite. Exemplo [1] (LIMITE 1) ou [0,1] (LIMITE 0, 1)

        Returns:
            str: Query limite. Exemplo "LIMITE 1000"
        """
        query_limit = ""
        if isinstance(limit, list):
            query_limit += f" LIMIT {limit[0]}"
            if len(limit) > 1:
                query_limit += f", {limit[1]}"
        return query_limit

    def fetch_one(self, table: str, fields="*", where=None, order=None, limit=(0, 1)):
        """
        Retorna apenas um registro.

        :param table: (str) table_name
        :param fields: (field1, field2 ...) list of fields to select
        :param where: ("parameterized statement", [parameters])
                    eg: ("id=%s and name=%s", [1, "test"])
        :param order: [field, ASC|DESC]
        :param limit: [from, to]
        :return:
        """
        self.logger.debug("Fetching one results.")
        cur = self._select(table=table, fields=fields, where=where, order=order, limit=limit)
        return cur.fetchone()

    def fetch_all(
        self,
        table: str,
        fields="*",
        where=None,
        distinct=False,
        group=None,
        order=None,
        limit=None,
    ):
        """
        Retorna todos registros que atendem a clausula where.

        :param table: (str) table_name
        :param fields: (field1, field2 ...) list of fields to select
        :param where: ("parameterized statement", [parameters])
                    eg: ("id=%s and name=%s", [1, "test"])
        :param group ("parameterized statement", [parameters])
                    eg: ("id=%s and name=%s", [1, "test"])
        :param order: [field, ASC|DESC]
        :param limit: list. [from, to] or [to]. Default is 1000
                    eg: [0, 1000] or [1000]
        :param distinct: bool
        :return:
        """
        self.logger.debug("Fetching all results.")
        if limit is None:
            limit = [1000]

        cur = self._select(
            table=table,
            fields=fields,
            distinct=distinct,
            where=where,
            group=group,
            order=order,
            limit=limit,
        )
        return cur.fetchall()

    def insert(self, table: str, data):
        """
        Insere um registro.

        :param table:
        :param data: dict e.g {"column1": "value1", "column2": "value2", "color": "red"}
        :return:
        """
        try:
            columns, values = self._serialize_insert(data)
            sql = "INSERT IGNORE INTO %s (%s) VALUES(%s)" % (table, columns, values)
            cursor = self.query(sql, tuple(data.values()))
        except MySQLdb.OperationalError:
            self.reconnect()
            self.insert(table=locals().get("table", ""), data=locals().get("data", ""))

        except MySQLdb.IntegrityError as error:
            code, message = error.args
            raise InsertFailed({"code": code, "message": message, "table": table}) from error
        else:
            return cursor.lastrowid
        return None

    def insert_fields(self, table: str, columns_insert: tuple, values_insert: list):
        """
        Insere um registro parcialmente.

        :param table:
        :param columns_insert: tuple e.g ("column1", "column2", "column2", ...)
        :param values_insert : list e.g [(value1, value2, value3), (value1, value2, value3), ...]
        :return:
        """
        try:
            columns, values = self._serialize_insert_fields(columns_insert, values_insert)

            sql = "INSERT INTO %s (%s) VALUES %s" % (table, columns, values)

            cursor = self.query(sql, tuple(values_insert))

        except MySQLdb.IntegrityError as error:
            code, message = error.args
            raise InsertFailed({"code": code, "message": message, "table": table}) from error

        return cursor.lastrowid

    def update(self, table: str, data, where):
        """
        Atualiza um registro.

        :param table:
        :param data: dict e.g {"column1": "value1", "column2": "value2", "color": "red"}
        :param where: e.g ("id=%s AND year=%s", [id, year]) or ["id=1"]
        :return:
        """
        try:
            query = self._serialize_update(data)
            sql = "UPDATE %s SET %s WHERE %s" % (table, query, where[0])
            values = tuple(data.values())
            cursor = self.query(
                sql, values + tuple(where[1]) if where and len(where) > 1 else values
            )

        except MySQLdb.OperationalError:
            self.reconnect()
            self.update(
                table=locals().get("table", ""),
                data=locals().get("data", ""),
                where=locals().get("where", ""),
            )

        except MySQLdb.IntegrityError as error:
            code, message = error.args
            raise UpdateFailed({"code": code, "message": message, "table": table}) from error

        else:
            return cursor
        return None

    def delete(self, table: str, where):
        """
        Apaga um registro.

        :param table:
        :param where:
        :return:
        """
        try:
            self.query("SET FOREIGN_KEY_CHECKS=0")
            sql = "DELETE FROM %s" % table

            if where and len(where) > 0:
                sql += " WHERE %s" % where[0]

            cursor = self.query(sql, where[1] if where and len(where) > 1 else None)

        except MySQLdb.IntegrityError as error:
            code, message = error.args
            raise DeleteFailed({"code": code, "message": message, "table": table}) from error

        return cursor

    def max(self, column: str, table: str):
        """
        Executa a instrução MAX em uma determinada tabela/coluna.

        :param column:
        :param table:
        :return:
        """
        sql = "SELECT MAX(%s) FROM %s" % (column, table)

        cur = self.query(sql)
        result = cur.fetchone()
        return result["MAX(%s)" % column]

    def select_join_raw(self, fields, main_table, join_fields, where, order=None, limit=100):
        """
        Monta uma instrução sql, conforme os campos enviados, e executa a busca.

        :param fields: tuple
        :param main_table: str
        :param join_fields: dict {"table": {"join": join_type, "on": "query"}}
        :param where: str
        :param order: str
        :param limit: int. Default is 100
        :return:
        """
        fields = ",".join(fields)
        sql_join = [
            "%s JOIN %s ON %s" % (x.get("join"), y, x.get("on")) for y, x in join_fields.items()
        ]
        sql_join = " ".join(sql_join)

        sql = "SELECT %s FROM %s %s WHERE %s" % (fields, main_table, sql_join, where)

        if order:
            sql += " ORDER BY %s" % order

        sql += " LIMIT %s " % limit
        cur = self.query(sql=sql)
        return cur.fetchall()

    def query_raw(self, sql, params=None):
        """
        Executa uma consulta conforme a instrução sql e os parametros enviados.

        :param sql: str
        :param params: str
        :return cursor
        """
        return self.query(sql, params)

    def drop_table(self, table: str):
        """
        Executa um drop da tabela conforme a instrução sql.

        :param table: str
        :return cursor
        """
        query = f"""DROP TABLE {table} """
        return self.query(sql=query)
