from datetime import datetime

# 搜索条件
TableSearchSchema = '''
{
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "field": {"type": "string"},
            "value": {"not": {"type": "null"}},
            "type": {"type": "string", "desc":"非必填，目前标识是否是timestamp形式"},
            "op": {"type": "integer"}
        },
        "required": ["field", "value", "op"]
    }
}
'''
# 排序条件
TableSortSchema = '''
    {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "field": {"type": "string"},
                "order": {"type": "integer", "desc": "0_正序，1为倒叙"}
            }
        }
    }
'''
# 限制条件
TableLimitSchema = '''
{
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "count": {"type": "integer"} 
    },
    "required": ["page", "count"]
}
'''


class REL(object):
    EQUAL = 0  # 等于
    NOT_EQUAL = 1  # 不等于
    IN_ = 2  # in
    NOT_IN_ = 3  # notin
    MORE_THAN = 4  # 大于
    LESS_THAN = 5  # 小于
    BETWEEN = 6  # between
    LIKE = 7  # like
    IS_NULL = 8  # 等于None
    IS_NOT_NULL = 9  # 不等于None


class _SearchCell:
    """搜素元素
    """
    def __init__(self, field, value, _type, op: int):
        self.field = field
        self.value = value
        self.type = _type
        self.op = op


class _SortCell:
    """排序元素
    """
    def __init__(self, field, order):
        self.field = field
        self.order = order


class TableQuery:
    """对page count search sortby 这种常用表单的schema 和 query封装
    如果涉及到了不同表 join情况，上层可以 初始化两个实例来处理，前端传参时也可以search 分为两个传进来
    """
    @staticmethod
    def _get_search_cell(search_list):
        search_cells = []
        for search in search_list:
            search_cells.append(_SearchCell(
                search.get("field"), search.get("value"), search.get("type"), search.get("op")))
        return search_cells

    @staticmethod
    def _get_sort_cell(sort_list):
        sort_cells = []
        for sort in sort_list:
            sort_cells.append(_SortCell(sort.get("field"), sort.get("order")))
        return sort_cells

    def __init__(self, session, db_class, limit, search=None, sort=None):
        self.query = session.query(db_class)
        self.db_class = db_class
        self._search = search
        self._sort = sort
        self._limit = limit

    def search(self):
        """获取search对应的 cond值！
        """
        if not self._search:
            return self
        search_cells = self._get_search_cell(self._search)
        search_cond = []
        for search in search_cells:
            if search.type == "timestamp":  # 对时间戳 处理成datetime
                timestamps = []
                if isinstance(search.value, list):
                    timestamps.extend(search.value)
                    search.value = []
                    for timestamp in timestamps:
                        search.value.append(datetime.fromtimestamp(timestamp))
                else:
                    search.value = datetime.fromtimestamp(search.value)
            if search.op == REL.NOT_EQUAL:
                search_cond.append(getattr(self.db_class, search.field) != search.value)
            elif search.op == REL.IN_:
                if not isinstance(search.value, list):
                    raise Exception('op in must be a list!')
                search_cond.append(getattr(self.db_class, search.field).in_(search.value))
            elif search.op == REL.NOT_IN_:
                if not isinstance(search.value, list):
                    raise Exception('op in must be a list!')
                search_cond.append(getattr(self.db_class, search.field).notin_(search.value))
            elif search.op == REL.MORE_THAN:
                search_cond.append(getattr(self.db_class, search.field) > search.value)
            elif search.op == REL.LESS_THAN:
                search_cond.append(getattr(self.db_class, search.field) < search.value)
            elif search.op == REL.BETWEEN:
                if not isinstance(search.value, list) or len(search.value) != 2:
                    raise Exception('op between must be a list and length = 2!')
                search_cond.append(getattr(self.db_class, search.field).between(*search.value))
            elif search.op == REL.LIKE:
                search_cond.append(getattr(self.db_class, search.field).like("%{}%".format(search.value)))
            elif search.op == REL.IS_NULL:
                search_cond.append(getattr(self.db_class, search.field).is_(None))
            elif search.op == REL.IS_NOT_NULL:
                search_cond.append(getattr(self.db_class, search.field).isnot(None))
            else:  # 默认是等于
                search_cond.append(getattr(self.db_class, search.field) == search.value)
        if search_cond:
            self.query = self.query.filter(*search_cond)
        return self

    def sort(self):
        """获取对应的order by 的query
        """
        if not self._sort:
            return self
        sort_cells = self._get_sort_cell(self._sort)
        sort_cond = []
        for sort_cell in sort_cells:
            if sort_cell.order:
                sort_cond.append(getattr(self.db_class, sort_cell.field).desc())
            else:
                sort_cond.append(getattr(self.db_class, sort_cell.field))
        self.query = self.query.order_by(*sort_cond)
        return self

    def limit(self):
        if not self._limit:
            return self
        if not self._limit.get("page") or not self._limit.get("count"):
            raise Exception("page count 不能为0")
        self.query = self.query.offset((self._limit.get("page") - 1) * self._limit.get("count")).\
            limit(self._limit.get("count"))
        return self
